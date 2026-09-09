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
- **BA SCRIPT PHẢI CHẠY LẠI KHI THÊM/XÓA BÀI HOẶC ẢNH — gom một chỗ để khỏi sót:**
  `python3 tools/gen-search-index.py` (sau khi **thêm/xóa/đổi tựa hoặc description một bài**
  — nếu quên thì bài mới không tìm được trong ô search) · `python3 tools/gen-image-manifest.py`
  và `python3 tools/gen-image-sitemap.py` (sau khi **thêm/xóa/đổi tên ảnh**). Commit luôn file
  chúng sinh ra (`search-index.json`, `data/images-manifest.json`, `image-sitemap.xml`).
- Xong: `git add -A && git commit && git push origin main` → chờ Vercel → **báo link**.

### Ô TÌM KIẾM — CHỈ TRANG CHỦ + THANH MENU (Chú chốt 9/9/2026)

Chạy hoàn toàn client-side, không backend, không dịch vụ ngoài. Ba mảnh:
`tools/gen-search-index.py` → `search-index.json` (163 trang, ~123KB, gzip ~35KB) ·
phần cuối `panorama-utils.js` dựng giao diện · `index.html` có slot `#pm-home-search`.

- **Ô mở sẵn CHỈ ở trang chủ** (slot đó). Mọi trang khác chỉ có **icon kính lúp trong nav
  + trong menu mobile** — bấm mới mở lớp phủ. Đừng thêm ô mở sẵn vào bài, sai chốt.
- `search-index.json` **tải lười** — chỉ `fetch` lần đầu người đọc mở ô, không nặng trang.
- **Hai nhánh, đừng gộp.** Gõ **một chữ** → `searchOne`, 5 bậc, khớp trọn một từ trong
  tiêu đề đứng đầu. Gõ **từ hai chữ trở lên** → `searchMany`, **mọi chữ phải có mặt,
  không cần dính liền**. Thiếu nhánh sau thì gõ "chi phí tách thửa" ra **0 kết quả** —
  đã vấp thật 9/9/2026, vì bản đầu chỉ dò nguyên cụm làm chuỗi con.
- Ba lỗi đã vá, đừng làm lại: gộp một chuỗi dò thì "ho bai cong" ra bài đường Hà Bắc
  trước; chỉ so tiền tố thì "ho" ra "**Hợp** tác" trước "**Hồ** Thanh Trì"; chỉ dò nguyên
  cụm thì truy vấn nhiều chữ trượt sạch. **Đừng gộp lại `ft`/`f` làm một.**
- **Index KHÔNG chứa thân bài** — chỉ tựa + description + keywords. Nên câu ghép một chữ
  ở thân bài với một chữ ở tựa sẽ không khớp. Đã cân nhắc nhét thêm H2+H3 (83KB thô toàn
  site) và **cố ý bỏ**: ca thúc đẩy ý đó là "chi phí tách thửa", mà `/tach-thua-dat-nam-ban`
  không hề có chữ "chi phí" ở bất cứ đâu — kể cả H2. Thêm index không cứu được nội dung
  chưa có. Đây là Luật 14: chưa chứng minh được cải thiện thì chưa thêm.
- Chỉ index trang `lang="vi"` — ô search nằm ở trang tiếng Việt, trộn trang ngoại ngữ vào
  là trả kết quả người đọc không mở được.
- Phím `/` mở, `Esc` đóng. Không kết quả → "Chưa có bài nào về chuyện này." (không CTA).

### CHẶN COPY — CHỪA MỘT CHÌA CHO CHÚ (9/9/2026)

Cuối `panorama-utils.js` có lớp chặn bôi đen chữ, kéo ảnh, chuột phải trên ảnh, Ctrl+S.
Cố ý — giữ ảnh Chú tự chụp và chữ Chú viết khỏi bị lấy nguyên. **Đừng gỡ.**

**Chìa của Chú: thêm `?copy=1` vào cuối bất kỳ địa chỉ nào** → tắt lớp chặn trên máy đó
và **nhớ luôn** (localStorage `pm-copy-ok`), lần sau vào thẳng vẫn copy được. Khoá lại
bằng `?copy=0`. Người khác không có chìa thì vẫn bị chặn nguyên.

Ba điều đã kiểm, đừng bàn lại:
- **Không hại SEO/AEO.** Google và AI đọc thẳng HTML nguồn, không chạy sự kiện `copy`;
  `user-select:none` không đụng tới crawler. Lớp này chỉ ngăn người dùng phổ thông.
- **Chừa sẵn phần liên hệ** (`EXEMPT`): footer, khối liên hệ cuối bài, `tel:`/`mailto:`/
  Zalo, mọi ô nhập. Khách vẫn copy được số mà gọi — không được chặn mấy chỗ này, chặn là
  tự cắt phễu.
- **Chuột phải trên CHỮ vẫn mở menu** (chỉ chặn trên ảnh) để người đọc còn dùng được
  chức năng dịch của trình duyệt. Đừng chặn luôn cho gọn.

Đã QA Playwright 8 nhánh: khách thường bị chặn cả chữ lẫn ảnh · `?copy=1` mở được cả hai ·
vào thẳng lần sau vẫn nhớ · `?copy=0` khoá lại · khách trên máy khác vẫn bị chặn.
`localStorage` lỗi (chế độ ẩn danh) thì **cứ chặn** — ngã về phía an toàn.

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

**NEO VÙNG — ĐÃ CHẠY HẾT MỘT LƯỢT, ĐÓNG SỔ (Chú chốt 2/9/2026).** Quét toàn bộ H2 và
FAQ trang `lang="vi"`: **638 ca thiếu neo**, lọc theo bốn luật dưới còn **20 ca đáng
neo**, đã làm. 618 ca còn lại **cố ý bỏ** — không phải quên, không rà lại. Ba nhóm bỏ
lớn nhất: **291 ca là H2 tu từ hoặc nhãn mục** (không phải câu hỏi, neo vào là giết
câu); **150 ca không nói về vật thể trong vùng**; **116 ca không thuộc ba nhóm ưu tiên**.
Bốn luật lọc (dùng lại cho mọi đợt sau, và cho bài mới):

1. **Không neo khi sai phạm vi.** Nam Hà là xã riêng. Tà Nung thuộc phường Cam Ly,
   Đà Lạt. Bảo Lộc, Di Linh, D'ran, Đơn Dương, Đức Trọng, Lạc Dương là vùng khác.
   Quy định pháp lý cấp tỉnh → neo **"Lâm Đồng"**, không neo "Nam Ban" (neo hẹp lại
   vừa sai vừa đẩy người Bảo Lộc, Di Linh ra khỏi kết quả). Câu so sánh hai vùng →
   không neo bên nào. Khái niệm toàn quốc (sổ chung, vi bằng, công chứng, thuế, "một
   sào là bao nhiêu mét vuông") → không neo.
2. **Không neo khi câu đã có neo khác** — tên riêng đủ mạnh (thác Voi, chùa Linh Ẩn,
   Liên Khương, ĐT.725, hồ Bãi Công, cầu Tổng Đội) hoặc đã có địa danh vùng.
3. **Không neo khi giết câu.** Câu đang chủ động sửa hiểu nhầm (*"Chùa Linh Ẩn ở
   đâu?"* — người cần đọc chính là người gõ câu chưa có "Nam Ban"). Nhãn khu có mô tả
   thơ. Câu hỏi mà đáp án chính là tên vùng (*"Mê Linh thuộc xã nào?"*). H2 tu từ,
   không phải câu hỏi. Câu dài sẵn, thêm vào vượt hai dòng ở 360.
4. **Mỗi bài tối đa 3 câu** (hub `/hoi-nhanh` tối đa 5), chọn theo thứ tự: câu định vị
   → câu về giá hoặc tiền → câu quyết định mua. Cách viết: **"ở Nam Ban"**, không ghép
   liền, cho khớp nếp site.

**Bài MỚI viết đúng neo ngay từ đầu** (một dòng kiểm trong phiếu content), không đi vá
bài cũ. Cùng nguyên tắc này áp cho mọi sổ rà tương tự — 52 ca contrast màu cứng, 34 màu
ngoài palette, entity graph, card title dài: đã cân nhắc và **cố ý bỏ**.

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

### FAQ CHO TÊN RIÊNG — KILL LIST, ĐÃ CÂN NHẮC VÀ CỐ Ý BỎ (Chú chốt 7/9/2026)

Có một lỗi hệ thống đáng bắt: **bài liệt kê tên riêng mà không có FAQ cho từng
tên**. Bài kể tám cái hồ, hai chục tên thôn, rồi chỉ ba FAQ chung — người ta gõ
TỪNG tên một, mình chỉ mở cửa cho câu tổng. Mất long-tail ở chỗ dễ thắng nhất,
vì tên riêng địa phương gần như không ai cạnh tranh. Rà bằng
`python3 tools/scan-faq-coverage.py`.

**Nhưng ba nhóm dưới đây ĐÃ QUYẾT BỎ. Đợt rà sau gặp lại thì đừng quyết lại từ đầu.**

1. **Tên đã có bài riêng → KHÔNG thêm FAQ ở bài khác.** Đây là chống
   cannibalization đúng chỗ. Mỗi tên chỉ có MỘT nhà. Đã đóng: `hồ Bãi Công` ở
   `/ho-tron-nam-ban` và `/dat-trung-tam-nam-ban` · `hồ Từ Liêm` ở
   `/ho-bai-cong-nam-ban` · `hồ Đông Thanh` · `thác Voi` · `chùa Linh Ẩn` ·
   `cầu Tổng Đội` và `cầu Tiền Lâm` ở mọi bài không phải `/cau-tong-doi-nam-ban`
   (bài đó đã có 7 FAQ phủ cả hai tên, kể cả tên trên giấy tờ).
   **Cách nhận ra nhà của một tên:** vai trò nội dung thắng số đếm — bài *về* cái
   đó là nhà, không phải bài nhắc nó nhiều nhất. Ví dụ `chợ Thăng Long` được
   `/ho-bai-cong-nam-ban` nhắc 5 lần, `/cho-nam-ban` nhắc 4 — nhà vẫn là
   `/cho-nam-ban`, vì bài kia chỉ dùng chợ làm mốc chỉ đường (§7.4).

2. **Mốc là cơ sở kinh doanh → KHÔNG FAQ, KHÔNG link, KHÔNG đứng tên giới thiệu.**
   `Nacasoo Hill` · `Phương Minh Farm` · `HT86` · `Hualong` · `King Coffee` và mọi
   tên cùng loại. Chỉ được nhắc tên làm mốc chỉ đường. Bộ quét cố ý không bắt
   nhóm này (nó không có danh từ chỉ loại đứng trước) — **đừng đi đọc tay để bù**.

3. **Mốc nằm ngoài vùng → KHÔNG neo FAQ vào bài Nam Ban.** Ca thật đã loại:
   `Suối Vàng` (ở Đà Lạt), `đèo Bảo Lộc`, `đèo Gia Bắc`, `đèo Đa Mi`,
   `đèo Ngoạn Mục`, `QL55`, `QL27` — mấy cái này xuất hiện ở `/duong-di-nam-ban`
   và `/dat-gan-da-lat` như chặng đường, không phải thực thể của vùng. Neo vào là
   kéo bài lệch vùng, sai §5 luật lọc 1.

### GROUND TRUTH — RỪNG THÔNG Ở NAM BAN (Chú chốt 9/9/2026)

**Rừng thông ở Nam Ban: CÓ nhưng ÍT.** Và cái có thì **phần nhiều là đồi thông người dân
tự trồng trên đất của họ, KHÔNG phải rừng nhà nước**. Người ta trồng để giữ đất, lấy gỗ,
hoặc đơn giản là thích.

**Hai hệ quả, cả hai đều đảo trục bài:**

1. **Lô giáp thông là lô HIẾM**, không phải chuyện gặp thường. Cấm viết kiểu "ai đi xem
   đất vài lần cũng gặp" — đó là viết bài trụ cho tình huống hiếm.
2. **Tầm nhìn ra thông KHÔNG mặc định ổn định.** Vạt thông bền hay không **tùy chủ vạt
   thông** — họ có quyền làm gì với đất của mình. Cấm câu "rừng do nhà nước quản lý thì
   ổn định hơn" đứng làm vế chính; vẫn có vạt nhà nước, nhưng đó là thiểu số ở đây.
   Câu hỏi thực tế không phải *"rừng loại gì"* mà là **"thông của nhà ai"**.

Viết **"phần nhiều"**, không viết "tất cả". Và **cấm cấu trúc câu `phần nhiều rừng thông
ở Nam Ban là…`** — nó ngầm nói rừng thông nhiều. Quét `phần nhiều rừng thông` phải = 0.
Đã áp cho `/dat-giap-rung-thong-nam-ban`, `/xay-nha-giap-rung-thong-nam-ban`,
`/view-panorama-nam-ban`, `llms.txt`, `llms-full.txt`.

### PHÍ 0 ĐỒNG KHI LÀM THỦ TỤC TRỰC TUYẾN — KHÔNG ĐƯA VÀO BÀI (đóng sổ 9/9/2026)

Có phiếu nhắc **Nghị quyết 51/2025/NQ-HĐND Lâm Đồng** quy định mức thu 0 đồng với phí,
lệ phí khi làm dịch vụ công trực tuyến. **Tra hai lần, không xác minh được văn bản của
Lâm Đồng.** Cái tra ra là nghị quyết CÙNG LOẠI của tỉnh khác: An Giang 14/2025, Bà Rịa –
Vũng Tàu 08/2025, Quảng Ngãi 05/2025, TP.HCM 411. Đây đúng kiểu lấy số hiệu của tỉnh này
gán cho tỉnh kia — cùng họ với Luật 23.

**Chưa có văn bản Lâm Đồng thì KHÔNG ghi con số nào**, §2.6. Muốn mở lại thì phải có số
hiệu tra được trên cổng HĐND tỉnh Lâm Đồng, không lấy từ bài báo tổng hợp nhiều tỉnh.

### SỔ CHỜ ẢNH — BA BÀI ĐANG TRỐNG, CHỜ CHÚ CHỤP (mở 8/9/2026)

Ba bài dưới đây **cố ý không có ảnh trong thân bài** — kho không có tấm nào đúng chủ đề,
và Luật 19 cấm gắn tạm rồi chú thích chung chung. Không phải quên, đừng đi gắn bừa:

- `/xay-nha-giap-suoi-nam-ban` — **kho không có ảnh suối nào.** Bài này còn dùng
  `og:image` là ảnh brand `nam-ban-toan-canh-og.jpg`, không phải ảnh suối. Cần: một
  con suối trong xã, thấy được **mép bờ** và mực nước — tốt nhất chụp hai lần, mùa khô
  và cuối mùa mưa, cùng một khúc, để minh họa đúng cái bài đang nói.
- `/nha-go-thong-nam-ban` — cần cận cảnh **vách hoặc sàn gỗ thông** (thấy vân, thấy mắt
  gỗ), hoặc một căn đang lắp ghép. Ảnh nhà gỗ hiện có (`nha-go-farmstay-nam-ban.webp`)
  đã dùng cho bài mẹ `/nha-go-nam-ban`, dùng lại lần nữa là loãng.
- `/10-10-1975-nam-ban` — cần ảnh tư liệu hoặc dấu vết còn lại (bia, cổng chào, nhà cũ
  thời kinh tế mới). **Không lấy ảnh tư liệu trên mạng** — bản quyền, và Luật 19.

**Khi có ảnh:** thêm figure vào thân bài, cắt `og:image` mới theo `/images/<slug>.jpg`
1200×630, chạy lại `tools/gen-image-manifest.py` + `tools/gen-image-sitemap.py`. Ảnh không
đổi lời đọc (Luật 21) nên **không cần sinh lại MP3**.

### SỔ CHỜ — SỬA KHI CÓ VĂN BẢN TÁCH NAM HÀ KHỎI PHI TÔ (mở 7/9/2026)

Hiện Nam Hà và Phi Tô cùng một xã (xã Nam&nbsp;Hà Lâm&nbsp;Hà, từ 1/7/2025, Nghị quyết
1671). Có thông tin đợt sắp xếp tiếp theo sẽ đưa **phần Nam Hà vào Nam Ban, còn Phi Tô
thì không** — chưa có văn bản, nên site chưa sửa gì.

Quét toàn site ra **36 câu** ghép Nam Hà với Phi Tô. Nhưng **chỉ ba câu sẽ sai**, vì
chúng viết ở **thể vĩnh viễn, không có mốc thời gian**. Khi có quyết định thì sửa đúng
ba câu này trước, đừng đi rà lại 36 ca:

- `/xa-nam-ha-lam-ha` — *"nay là một xã riêng **gồm cả vùng Phi Tô**"*
- `/nam-ban-va-nam-ha` — *"Nam Hà là xã riêng (xã Nam Hà Lâm Hà, **gồm Nam Hà và Phi Tô cũ**)"*
- `/phi-to-nam-ha-lam-ha` — *"**Phi Tô thuộc xã Nam Hà Lâm Hà**, là một xã khác với Nam Ban"*
  (câu này còn là câu trả lời trong FAQPage, sửa cả hiển thị lẫn schema)

**Luật rút ra — CÁCH VIẾT DỮ KIỆN HÀNH CHÍNH CHO BỀN:** câu **có mốc thời gian** thì
không hỏng theo thời gian, vì nó mô tả một thời điểm ("từ 1/7/2025, Phi Tô nhập với
Nam Hà…" — sau này vẫn đúng). Câu viết ở **thể vĩnh viễn** mới hỏng ("Phi Tô thuộc xã
Nam Hà Lâm Hà"). Địa giới vùng này đã đổi tám lần trong năm mươi năm, nên mọi câu về
đơn vị hành chính **phải gắn mốc**. Áp cho bài mới ngay từ đầu, đừng đi vá sau.

**Trước khi thêm FAQ cho một tên, hỏi ba câu:** tên này đã có bài riêng chưa · nó
có phải cơ sở kinh doanh không · nó có nằm trong vùng không. Ba câu đó loại phần
lớn ứng viên. Còn lại mới đáng viết.

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

## 6. LUẬT GREP & QA — 23 điều (khóa 8/2026, bổ sung 9/2026 — rút từ lỗi thật)

Điều 1–17 là 17 lần **audit tự động báo SAI** trong đợt rà 8/2026; điều 18–23 bổ sung 9/2026.
Mỗi luật = một lỗi đã thật sự
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

18. **KHÔNG TRỘN ÂM LỊCH VỚI DƯƠNG LỊCH TRONG MỘT CÂU** (khóa 6/9/2026, 24 ca thật, 8 file).
    "Tháng Chạp" là tháng 12 **âm**, rơi vào khoảng tháng 1–2 dương. "Tháng Giêng" là tháng 1
    **âm**, khoảng tháng 2 dương. Ghép chúng cạnh tên tháng dương ("tháng Mười Một tháng Chạp",
    "từ tháng Mười tới tháng Giêng") là trộn hai hệ lịch trong một câu, và lệch hẳn bài trụ.
    Đã sửa cả 24 ca về dương lịch, khớp `/mua-ca-phe-nam-ban` (thu tháng 10 → tháng 1 năm sau,
    rộ tháng 11 và 12) và `/mua-bo-nam-ban` (Booth tháng 8 → tháng 12).
    **Luật:** mùa vụ, thời tiết, tiến độ, giờ giấc → **luôn dương lịch**. Chỉ dùng tên tháng âm
    khi câu đang thật sự nói chuyện âm lịch — Tết, rằm, cúng, giỗ. Quét định kỳ `tháng Chạp` và
    `tháng Giêng`; ca nào đứng cạnh tên tháng dương là lỗi.

19. **KHÔNG SUY CHỦ ĐỀ ẢNH TỪ TÊN FILE** (khóa 6/9/2026). Ảnh og đặt theo quy ước `<slug>.jpg`,
    nên **tên file trùng slug KHÔNG chứng minh ảnh chụp ở đó**. Ca thật: `ho-tu-liem-nam-ban.jpg`
    từng là toàn cảnh trung tâm kèm thác Voi và tượng Quan Âm, không phải hồ Từ Liêm — **đã vá
    6/9/2026**, giờ cắt từ ảnh thật của Chú (`ho-tu-liem-nha-mai-do-nam-ban.webp`, nhận diện bằng
    căn nhà mái đỏ sát mép nước); `thuy-dien-da-chomo-phi-to.jpg` là đường bê tông qua rẫy, không
    phải nhà máy — **chưa vá**.
    **Luật:** trước khi gắn, **mở ảnh ra nhìn**. Không xác định được chụp ở đâu thì **để trống**,
    không gắn tạm rồi chú thích chung chung. Caption chỉ được nhận đúng thứ nhìn thấy trong ảnh.

20. **ẢNH PUBLICATION KHÔNG ĐƯỢC MANG DẤU TIN RAO** (khóa 6/9/2026). Không dùng ảnh có **vạch
    khoanh ranh**, mũi tên, chữ chèn, khung highlight, hay bất kỳ chú thích đồ họa nào của tin
    rao. Ca thật đã loại: `nam-ban-thung-lung-ao-ho.webp` — rất hợp đoạn "nhiều mặt nước không
    có tên" nhưng có vạch đỏ khoanh một lô bán, đặt vào bài là lệch lane.

21. **AUDIO: CHỜ `audio-auto` ĐÁP XUỐNG RỒI MỚI DISPATCH** (khóa 6/9/2026, fail 2 lần liên tiếp
    cùng một nguyên nhân). `audio-auto.yml` tự chạy khi push nội dung; nếu dispatch
    `generate-audio-free.yml` ngay sau push thì hai workflow đua nhau, `audio-auto` commit
    trước, `git push` của run dispatch bị **reject** — MP3 sinh ra rồi vứt, run báo failure mà
    không phải lỗi sinh audio. **Trình tự đúng:** commit → push → **chờ commit của `audio-auto`
    đáp xuống `main`** → xác nhận `git ls-remote origin main` đã đứng yên → mới dispatch
    `generate-audio-free` với `overwrite=true`. Làm đúng thứ tự thì xong ngay lần đầu.
    Hệ quả của Luật 16, không thay thế nó.
    **Ảnh không đổi lời đọc** — bộ trích bỏ qua `<figure>`, nên chỉ thêm/đổi ảnh thì **không cần**
    sinh lại MP3; kiểm bằng chính `scripts/gen_audio_edge.py` thay vì đoán.
    **21b — SO LỜI ĐỌC VỚI BẢN TẠI COMMIT SINH RA MP3, KHÔNG PHẢI VỚI MỘT MỐC GIỮA DÒNG**
    (khóa 6/9/2026, vấp ngay trong phiên đặt Luật 21). Câu hỏi đúng luôn là: *lời đọc trong MP3
    đang có còn khớp lời đọc hiện tại không?* Nên mốc so sánh **bắt buộc** là
    `git log -1 --format=%H -- audio/<slug>.mp3`, rồi `git show <mp3-commit>:<slug>.html` và đưa
    cả hai bản qua `narration()`. Lấy bất kỳ mốc nào khác — kể cả "trước loạt sửa lần này" — sẽ
    bỏ sót mọi lần sửa nội dung nằm giữa commit MP3 và mốc đó. Ca thật: so với mốc giữa dòng ra
    "3 bài cần sinh lại", so đúng mốc MP3 ra **6 bài**; ba bài lọt là ba bài đã sửa chữ từ đợt
    trước mà MP3 chưa theo kịp. **Ngược lại, đừng tin `git merge-base --is-ancestor` giữa commit
    nội dung và commit MP3** — nó báo đỏ cả bài chỉ thêm `<figure>` (báo động giả kiểu Luật 17).
    Ancestry chỉ để khoanh vùng; quyết định phải bằng so `narration()`.
    **21c — ĐÃ VÁ GỐC 6/9/2026: hai workflow audio giờ tự rebase rồi thử lại 5 lần.**
    Nguyên nhân thật của cả ba lần fail không phải "dispatch sai lúc" mà là `git push` TRẦN
    trong `audio-auto.yml` và `generate-audio-free.yml` — `main` nhích một commit bất kỳ (kể cả
    commit không liên quan nội dung, như sửa chính CLAUDE.md) là run bị `! [rejected] (fetch
    first)`, MP3 sinh xong rồi vứt. Đã thay bằng vòng `git push || git pull --rebase origin main`
    lặp 5 lần ở cả hai file. Từ nay **không cần canh me `main` đứng yên nữa**; Luật 21 và 21b
    vẫn giữ để hiểu vì sao, nhưng cách chữa là ở workflow chứ không phải ở người bấm nút.
    **21d — VÁ TIẾP 7/9/2026: rebase KHÔNG đủ khi hai run cùng sinh một file MP3.**
    Bài MỚI thì `audio-auto` tự sinh MP3 (vì bài chưa có `<meta name="pm-audio">`), rồi
    push trước. Run `generate-audio-free` dispatch sau cũng sinh đúng file đó, rebase lên
    thì gặp **CONFLICT (add/add) trên file nhị phân** — git không tự gộp được, rebase dừng,
    MP3 vẫn bị vứt. Vòng rebase ở 21c chỉ xử được xung đột văn bản.
    Đã thay bằng: `git fetch` → `git rebase origin/main` → nếu đụng độ thì
    `git checkout --theirs -- audio/` (trong rebase, "theirs" là bản của commit đang được
    áp lại, tức bản vừa sinh) → `git add -A` → `git rebase --continue`.
    **Hệ quả cho người bấm nút: với BÀI MỚI thì đừng dispatch `generate-audio-free` nữa** —
    `audio-auto` đã sinh sẵn rồi, dispatch thêm chỉ tạo ra đúng cái đụng độ này. Chỉ dispatch
    cho bài CŨ vừa sửa chữ.

22. **TỰA HỨA GÌ THÌ THÂN BÀI PHẢI CÓ** (khóa 6/9/2026, ca thật `/duong-ha-bac-nam-ban`). Đổi tựa
    thành "Nam Ban – Mê Linh" trong khi **"Mê Linh" xuất hiện 0 lần** trong thân bài là tựa hứa
    suông — hại cả người đọc lẫn xếp hạng. **Luật:** tựa và H1 chỉ được chứa địa danh, cụm hoặc
    khái niệm mà thân bài có nói tới. Đổi tựa thì kiểm ngay: cụm mới vừa thêm xuất hiện mấy lần
    trong thân bài — **bằng 0 thì phải bổ sung nội dung**, không để tựa đứng một mình. Bổ sung
    bằng **dữ kiện chứng minh được** (ca này: Buôn Chuối thuộc Mê Linh theo `/nen-xem-khu-nao-o-nam-ban`,
    Chi Lăng thuộc trung tâm theo `/dat-gia-lam-nam-ban` — dữ liệu sẵn trong repo, không lấy nguồn ngoài).
    **Kèm:** `<title>`, H1 và `og:title` phải là **một chuỗi thống nhất**, không để ba kiểu như bài
    đó từng có. Và khi bài khó tìm, nhớ lý do lớn nhất thường không phải kỹ thuật: **tên riêng mới
    chưa ai biết thì tự nó không kéo được ai** — phải gắn vào cụm người ta đã gõ.

23. **DỮ KIỆN CỦA XÃ BÊN CẠNH KHÔNG ĐƯỢC GÁN CHO NAM BAN** (khóa 6/9/2026, ca thật đã sửa).
    `/rau-hoa-cay-do-la-nam-ban` và `/dat-nam-ban-trong-cay-gi` ghi "một hợp tác xã rau hoa lập năm
    2015" như của Nam Ban. Tra ra đó là **Hợp tác xã rau, hoa công nghệ cao Nam&nbsp;Hà** — lập 2015
    tại **xã Nam Hà**, huyện Lâm Hà, do ông Phương và 10 nông dân; câu "có hộ trước kia trồng cà phê
    chuyển sang làm hoa nhà kính" cũng chính là chuyện của hộ đó. Đã gỡ khỏi cả hai bài, `llms.txt`
    và `llms-full.txt`. **Luật:** bài báo về "Lâm Hà" có thể trộn nhiều xã trong một bài — trước khi
    lấy một mô hình, hợp tác xã, con số hay câu chuyện hộ dân, **phải xác định nó thuộc xã nào**.
    Cùng họ với §5 (Nam Hà là xã riêng, cạnh Nam Ban chứ không thuộc). Nghi ngờ thì mô tả bằng
    **quan sát tại chỗ** thay vì dẫn mô hình của ai.


24. **NGHE "CÓ NHIỀU X, X LÀ Y" THÌ HỎI LẠI: "NHIỀU" LÀ SỐ LƯỢNG HAY LÀ MỞ ĐẦU CÂU?**
    (khóa 9/9/2026, ca thật). Chú nói *"Nam Ban có nhiều rừng thông, đồi thông tự trồng"* —
    đọc thành **rừng thông NHIỀU**, trong khi ý là **"nhiều cái trong số đó là thông tự
    trồng"**, còn tổng thể thì **ÍT**. Một chữ đọc lệch làm cả cụm hai bài đặt sai chỗ:
    viết bài trụ cho một tình huống hiếm, mở bài bằng "ai đi xem đất vài lần cũng gặp",
    và ngầm hứa tầm nhìn ổn định.
    **Luật:** dữ kiện về **mật độ / số lượng** thì hỏi lại trước khi viết, đừng suy từ
    ngữ cảnh. Câu mở bài kiểu *"ai cũng gặp"*, *"bao giờ cũng"*, *"đi vài lần sẽ thấy"*
    là **câu khẳng định mật độ** — chỉ viết khi có ground truth, không viết cho đủ giọng.

25. **`llms-full.txt`: MỖI ENTRY PHẢI CÓ `\n\n---\n\n## ` ĐỨNG TRƯỚC** (khóa 9/9/2026,
    hệ quả của chính đợt vá 22 ca hôm 8/9). Đợt đó chèn dòng `## tiêu đề` nhưng **thiếu
    dấu `---` phân cách**, nên 11 bài dính vào khối của bài trước — checker "thiếu `##`"
    vẫn báo 0 vì `##` có thật. Hậu quả thật: lần sinh lại entry sau đó **nuốt mất 5 bài**
    (163 → 158 URL), bắt được nhờ đối chiếu số URL trước/sau.
    **Luật:** sau mọi thao tác trên `llms-full.txt`, kiểm ba số — **tổng URL không đổi** ·
    **`split('\n---\n')` không có khối nào chứa >1 URL** · **không có khối rỗng**. Và khi
    cắt entry theo `rindex('\n---\n', k, nx)`, nhớ `nx` là vị trí của `\n` trước `## `
    nên slice **không chứa** ký tự đó — phải nới biên trên, nếu không `rindex` ném
    `ValueError` giữa chừng.

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
- **Nhóm thứ 5 phát hiện 9/9/2026 — ĐÃ XỬ, KHÔNG phải ngoại lệ:** *"Xã Nam Ban Lâm Hà
  rộng bao nhiêu, bao nhiêu dân?"* từng nằm ở cả `/nam-ban-la-gi` và `/xa-nam-ban-lam-ha`.
  Không dính `/hoi-nhanh`, không phải intent khác nhau — chỉ là hai bài cùng giữ một câu
  vì chưa ai rà. **Đã gỡ khỏi FAQPage của pillar `/nam-ban-la-gi`** (thân bài vẫn nói
  diện tích, dân số — chỉ bỏ khỏi schema), giữ ở `/xa-nam-ban-lam-ha` theo §5 *"bài về
  cái đó là nhà"*. Rà bằng: quét mọi `FAQPage` trang `lang="vi"`, chuẩn hoá `\xa0` +
  bỏ dấu câu + lowercase rồi gom theo chuỗi. Lần quét 9/9: **951 câu, 946 chuỗi khác
  nhau, 5 nhóm trùng nguyên câu, 0 trùng trong cùng một bài.**

### 7.3b FAQ HIỂN THỊ NHIỀU HƠN FAQ TRONG SCHEMA — LÀ THIẾT KẾ, KHÔNG PHẢI LỖI (đóng sổ 9/9/2026)

Có phiếu báo `/ho-bai-cong-nam-ban` hiển thị FAQ *"Đường Hà Bắc ở Nam Ban là đường
nào?"* mà thiếu trong `FAQPage`. Nghe như lỗi. **Quét cả site thì ra 19 trang, 23 ca
cùng kiểu — và cả 23 ca đều CỐ Ý.**

Bằng chứng: với mỗi câu bị bỏ khỏi schema, **có một bài khác đang giữ đúng câu đó
trong schema của nó** — tức bài nhà. 18/23 khớp nguyên văn, 5 ca còn lại khớp biến
thể (*"Nam Ban trồng cây gì?"* ↔ `/dat-nam-ban-trong-cay-gi` giữ *"Đất Nam Ban trồng
được những cây gì?"*; *"Nam Ban ở đâu, cách Đà Lạt bao xa?"* ↔ `/nam-ban-la-gi` giữ
cả hai vế rời). **23/23 đều có nhà.** Một ca còn là ca §5 kill-list luật 2 chạy đúng:
*"Nacasoo Hill ở đâu?"* là cơ sở kinh doanh nên cố ý không vào schema.

**Vì sao nếp này đúng, và là nếp nên giữ:**
- Google **bắt buộc** nội dung `FAQPage` phải hiển thị được trên trang. Nên
  **hiển thị mà không có trong schema = hợp lệ**; **có trong schema mà không hiển
  thị = vi phạm chính sách**. Quét 9/9: chiều vi phạm đó **0 ca**. Không có lỗi nào.
- Câu hiển thị phục vụ **người đọc đang ở trang đó**. Bỏ nó khỏi schema để **chỉ bài
  nhà tranh rich result** cho truy vấn đó. Đúng §5 kill-list luật 1, đúng §7.3.
- Thêm câu vào schema = tự tay tạo trùng nguyên câu giữa hai bài — đúng thứ §7.3
  vừa dọn hôm 9/9.

**Luật:** phiếu nào báo "FAQ thiếu trong schema" thì **KHÔNG vá**. Hỏi trước: câu này
có bài nhà chưa? Có rồi thì schema bỏ nó ra là ĐÚNG. Chỉ xét thêm vào schema khi câu
đó **không có nhà ở đâu cả** — và kể cả lúc đó vẫn phải qua bộ lọc Luật 14.
Rà lại bằng: so `<h3>` trong khối FAQ hiển thị (cắt từ `<h2>Câu hỏi thường gặp</h2>`
tới `<div class="source-box">`, không tính `<h3>Nguồn &amp; lưu ý</h3>`) với
`mainEntity` của `FAQPage`. **Chiều duy nhất cần báo động là schema-có-mà-không-hiển-thị.**

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

### 7.7 SỐ TRÒN vs SỐ LẺ — luật chung (Chú chốt 4/9/2026)

**Số làm tròn dùng trong văn kể. Số lẻ chỉ xuất hiện KÈM NGUỒN, trong bài tra cứu và trong
schema. Không đồng nhất hai loại.**

Rút ra từ hai ca thật cùng ngày:
- `117,53 km²` **giữ** ở `/ban-do-quy-hoach-nam-ban` vì trích thẳng văn bản quy hoạch, có nguồn
  kèm, và đó là bài tồn tại để truyền độ chính xác. Bài kể chuyện ghi `khoảng 117 km²`.
- `khoảng 33.035 người` **giữ** ở `/quy-hoach-chung-nam-ban` và các bản sao dữ liệu, vì nó luôn
  đứng cùng câu với `11.753,83 ha` — cặp số trích từ một hồ sơ. Làm tròn một nửa cặp là tự
  mâu thuẫn ngay trong câu.

**DÂN SỐ — số chuẩn cho văn kể là `khoảng 33.000 người`.** Trước 4/9/2026 site có **bảy cách
viết, bốn con số** (33.035 · 33.000 · 32.770 · 30.000), ai trích rời một câu là ra số khác nhau.
Đã quét dọn một lượt. **Số lịch sử KHÔNG đụng**: `4.100 nhân khẩu` và `2.345 ha` (xã Nam Hà lập
2002), `~11.000 nhân khẩu` và `2.089 ha` (thị trấn Nam Ban còn lại sau 2002) — đó là số của một
thời điểm khác, không phải cách làm tròn khác.

Khi thấy hai số lẻ khác nhau cho **cùng một đại lượng** (ví dụ 32.770 và 33.035 cùng là dân số
xã), đó là mâu thuẫn thật — gom về số tròn, đừng giữ cả hai.

---

**Ghi nhớ chung cho §7:** cả 6 điểm trên đều là ca *"checker báo lỗi nhưng nội dung đang đúng"*.
Đây chính là Luật 14 trong thực tế — **chứng minh cải thiện trước, sửa sau.**
