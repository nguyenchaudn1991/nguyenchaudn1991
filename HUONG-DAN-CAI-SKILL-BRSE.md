# Hướng dẫn cài & dùng bộ skill BrSE (jp-comm + jp-requirement)

Bộ 2 skill hỗ trợ công việc BrSE với khách Nhật. Cài **cả hai** (chúng tham chiếu lẫn nhau):

| Skill | File | Dùng cho việc |
|---|---|---|
| **jp-comm** | `jp-comm-brse.zip` | Viết cho khách: 障害報告 (báo sự cố), 催促 (nhắc trả lời), 納期交渉 (thương lượng deadline), 謝罪, 依頼 · Bảng Q&A / 課題表 · 納品報告 / リリース連絡 / 週次報告 |
| **jp-requirement** | `jp-requirement-brse.zip` | Xử lý yêu cầu: phân tích yêu cầu (từ pptx/md/html/Figma/Backlog) → đề xuất phương án + trade-off · Viết 要件定義書 · Dịch & "nhai nhỏ" spec Nhật cho team dev VN |

> **Không hỗ trợ:** 議事録 và 工数見積 — theo quy trình công ty, vai trò khác đảm nhận.

---

## 1. Cài trên Claude (khuyến nghị — chất lượng tốt nhất, hỗ trợ skill gốc)

### claude.ai (web / app)
1. Vào **Settings → Capabilities → Skills** (tài khoản cần bật tính năng Skills).
2. Bấm **Upload skill** → chọn `jp-comm-brse.zip` → Upload.
3. Lặp lại với `jp-requirement-brse.zip`.
4. Xong — trong chat, skill **tự kích hoạt theo từ khóa**, không cần bật tắt gì thêm.

### Claude Code (terminal / VS Code)
Giải nén 2 zip vào thư mục skill cá nhân:
```
C:\Users\<tên bạn>\.claude\skills\jp-comm\        (chứa SKILL.md + references\)
C:\Users\<tên bạn>\.claude\skills\jp-requirement\
```
Mở phiên mới là skill được nhận.

## 2. Cài trên ChatGPT (không có định dạng skill — dùng Projects / Custom GPT)

1. Tạo **Project** mới (hoặc Custom GPT nếu muốn share trong team).
2. Giải nén zip. Mở file `SKILL.md`, copy toàn bộ nội dung → dán vào ô **Instructions** của Project.
3. Upload các file trong thư mục `references\` vào phần **Files** (knowledge).
4. Làm 2 Project riêng cho 2 skill (hoặc 1 Project gộp: dán cả 2 SKILL.md, upload cả 6 file references).

## 3. Cài trên Gemini (Gems)

1. Tạo **Gem** mới.
2. **Instructions** = nội dung `SKILL.md`; đính kèm các file trong `references\`.
3. Tương tự ChatGPT: 2 Gem riêng hoặc 1 Gem gộp.

---

## 4. Cách dùng — gõ tự nhiên kèm từ khóa

Ví dụ prompt thực tế (skill tự nhận diện):

- 「Khách gửi file pptx yêu cầu mới (đính kèm), **phân tích yêu cầu** và đề xuất phương án giúp mình」
- 「Viết **要件定義書** từ kết quả phân tích này」
- 「**Dịch spec** này và nhai nhỏ thành task cho team dev」
- 「Viết **障害報告** về sự cố login sáng nay: [dán thông tin sự cố]」
- 「Soạn tin **nhắc khách** trả lời Q&A số 12, đã quá hạn 3 ngày, đang chặn việc X」
- 「Viết **週次報告** tuần này từ các thông tin sau: [dán data]」
- 「Làm **bảng Q&A** từ các điểm chưa rõ trong spec này」

Mẹo: đưa càng nhiều bối cảnh thật (số liệu, ngày, tên màn hình, nội dung khách viết) thì đầu ra càng chuẩn. Thiếu thông tin, skill sẽ tự hỏi lại hoặc đánh dấu `未確認` — **đừng để AI tự bịa số**.

## 5. Quy tắc bắt buộc khi dùng

1. **Data policy:** tuân thủ quy định công ty khi đưa tài liệu khách hàng vào AI tool. Chưa rõ tài khoản/plan nào được phép → hỏi quản lý **trước** khi dán tài liệu khách.
2. **Người gửi chịu trách nhiệm cuối:** skill là khung hỗ trợ — luôn tự review (đặc biệt số liệu, tên riêng, 敬語) trước khi gửi khách.
3. Đầu ra tiếng Nhật mặc định です・ます調, hướng tới khách quản lý cấp cao — nếu khách của bạn là kỹ sư/casual hơn, cứ yêu cầu chỉnh tone trong prompt.

## 6. Cập nhật & feedback

- **Phiên bản hiện tại: v1.0 (2026-07-11)** — maintainer: **Châu**.
- Có bản mới: xóa skill cũ trong Settings → upload zip mới (claude.ai), hoặc thay nội dung Instructions/Files (ChatGPT/Gemini).
- Gặp case chưa được cover, output sai manner, hoặc muốn thêm tình huống → nhắn Châu kèm ví dụ cụ thể. Skill lớn lên bằng feedback thật của mọi người.
