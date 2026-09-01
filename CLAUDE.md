# CLAUDE.md — Namban Panorama

Hướng dẫn vận hành cho Claude (tự nạp mỗi phiên). Đọc hết trước khi làm.

---

## 0. NGUYÊN TẮC VẬN HÀNH (Chú D chốt — ưu tiên cao nhất)

1. **AUTO TẤT CẢ.** Từ nay tự làm, tự quyết, tự tìm cách tối ưu nhất để tự động hóa.
   KHÔNG chờ duyệt từng bước. (Điều này **thay thế** quy trình cũ "em đề xuất → Chú
   duyệt → em làm".) Chỉ dừng hỏi khi việc thật sự mơ hồ và câu trả lời làm đổi hẳn kết quả.
2. **Việc 100% bắt buộc Chú phải tự tay làm** (cấp quyền, đăng nhập, tài khoản bên thứ ba,
   thanh toán…) → **dán link trực tiếp + hướng dẫn cực chi tiết như cho người mới** (từng
   nút bấm, từng bước). Không nói chung chung.
3. **BÁO LINK — KHÔNG ĐƯỢC QUÊN (Chú nhắc SUỐT CẢ THÁNG, đây là lỗi hay tái phạm nhất).**
   Xong BẤT KỲ việc gì → cuối lượt phải liệt kê **ĐẦY ĐỦ link live** của mọi trang vừa tạo/sửa.
   **BẮT BUỘC dạng BẤM ĐƯỢC — markdown `[tên](https://nambanpanorama.com/slug)` — có đủ
   `https://`.** CẤM đưa link trơn kiểu `nambanpanorama.com/slug` (Chú phải copy dán = SAI,
   đã bị mắng nhiều lần). Làm nhiều đợt nhỏ thì cuối cùng vẫn phải gom LẠI TẤT CẢ thành 1
   danh sách bấm-được, không để Chú tự dò. **Trước khi kết thúc mỗi lượt: kiểm lại có danh
   sách link `[...](https://...)` chưa — chưa có thì CHƯA được kết thúc.**
3. **Xong bất kỳ việc gì → báo kết quả + link kiểm tra** (link live/preview, ảnh QA,
   commit). Số thật, không hứa suông.
4. **Luôn QA + tối ưu cả 2 giao diện: PC (1440/1920px) VÀ mobile (390px)** — bằng thiết kế
   + công nghệ mới nhất. Không bao giờ chỉ xem một khổ.
5. **Luôn tối ưu AEO / SEO / GEO / UX / UI** để đưa web lên **top Google Search và các bề
   mặt AI** (ChatGPT, Gemini, Perplexity, Google AI Overviews…) **nhanh nhất, sớm nhất**.
   Mỗi thay đổi nội dung/kỹ thuật đều cân nhắc góc này.
6. **MỤC ĐÍCH CUỐI CÙNG LÀ TẠO PHỄU — sau đó mới tới viết hay (Chú D chốt).** Mỗi bài, mỗi
   trang, mỗi thay đổi phải trả lời trước: *"Cái này kéo được tệp khách nào vào phễu?"*
   Trình tự ưu tiên: **(1) bám đúng từ khóa người ta thật sự search** (nghiên cứu AEO/SEO/GEO
   theo intent từng tệp, kể cả khách nước ngoài — EN/FR/ZH/KO/JA) → **(2) được tìm thấy & được
   AI trích** → **(3) giữ chân bằng nội dung hay + trust**. Viết hay mà không ai search tới thì
   vô nghĩa. Nhưng phễu KHÔNG được phá luật publication (mục 2): kéo khách bằng đúng từ khóa +
   trust, KHÔNG bằng CTA bán. Mỗi bài mới/sửa: gắn từ khóa chính vào title/description/H1/H2/
   alt/JSON-LD + đảm bảo có lối dẫn vào phễu (bài liên quan → hub → Trao đổi).

Giọng: xưng **"em"**, gọi **"Chú"**, tiếng Việt, gọn, thẳng, đi thẳng việc. Không xưng "tôi".

**Nội dung dán nhầm → BỎ QUA, đừng hỏi (Chú chốt 31/8/2026).** Tin nhắn đôi khi kèm nội dung
của việc khác (dự án khác, app khác, hội thoại khác) — Chú dán nhầm. Gặp thì **lặng lẽ bỏ, làm
tiếp phần thuộc repo này**, KHÔNG liệt kê phương án, KHÔNG hỏi lại, KHÔNG ghi vào sổ treo. Chỉ
nói một câu ngắn nếu thật sự không phân biệt được đâu là việc chính.
Dám phản biện khi có cái SAI THẬT (vai tỉnh táo viên), nhưng không tự ý đề xuất dừng dự án.

### ⚠️ CHÚ NHẮC ĐI NHẮC LẠI CẢ THÁNG — GOM 1 CHỖ, ĐỪNG ĐỂ NHẮC NỮA

Rà 135 tin của Chú, đây là những lỗi Claude tái phạm nhiều nhất. Kiểm 5 mục này TRƯỚC khi
kết thúc mỗi lượt:

1. **LINK (nhắc 22 lần — lỗi số 1).** Cuối MỌI lượt phải có danh sách link **BẤM ĐƯỢC**:
   markdown `[tên](https://nambanpanorama.com/slug)`, đủ `https://`. CẤM link trơn. Xong
   nhiều bài → gom hết thành 1 danh sách để Chú **lập chỉ mục** (dán vào GSC/IndexNow). Việc
   nào Chú phải tự tay (up ảnh/audio…) → **đưa sẵn link Drive + hướng dẫn từng nút**, đừng
   bắt Chú tự mò.
2. **AUTO với VIỆC RÕ — đừng bắt duyệt từng bước (nhắc 10 lần).** Việc cụ thể, cơ học, sửa
   theo lệnh rõ (thi công, đổi ảnh, sửa số đã chốt, dọn code…) → **LÀM LUÔN** rồi báo kết
   quả + link, đừng dừng xin OK từng bước. Bài mới → **mặc định tạo audio giọng NAM** (không
   để giọng máy tiếng Anh). Video trang chủ auto chạy 2-3 lần/phiên (đã chốt).
3. **VIỆC LỚN / MỚI / ĐỔI HƯỚNG → RESEARCH → ĐỀ XUẤT → CHÚ DUYỆT MỚI LÀM.** Cái gì đổi
   thiết kế, thêm thành phần mới, đổi cấu trúc, quyết định chiến lược, hay ảnh hưởng nhiều
   trang → **KHÔNG tự ý làm**: nghiên cứu kỹ, trình phương án rõ, chờ Chú gật rồi mới thực
   thi. (Phân biệt với mục 2: việc rõ thì auto; việc lớn/mơ hồ thì hỏi. Sai bên nào cũng bị
   mắng — auto chuyện lớn, hoặc hỏi chuyện vặt.)
4. **CHỮ ĐƠN GIẢN — MỘT SỐ TRƯỜNG HỢP, không phải mọi chỗ (nhắc 5 lần).** Caption mốc chỉ
   đường / ảnh nhận diện nhanh → ngắn gọn: "Ngã tư Đạo Nga." Nhưng caption bài phân tích,
   câu dẫn, thân bài → vẫn viết ĐỦ Ý, đúng giọng publication; đừng cụt lủn cho có. Tùy ngữ cảnh.
5. **SỐ ĐÃ CHỐT → ÁP THẲNG, ĐỪNG BÁO CÁO LẠI (nhắc 5 lần).** 25km/28km/20km (mục 2.7) và các
   con số đã quyết: cứ sửa đúng, KHÔNG bàn lại, KHÔNG xin xác nhận từng lần.

---

## 1. WEBSITE LÀ GÌ

`nambanpanorama.com` — **publication (báo/tạp chí)** về bất động sản vùng Nam Ban, Lâm Hà,
Lâm Đồng. **KHÔNG phải web bán hàng.**

- Repo: `doanquocduyet/namban-panorama` · Deploy: **Vercel auto khi push `main`**.
- Cấu trúc: `index.html` + ~30 bài `.html` + `nav.css` + `panorama-article.css` +
  `sitemap.xml` + `robots.txt` + `llms.txt` / `llms-full.txt` + `feed.xml` + `/images/`.
- 1 trong 3 web cùng chủ: **Panorama** (tạo trust, không bán) · Villas `nambanvillas.vn`
  (bán đất) · Greenspacers `greenspacers.vn` (giữ đất). **Repo này CHỈ lo Panorama.**

---

## 2. LUẬT NỘI DUNG (không được phạm)

1. Publication, KHÔNG landing bán. **Cấm CTA bán**: "liên hệ ngay", "mua ngay", "đăng ký
   nhận giá", "trả lời trong ngày", "không cần đăng ký". Giọng "chúng tôi".
2. Không lôi tên/mặt/SĐT chủ ra giữa trang chủ hay chèn CTA bán giữa bài. Liên hệ nằm ở:
   (a) footer (chữ trầm) + trang `trao-doi`; (b) **một khối liên hệ trầm cuối bài** — CHỈ ở
   bài phân tích về đất/mua bán/thị trường/BĐS/index (không phải mọi bài). Khối đặt SAU
   nội dung/miễn trừ, chữ Fraunces màu forest, vạch mảnh, dạng "Có câu hỏi về một khu cụ
   thể? — 0978 758 788 · Zalo"; KHÔNG nút, KHÔNG "ngay", KHÔNG màu nóng. Khối này do
   `panorama-utils.js` tự chèn theo danh sách slug IN (sửa danh sách trong file đó, đừng
   dán tay từng bài). **Footer:** bài CÓ khối → footer bỏ SĐT (giữ mail + Trao đổi); mọi
   footer còn lại → **SĐT đứng trước** `nambanpanorama@gmail.com`.
3. **"Im lặng mà sang"** — thẩm mỹ Aesop/Monocle/Stratechery: khoảng trắng rộng, tiết chế,
   không lòe loẹt, không màu nóng, không nhấp nháy.
4. **Palette CHỈ các biến này** (không thêm màu thứ hai ngoài clay):
   `--ink:#1a1815 · --paper:#f1ece2 · --card:#faf6ee · --forest:#2f4034 ·
   --forest-deep:#1e2a20 · --clay:#9d5d38 · --clay-soft:#bb8862 · --stone:#a79c87 ·
   --muted:#6e6759 · --line:#e1d9c8`
5. **Fonts CHỈ**: Fraunces (serif) + Be Vietnam Pro (sans). Không thêm font.
6. **Số liệu chính xác tuyệt đối** — sai một số là sập uy tín. Không chắc thì KHÔNG ghi,
   không đoán. Cần thì web-search kiểm.
7. **Số đang dùng (Chú chốt lại 13/8/2026 — GỘP VỀ 25km)**: trung tâm Nam Ban → Đà Lạt
   **~25km** (qua đèo Tà Nung, ~45 phút); Thác Voi / chùa Linh Ẩn → Đà Lạt **~25km** (cùng
   khu Nam Ban); Nam Ban → sân bay Liên Khương **~20km, đi 35 – 45 phút** (lối ngã ba Cửa
   Rừng rồi vào ĐT.725 — KHÔNG dùng "30 – 40 phút", đã sửa 26/8/2026). KHÔNG dùng số cũ
   23km/27km/22km, và **KHÔNG dùng 28km cho Thác Voi nữa** (đã đổi 28→25 toàn site 13/8/2026)
   trừ khi Chú yêu cầu đổi lại. Cả Nam Ban lẫn Thác Voi giờ đều 25km — đừng tách 25/28 như bản cũ.
   **Tên địa danh (đã research 7/2026)**: giữ **"Chùa Linh Ẩn" (Linh Ẩn Tự)** vì đây là tên
   MẠNH SEO — trang chính quyền lamdong.gov.vn + mọi trang du lịch lớn + 100% kết quả search
   đều dùng "Chùa Linh Ẩn"; "Thiền Viện Linh Ẩn" gần như 0 search, không phải tên chính thức.
   Nguyên tắc chung: tên nào MẠNH SEO thì giữ; chỉ đổi tên khi tên mới vừa đúng vừa được
   search nhiều hơn. Thác cạnh bên = **thác Voi** (25km — vị trí cụ thể). Bài ngoại ngữ giữ
   "Linh An Pagoda / 灵隐寺 / 린안 사원 / リンアン寺" (từ khóa khách nước ngoài search).
8. **Dám nói "đừng mua"**. Xây trust bằng đọc rủi ro, không bán giấc mơ. Kết bài nhẹ, an
   yên — không hô "mua ngay".
9. Nút **"Chia sẻ"** trầm cuối bài = GIỮ (chuẩn tờ báo). Khác với CTA bán.
10. **HƯỚNG LÊN / XUỐNG — theo cao độ, KHÔNG lẫn (Chú chốt).** Đà Lạt là điểm **CAO NHẤT**,
    **KHÔNG bao giờ "xuống Đà Lạt"** — mọi nơi đều **LÊN Đà Lạt**. Từ đồng bằng (Sài Gòn,
    Bình Dương, miền Tây…) đi tới vùng cao → **LÊN Nam Ban / LÊN Đà Lạt** (kể cả "lên thẳng
    Nam Ban", "xe khách lên Nam Ban"). Chỉ khi xuất phát **TỪ Đà Lạt** (cao hơn Nam Ban) mới
    được **XUỐNG Nam Ban** (đổ đèo Tà Nung). Mỗi bài: rà lại mọi câu "lên/xuống Nam Ban/Đà Lạt"
    cho đúng chiều cao độ trước khi đăng.

---

## 3. LUẬT KỸ THUẬT (bắt buộc mỗi lần sửa)

- Sửa bằng **`str_replace`/Edit exact từng đoạn**. TUYỆT ĐỐI KHÔNG regex DOTALL xóa cả
  block (đã từng gây vỡ layout). Đọc chuỗi thật → thay chuỗi thật.
- **Verify trước khi push**: (1) CSS braces cân `{`=`}` trong `<style>`; (2)
  `<div>/<section>/<nav>/<footer>/<script>` mở=đóng; (3) mọi JSON-LD `JSON.parse()` được.
- **QA THẬT bằng Playwright trên CẢ HAI khổ 1440px + 390px** (và kiểm 1920px không tràn):
  tràn ngang (`scrollWidth > innerWidth`), tỷ lệ/kích thước ảnh, số dòng chữ, contrast.
- Không tràn ngang ở 1440/1920/390. Trang dùng `html{overflow-x:clip}` + ẩn `.mobile-menu`
  trên PC (`@media(min-width:901px)`) — **giữ nguyên cơ chế, đừng chồng `overflow-x:hidden`**.
- Hamburger nằm **NGOÀI** `.navlinks`. Menu mobile là panel `#mobileMenu` + `#menuOverlay`,
  mở bằng `toggleMenu()`.
- **WCAG ≥ 4.5.** Số/giá KHÔNG để màu clay/gold trên nền trắng (fail contrast). Chữ trắng
  trên ảnh phải có overlay đủ tối.
- **VỠ DÒNG CHỮ PHẢI ĐẸP — KHÔNG "RỚT CHỮ" (Chú nhắc SUỐT — bổ sung 29/7, phần UX/UI hay bị bỏ sót).**
  Mọi câu — nhất là **câu dẫn (standfirst), câu ký/khẩu hiệu, tiêu đề, caption, tên/dòng mô tả** —
  phải ngắt dòng ĐẸP: **không để 1–2 chữ rơi lẻ xuống dòng cuối** (widow/orphan), **không cắt giữa
  cụm từ** (vd "Những gì" treo cuối dòng). 3 tầng xử lý: (1) câu ký/khẩu hiệu **2 vế → chủ động
  `<br>` đúng chỗ ngắt ý** (vd `Panorama không có huy chương.<br>Chỉ có dấu chân trên từng nơi đã đi.`);
  (2) thêm **`text-wrap:balance`** cho tiêu đề/câu ngắn, **`text-wrap:pretty`** cho thân bài; (3)
  **`&nbsp;`** giữa 2 chữ cuối để chữ chót không rớt lẻ. **BẮT BUỘC ngó lại chữ đã wrap trên CẢ
  1440 lẫn 390 (Playwright screenshot) trước khi đăng** — chữ vỡ dòng đẹp là một phần của "im lặng
  mà sang", đừng để câu hay bị hình thức làm hỏng.
  **KHÔNG có luật "đoạn tối đa N dòng ở 360px" (gỡ 31/8/2026).** Từng có phiếu đặt trần
  "tối đa 3 dòng" — đo thật thì KHÔNG bài nào trên site đạt, kể cả bài trụ (`/truoc-khi-xuong-tien`
  đoạn dài nhất **19 dòng**; bài mới nhất 8 dòng, tức đã gọn hơn nhiều). Giữ trần đó = phải bẻ
  văn Chú thành câu cụt, trái mục 4 §0. Thước đo đúng chỉ là: **chữ vỡ dòng đẹp, không rớt lẻ
  1–2 chữ ở CẢ 1440 lẫn 360**. Đừng tự đặt lại trần số dòng, cũng đừng nhận phiếu có trần đó.
- **Animation phải có fallback**: khối `.reveal` ẩn tự hiện sau 2.5s nếu observer lỗi; hiện
  luôn nếu không JS (chỉ ẩn khi `<html class="js">`). Không để nội dung biến mất.
- **Ảnh chỉ dùng file trong `/images/`.** KHÔNG URL ảnh ngoài. Ảnh mới optimize <300KB
  (~quality 85), đặt vào `/images/`. File nặng/rác/0-tham-chiếu → xóa.
- **CHỌN LỌC ẢNH — KHÔNG NHỒI (Chú chốt 30/7, "ko phải web tạp nham").** Chú đưa cả kho ảnh
  là để **CHỌN**, không phải nhét hết. Kho hình là **dữ liệu dùng dần cho nhiều bài sau** — cứ để dành.
  Mỗi bài chỉ gắn **1–2 ảnh thật sự TÔN bài** (đúng nội dung đoạn đó), đặt cách nhau bằng chữ; **cấm
  2 ảnh cùng loại dính sát nhau** (vd 2 quán café kề nhau → nát bài). Ảnh Chú up **không xóa tấm nào**
  (mỗi tấm có ý — kể cả đồ ăn/đồ uống = sinh hoạt thường nhật, để dành bài đời sống), chỉ **nén lại**
  cho web. Thà ít mà tinh (quiet luxury) còn hơn nhiều mà rối. Không chắc ảnh có tôn bài không → để dành.
- **BẢN ĐỒ ẢNH — đọc trước, đừng rà tay (tiết kiệm token/time).** Ảnh nào dùng ở đâu, đóng
  vai gì (`display`/`og`/`twitter`/`schema`), tấm nào chưa dùng → xem `data/images-manifest.json`.
  Sinh bằng `python3 tools/gen-image-manifest.py`. **Sau mỗi lần thêm/xóa/đổi tên ảnh → chạy
  lại script rồi commit manifest.** Quy ước site: `.webp` cho ảnh hiển thị (nhẹ, nhanh),
  `.jpg` cho ảnh `og:image` chia sẻ (Facebook/Zalo — 56 trang theo chuẩn này). Không nuôi
  cả 2 định dạng cùng 1 ảnh trừ khi mỗi bản đóng đúng 1 vai (vd `deo-ta-nung`: webp=hiển thị,
  jpg=OG). 2 tấm để dành có chủ đích trong kho: `gia-lam-biet-thu-o-to.webp` (biệt thự người
  khác — lệch làn), `me-linh-vuon-doi-cao.webp` (đồi chè — sai chủ đề cà phê), `duong-deo-mua-suong-mo.webp` (đường đèo mưa sương mờ — Chú để dành up bài khác).
- **CHUẨN og:image (Chú chốt 26/7/2026 — làm VẬY cho MỌI bài từ nay):** ảnh chia sẻ Zalo/FB
  = **`/images/<slug>.jpg`, cắt chuẩn 1200×630** (tỷ lệ 1.91:1) từ ảnh đẹp của bài,
  **KHÔNG ghi chữ lên hình** (thiết kế chữ-trên-ảnh không đẹp), có **mờ đen NHẸ mép dưới**
  (gradient bắt đầu ~60% chiều cao, tối đa ~28%). Chèn 4 thẻ: `og:image` + `og:image:width=1200`
  + `og:image:height=630` + `twitter:image`. **Bài KHÔNG có ảnh** → lấy ảnh HỢP CHỦ ĐỀ nhất từ
  kho làm og (bài bơ→ảnh bơ; bài đất→ảnh lô đất/toàn cảnh); không có ảnh hợp thì dùng **ảnh
  brand mặc định** (`nam-ban-aerial.jpg` / `nam-ban-toan-canh.jpg`) — TRÁNH ảnh lệch làn
  (villa/HT86). Không để bài nào thẻ share trống.
- Xong: `git add -A && git commit && git push origin main` → chờ Vercel → **báo link**.

### QUYẾT ĐỊNH ĐÃ CHỐT — ĐỪNG BÀN LẠI (26/7/2026)

**0. CÂU CHỦ LỰC (chữ ký) = "Hiểu vùng đất trước khi hiểu giá đất"** (Chú chốt 28/7).
Dùng nhất quán làm tagline định vị (đã sẵn ở slogan trang chủ). Câu phụ *"Panorama không
có huy chương — chỉ có dấu chân trên từng lô đất"* Chú rất thích nhưng **chỉ đặt trong ô
giới thiệu/contact (vd trang Founder), KHÔNG dùng làm slogan.** **Hai biến thể câu ký đều
được — dùng linh hoạt (Chú chốt 29/7):** *"…trên từng lô đất"* (bám business đất) và *"…trên
từng nơi đã đi"* (trầm, rộng hơn — đang dùng ở khối founder trang Trao đổi). Chọn theo ngữ cảnh.

**1. CSS trùng lặp giữa 63 trang → ĐỂ YÊN, KHÔNG GOM.**
Mỗi trang tự chứa ~6,4KB CSS trong `<style>`, trong đó ~5,1KB trùng với trang khác.
Đã đo thật: máy chủ nén trước khi gửi nên mỗi trang chỉ còn **3,3KB**; gom lại chỉ đỡ
**1,4KB/trang ≈ 1 mili-giây trên 4G**. Không đáng đổi lấy rủi ro sửa 63 file.
→ Chỉ gom KHI NÀO làm lại thiết kế toàn site (lúc đó đằng nào cũng mở hết 63 file).
Hại duy nhất hiện tại là **công bảo trì**: đổi màu/font phải sửa 63 chỗ, dễ sót.

**2. `nav.css` → GIỮ, KHÔNG GỠ.** (đã suýt gỡ nhầm, kiểm mới biết)
Site có **HAI hệ thanh nav song song**:
- **Hệ A** — `<nav>` + `.navin` + `.navlinks` · **52 trang** · **CẦN `nav.css`**
  (nav.css cấp `.navin{max-width:1180px;padding:16px 40px}`, `.logo` màu, `.logo-intel`,
  `-webkit-backdrop-filter` cho Safari — CSS inline của trang KHÔNG có mấy thứ này)
- **Hệ B** — `<nav class="nav">` + `.nav-inner` + `.nav-links` · **14 trang** · **KHÔNG cần**
  (có CSS riêng đầy đủ trong `<style>`)
Gỡ `nav.css` = vỡ thanh nav 48 trang hệ A. Đây là nợ kỹ thuật (2 template), không phải lỗi.
Thêm bài mới: theo hệ A thì **nhớ nạp `nav.css`**.

### Ghi chú ảnh trang chủ (Chú đã chốt — giữ nguyên)
- 5 khối dưới hero có class `.reveal` (scroll-reveal fade-up, có fallback).
- Nút chat nổi `.fab-contact` (glass 44px, viền forest, góc phải dưới).
- **3 ảnh nhịp kích cỡ khác nhau (Kinfolk)**: desktop **360/440/600px**, mobile
  **230/280/370px** — KHÔNG đổi chiều cao này.
- Ảnh đèo Tà Nung (`deo-ta-nung.jpg` 1600×900) **có chữ in sẵn góc dưới-trái**
  ("ĐƯỜNG VỀ NAM BAN — Qua đèo Tà Nung") → dùng `object-position:left bottom` để không cắt
  chữ khi `cover` crop ở cả 2 khổ.

### Nghe bài (audio) — `panorama-utils.js` tự chèn nút `#pm-audio` đầu mỗi bài
- Nút trầm (nút tròn forest + "Nghe bài" + ~phút + tốc độ 1×/1.25×/1.5×), chèn đầu
  `.art-body`/`article`; giọng + nhãn theo `<html lang>` (vi/en/fr/zh/ko/ja).
- **GIỌNG ĐÃ CHỐT (26/7/2026): dùng GIỌNG CÓ SẴN — `vi-VN-NamMinhNeural`** (Microsoft Neural,
  giọng nam Việt, MIỄN PHÍ) qua workflow `.github/workflows/generate-audio-free.yml` (edge-tts).
  **KHÔNG dùng giọng ElevenLabs cá nhân của Chú nữa.** Bài nào có `<meta name="pm-audio"
  content="/audio/<slug>.mp3">` thì player phát MP3 + bật MediaSession (điều khiển màn hình
  khoá → nghe khi lái xe). Bài chưa có MP3 → fallback giọng máy trình duyệt (Web Speech API).
- Tạo audio cho bài mới/còn thiếu = **chạy workflow `generate-audio-free.yml`** (nó tự sinh MP3
  NamMinh + tự chèn `<meta name="pm-audio">`). Không cần Chú thu âm tay.

---

## 4. DEPLOY & MÔI TRƯỜNG

- Push `main` → Vercel tự build production `nambanpanorama.com`.
- **VERCEL ĐÔI KHI NHỠ WEBHOOK — không tự deploy commit (gặp thật 26/7/2026).** Dấu hiệu: sửa/thêm
  ảnh rồi mà web không đổi, ảnh mới báo 404 dù đã commit+push đúng (ảnh cũ vẫn sống). Cách chữa:
  **đẩy 1 commit rỗng ép build** — `git commit --allow-empty -m "ép deploy" && git push origin main`.
  Vercel nhận commit mới → build lại → mọi thay đổi tồn đọng lên hết. Đây KHÔNG phải lỗi repo,
  đừng đi sửa code. (Hôm đó Chú test nhiều lần thấy "chưa sửa" thực ra là đang xem bản cũ do nhỡ deploy.)
- **Nếu push bị `403` / "Resource not accessible by integration"**: GitHub App của Claude
  **chưa có quyền Contents: Write** trên repo (không liên quan public/private). Đây là việc
  Chú phải tự cấp — dán link + hướng dẫn từng bước, rồi chờ Chú xác nhận mới push lại.

### Chạy Playwright QA (môi trường web session)
- Playwright cài global tại `/opt/node22/lib/node_modules`; Chromium tại
  `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`.
- Script `.cjs`: `require('/opt/node22/lib/node_modules/playwright')`,
  `chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' })`.
  KHÔNG chạy `playwright install`.

---

## 5. AEO / SEO / GEO — hướng tối ưu thường trực

**ĐÓNG SỔ NEO VÙNG — không mở lại (Chú chốt 2/9/2026).** Đã neo xong nhóm nặng nhất:
ba bài khuôn Mê Linh/Gia Lâm/Đông Thanh, hồ Đông Thanh, hồ Bãi Công, cầu Tổng Đội,
chùa Linh Ẩn, tách thửa. **KHÔNG đi rà 53 bài còn lại, không mở `/hoi-nhanh` 21 câu.**
Lý do: mỗi bài còn lại chỉ 1–4 câu, sửa hết cũng không đổi được gì đo đếm được — đúng
cái Luật 4 cấm, quy trình lớn hơn mục tiêu. Thay vào đó: **bài MỚI viết đúng neo ngay
từ đầu** (một dòng kiểm trong phiếu content), không đi vá bài cũ. Cùng nguyên tắc này
áp cho mọi sổ rà tương tự — 52 ca contrast màu cứng, 34 màu ngoài palette, entity graph,
card title dài: đã cân nhắc và **cố ý bỏ**, không phải quên.

**Neo bằng tên vùng ĐÚNG PHẠM VI, không mặc định "Nam Ban".** Ba bẫy đã vấp thật:
Nam Hà là **xã riêng** (Nam Hà + Phi Tô), cạnh Nam Ban chứ không thuộc — neo vào là tạo
lỗi địa lý. Tà Nung thuộc **phường Cam Ly, Đà Lạt** — câu so sánh Tà Nung ↔ Mê Linh mà
neo "ở Nam Ban" là gán nhầm. Câu về **quy định tách thửa** áp cho cả tỉnh nên phải neo
"ở Lâm Đồng" — neo "ở Nam Ban" vừa sai vừa đẩy người Bảo Lộc, Di Linh ra khỏi kết quả.

**KHÔNG neo khi câu đang chủ động sửa hiểu nhầm.** Ví dụ thật: *"Chùa Linh Ẩn ở đâu?"* —
đáp giải thích "nhiều người gọi là chùa Linh Ẩn Đà Lạt, nhưng chùa không nằm trong thành
phố Đà Lạt". Nhét "Nam Ban" vào câu hỏi là giết đúng công dụng của nó, vì người cần đọc
chính là người gõ câu chưa có "Nam Ban".

**Nguyên tắc lọc (thước đo trước khi thêm bất cứ thứ gì):** KHÔNG thêm thành phần nào
nếu nó không phục vụ **đồng thời ít nhất 2 trong 3**: *người đọc · Google · AI*. Cái chỉ
để "chiều Google" mà không giúp người đọc, cũng không tạo tài sản dữ liệu lâu dài → bỏ.
Lợi thế của Panorama là **kho dữ liệu gốc đáng tin** (ảnh tự chụp, số từ văn bản, tọa độ,
là nguồn đầu tiên), không phải mẹo SEO. Mọi tối ưu phải phục vụ mục tiêu đó.
Quy trình xuất bản đầy đủ + checklist: xem `docs/quy-trinh-xuat-ban.md`.

Đã có nền: `llms.txt`, `llms-full.txt`, `sitemap.xml`, `image-sitemap.xml`, `robots.txt`,
`feed.xml`, IndexNow, và tầng dữ liệu mở `/data/*.json` (prices/infrastructure/places/
timeline) + JSON-LD (Organization/Person/Place+GeoCoordinates/WebSite/WebPage/Dataset/
TouristAttraction/Airport/ImageObject/Speakable). Mỗi lần đụng nội dung, luôn cân nhắc:
- **AEO/GEO** (để AI trích dẫn): câu trả lời trực tiếp, dữ kiện rõ, JSON-LD đúng &
  `JSON.parse()` được, cập nhật `llms.txt`/`llms-full.txt` khi thêm bài, `dateModified` mới.
- **SEO**: title/description/canonical/OG/Twitter đủ; heading mạch lạc; internal link giữa
  các bài; ảnh có `alt` mô tả thật; `sitemap.xml` + `feed.xml` cập nhật khi thêm/xóa bài.
- **UX/UI**: tốc độ (ảnh optimize, `loading=lazy`), không CLS, không tràn ngang, chạm tốt
  trên mobile, contrast đạt. Ưu tiên trải nghiệm đọc "im lặng mà sang".

**Entity graph (stable @id):** mỗi thực thể chính có `@id` cố định KHÔNG BAO GIỜ đổi —
`#namban`, `#thac-voi`, `#cau-tong-doi`, `#san-bay-lien-khuong`, `#founder`, `#organization`,
`#website`. Bài về địa danh nối vào graph bằng `containedInPlace`/`about` trỏ `@id` (vd thác
Voi `containedInPlace` → `#namban`). `data/places.json` giữ `schema_id` map tới đúng @id đó.
Đây là "Knowledge Graph" làm đúng cách của site tĩnh — KHÔNG cần API/backend.

**Tách FACT với ANALYSIS (giữ trust, AI thích):** dữ kiện đã kiểm chứng (có văn bản/ảnh/
tọa độ) ghi thẳng; còn suy đoán/dự phóng của Panorama (giá sẽ tăng, tác động…) phải gắn
nhãn rõ "đây là phân tích của Panorama, không phải dữ kiện đã xác nhận". Trong `/data`,
mốc/dữ kiện ghi `status`/nguồn thật ("đã ký" · "đang thi công" · "dự thảo" · "dự kiến") —
KHÔNG bịa điểm tin cậy dạng số (vd "98/100") vì đó là số tự chấm, sai luật mục 6.

---

## 6. LUẬT GREP & QA — 17 điều (khóa 8/2026, rút từ lỗi thật)

Đây là 17 lần **audit tự động báo SAI** trong đợt rà 8/2026. Mỗi luật = một lỗi đã thật sự
xảy ra. Đọc trước khi tin bất kỳ con số nào do script sinh ra.

1. **Không tin audit khi nó bảo XÓA.** Mở file, đọc markup thật, rồi mới xóa.
2. **Không tin audit khi nó báo "SẠCH".** Kiểm chéo tay ít nhất 1 ca trước khi kết luận.
3. **Quét cả chữ số VÀ chữ viết** — `tháng 4` và `tháng Tư` là hai chuỗi khác nhau.
4. **Case-insensitive.** `Bốn phân khu` ≠ `bốn phân khu` (đã sót thật ở `llms-full.txt`).
5. **Kiểm ngữ cảnh, không chỉ chuỗi.** Chuỗi khớp chưa chắc là ca cần sửa.
6. **File dùng chung → phải QA CHỨC NĂNG THẬT**, không chỉ kiểm cú pháp. (`panorama-utils.js`
   gọi `openMenu()` chưa hề định nghĩa → menu mobile CHẾT trên 18 trang, `try/catch` nuốt lỗi,
   cú pháp vẫn hợp lệ. Chỉ Playwright bấm thật mới bắt được.)
7. **Quét cả HOA lẫn thường** — kể cả trong `<title>`, `og:`, JSON-LD.
8. **Meta/og/JSON-LD phải cùng độ chắc với thân bài.** Thân bài ghi "nghe nói 80% thất bại"
   thì meta KHÔNG được ghi phẳng "80% thất bại". Sai luật §2.6.
9. **Không đo nội dung đa ngữ bằng số ký tự.** CJK ≠ Latin — `.split()` báo trang ZH/JA
   "mỏng 104 từ" trong khi thật ra 2.4–3.1k ký tự, đủ ý. **So theo Ý, không theo đếm.**
10. **Đếm inbound phải tính cả href tương đối** — site dùng cả `href="/slug"` lẫn `href="slug"`.
    Chỉ đếm dạng `/slug` → báo nhầm 3 trang mồ côi (thật ra 0).
11. **Sửa dữ kiện phải quét cả `.txt` `.xml` `.json`, không chỉ `.html`.** Tầng dữ liệu mở
    (`llms.txt` · `llms-full.txt` · `feed.xml` · `data/*.json`) là thứ AI đọc TRƯỚC. Đã có lần
    HTML đúng mà 4 file này vẫn ghi số cũ suốt nhiều ngày.
12. **File tồn tại (HTTP 200) KHÔNG chứng minh nội dung đúng.** Phải mở đọc.
13. **Mọi kết luận "sạch" phải nêu rõ PHẠM VI đã quét** (bao nhiêu file, đuôi gì, có
    case-insensitive không). "Sạch" không phạm vi = vô nghĩa.
    **13b — ranh giới "thân bài" (khóa 30/8/2026, lỗi thật khi kiểm `/ram-vu-lan-nam-ban`):**
    khi kiểm "thân bài", nhớ khối FAQ hiển thị nằm **trong** `.art-body` — cắt tới
    `<div class="source-box">` là tính nhầm cả FAQ vào thân bài. Ranh giới đúng: từ
    `<div class="art-body">` tới `<h2>Câu hỏi thường gặp</h2>`.
    **13c — ranh giới CHUỖI CẤM khác ranh giới "thân bài" (khóa 1/9/2026, vấp LẦN HAI
    cùng chỗ):** khi quét chuỗi cấm (`Panorama`, tên chuyên mục cũ, CTA bán…), cắt tới
    `<div class="source-box">` là **bỏ sót khối Nguồn & lưu ý và khối "Đọc gì tiếp"** —
    hai khối người đọc vẫn đọc, AI vẫn trích. Đã lọt thật: ba bài Brief 04–06 còn
    "loạt Selection" và "Panorama không đại diện bên bán" trong khối Nguồn sau khi
    grep báo sạch. **Ranh giới đúng cho chuỗi cấm: từ `<div class="art-body">` tới
    `<div class="share-row">`.** Nhớ phân biệt hai ranh giới: đo *độ dày thân bài* thì
    dừng ở FAQ (13b); quét *chuỗi cấm* thì chạy tới nút Chia sẻ (13c).
    **13d — CHUẨN HOÁ `\xa0` TRƯỚC KHI SO (khóa 1/9/2026, lệch grep 3 lần trong một
    phiên):** site chủ động chèn `&nbsp;` để chống rớt chữ và chống vỡ tên vùng
    (`Nam&nbsp;Ban`, `25–30&nbsp;km`). Chính nó làm mọi grep chuỗi thật trượt: đếm
    "Nam Ban" thiếu, `str_replace` không khớp, số cũ tưởng đã sạch. **Mọi checker phải
    `html.unescape()` rồi `.replace('\xa0',' ')` trước khi so.** Khi thay chuỗi bằng
    `str_replace` thì ngược lại — phải lấy **nguyên văn raw có `&nbsp;`** từ file, đừng
    gõ lại bản có dấu cách thường.
14. **KHÔNG sửa vì checker báo thiếu. Chỉ sửa khi chứng minh được nó cải thiện chuỗi:**
    *được tìm thấy → được hiểu → được trích dẫn → được dẫn sang bài tiếp.* Đây là bộ lọc
    tối thượng, đứng trên mọi gợi ý của công cụ.
15. **Đổi câu hỏi FAQ → PHẢI đọc lại câu trả lời có còn khớp không** (khóa 29/8/2026, lỗi thật
    ở cụm Living Intelligence: đổi câu hỏi để chống trùng FAQ nhưng giữ nguyên câu trả lời cũ
    — câu trả lời viết cho câu hỏi cũ nên lệch hẳn với câu hỏi mới). Kiểm bằng **dạng câu**:
    câu hỏi **có/không** thì đáp phải mở bằng có/chưa/không, không phải "Nếu…"/"Nên…" (đó là
    đáp cho câu **nên hay không**, khác câu có/không); câu hỏi **khác gì / bao lâu / có đủ
    không / thế nào** thì đáp **không được** mở bằng "Nếu…", "Nên…", "Đừng…" (dấu hiệu đáp
    đang trả lời một câu hỏi có/không hoặc lời khuyên, không phải câu hỏi đã đổi). Trùng chữ,
    đếm H2/FAQ đúng số, không chuỗi cấm — vẫn có thể "sạch" mà câu hỏi/câu trả lời lệch nhau;
    grep không bắt được lỗi này, phải đọc từng cặp Q↔A bằng mắt.
    **15b — đừng tự tay tạo báo động giả (khóa 29/8/2026, rút từ tổng rà 13 ca):** câu hỏi
    có/không mà bản chất phụ thuộc điều kiện thì đáp mở bằng "Nếu…"/"Nên…" là ĐÚNG, không
    phải lỗi — đó chính là cách trả lời một câu hỏi vốn không có đáp án có/không cứng (11/13
    ca máy gắn cờ đợt 29/8 là báo động giả kiểu này). **Chỉ tính lỗi khi đáp né chốt rồi trôi
    sang một chủ đề khác hẳn** (kiểu ca đã vá: hỏi "một năm có đủ" mà đáp kể "ai hợp Nam Ban").
    Phân biệt: đáp có điều kiện nhưng vẫn xoay quanh đúng câu hỏi → giữ; đáp bỏ qua câu hỏi,
    quay sang trả lời một câu khác → sửa.
16. **Audio/asset sinh từ nội dung chỉ được chạy SAU khi nội dung đã lên `main`** (khóa
    30/8/2026, lỗi thật: chạy workflow audio cùng lúc với push nên nó checkout bản cũ, sinh
    ra MP3 đọc đúng chỗ vừa sửa — mà không ai thấy vì file vẫn tồn tại, vẫn phát được).
    Workflow chạy trên GitHub, nó `checkout` `main` tại thời điểm nó khởi động, KHÔNG thấy
    commit còn nằm ở máy. Trình tự bắt buộc: **commit → push → xác nhận `git ls-remote origin
    main` đã đổi → mới trigger workflow**. Kiểm sau khi chạy: `git log -1 -- audio/<slug>.mp3`
    phải trỏ commit MỚI HƠN commit sửa nội dung; nếu trỏ commit cũ hơn thì MP3 đang lệch, chạy
    lại với `overwrite=true`. Cùng luật này áp cho mọi asset sinh từ nội dung (ảnh OG tự cắt,
    sitemap tự sinh…), không riêng audio.
17. **Grep chuỗi LỒNG NHAU không được đếm thô** (khóa 30/8/2026, rút từ ca đặt tên
    `Chùa Linh Ẩn (Thiền viện Linh Ẩn)`). Khi một chuỗi cấm nằm **bên trong** một chuỗi hợp lệ,
    grep thẳng sẽ báo đỏ giả — nó bắt trúng chính cụm đang đúng. Phải **đếm cặp**: tổng
    occurrence chuỗi con phải bằng tổng occurrence cụm hợp lệ chứa nó; **bằng nhau là pass**,
    lệch một là có chỗ đứng độc lập. Cùng họ với Luật 4 (case-insensitive) và bài học "44 ca
    đỏ chỉ 1 ca thật": trước khi tin một con số grep, hỏi xem chuỗi cấm có thể là một phần
    của chuỗi đúng không.

---

## 7. ĐÍNH CHÍNH LUẬT — 6 điểm đã kiểm chứng (26/8/2026)

Báo cáo rà soát 8/2026 nêu 6 luật quá tuyệt đối. Kiểm thật trên repo cho thấy nếu áp máy móc
sẽ **phá nội dung đang đúng**. Đây là bản đã sửa — dùng bản này, không dùng bản cũ.

### 7.1 "phía Tây" — TÁCH LÀM HAI, đừng gộp

- **Hướng địa lý:** Nam Ban nằm **phía tây Đà Lạt** — ĐÚNG, giữ nguyên. Đã kiểm **20 ca**
  trong repo, tất cả đều đúng nghĩa la bàn.
- **Vùng quy hoạch tỉnh:** tên hành chính là **"Vùng trung tâm phía Bắc"** — đây là danh từ
  riêng trong văn bản quy hoạch, KHÔNG phải hướng la bàn.
- ⚠️ Hai thứ này KHÁC NHAU. Sửa "phía tây" thành "phía Bắc" hàng loạt = **gây lỗi địa lý toàn
  site**. Chỉ đụng khi câu đang nói về *tên vùng quy hoạch*, không đụng khi nói *hướng đi*.

### 7.2 "EN → EN only" — CÓ NGOẠI LỆ: bộ chuyển ngữ

Luật gốc: bài `lang="en"` chỉ link tới trang `lang="en"` (tiền tố `/en/` không phải điều kiện).
**Ngoại lệ bắt buộc giữ:** `.l10n` (bộ chuyển ngữ), `<link rel="alternate" hreflang>`, và
`canonical`. Mấy cái này BẮT BUỘC trỏ sang ngôn ngữ khác — đó là chức năng của nó.
Gỡ đi = **vỡ cụm hreflang**, mất tín hiệu đa ngữ với Google. Khi đếm "link ra ngoài ngôn ngữ",
**loại trừ `.l10n` + `hreflang` + `canonical`** rồi mới đếm.

### 7.3 FAQ trùng — "1 ngoại lệ" là SAI, thật ra **1 + 3**

- **1 ngoại lệ có chủ đích:** *"Nam Ban cách Đà Lạt bao xa"* ở `/duong-di-nam-ban` và
  `/nam-ban-la-gi` — cố ý, giữ.
- **3 cặp hub↔spoke với `/hoi-nhanh`:** hợp lệ. `/hoi-nhanh` là hub hỏi-đáp, trùng câu với bài
  chuyên sâu là ĐÚNG mô hình hub↔spoke, không phải lỗi.
- → Tổng **4 nhóm trùng, cả 4 đều hợp lệ**. Đừng gỡ.

### 7.4 Pillar — GIẢI MÂU THUẪN

Báo cáo có 2 câu chọi nhau: *"pillar phải là trang nhiều inbound nhất site"* vs *"internal link
không tối ưu theo quota"*. Thực tế: `/nam-ban-la-gi` xếp **47/121** với 6 inbound;
`/truoc-khi-xuong-tien` có 29. **Chốt:**

- **Luật "không tối ưu theo quota" THẮNG.** Không đi rải link để kéo pillar lên hạng 1 — đó
  đúng là hành vi Luật 14 cấm.
- Pillar được nhận diện bằng **vai trò nội dung** (trang trả lời câu gốc "Nam Ban là gì"), không
  bằng thứ hạng inbound.
- Chỉ thêm link tới pillar khi **câu đó thật sự cần dẫn người đọc sang** — tự nhiên trong mạch bài.
- Khi đếm inbound để tham khảo: **loại link nav/footer**, chỉ đếm link trong thân bài.

### 7.5 "huyện Lâm Hà" — ĐƯỢC DÙNG khi nói về ranh giới CŨ

35 ca trong repo, gần hết đều đúng: đang mô tả đơn vị hành chính **trước sáp nhập**. Viết lịch
sử mà cấm gọi tên cũ là sai. **Chỉ sửa** khi câu đang mô tả hiện trạng SAU sáp nhập mà vẫn ghi
"huyện Lâm Hà" như thể còn tồn tại.

### 7.6 "cây số vuông" / "ba vạn dân" — ĐƯỢC DÙNG trong văn xuôi

5 ca, đều cố ý — giọng publication, đọc mượt. **Luật đúng:** bảng dữ kiện / fact card / JSON-LD
/ `data/*.json` dùng **số chuẩn** (`117 km²`, `khoảng 33.000 người`); thân bài được phép dùng
lối nói trên. Hai chỗ không mâu thuẫn vì cùng một con số.

---

**Ghi nhớ chung cho §7:** cả 6 điểm trên đều là ca *"checker báo lỗi nhưng nội dung đang đúng"*.
Đây chính là Luật 14 trong thực tế — **chứng minh cải thiện trước, sửa sau.**
