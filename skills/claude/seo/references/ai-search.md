# AEO & GEO + Maintenance

`last_verified: 2026-08-13`

> ⚠️ **File trôi nhanh nhất trong skill này.** AI search thay đổi theo tháng, và phần lớn
> "best practice" đang lưu hành là suy đoán chưa kiểm chứng. Quá ~3 tháng kể từ
> `last_verified` → **đọc lại nguồn chính thức trước khi dùng làm căn cứ tư vấn**.

## Mục lục

- 4. AEO & GEO (25đ) — viết để được trích dẫn
- `llms.txt` — mục thử nghiệm, 0 điểm
- 6. Maintenance & Monitoring (5đ)

---

## 4. AEO & GEO — 25đ

**Mục tiêu thực tế:** làm nội dung *dễ trích dẫn* — mỗi đoạn tự đứng được, có cấu trúc rõ,
có dữ liệu riêng, thực thể đáng tin. **Không phải** làm cho AI chắc chắn trích dẫn; điều đó
không ai điều khiển được.

### Nền tảng: đọc được đã

Điều kiện cần nằm ở `technical.md` — nội dung phải có trong **raw HTML** (phần lớn crawler AI
không chạy JS), và bot tương ứng không bị chặn ở robots/CDN/WAF. Không có cái đó thì mọi thứ
dưới đây vô nghĩa.

### Cấu trúc nội dung

- [ ] `[Heuristic]` **Answer-first:** 1–2 câu đầu của bài (và của mỗi section) trả lời thẳng
      câu hỏi ở tiêu đề/heading, đặt TRƯỚC đoạn dẫn nhập. Lý do giữ mục này: nó tốt cho
      người đọc lướt — đó là lý do đủ, không cần viện tới cơ chế trích xuất của AI.
- [ ] **TL;DR / executive summary** đầu bài: 3 gạch đầu dòng (bài toán → giải pháp → kết quả).
      ⚠️ Bỏ hẳn khái niệm "mật độ LSI keywords": **"LSI keywords" là thuật ngữ sai lệch**,
      không phải kỹ thuật mà search engine dùng. Viết bằng ngôn ngữ tự nhiên của chủ đề là đủ.
- [ ] **Q&A pairs tự đứng được:** 2–3 cặp hỏi–đáp theo câu người dùng hay gõ. Mỗi câu trả lời
      hiểu được mà không cần đọc đoạn trước — vì hệ thống trích xuất lấy từng đoạn rời.
- [ ] **Bảng so sánh:** nội dung "A vs B", "trước vs sau" đóng thành `<table>` HTML thật, không
      phải div giả bảng hay ảnh chụp bảng.
- [ ] **Đóng gói framework/dữ liệu độc quyền:** decision framework, ma trận lựa chọn, checklist,
      con số đúc kết từ dự án thật. `[Heuristic]` — nội dung không tồn tại ở nguồn khác thì chỉ
      có thể lấy từ mình; đó là lập luận đủ, không cần thêm.

### Thống kê, trích dẫn, quote

- [ ] `[Xác minh — nghiên cứu học thuật, phạm vi hẹp]` Nghiên cứu **GEO: Generative Engine
      Optimization** (Aggarwal et al., KDD 2024) đo thấy việc thêm **số liệu thống kê, trích
      dẫn nguồn và quote chuyên gia** làm tăng khả năng nội dung được generative engine dẫn
      nguồn. Giới hạn phải nói kèm khi viện dẫn: đo trên **tập benchmark riêng của nhóm tác
      giả tại thời điểm 2024**, không phải trên hệ thống production hiện tại của OpenAI/
      Google. → dùng làm **định hướng có cơ sở**, không phải bảo đảm.
      Paper: <https://arxiv.org/abs/2311.09735>
- [ ] Mọi số liệu đưa vào bài phải có nguồn thật (xem `eeat-local.md`, mục Trust).

### Freshness

- [ ] Cập nhật nội dung trụ cột định kỳ bằng **thông tin mới thật**, khi đó mới đổi
      `dateModified`. Tuyệt đối không fake ngày để "làm mới".

### Kiểm chứng đầu ra GEO — đây là quan sát, không phải phép đo

- [ ] Định kỳ hỏi ChatGPT/Perplexity/Claude các câu thuộc chủ đề của site, ghi lại site có
      được nhắc/trích không và thông tin có đúng không.
- [ ] ⚠️ **Đây là mẫu quan sát, không phải test xác định.** Kết quả thay đổi theo model,
      phiên bản, thời điểm, ngôn ngữ, vị trí, và cả ngẫu nhiên trong sinh văn bản. Log lại
      **model + version + ngày + câu hỏi nguyên văn + locale**, và **không suy ra nhân quả**
      từ một vài lần chạy. Giá trị lớn nhất của việc này: phát hiện AI đang nói **sai** về
      mình → truy ngược nguồn nó đọc để sửa.

---

## `llms.txt` / `llms-full.txt` — `[Thử nghiệm]`, **0 điểm**

- Đề xuất đặt file mô tả nội dung site ở root domain cho AI đọc: `llms.txt` = bản đồ ngắn
  (URL, tiêu đề, mô tả 1 dòng); `llms-full.txt` = full nội dung Markdown sạch.
- ⚠️ **Chưa có nhà cung cấp AI search lớn nào cam kết đọc và sử dụng file này**, và chưa có
  bằng chứng công khai nào cho thấy nó ảnh hưởng tới việc được trích dẫn.
- → **Không tính điểm. Không đưa vào điều kiện nghiệm thu. Không bán cho khách như một hạng
  mục có tác dụng.** Muốn làm thì làm vì chi phí thấp và có thể hữu ích về sau — nói đúng
  như vậy với khách.
- Nếu làm: **sinh tự động lúc build** từ chính nguồn nội dung để không lệch với site thật
  (số liệu lệch giữa `llms.txt` và trang web là tự bắn vào chân — xem mục Trust).

---

## 6. Maintenance & Monitoring — 5đ

- [ ] **Google Search Console + Bing Webmaster Tools định kỳ:** trạng thái index, trang
      Excluded và lý do, cảnh báo CWV, hiệu suất theo truy vấn/trang.
- [ ] `[Chưa rõ — phải tự kiểm trong property của khách]` **Báo cáo hiệu suất cho bề mặt AI
      của Google:** cách Google trình bày dữ liệu AI Overviews / AI Mode trong Search Console
      đã thay đổi vài lần và việc rollout không đồng đều giữa các property. **Mở Search
      Console của chính khách và xem có gì**, đừng khẳng định từ trí nhớ hay từ file này.
      Không có báo cáo riêng → dùng dữ liệu hiệu suất tổng + annotation mốc thay đổi, và nói
      rõ với khách là không tách được.
- [ ] **Theo dõi AI referral traffic:** tách traffic từ `chatgpt.com`, `perplexity.ai`,
      `gemini.google.com`… trong analytics. Đây là **số đo trực tiếp và đáng tin nhất** của
      GEO — hơn hẳn việc tự hỏi chatbot rồi suy đoán.
- [ ] **Quy trình đồng bộ số liệu:** bất kỳ con số kinh doanh cốt lõi nào thay đổi → sửa đồng
      loạt mọi nơi (front-end, HTML tĩnh, schema, `llms.txt`, profile ngoài) trong cùng 1 lần.
