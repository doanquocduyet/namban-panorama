# SỔ RÀ SOÁT NAMBAN PANORAMA — 22 ĐẾN 24/9/2026

> **Tờ này để làm gì.** Ghi lại **toàn bộ** những gì đã rà trên nambanpanorama.com trong ba ngày
> 22–24/9/2026: cái gì sai và đã sửa, cái gì đúng sẵn, cái gì máy báo sai mà suýt sửa nhầm,
> lỗi do chính người rà tự gây, việc cố ý không làm, và việc còn treo. Đưa nguyên văn cho người
> hoặc trợ lý đang lo **một web khác**, bảo họ **rà đúng từng mục** xem web đó có dính không.
>
> **Web này là gì.** Web tĩnh HTML/CSS/JS thuần, deploy Vercel. Ngày 24/9: 194 file HTML,
> 178 trang tiếng Việt, 188 URL trong `sitemap.xml`, 400 ảnh. Là một **tờ báo** về bất động sản
> một vùng, không phải web bán hàng — nên có mấy luật riêng (không CTA bán, dám nói "đừng mua").
>
> **Đọc theo thứ tự nào.** Phần A tra nhanh. Phần B chi tiết từng lỗi đã sửa, mỗi lỗi có:
> triệu chứng · vì sao nguy · cách tự kiểm · cách sửa · cách chặn tái phát. Phần C là thứ đã sạch.
> **Phần D và E quan trọng nhất cho người rà web khác**: báo động giả và lỗi tự gây — đó là chỗ
> người rà giỏi cũng hay sai. Phần I có lệnh kiểm copy chạy được.

---

## A. BẢNG TRA NHANH

Mức: 🔴 mất niềm tin / sai sự thật · 🟠 mất thứ hạng, mất trích dẫn AI · 🟡 khó dùng.

### A1. Lỗi thật đã sửa

| # | Lỗi | Mức | Quy mô |
|---|---|---|---|
| 1 | Bài cảnh báo thiên tai **gán rủi ro cho chính vùng mình** ở H1, keyword, FAQ, schema, ảnh | 🔴 | 1 bài, 7 chỗ |
| 2 | Phiếu viết bài đưa **số liệu không tra được nguồn** | 🔴 | 3 số + 1 tên tổ chức |
| 3 | Phiếu yêu cầu **ghi ngày đăng lùi** về trước ngày đăng thật | 🔴 | 1 bài |
| 4 | Form "Nhận Brief" hiện ra nhưng **bấm không có gì xảy ra** | 🔴 | 2 trang |
| 5 | Tựa **hứa thứ thân bài không có** | 🟠 | 2 bài |
| 6 | `lastmod` trong sitemap **cũ hơn** ngày sửa thật trong bài | 🟠 | 106 URL |
| 7 | H1 là **câu văn của người viết**, không phải câu người ta gõ | 🟠 | 8 bài |
| 8 | Title là câu văn, không phải câu tìm kiếm | 🟠 | 5 bài |
| 9 | Description **không nhắc tên vùng** lần nào | 🟠 | 25 bài |
| 10 | Cụm 3 bài **chỉ trỏ vào nhau**, không bài nào khác trỏ tới | 🟠 | 3 bài |
| 11 | Bài mới **mồ côi**, 0 link vào từ thân bài | 🟠 | 3 bài |
| 12 | Thiếu `og:url` | 🟠 | 4 trang |
| 13 | Ảnh dùng **đường dẫn tương đối** `images/…` | 🟠 | 9 thẻ / 5 file |
| 14 | Một ảnh dùng ở **quá 2 bài**, trái trần của site | 🟡 | 9 chỗ → xử 9 |
| 15 | Alt/caption ảnh **tả thứ không có trong ảnh** | 🟠 | 2 ca bắt được |
| 16 | Chữ neo ở bài khác **còn tựa cũ** sau khi đổi tựa | 🟡 | 6 neo |
| 17 | `speakable` trỏ vào class **không tồn tại** | 🟠 | 1/213 selector |
| 18 | Ô nhập chữ **dưới 16px** → iPhone tự phóng to trang | 🟡 | 6 trang |
| 19 | Nút hamburger **dưới vùng chạm 44px** | 🟡 | 2 trang |
| 20 | Bộ lọc CTA của máy đăng tự động **chặn nhầm bài tốt** | 🟠 | 2 bài bị chặn vĩnh viễn |
| 21 | Hàng đợi đăng mạng xã hội **trống từ 18/9**, không ưu tiên | 🟠 | 0 bài chờ |
| 22 | H1 **rớt lẻ 1–2 chữ** xuống dòng cuối | 🟡 | 7 H1 |

### A2. Thứ đã rà và **sạch** — xem phần C (19 hạng mục, có số)

### A3. Báo động giả — suýt sửa nhầm — xem phần D (17 ca)

### A4. Lỗi do người rà tự gây — xem phần E (11 ca)

---

## B. CHI TIẾT TỪNG LỖI ĐÃ SỬA

### 🔴 1. Bài cảnh báo thiên tai gán rủi ro cho chính vùng mình

**Triệu chứng.** Bài về đợt mưa lớn 21–24/9 có thân bài trung dung, nhưng **khung ngoài** cùng đẩy
một ý "vùng này mưa là sạt lở":
- H1 và title: *"Mưa lớn ở Nam Ban: dấu hiệu sạt lở và lô đất nào đáng để ý"*
- Keyword: `sạt lở đất Nam Ban`, `Nam Ban có sạt lở không`, `đất ở Nam Ban có dễ sạt lở không`
- FAQ mở đầu: *"Đất ở Nam Ban có dễ sạt lở không?"*
- Trường `about` trong schema: *"Mưa lớn và sạt lở đất ở Nam Ban"*
- Ảnh đầu bài: sườn đồi trọc vừa san, trời sắp mưa, caption "chưa có cây giữ đất"

**Vì sao nguy.** Người đọc chỉ thấy H1 và ảnh. Google và AI đọc keyword, FAQ, schema. Cả hai phía
cùng nhận một thông điệp mà thân bài không hề nói. Một web sống bằng niềm tin vào vùng đất lại tự
gắn nhãn rủi ro cho vùng đó, và AI sẽ trích nguyên câu FAQ đó khi ai hỏi "vùng X có sạt lở không".

**Tự kiểm.** Với mọi bài về thiên tai, rủi ro, môi trường: đọc riêng `<title>`, H1, meta
description, meta keywords, câu hỏi FAQ, `about`/`name` trong JSON-LD, alt và caption ảnh. Hỏi:
*có chỗ nào ghép tên vùng mình với tên thiên tai không?*
```bash
grep -n '<title>\|<h1\|name="keywords"\|name="description"\|"about"\|"name":\|alt=\|<figcaption' bai.html \
  | grep -i 'sạt lở\|ngập\|lũ\|thiên tai\|nguy hiểm'
```

**Sửa.** H1 đổi sang *cách nhìn lô đất khi mưa lớn*. Bỏ 3 keyword, thêm 3 keyword về "nhìn đất mùa
mưa". FAQ đổi thành *"Mưa lớn thì lô đất nào ở Nam Ban cần nhìn kỹ hơn?"*. Schema `about` đổi.
Bỏ hẳn ảnh, ảnh chia sẻ về ảnh thương hiệu. Thân bài giữ nguyên.

**Chặn tái phát (đã thành luật).** Bài về mưa bão, thiên tai, rủi ro môi trường: H1, title, meta,
keyword, FAQ, schema, ảnh **không được tự tạo cụm khẳng định hay gợi rủi ro cho cả vùng** ("sạt lở
đất X", "X có dễ sạt lở không", ảnh đồi trọc dưới mưa). Rủi ro nằm ở **từng lô**, nói trong thân bài.
Dấu hiệu chung thì dẫn nguồn cơ quan chức năng, không neo tên vùng.
**Phân biệt:** câu hỏi **có sẵn, người ta thật sự gõ** ("Mùa mưa X có ngập không?") mà câu trả lời
trả lời thẳng bằng dữ kiện thì **giữ** — đó là nhà của truy vấn, và thường chính là chỗ gỡ nỗi sợ.

---

### 🔴 2. Số liệu trong phiếu không tra được nguồn

**Triệu chứng.** Phiếu viết bài mưa lớn ghi "Sơn Điền 112mm, Đơn Dương 66mm, Lạc Dương 55mm" và
"tài liệu của Cục… phối hợp UNICEF". Tra nhiều nguồn: không thấy ba số này ở đâu, không thấy UNICEF
trong tài liệu nào. Các số khác trong phiếu thì khớp: 150–250mm, trên 400mm, trên 100mm/3 giờ,
văn bản 54/BCĐ-BNNMT ngày 20/9/2026.

**Vì sao nguy.** Một số sai là sập uy tín cả web. Số lẻ cụ thể nhìn rất "thật", nên người đọc và AI
đều tin, rồi trích lại.

**Tự kiểm.** Lập bảng mọi con số và mọi tên cơ quan trong bài, cạnh mỗi dòng ghi **URL nguồn**.
Dòng nào không có URL thì không được đăng.

**Sửa.** Gỡ ba số và chữ UNICEF. Danh sách dấu hiệu sạt lở viết lại **đúng theo** bản của Cục Quản lý
đê điều và Phòng, chống thiên tai. Hai khuyến cáo không tìm được nguồn thì viết lại thành quan sát,
ghi rõ là quan sát của web.

**Chặn tái phát.** Phiếu có dòng "lệch → dừng, báo". Cách làm đúng khi bài gấp: **gỡ đúng chỗ lệch,
đăng phần đã kiểm, báo lại** — không dừng cả bài, cũng không đăng số chưa kiểm.

---

### 🔴 3. Ghi ngày đăng lùi về trước

**Triệu chứng.** Phiếu ghi `datePublished 20/9/2026` cho bài đăng ngày 24/9.

**Vì sao nguy.** Ngày đăng trong schema là một **khẳng định sự thật**. Lùi ngày để bài trông "kịp
thời" là làm giả. Google đối chiếu ngày index thật; AI trích sai thời điểm.

**Sửa.** Ghi ngày đăng thật 24/9. Đầu bài thêm một dòng: *"Bài đăng ngày 24/9/2026, ngày cuối của
đợt dự báo."*

---

### 🔴 4. Form hiện ra nhưng bấm không có gì xảy ra

**Triệu chứng.** Trang hub Brief và bài Brief 01 có ô "Email của bạn" + nút "Nhận Brief khi có số
mới". Form đặt `onsubmit="return false"`, nút `type="button"` không gắn hàm nào.

**Vì sao nguy.** Khách nhập email, bấm, không có gì xảy ra, không báo lỗi. Mất đúng người muốn quay
lại. Không log nào ghi lại, nên không ai biết.

**Tự kiểm.**
```bash
grep -n '<form[^>]*onsubmit="return false' *.html
grep -n '<button type="button"' *.html   # rồi xem nút đó có onclick/listener không
```
Rộng hơn: với mọi `<form>` và mọi nút, **bấm thật bằng Playwright** và đo xem có request nào đi ra
hoặc DOM có đổi không.

**Sửa.** Thay form chết bằng một dòng trầm dẫn sang trang liên hệ. Không dựng form mới.

---

### 🟠 5. Tựa hứa thứ thân bài không có

**Triệu chứng.**
- Title *"Có nên mua đất 2026? Cơ hội, rủi ro và **sai lầm** thường gặp"* — thân bài có 0 chữ
  "sai lầm".
- Title mới đề xuất *"**Lịch sử** Nam Ban: 10/10/1975…"* — thân bài có 0 chữ "lịch sử".

**Vì sao nguy.** Người bấm vào để đọc "sai lầm" rồi không thấy, thoát ra ngay. Google đọc được cả
hai phía và hạ độ tin của trang.

**Tự kiểm.** Mỗi cụm trong title/H1 phải xuất hiện ≥1 lần trong thân bài — lệnh ở I.5.

**Sửa.** Bài 1: bỏ vế "sai lầm" khỏi title, description, keyword. Bài 2: đổi một H2 thành
*"Lịch sử Nam Ban từ 1975 tới nay đi qua những mốc nào?"* để cụm có thật trong bài.

---

### 🟠 6. `lastmod` trong sitemap cũ hơn ngày sửa thật

**Triệu chứng.** 106/187 URL có `lastmod` cũ hơn `dateModified` trong bài. Ví dụ trang chủ ghi
24/7 trong khi bài ghi sửa 5/9.

**Vì sao nguy.** Google dựa vào `lastmod` để quyết định có quét lại không. Ghi cũ thì bài đã sửa
không được quét lại, mà độ tươi là thứ AI ưu tiên khi trích.

**Tự kiểm.** Xem lệnh I.4.

**Sửa.** Đồng bộ `lastmod` theo ngày lớn nhất trong `dateModified`/`datePublished`.
**Chỉ cho tiến, không cho lùi.** Bản đầu của script đồng bộ hai chiều và sẽ **lùi** 10 URL về ngày
cũ hơn (vì bài đó đã được bump sitemap mà quên bump schema). Đã sửa thành chỉ cập nhật khi ngày
trong bài **mới hơn**.

---

### 🟠 7. H1 là câu văn của người viết

**Triệu chứng.** 8 H1 đọc hay nhưng không ai gõ:

| H1 cũ | H1 mới |
|---|---|
| Nam Ban và Đại học Đà Lạt ngồi lại với nhau | Nam Ban có trường đại học không? Hợp tác với Đại học Đà Lạt 9/2026 |
| Người rời Sài Gòn, và mảnh vườn anh không tính trước | Người rời Sài Gòn lên Nam Ban: chuyện bỏ phố và làm cà phê |
| Tiềm năng đầu tư Nam Ban: đọc cơ hội qua lăng kính toàn cảnh | Có nên mua đất Nam Ban 2026? Cơ hội và rủi ro không ai nói thẳng |
| Đọc một tin rao đất Nam Ban thế nào cho khỏi hoa mắt | Đọc tin rao đất Nam Ban: chia giá, nhìn thổ cư, hỏi đường vào |
| Nam Ban hay Di Linh? Nếu hỏi một người đã đi về nhiều năm. | Nam Ban hay Di Linh? Một người Sài Gòn đi về nhiều năm sẽ chọn nơi nào |
| Nam Ban hay Đơn Dương? | Nam Ban hay Đơn Dương? Hai vùng ven Đà Lạt cho hai kiểu người |
| Nam Ban hay D'ran | Nam Ban hay D'ran: chọn vùng nào để mua đất, làm vườn |
| Có đất Nam Ban nhưng chưa xây nhà | Có đất Nam Ban nhưng chưa xây nhà: nên chờ hay nên làm? |

**Cách nhận ra.** Hỏi *"có ai gõ đúng cụm này vào Google không?"*. Dấu hiệu H1 đang phục vụ tai
người viết: câu đảo ngữ, câu hai vế kiểu "A, và B", chữ văn vẻ ("lăng kính", "ngồi lại", "hoa mắt").

**Sửa.** H1, `og:title`, `headline` đổi cùng lúc thành **một chuỗi**. Title giữ nguyên ở đợt này để
tín hiệu xếp hạng không đổi. Mỗi cụm mới đều đã kiểm có trong thân bài.

**Kèm.** Đổi H1 thì **lời đọc audio đổi** (bộ đọc đọc H1 trước) → phải sinh lại MP3. Đổi H1 thì
feed, llms.txt, chữ neo ở bài khác cũng phải đổi theo (xem lỗi 16).

---

### 🟠 8. Title là câu văn

5 title đổi (có duyệt của chủ web):

| Cũ | Mới | Lý do chọn |
|---|---|---|
| Những điều Google Maps không nói về Nam Ban | Nam Ban có yên tĩnh không? Những điều bản đồ không cho thấy | Các cụm "sống ở Nam Ban", "có buồn không", "thiếu gì" **đã có bài nhà** khác. "Có yên tĩnh không" chưa bài nào giữ và đúng mục đầu của bài. "Google Maps" giữ lại ở câu dẫn và thân bài. |
| Nhiều người tính mua đất Đà Lạt, cuối cùng lại dừng ở Nam Ban | Mua đất Đà Lạt hay Nam Ban? Vì sao nhiều người dừng ở Nam Ban | Đưa cụm so sánh người ta gõ lên đầu |
| 2 cây xăng Petro mới… một tín hiệu nhỏ đáng chú ý | Cây xăng mới ở Nam Ban: hai trạm Petrolimex trên ĐT.725 | **Bỏ "đang hoàn thiện"** để tựa không sai khi cây xăng khai trương |
| 10/10/1975: ngày người Hà Nội bắt đầu câu chuyện Nam Ban | Lịch sử Nam Ban: 10/10/1975, ngày người Hà Nội bắt đầu câu chuyện | Thêm cụm "lịch sử Nam Ban" + thêm cụm đó vào một H2 |
| Có nên mua đất 2026? Cơ hội, rủi ro và sai lầm thường gặp | Có nên mua đất Nam Ban 2026? Cơ hội và rủi ro không ai nói thẳng | Bỏ vế hứa suông |

**Chặn tái phát.** Trước khi chọn cụm mới cho một title, **quét toàn site** xem cụm đó đã có trang
nào làm nhà chưa (title, H1, FAQ). Có rồi thì chọn cụm khác, nếu không hai bài tự tranh nhau.

---

### 🟠 9. Description không nhắc tên vùng

**Triệu chứng.** 26/171 bài có description không chứa "Nam Ban" lần nào. Ví dụ: *"Hoa cà phê nở
tháng 2–4, rộ nhất tháng 3…"*.

**Vì sao nguy.** Description là đoạn trích Google và AI hay lấy. Không có tên vùng thì đoạn trích
không gắn được vào thực thể, người tìm "cà phê Nam Ban" không thấy chữ mình gõ.

**Sửa.** 25 bài thêm cụm định vị ngay đầu câu, giữ nguyên ý: *"Mùa cà phê Nam Ban: hoa nở tháng
2–4…"*. Sửa đồng bộ **ba chỗ**: meta description, og:description, `description` trong JSON-LD.
**1 bài cố ý giữ**: bài về bảng giá đất cấp tỉnh — quy định cấp tỉnh thì neo tên tỉnh, neo tên xã
là sai phạm vi và đẩy người ở xã khác ra khỏi kết quả.

---

### 🟠 10 và 11. Bài mồ côi, cụm bài ốc đảo

**Triệu chứng.** 3 bài cùng cụm "lên Lâm Đồng sống" chỉ trỏ vào nhau; không bài nào khác trỏ tới,
không tới được từ trang chủ bằng link. 3 bài mới đăng khác có 0 link vào từ thân bài.

**Vì sao nguy.** Google chỉ biết tới qua sitemap, đánh giá thấp. Người đọc không bao giờ đi tới.

**Tự kiểm.** Dựng đồ thị link, **chỉ đếm link trong thân bài** (loại nav, footer, menu). Xem I.7.
Nhớ đếm cả `href="/slug"` lẫn `href="slug"` — chỉ đếm một kiểu sẽ báo mồ côi giả.

**Sửa.** Gắn link **vào câu có sẵn** trong bài liên quan, chữ neo là chính cụm trong câu. Không viết
thêm câu mới, nên lời đọc audio không đổi. Không rải link lấy số.

---

### 🟠 12 và 13. Thiếu `og:url`, ảnh đường dẫn tương đối

4 trang thiếu `og:url` → đã thêm. 9 thẻ `<img>` dùng `images/x.webp` thay vì `/images/x.webp` →
vỡ ngay khi URL đổi cấu trúc (thêm thư mục, thêm `/` cuối) → đã sửa cả 9.
```bash
grep -L 'property="og:url"' *.html
grep -n 'src="images/' *.html
```

---

### 🟡 14 và 🟠 15. Ảnh vượt trần dùng lại, và alt tả thứ không có

**Luật của site.** Một ảnh tối đa 2 bài (tính trên bài gốc, **không tính bản dịch**, tách vai ảnh
hiển thị với ảnh chia sẻ).

**Cách đã làm.** Workflow nhiều tác tử: tác tử chọn **bắt buộc mở ảnh ra nhìn** trước khi chọn, rồi
tác tử khác **cố bác**. Đợt 1: 4/9 lựa chọn qua phản biện. Đợt 2: 4 thay + 1 gỡ hẳn ảnh (kho không có
tấm nào đúng chủ đề — bài không ảnh còn hơn ảnh gán tạm).

**Lỗi alt bị phản biện bắt được — rất dễ mắc:**
- Ảnh tên `ca-phe-che-bien-rua-qua` → alt viết "lúc **rửa** quả sau thu hái". Trong ảnh chỉ thấy bàn
  tay vốc quả trên miệng thùng. Chữ "rửa" lấy **từ tên file**.
- Alt "đồi **thông** phía sau" — cây trong ảnh là tùng trồng cảnh. Viết sai loài cây còn trái sự thật
  của vùng (rừng thông ở vùng này ít).
- Ảnh vệ tinh thửa đất có **đường vẽ đè và một lô khoanh vàng** — nhìn y như ảnh tin rao. Bác.
- Bản đồ quy hoạch chữ ~3px ở màn điện thoại — caption khẳng định "đã ghi tên đơn vị mới" mà người
  đọc không tự thấy được. Bác.

**Chặn tái phát.** Alt và caption **chỉ tả thứ nhìn thấy trong khung**. Không suy từ tên file. Không
suy động từ ("rửa", "hái"). Không đoán địa danh khi khung không có dấu hiệu nhận diện.

**Kèm.** Ảnh vuông/dọc đặt vào khung ngang thì phải đổi `width`/`height` thật (chống nhảy trang) và
giới hạn bề rộng (ảnh vuông 1080px chiếm cả màn PC). Đổi ảnh **không đổi lời đọc** → không cần
sinh lại audio (kiểm bằng hàm trích lời đọc, không đoán).

---

### 🟡 16. Chữ neo ở bài khác còn tựa cũ

Sau khi đổi tựa, **6 link** ở bài khác vẫn mang tựa cũ, trong đó 4 link trỏ tới bài "tiềm năng đầu
tư" vẫn hứa "sai lầm thường gặp". Feed, llms.txt, llms-full.txt cũng còn tựa cũ.
```bash
grep -rn 'Tựa cũ nguyên văn' --include=*.html --include=*.xml --include=*.txt .
```
**Luật.** Đổi tựa một bài = quét tựa cũ trong **mọi** đuôi file, không chỉ bài đó.

---

### 🟠 17. `speakable` trỏ vào class không tồn tại

Web bên cạnh dính 196 trang. Web này dính **1/213** selector: một bài khai `.quick-answer` mà trang
không có phần tử đó. Sửa thành `.art-body > p:first-of-type`. Xem lệnh I.3.

---

### 🟡 18 và 19. Ô nhập dưới 16px, hamburger dưới 44px

iPhone **tự phóng to trang** khi chạm vào ô có chữ dưới 16px. Trang liên hệ có 6/7 ô 15px, ba hub
có ô 14px. Đưa hết lên 16px. Hamburger hai trang liên hệ 38×39 và 30×23 trong khi toàn site 42×43 —
sửa padding, không đổi hình. Đo bằng Playwright ở 390px, không đo bằng đọc CSS (CSS có nhiều lớp đè).

---

### 🟠 20. Bộ lọc CTA chặn nhầm bài tốt

Máy đăng tự động lên mạng xã hội có danh sách chữ cấm để chặn giọng bán hàng. Hai lỗi:
- Cấm cụm "chỉ còn" — nhưng tiếng Việt thường ngày dùng để đo khoảng cách ("chỉ còn 3km").
- Grep thẳng chặn luôn bài **trích lời rao trong ngoặc kép rồi bác lại** — đúng là giọng "dám nói
  đừng mua" mà web muốn.

Hai bài bị chặn **vĩnh viễn** mà không ai biết. Sửa: bỏ "chỉ còn"; chữ cấm nằm **trong ngoặc kép**
thì chỉ nhắc, không chặn. Bản đầu của hàm tách ngoặc cũng sai (ngoặc thẳng `"` mở và đóng cùng ký
tự, phải lấy đoạn chẵn/lẻ xen kẽ) — bắt được vì chạy lại trên **bài thật**, không tin test tự viết.

---

### 🟠 21. Hàng đợi đăng tự động trống

Hàng đợi hết bài từ 18/9, bộ chọn lấy theo thứ tự trong file. Thêm tầng ưu tiên: 1 = tin cập nhật,
2 = bài nền về vùng, 5 = còn lại; sắp theo (ưu tiên, ngày). Nạp thêm 8 bài. Không nạp bài lấy tên
một cơ sở kinh doanh làm trung tâm.

---

### 🟡 22. H1 rớt lẻ chữ xuống dòng cuối

7 H1 vừa đổi bị rớt 1–2 chữ ở 390px hoặc 1440px. Sửa bằng `&nbsp;` giữa các chữ cuối. **Bắt buộc đo
bằng Playwright ở cả hai khổ** sau mỗi lần đổi H1 — đo bề rộng dòng cuối, dưới ~28% bề rộng H1 là rớt.

---

## C. ĐÃ KIỂM VÀ SẠCH — VẪN NÊN KIỂM Ở WEB KHÁC

Đo thật, không đoán. Web khác rất có thể sai ở đúng những chỗ này.

| Hạng mục | Kết quả | Phạm vi |
|---|---|---|
| Canonical trỏ ra web khác / nhiều trang cùng một đích | 0 | 193 file |
| FAQ trong schema mà **không hiện** trên trang | 0 câu | 1.029 câu / 151 bài |
| FAQ trùng nguyên câu giữa 2 bài | 4 nhóm, cả 4 là ngoại lệ có chủ đích | 171 trang |
| Chuỗi CTA cấm trong câu trả lời FAQ | 0 (2 ca "mua ngay" là câu phủ định) | 1.029 câu |
| Nút nổi liên hệ **rỗng** (lỗi nặng nhất web bên cạnh) | 0 — hiện đủ icon 185/187 trang, 2 trang liên hệ cố ý không có | 187 trang × 2 khổ |
| Menu mobile mở được | 187/187 | Playwright bấm thật |
| Mục cuối menu nằm ngoài màn 667px | 0 | 187 trang |
| Tràn ngang | 0 | 187 trang × 390/1440/1920 |
| Preload / prefetch rác hoặc 404 | 0 thẻ | 187 trang |
| Link nội bộ gây chuyển hướng (thiếu `/`, `.html`, `http://`, `www.`) | 0 | trang + sitemap + feed |
| Breadcrumb trỏ trang không tồn tại / item cuối ≠ trang | 0 | 183 trang có breadcrumb |
| JS chặn theo đường dẫn | 0 | file dùng chung + inline |
| JSON-LD hỏng | 0 (trừ file mẫu noindex) | toàn site |
| Link / ảnh / audio gãy | 0 (trừ file mẫu noindex) | toàn site |
| Viewport chặn phóng to | 0 | toàn site |
| Bảng tràn không bọc cuộn ngang | 0 | toàn site |
| `<img>` thiếu `alt` hoặc thiếu `width`/`height` | 0 | 265 thẻ |
| Title trùng / description trùng | 0 | toàn site |
| Thì tương lai cho việc đã xảy ra (sáp nhập 1/7/2025) | 0 ca sai (3 ca "sẽ" đều là việc chưa xảy ra thật) | 171 trang |
| Số tự chọi nhau (khoảng cách, độ cao, dân số, diện tích) | Nhất quán; các biến thể đều là vùng khác hoặc số lịch sử | 171 trang |
| Độ sâu bấm từ trang chủ | Tối đa 3 lần bấm | BFS |

---

## D. BÁO ĐỘNG GIẢ — ĐỪNG SỬA NHẦM

Máy quét báo đỏ, soi tay thì đúng. **Tỉ lệ báo động giả rất cao** — đây là phần người rà web khác
cần đọc kỹ nhất.

| Máy báo | Thật ra |
|---|---|
| "72 rồi 77 câu FAQ trong schema không hiện trên trang" | 0. Bộ quét chỉ tìm `<h3>`, nhiều bài in FAQ bằng `<p><strong>`; và gộp khoảng trắng **trước** khi bỏ dấu câu sinh dấu cách đôi. Gộp khoảng trắng **sau cùng** ra 0. |
| "8/8 khối hiệu ứng trang chủ không hiện khi cuộn" | Hiện đủ. Script cuộn 500px mỗi 20ms, nhanh hơn người thật nên observer chưa kịp bắn. Cuộn tốc độ người thì 8/8. |
| "Bài X thiếu description" | Có đủ. Bộ quét giải mã `&quot;` **trước** khi đọc thuộc tính nên cắt vỡ thuộc tính. |
| "6 trang thiếu toàn bộ thẻ SEO" | 5 trang demo + 404, đều `noindex` và ngoài sitemap. |
| "69 ảnh 0 tham chiếu, 14,6 MB rác" | Kho ảnh để dành có chủ đích, luật cấm xoá. |
| "87 câu FAQ có/không mà đáp không mở bằng có/không" | Đọc tay 48 ca còn lại: đều là câu hỏi phụ thuộc điều kiện, đáp "Nếu…" là đúng. Chỉ lỗi khi đáp trôi sang chủ đề khác. |
| "441 câu trả lời FAQ không có số hay tên riêng" | Không phải lỗi, chỉ là thống kê. |
| "44 ca lặp từ" | 0 ca thật: "năm năm", "chung chung", "đều đều", ô bảng kề nhau. |
| "13 cặp bài giành nhau một từ khoá (>30%)" | Bài anh em khác vùng, khác cây (Gia Lâm ↔ Mê Linh, bơ ↔ cà phê). Ý định tìm kiếm khác nhau. |
| "57 chữ neo lệch hẳn tựa trang đích" | Chữ neo ngắn trong câu ("trước khi xuống tiền") — đúng thiết kế. |
| "15 lớp CSS không có định nghĩa" | Đều có style inline hoặc chỉ là lớp đánh dấu cho JS. Không vỡ gì. |
| "5 trang nhảy bậc tiêu đề h1→h3" | Trang chủ và hub dạng lưới thẻ, trang tin ngắn. Là layout. |
| "Trang lịch mốc không có H2 — ĐỎ" | Trang lịch mốc cố ý không có H2. Checker của người rà sai. |
| "Bài không có ảnh — ĐỎ" | Ảnh vừa được bỏ theo phiếu. Checker đòi ảnh là sai với bài này. |
| "Máy chủ QA trả trang sạch hoàn hảo" | **Máy chủ test đã chết**, trang rỗng đo ra "0 lỗi". Luôn đo thêm một số dương bắt buộc (độ dài title, số H2) và báo đỏ khi bằng 0. |
| "140 title dài hơn 60 ký tự — rút gọn hết" | Xem F1 — **cố ý không làm**. |
| "13 trang ghép tên vùng với từ rủi ro ở khung ngoài" (lệnh I.2 bản đầu) | Bản đầu **nối mọi trường thành một chuỗi** rồi dò → cụm vắt qua hai trường (tên vùng ở keyword này, "sạt lở" ở keyword kia). Dò từng trường riêng thì chỉ còn các **câu hỏi có sẵn người ta thật sự gõ** ("Mùa mưa Nam Ban có ngập không?") — câu trả lời trả lời thẳng, là nhà của truy vấn đó. Giữ. |
| "Bài X thiếu phần tử speakable `.art-body > p:first-of-type`" | Selector phức, bộ quét đơn giản hiểu thành một class. Phần tử có thật. |
| "5km-o-nam-ban mồ côi" | Bộ đếm chỉ đọc khối thân bài, mà trang hub trỏ tới nó không có khối đó → không đếm link từ hub. |
| "Khoảng cách khai khác nhau giữa các bài" | Mỗi bài nói một vùng khác (Đức Trọng 26km, D'ran 35–40km). Chỉ thống nhất thuộc tính **của cả vùng mình**. |

---

## E. LỖI DO NGƯỜI RÀ TỰ GÂY HOẶC SUÝT GÂY

Ghi lại vì **rất dễ lặp**.

1. **Nén lại ảnh đã tối ưu làm ảnh TO RA.** 5 ảnh 300–308KB nén lại để lọt trần 300KB → 4/5 to hơn
   (304→346KB). Đã hoàn nguyên. Vượt trần 0–3% không đáng đổi lấy mất chất lượng.
2. **Script đồng bộ sitemap hai chiều sẽ lùi ngày.** Xem B6. Luôn chạy `--dry` trước, đọc danh sách.
3. **Đổi câu hỏi FAQ mà giữ nguyên câu trả lời.** Phiếu bảo "đổi câu hỏi, giữ câu trả lời" — câu trả
   lời mở bằng "Không nói chung được cho cả vùng." là đáp cho câu hỏi **cũ**. Phải bỏ câu mở đó.
4. **Checker của người rà sai** ở 4 chỗ trong một phiên: đòi H2 ở trang không có H2, đòi ảnh ở bài
   bỏ ảnh, đo bề rộng dòng cuối cộng trùng hộp chữ lồng nhau, regex bắt số vượt qua ranh giới câu.
5. **Cuộn trang về đầu trước khi đo ảnh** → huỷ lazy-load, đo ra ảnh 0px. Đợi `naturalWidth > 0`.
6. **Chụp màn hình giữa lúc cuộn mượt** → nửa dưới trắng, tưởng nội dung mất. Chụp lại khi đứng yên.
7. **Workflow nhiều tác tử viết sai tham số**: danh sách 43KB nhét vào tham số → lỗi; truyền danh sách
   slug thay vì nội dung. Chạy nhầm 1 mục thay vì 140. Hết hạn mức giữa chừng → phải tiếp tục từ nhật
   ký, không chạy lại từ đầu.
8. **Phiếu cho sẵn chuỗi thay thế sai khoảng trắng.** Site chèn `&nbsp;` khắp nơi, gõ lại chuỗi bằng
   dấu cách thường thì thay thế không khớp. Luôn lấy chuỗi raw từ file.
9. **Tưởng đổi ảnh thì phải sinh lại audio.** Không — bộ đọc bỏ qua `<figure>`. Kiểm bằng hàm trích
   lời đọc trước/sau, không đoán.
10. **Kích hoạt sinh audio trước khi nội dung lên nhánh chính** → MP3 đọc bản cũ. Trình tự: đẩy nội
    dung → xác nhận nhánh chính đã đổi → mới kích hoạt. Kiểm commit MP3 phải **mới hơn** commit nội dung.
11. **Sửa ngày trong bài mà quên sitemap.** Khi gắn link vào hai bài cũ, đã đổi `dateModified` nhưng
    không chạy lại đồng bộ `lastmod` → 2 URL lệch. Bắt được khi **chạy thử chính lệnh trong sổ này**.
    Đã sửa. Luật: đổi `dateModified` bài nào thì chạy lại I.4.
12. **Suýt dùng ảnh chủ web để dành cho bài khác** (đường đèo mưa sương). Ảnh có ghi "để dành" trong
    sổ thì không dùng, kể cả khi hợp chủ đề.

---

## F. CỐ Ý KHÔNG LÀM — VÀ VÌ SAO

1. **Không rút gọn 140 title dài hơn 60 ký tự.** Đo thật: 115/140 đã có cụm tìm kiếm nằm trong 42 ký
   tự đầu; **46 bài sẽ mất từ khoá** không có ở H1/description/H2 nếu cắt vế sau. Google xếp hạng bằng
   nguyên văn title, 60 ký tự chỉ là giới hạn hiển thị. Đổi tín hiệu của 80% site cùng lúc để đổi lấy
   lợi ích chưa chứng minh — không làm. Chỉ sửa từng title cụ thể có lỗi thật (B8).
2. **Không gỡ `FAQPage`** dù Google đã khai tử ô FAQ trên kết quả tìm kiếm (5/2026). Structured data
   vẫn là thứ AI đọc để trích.
3. **Không gỡ `llms.txt`** dù 97% file loại này không được bot nào đọc (Ahrefs 5/2026). Không hại,
   nhưng không để nó chặn việc đăng bài.
4. **Không gom CSS trùng giữa các trang.** Đo: sau nén chỉ đỡ ~1,4KB/trang. Không đáng rủi ro sửa
   hàng trăm file.
5. **Không cấm chữ "đầu tư".** 177/178 trang có chữ này (phần lớn là menu), hub `/dau-tu` là mục menu
   chính, người ta gõ "đầu tư đất…". Cái cấm là **giọng hô hào** ("cơ hội vàng", "x2 x3", "chắc lời").
6. **Không mở trang riêng cho khóa tu ở chùa** dù có từ khoá — chùa đã có bài nhà, và thông tin khóa
   tu chưa kiểm được nguồn chắc.
7. **Không gỡ lead form** giữa bài bản đồ quy hoạch và ô nhận tin ở 3 hub — chạm luật "không CTA",
   nhưng là thành phần chủ web dựng có chủ đích. Để chủ web quyết.
8. **Không đổi H1 "mấy ngày này" của bài mưa lớn** dù chữ đó chỉ đúng trong đợt mưa. Chủ web chốt:
   bài có ngày đăng, người đọc tự biết.

---

## G. BÀI HỌC GỐC

1. **Khung ngoài nói to hơn thân bài.** Thân bài trung dung mà H1, keyword, FAQ, schema, ảnh cùng
   lệch một hướng thì người đọc và AI chỉ nhận cái lệch. Rà bài thì rà **khung** riêng: title, H1,
   description, keyword, câu hỏi FAQ, trường `about`/`name` trong schema, alt, caption, ảnh chia sẻ.
2. **Một chỗ đổi, mười chỗ theo.** Đổi một tựa kéo theo: og:title, headline, schema `name`, chữ neo ở
   bài khác, feed, llms, ô tìm kiếm, sitemap lastmod, lời đọc audio. Lập danh sách này thành bước cố
   định, đừng nhớ bằng đầu.
3. **Máy quét để khoanh vùng, người đọc để quyết.** Ba ngày rà: phần lớn cờ đỏ là báo động giả (D).
   Nhưng lỗi nặng nhất (B1) **không máy nào báo** — phải đọc bằng mắt với đúng câu hỏi.
4. **Kiểm nguồn từng con số, kể cả số trong phiếu của người khác.** Phiếu viết tự tin không có nghĩa
   là số đúng. Gỡ số không kiểm được, đăng phần đã kiểm, báo lại.
5. **Đừng tối ưu theo con số của công cụ.** "Title >60 ký tự", "đoạn >3 dòng", "chữ neo lệch tựa" —
   chỉ sửa khi chứng minh được nó cải thiện chuỗi *được tìm thấy → được hiểu → được trích → được
   dẫn sang bài tiếp*.
6. **Ảnh là lời khẳng định.** Alt và caption là dữ kiện. Chỉ tả thứ thấy trong khung.
7. **Lỗi tệ nhất không báo lỗi.** Form bấm không ăn, bộ lọc chặn nhầm bài, máy chủ QA chết, sitemap
   ghi ngày cũ — tất cả đều im lặng. Phải chủ động đo định kỳ.

---

## H. CÒN TREO

| Việc | Vì sao chưa làm |
|---|---|
| Ảnh chưa có bản cho điện thoại (`srcset`): 164/186 ảnh rộng >900px, ước tiết kiệm ~21 MB (55%) cho khách điện thoại | Đụng 265 thẻ ảnh — việc lớn, chờ chủ web duyệt |
| Thiếu landmark `<main>` (183/187 trang) và skip link | Không ảnh hưởng xếp hạng; đề xuất làm qua file JS dùng chung |
| 70 description dài hơn 165 ký tự (Google cắt khi hiện) | Không phải lỗi xếp hạng; làm theo đợt nếu chủ web muốn |
| Lead form giữa bài + ô nhận tin ở hub | Chờ chủ web quyết (F7) |
| Cụm bài "chữa lành" (bài trụ + bài cầu phễu) | Đã nghiên cứu, chờ duyệt |
| Rà H1 toàn site theo luật "câu người ta gõ" | Mới sửa 8 bài; chưa mở đợt toàn site |
| 39 ảnh chia sẻ của bài không có ảnh thân bài chưa ai mở ra xem | Chưa mở đợt; phải mở từng ảnh, không suy từ tên file |
| Vài ảnh còn vượt trần 2 bài (ảnh đèo, ảnh chùa, ảnh thác, ảnh toàn cảnh) | Một phần là bài tiếng Anh nằm ở gốc (không có tiền tố `/en/`) nên đếm bị thổi lên; cần lọc lại trước khi xử |
| Nhiệt độ 18–25°C dùng ở ~16 bài nhưng không có nguồn khí tượng | Bài mới không ghi số nhiệt độ; muốn chốt phải có văn bản |
| Dòng cập nhật đầu bài mưa lớn sau 25/9 | Đã hẹn |

---

## I. LỆNH TỰ KIỂM — COPY CHẠY ĐƯỢC

Chạy ở thư mục gốc web tĩnh. Đổi `TEN_VUNG`, `DOMAIN` cho đúng web của mình.
Mọi lệnh so chuỗi đều **giải mã HTML và đổi `\xa0` thành dấu cách trước** — bỏ bước này là đếm sai.

### I.1 — FAQ trong schema phải hiện trên trang
```python
import re, glob, json, html
def chu(s): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',re.sub(r'<(script|style)[\s\S]*?</\1>','',s))).replace('\xa0',' '))
for f in glob.glob('**/*.html', recursive=True):
    s = open(f, encoding='utf-8').read(); t = chu(s)
    for b in re.findall(r'<script type="application/ld\+json">([\s\S]*?)</script>', s):
        try: d = json.loads(b)
        except Exception: print('JSON HỎNG', f); continue
        def di(n):
            if isinstance(n, dict):
                if n.get('@type') == 'FAQPage':
                    for q in n.get('mainEntity', []):
                        qn = re.sub(r'\s+',' ',html.unescape(q.get('name','')).replace('\xa0',' '))
                        if qn[:40] not in t: print('KHÔNG HIỆN', f, qn[:60])
                for v in n.values(): di(v)
            elif isinstance(n, list):
                for v in n: di(v)
        di(d)
```

### I.2 — Khung ngoài có ghép tên vùng với từ rủi ro không
```python
import re, glob, html
VUNG = 'nam ban'; RUI_RO = ['sạt lở','ngập','lũ quét','nguy hiểm','thiên tai']
for f in glob.glob('*.html'):
    s = html.unescape(open(f, encoding='utf-8').read()).lower()
    truong = re.findall(r'<title>.*?</title>|<h1[\s\S]*?</h1>|name="description" content="[^"]*"|"(?:name|about|headline)":\s*"[^"]*"|alt="[^"]*"|<figcaption[\s\S]*?</figcaption>', s)
    kw = re.search(r'name="keywords" content="([^"]*)"', s)
    truong += kw.group(1).split(',') if kw else []          # keyword: từng cụm một, không nối
    for t in truong:                                         # dò TỪNG trường riêng, không ghép chuỗi
        for r in RUI_RO:
            if VUNG in t and r in t: print(f, '→', r, '|', t.strip()[:90])
# Kết quả là danh sách ĐỂ ĐỌC TAY. Câu hỏi có sẵn mà người ta thật sự gõ ("Mùa mưa X có ngập không?")
# và câu trả lời trả lời thẳng thì GIỮ — đó là nhà của truy vấn. Lỗi là khung KHẲNG ĐỊNH/GỢI rủi ro.
```

### I.3 — `speakable` trỏ vào phần tử có thật
```python
import re, glob, json
for f in glob.glob('**/*.html', recursive=True):
    s = open(f, encoding='utf-8').read()
    for sel in re.findall(r'"cssSelector":\s*\[([^\]]*)\]', s):
        for x in re.findall(r'"([^"]+)"', sel):
            if not re.fullmatch(r'[.#][\w-]+', x): continue   # selector phức (vd ".art-body > p") thì soi tay
            if x.startswith('.') and not re.search(r'class="[^"]*\b' + re.escape(x[1:]) + r'\b', s): print(f, 'thiếu', x)
            if x.startswith('#') and ('id="' + x[1:] + '"') not in s: print(f, 'thiếu', x)
```

### I.4 — `lastmod` trong sitemap không được cũ hơn ngày sửa trong bài
```python
import re, os
sm = open('sitemap.xml', encoding='utf-8').read(); DOMAIN = 'https://nambanpanorama.com'
for loc, lm in re.findall(r'<loc>([^<]*)</loc>\s*<lastmod>([^<]*)</lastmod>', sm):
    p = loc.replace(DOMAIN, '').strip('/') or 'index'
    f = next((c for c in (p + '.html', p + '/index.html') if os.path.exists(c)), None)
    if not f: print('URL KHÔNG CÓ FILE', loc); continue
    d = [x[:10] for x in re.findall(r'"date(?:Modified|Published)":\s*"([^"]+)"', open(f, encoding='utf-8').read())]
    if d and max(d) > lm[:10]: print(loc, 'sitemap', lm[:10], '< bài', max(d))   # chỉ sửa chiều này
```

### I.5 — Mỗi cụm trong title/H1 phải có trong thân bài
```python
import re, html
def than_bai(s):
    a = s.find('<div class="art-body">'); b = s.find('<div class="share-row">')   # đổi mốc theo web của mình
    return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',s[a:b])).replace('\xa0',' ')).lower()
s = open('bai.html', encoding='utf-8').read(); t = than_bai(s)
for cum in ['sai lầm', 'lịch sử', 'ĐT.725']:   # các cụm vừa thêm vào tựa
    print(cum, t.count(cum.lower()))          # 0 là tựa hứa suông
```

### I.6 — Description có tên vùng không
```bash
grep -L 'name="description" content="[^"]*Nam Ban' *.html
```

### I.7 — Bài mồ côi (chỉ đếm link trong thân bài, cả hai kiểu href)
```python
import re, glob, collections
vao = collections.Counter(); bai = {f[:-5] for f in glob.glob('*.html')}
for f in glob.glob('*.html'):
    s = open(f, encoding='utf-8').read(); a = s.find('<div class="art-body">'); b = s.find('<footer')
    than = s[a:b] if a > 0 else re.sub(r'<(nav|footer)[\s\S]*?</\1>|id="mobileMenu"[\s\S]*?</div>', '', s)  # trang hub không có art-body
    for h in set(re.findall(r'href="/?([a-z0-9\-]+)"', than)):
        if h in bai and h != f[:-5]: vao[h] += 1
print([x for x in sorted(bai) if vao[x] == 0])
```

### I.8 — Form và nút chết
```bash
grep -n '<form[^>]*onsubmit="return false' *.html
```
Rồi với mọi `<form>`/`<button>` còn lại: Playwright bấm thật, đo có request ra hoặc DOM đổi không.

### I.9 — Ô nhập dưới 16px và vùng chạm dưới 44px (đo computed style, không đọc CSS)
```js
// Playwright, viewport 390×667, isMobile:true
const r = await page.evaluate(() => ({
  oNhoChu: [...document.querySelectorAll('input:not([type=hidden]),textarea,select')].filter(i => parseFloat(getComputedStyle(i).fontSize) < 16).length,
  nutNho: [...document.querySelectorAll('button,a.hamburger,.hamburger')].filter(b => { const x = b.getBoundingClientRect(); return x.width && (x.width < 40 || x.height < 40); }).length,
  tranNgang: document.documentElement.scrollWidth > innerWidth,
  soDuong: document.title.length   // = 0 là máy chủ chết, KHÔNG phải trang sạch
}));
```

### I.10 — Ảnh dùng quá 2 bài (không tính bản dịch)
```python
import re, glob, collections
dung = collections.defaultdict(set)
for f in glob.glob('**/*.html', recursive=True):
    if f.split('/')[0] in ('en','fr','zh','ko','ja'): continue
    for a in re.findall(r'<img[^>]*src="/?(images/[^"]+)"', open(f, encoding='utf-8').read()): dung[a].add(f)
for a, s in sorted(dung.items(), key=lambda x: -len(x[1])):
    if len(s) > 2: print(len(s), a, sorted(s))
```

### I.11 — H1 rớt lẻ chữ
```js
// Playwright ở 390 và 1440
const r = await page.evaluate(() => { const h = document.querySelector('h1'); const rg = document.createRange(); rg.selectNodeContents(h);
  const rs = [...rg.getClientRects()].filter(x => x.width > 2); const top = Math.max(...rs.map(x => Math.round(x.top)));
  const cuoi = rs.filter(x => Math.round(x.top) === top); return { cuoi: Math.max(...cuoi.map(x => x.right)) - Math.min(...cuoi.map(x => x.left)), rong: h.getBoundingClientRect().width }; });
// cuoi < 0.28 * rong → rớt chữ, thêm &nbsp; giữa 2–3 chữ cuối
```

---

## J. DANH SÁCH KIỂM — TRẢ LỜI CÓ/KHÔNG

**Sự thật và niềm tin**
- [ ] Mọi con số trong bài có URL nguồn cạnh nó chưa? Số nào không có thì đã gỡ chưa?
- [ ] Ngày đăng trong schema có đúng ngày đăng thật không?
- [ ] Bài về rủi ro, thiên tai: khung ngoài có ghép tên vùng mình với tên thiên tai không?
- [ ] Alt và caption ảnh có tả thứ **không có** trong khung không?
- [ ] Tựa có hứa cụm nào mà thân bài không có không?

**SEO / AEO / GEO**
- [ ] H1 có phải câu người ta thật sự gõ không?
- [ ] Title, H1, og:title, headline có cùng một chuỗi không?
- [ ] Description có tên vùng/thực thể chính không?
- [ ] Cụm từ khoá mới đã có trang nào khác làm nhà chưa?
- [ ] FAQ trong schema có hiện trên trang không? Đổi câu hỏi thì câu trả lời còn khớp không?
- [ ] `speakable` có trỏ vào phần tử có thật không?
- [ ] `lastmod` trong sitemap có cũ hơn ngày sửa trong bài không?
- [ ] Có bài nào 0 link vào từ thân bài không? Có cụm bài nào chỉ trỏ vào nhau không?
- [ ] Đổi tựa xong: đã quét tựa cũ trong mọi đuôi file (html, xml, txt, json) chưa?

**Trải nghiệm**
- [ ] Mọi form và nút: bấm thật có ăn không?
- [ ] Ô nhập ≥16px? Nút ≥44px? Không tràn ngang ở 390/1440/1920?
- [ ] H1 có rớt lẻ chữ ở cả hai khổ không?

**Kỷ luật**
- [ ] Máy quét báo đỏ: đã soi tay từng ca trước khi sửa chưa?
- [ ] Script QA có đo một số dương bắt buộc để không nhầm trang trắng là trang sạch không?
- [ ] Script sửa hàng loạt đã chạy `--dry` và đọc danh sách trước chưa?
- [ ] Nội dung đổi lời đọc: audio đã sinh lại **sau** khi nội dung lên nhánh chính chưa?
