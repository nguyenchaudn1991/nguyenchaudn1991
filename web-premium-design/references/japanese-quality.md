# 日本品質 — Japanese Quality reference (cho premium-design)

> Áp dụng khi **khách / audience là Nhật**. Đây là tầng "kỷ luật thiết kế kiểu Nhật" — chồng lên
> triết lý "tránh AI-vibe" của skill chính. **Nguyên tắc, KHÔNG phải token sản phẩm.**
> Rút từ design guideline chuẩn Nhật (ニューロマジック / MEO dashboard) — phần phổ quát.
> Nếu là **code FE của 1 sản phẩm có design system riêng** (vd MEO dashboard) → dùng skill `meo-frontend-check`
> (có token chính xác). File này dành cho web/marketing hướng khách Nhật.

## Vì sao khách Nhật khó hơn
Trong văn hoá Nhật, **độ chỉn chu = độ tin cậy (信頼)**. Lệch vài px, kẻ bảng mất 1 đường, heading
sai cấp weight… bị đọc là "作りが粗い (làm ẩu) → không đáng tin". Ưu tiên: **chính xác · nhất quán ·
tiết chế** hơn hoa mỹ. Đây cũng chính là tinh thần "handcrafted, not AI" của skill này — chỉ khắt khe hơn.

## 1. 4 nền tảng (デザインの4原則)
- **近接 Proximity:** liên quan đặt gần, không liên quan tách xa. Khoảng cách = ngữ nghĩa nhóm.
- **整列 Alignment:** mọi phần tử canh theo đường vô hình. Canh mép chuẩn = "an tâm".
- **反復 Repetition:** cùng vai trò → cùng màu/hình/quy tắc, lặp lại để người dùng học 1 lần.
- **強弱 Contrast:** quan trọng thì khác **rõ rệt**, không "hơi khác".

## 2. Typography (bổ sung cho phần Typography của skill)
- **Tương phản weight rõ:** heading bold ↔ body regular. (Skill đã khuyến nghị thêm Medium/SemiBold —
  với khách Nhật, càng phải giữ phân cấp weight kỷ luật, không bold loạn / mảnh loạn.)
- **Type-scale cố định:** chọn 1 bộ size dùng đúng nó; cấm size lẻ tuỳ hứng.
- **Font JP:** Noto Sans JP / Zen Kaku Gothic (đã có trong skill); line-height 1.6–1.8 cho text Nhật thở.
- **1 page-title / màn, trên cùng.**

## 3. Spacing — khoảng trắng có nghĩa
- 1 hệ spacing nhất quán; **gap block↔block PHẢI lớn hơn gap heading↔body** (cấm mọi gap bằng nhau).
- Lề trái/phải đối xứng, rộng rãi. (Khớp mục "Missing whitespace / double the spacing" của skill.)

## 4. Color — tiết chế & nghĩa cố định
- **1 màu = 1 ý nghĩa** xuyên suốt (đỏ = lỗi/cảnh báo, không lẫn). (Khớp "one accent color" của skill.)
- **Contrast nền/chữ ưu tiên cao nhất.** Cấm chữ nhạt trên nền nhạt / trắng trên nền nhạt.

## 5. Chống "AI smell" — khách Nhật đặc biệt ghét (bổ sung danh sách của skill)
- ❌ **Gạch chân accent dưới tiêu đề** → khoảng trắng / dải nền đậm.
- ❌ **Thanh màu dọc ở cạnh card** (stripe trái/phải) → card 1 nền phẳng, hoặc dải header đậm trên đầu card.
- ❌ Gradient/glow/shadow tràn lan, card "bồng bềnh" → bề mặt phẳng, sạch, bo góc đồng nhất.
- ❌ Emoji làm icon mục → số (01/02) hoặc nhãn chữ.
- (Trùng & củng cố các mục AI-smell sẵn có: purple-blue gradient, glow shadow, 3-card farm…)

## 6. Icon — 1 hệ thống, nghĩa cố định
- 1 bộ icon thống nhất, cùng độ dày nét; cấm trộn icon tự vẽ/tải lẻ. 1 icon = 1 nghĩa phổ thông.
  (Khớp "inconsistent stroke widths" của skill; với khách Nhật tính nhất quán càng bị soi.)

## 7. Bảng & số — chỗ khách Nhật soi kỹ nhất
- **Kẻ bảng hiện rõ & đều**, đừng mất đường dọc; header có nền phân biệt.
- **Số canh phải / thẳng cột,** thẳng hàng thập phân (dùng `tabular-nums`).
- Đơn vị để trong ngoặc ở header (件/%/点…).

## 8. Tinh thần
Precision > decoration. Trang **canh chuẩn · tương phản rõ · tiết chế màu · nhất quán** được khách Nhật
đánh giá 信頼できる hơn nhiều trang hào nhoáng nhưng lệch lạc.

---
### Lưu ý mâu thuẫn nhẹ cần cân chỉnh theo loại trang
- Skill khuyên với Nhật: "Zen — nhiều whitespace, tối giản" → đúng cho **landing/marketing**.
- Guideline khách lại **mật độ cao** (vì là **dashboard sản phẩm**). Mật độ cao OK *nếu* sạch & canh chuẩn,
  nhưng đó là địa hạt của `meo-frontend-check`, không phải skill này. Với web marketing → ưu tiên Zen.
