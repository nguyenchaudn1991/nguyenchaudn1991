# Bài thực hành 12 — TOOLS (định nghĩa tool, KHÔNG chạy trực tiếp)
# File này chỉ CHỨA tool + schema; file 12_tool_use.py sẽ import và dùng.
# Tách ra 2 file để giống thực tế: "kho tool" nằm riêng, code gọi Claude nằm riêng.
#
# Mỗi tool ở đây gồm 2 nửa, đúng BƯỚC 1 và BƯỚC 2 của pipeline:
#   - BƯỚC 1: một HÀM PYTHON THƯỜNG (get_exchange_rate)
#   - BƯỚC 2: một JSON SCHEMA mô tả hàm đó cho Claude (get_exchange_rate_schema)

# =====================================================================
# BƯỚC 1 — TOOL FUNCTION (hàm Python thường)
# =====================================================================
# Tỉ giá "giả lập" — cố tình bịa để Claude KHÔNG biết sẵn => buộc phải gọi tool.
# (Trong thực tế đây là chỗ anh gọi API ngân hàng / query database.)
RATES = {
    ("USD", "VND"): 25400,      ("VND", "USD"): 1 / 25400,
    ("USD", "JPY"): 157.2,      ("JPY", "USD"): 1 / 157.2,
    ("JPY", "VND"): 161.6,      ("VND", "JPY"): 1 / 161.6,
}


def get_exchange_rate(from_currency, to_currency):
    """Trả về: 1 đơn vị from_currency = bao nhiêu đơn vị to_currency."""
    key = (from_currency.upper(), to_currency.upper())

    # ⭐ Best practice: VALIDATE INPUT + MEANINGFUL ERROR MESSAGE.
    # Claude ĐỌC được câu lỗi này (qua is_error) và tự sửa tham số rồi gọi lại.
    if key not in RATES:
        raise ValueError(
            f"Unknown currency pair {from_currency}->{to_currency}. "
            f"Supported currencies: USD, VND, JPY."
        )
    return RATES[key]


# Tool 2 — CỐ TÌNH không tự tra tỉ giá: chỉ nhân amount * rate.
# => Claude buộc phải gọi get_exchange_rate LẤY rate TRƯỚC, rồi đưa vào đây
#    -> đó là TOOL CHAINING (output tool này = input tool kia).
def convert_amount(amount, rate):
    """Đổi một khoản tiền theo tỉ giá cho sẵn: trả về amount * rate."""
    if rate <= 0:
        raise ValueError(f"rate must be a positive number, got {rate}.")
    return amount * rate


# Tool 3 — ZERO-ARG: không nhận tham số nào (input_schema rỗng).
def list_supported_currencies():
    """Danh sách mã tiền tệ hệ thống hỗ trợ (không cần tham số)."""
    return sorted({code for pair in RATES for code in pair})   # {'JPY','USD','VND'} -> list


# Tool 4 — trả về DICT: bảng tỉ giá base -> mọi đồng khác (để thấy json.dumps serialize dict).
def rate_table(base_currency):
    """Bảng tỉ giá từ base_currency sang mọi đồng được hỗ trợ."""
    base = base_currency.upper()
    supported = {code for pair in RATES for code in pair}
    if base not in supported:
        raise ValueError(f"Unknown currency {base_currency}. Supported: {sorted(supported)}.")
    return {to: RATES[(frm, to)] for (frm, to) in RATES if frm == base}


# =====================================================================
# BƯỚC 2 — JSON SCHEMA (tờ hướng dẫn để Claude biết tool tồn tại & cách gọi)
# =====================================================================
# 3 phần: name · description · input_schema.
# ⭐ description là phần Claude ĐỌC để quyết định CÓ gọi tool không + điền đối số.
get_exchange_rate_schema = {
    "name": "get_exchange_rate",
    "description": (
        "Get the current exchange rate between two currencies. "
        "Use this whenever the user asks to convert money or asks for an exchange rate. "
        "Returns a float: how many units of to_currency equal 1 unit of from_currency."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "from_currency": {"type": "string", "description": "Source currency code, e.g. USD"},
            "to_currency":   {"type": "string", "description": "Target currency code, e.g. VND"},
        },
        "required": ["from_currency", "to_currency"],
    },
}


convert_amount_schema = {
    "name": "convert_amount",
    "description": (
        "Convert a money amount using a known exchange rate (returns amount * rate). "
        "This tool does NOT look up rates. To convert between two currencies, first call "
        "get_exchange_rate to obtain the rate, then pass that rate here. "
        "Use this instead of doing the multiplication yourself."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "amount": {"type": "number", "description": "The amount of money to convert"},
            "rate":   {"type": "number", "description": "Exchange rate from get_exchange_rate"},
        },
        "required": ["amount", "rate"],
    },
}


# ⭐ Tool zero-arg: properties rỗng {}, required rỗng [] -> Claude gọi không cần đối số.
list_supported_currencies_schema = {
    "name": "list_supported_currencies",
    "description": (
        "List every currency code the exchange-rate system supports. "
        "Use this when the user asks which currencies are available, or before "
        "trying to convert an unfamiliar currency. Takes no arguments."
    ),
    "input_schema": {"type": "object", "properties": {}, "required": []},
}


rate_table_schema = {
    "name": "rate_table",
    "description": (
        "Get a table of exchange rates from one base currency to every other "
        "supported currency. Use this when the user wants an overview of rates for a "
        "currency. Returns an object mapping each target currency code to its rate."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "base_currency": {"type": "string", "description": "Base currency code, e.g. USD"},
        },
        "required": ["base_currency"],
    },
}


# =====================================================================
# ĐĂNG KÝ TOOL — 2 "sổ tra cứu" để file chạy dùng
# =====================================================================
# ⭐ PATTERN 4 BƯỚC: đã (1) viết function + (2) viết schema ở trên; giờ (3)+(4) là
#    đăng ký vào 2 "sổ" dưới đây. Nhờ dùng DICT router, file 12_tool_use.py KHÔNG
#    phải sửa một dòng nào — thêm tool = thêm đúng 2 dòng ở đây.
# TOOL_SCHEMAS: đưa vào tham số tools=[...] khi gọi Claude.
# TOOL_FUNCTIONS: tra tên -> hàm thật, để chạy đúng hàm Claude xin (bước 4).
TOOL_SCHEMAS = [
    get_exchange_rate_schema,
    convert_amount_schema,
    list_supported_currencies_schema,   # ← thêm
    rate_table_schema,                  # ← thêm
]
TOOL_FUNCTIONS = {
    "get_exchange_rate": get_exchange_rate,
    "convert_amount": convert_amount,
    "list_supported_currencies": list_supported_currencies,   # ← thêm
    "rate_table": rate_table,                                 # ← thêm
}
