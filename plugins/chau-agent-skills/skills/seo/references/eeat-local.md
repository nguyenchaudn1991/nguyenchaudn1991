# E-E-A-T + Local SEO / MEO

`last_verified: 2026-08-13` — kiểm lại nguồn chính thức nếu quá ~3 tháng.

## Mục lục

- 3. E-E-A-T (25đ) — Experience · Expertise · Authoritativeness · Trust
- Local SEO / MEO — khi doanh nghiệp có địa điểm phục vụ

---

## 3. E-E-A-T — 25đ

### E-E-A-T thật ra là gì

`[Xác minh]` **E-E-A-T không phải một ranking factor.** Google nói rõ: đây là khung khái niệm
trong tài liệu hướng dẫn cho **người đánh giá chất lượng tìm kiếm** (Search Quality Raters),
dùng để mô tả *thế nào là nội dung tốt* — không phải một chỉ số mà thuật toán chấm điểm và
cũng không có "điểm E-E-A-T" nào tồn tại.

Vậy tại sao vẫn làm? Vì các tín hiệu cụ thể của nó — tác giả có danh tính, thông tin liên hệ
thật, số liệu có nguồn, entity nhất quán — đều là **thứ người đọc và hệ thống máy có thể kiểm
chứng được**. Trong đó `Trust` là trục quan trọng nhất.

⚠️ **Không viết:** "E-E-A-T quyết định việc Google và AI có trích dẫn hay không." Đó là suy
diễn nhân quả không có căn cứ. **Viết đúng:** "đây là các tín hiệu tin cậy máy đọc được;
làm đủ thì loại bỏ được lý do để bị đánh giá thấp."

### Experience — trải nghiệm thực

- [ ] **Bằng chứng "tôi đã làm":** case study có số liệu thật (con số, thời gian, quy mô),
      ảnh chụp/diagram tự làm — không dùng stock/AI image cho phần bằng chứng. Viết từ góc
      nhìn người trực tiếp làm ("chúng tôi đã triển khai X, gặp lỗi Y, xử lý bằng Z").
- [ ] **Định nghĩa thực chiến:** không copy định nghĩa Wikipedia; tự định nghĩa lại khái niệm
      từ kinh nghiệm dự án. `[Heuristic]` — làm vì nội dung gốc có giá trị hơn nội dung nhai
      lại, không phải vì có cơ chế nào ưu tiên nó.

### Expertise — chuyên môn

- [ ] **Byline mọi bài viết:** tên tác giả + link tới trang tác giả. Không bài nào "vô danh".
- [ ] **Trang tác giả/About chuẩn entity:** 1 trang duy nhất làm **entity home**, liệt kê
      credential **thật** (năm kinh nghiệm, chứng chỉ, chức danh, dự án). Đây là trang
      canonical để mọi hệ thống hiểu "người này là ai".
- [ ] **Person schema:** dùng property **đúng và có thật** — `jobTitle`, `worksFor`,
      `knowsAbout`, `hasCredential`, `alumniOf`. Không có chứng chỉ thì **bỏ trống
      `hasCredential`**, không bịa để "cho đủ field". Field sai còn hại hơn field thiếu.

### Authoritativeness — thẩm quyền

- [ ] **Entity linking (`sameAs`) nhất quán:** Person/Organization schema trỏ tới đúng bộ
      profile thật (LinkedIn, GitHub, Google Maps, X…).
- [ ] Cách làm gọn: xây **1 entity page trung tâm** mang bộ `sameAs` đầy đủ, các trang khác
      tham chiếu tới entity đó (`@id`) thay vì lặp lại toàn bộ danh sách trên mọi trang.
      Mục tiêu là **không mâu thuẫn**, không phải "copy y hệt khắp nơi".
- [ ] **Nhất quán cross-platform:** tên, chức danh, mô tả trên website = LinkedIn = GitHub =
      mọi profile. Mâu thuẫn giữa các nguồn làm loãng việc nhận diện thực thể.
- [ ] `[Thử nghiệm]` **Được nhắc đến ngoài domain** (guest post, phỏng vấn, directory ngành):
      hợp lý về mặt trực giác và tốt cho kinh doanh, nhưng đừng trình bày như cơ chế đã được
      chứng minh. Đo bằng: có bao nhiêu nguồn độc lập nhắc đúng tên + đúng mô tả.

### Trustworthiness — tin cậy

- [ ] HTTPS toàn site; trang Liên hệ thật (form/email/địa chỉ hoạt động); Privacy Policy nếu
      có thu thập dữ liệu.
- [ ] **Không fake tín hiệu:** không fake `dateModified`, không fake review, không nhồi
      credential không có thật. Đây là ranh giới đạo đức, không phải mẹo SEO — và tín hiệu
      giả bị phát hiện thì thiệt hại lan ra toàn domain.
- [ ] **Trích nguồn khi nêu số liệu ngoài:** số liệu không phải của mình → link tới nguồn gốc
      (primary source, không phải bài blog dẫn lại). Số liệu của mình → nêu rõ bối cảnh đo
      (dự án nào, thời điểm nào, đo thế nào).
- [ ] **Đồng bộ số liệu tuyệt đối:** một con số kinh doanh (năm kinh nghiệm, số nhân sự, số
      khách hàng) xuất hiện ở N nơi (UI, HTML tĩnh, schema, `llms.txt`, README, LinkedIn) thì
      cả N nơi phải giống nhau. Mâu thuẫn số liệu là thứ người đọc kỹ lẫn hệ thống đối chiếu
      đều bắt được.

---

## Local SEO / MEO — khi doanh nghiệp có địa điểm phục vụ

- [ ] **NAP nhất quán:** Name–Address–Phone trên website = Google Business Profile = mọi
      directory/map/SNS. Mục tiêu là **cùng một thực thể, không mâu thuẫn** — cho phép khác
      biệt về format do ràng buộc từng platform (có/không mã vùng, cách viết tầng/phòng), miễn
      là **có một nguồn dữ liệu chuẩn (canonical) rõ ràng** và mọi nơi phái sinh từ đó. Yêu
      cầu giống nhau *từng ký tự* là quá cứng và không khả thi khi platform tự chuẩn hoá.
- [ ] **Google Business Profile là entity local gốc:** category chính xác, giờ mở cửa thật,
      ảnh thật cập nhật định kỳ, review được trả lời; website ↔ GBP link 2 chiều (`sameAs`
      trong LocalBusiness schema trỏ GBP/map URL).
- [ ] **Trang riêng cho từng địa điểm — chỉ khi có nội dung thật sự riêng.** Mỗi trang phải
      có thông tin riêng có giá trị (đội ngũ, dịch vụ tại chỗ, hướng đi, giờ mở cửa, ảnh thật).
      ⚠️ Nhân bản một template và chỉ thay tên khu vực là **doorway page** — vi phạm guideline
      Google và có thể bị phạt. Không đủ nội dung riêng → **gộp lại một trang danh sách**.
- [ ] **Tín hiệu khu vực trong nội dung:** tên khu vực xuất hiện tự nhiên trong
      title/H1/nội dung/alt; đường đi, landmark gần đó — dùng đúng cách gọi của khách địa
      phương khi họ tìm kiếm.
