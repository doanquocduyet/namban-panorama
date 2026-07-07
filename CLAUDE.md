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
3. **Xong bất kỳ việc gì → báo kết quả + link kiểm tra** (link live/preview, ảnh QA,
   commit). Số thật, không hứa suông.
4. **Luôn QA + tối ưu cả 2 giao diện: PC (1440/1920px) VÀ mobile (390px)** — bằng thiết kế
   + công nghệ mới nhất. Không bao giờ chỉ xem một khổ.
5. **Luôn tối ưu AEO / SEO / GEO / UX / UI** để đưa web lên **top Google Search và các bề
   mặt AI** (ChatGPT, Gemini, Perplexity, Google AI Overviews…) **nhanh nhất, sớm nhất**.
   Mỗi thay đổi nội dung/kỹ thuật đều cân nhắc góc này.

Giọng: xưng **"em"**, gọi **"Chú"**, tiếng Việt, gọn, thẳng, đi thẳng việc. Không xưng "tôi".
Dám phản biện khi có cái SAI THẬT (vai tỉnh táo viên), nhưng không tự ý đề xuất dừng dự án.

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
2. Không lôi tên/mặt/SĐT chủ ra giữa trang chủ. Liên hệ **chỉ ở footer** (chữ trầm) +
   trang `trao-doi`.
3. **"Im lặng mà sang"** — thẩm mỹ Aesop/Monocle/Stratechery: khoảng trắng rộng, tiết chế,
   không lòe loẹt, không màu nóng, không nhấp nháy.
4. **Palette CHỈ các biến này** (không thêm màu thứ hai ngoài clay):
   `--ink:#1a1815 · --paper:#f1ece2 · --card:#faf6ee · --forest:#2f4034 ·
   --forest-deep:#1e2a20 · --clay:#9d5d38 · --clay-soft:#bb8862 · --stone:#a79c87 ·
   --muted:#6e6759 · --line:#e1d9c8`
5. **Fonts CHỈ**: Fraunces (serif) + Be Vietnam Pro (sans). Không thêm font.
6. **Số liệu chính xác tuyệt đối** — sai một số là sập uy tín. Không chắc thì KHÔNG ghi,
   không đoán. Cần thì web-search kiểm.
7. **Số đang dùng (quyết định cuối)**: Đà Lạt **~23km**, sân bay Liên Khương **~20km**.
   KHÔNG dùng số cũ 27km/22km trừ khi Chú yêu cầu đổi lại.
8. **Dám nói "đừng mua"**. Xây trust bằng đọc rủi ro, không bán giấc mơ. Kết bài nhẹ, an
   yên — không hô "mua ngay".
9. Nút **"Chia sẻ"** trầm cuối bài = GIỮ (chuẩn tờ báo). Khác với CTA bán.

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
- **Animation phải có fallback**: khối `.reveal` ẩn tự hiện sau 2.5s nếu observer lỗi; hiện
  luôn nếu không JS (chỉ ẩn khi `<html class="js">`). Không để nội dung biến mất.
- **Ảnh chỉ dùng file trong `/images/`.** KHÔNG URL ảnh ngoài. Ảnh mới optimize <300KB
  (~quality 85), đặt vào `/images/`. File nặng/rác/0-tham-chiếu → xóa.
- Xong: `git add -A && git commit && git push origin main` → chờ Vercel → **báo link**.

### Ghi chú ảnh trang chủ (Chú đã chốt — giữ nguyên)
- 5 khối dưới hero có class `.reveal` (scroll-reveal fade-up, có fallback).
- Nút chat nổi `.fab-contact` (glass 44px, viền forest, góc phải dưới).
- **3 ảnh nhịp kích cỡ khác nhau (Kinfolk)**: desktop **360/440/600px**, mobile
  **230/280/370px** — KHÔNG đổi chiều cao này.
- Ảnh đèo Tà Nung (`deo-ta-nung.jpg` 1600×900) **có chữ in sẵn góc dưới-trái**
  ("ĐƯỜNG VỀ NAM BAN — Qua đèo Tà Nung") → dùng `object-position:left bottom` để không cắt
  chữ khi `cover` crop ở cả 2 khổ.

---

## 4. DEPLOY & MÔI TRƯỜNG

- Push `main` → Vercel tự build production `nambanpanorama.com`.
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

Đã có nền: `llms.txt`, `llms-full.txt`, `sitemap.xml`, `robots.txt`, `feed.xml`, JSON-LD
(Organization/Person/Place/WebSite/WebPage). Mỗi lần đụng nội dung, luôn cân nhắc:
- **AEO/GEO** (để AI trích dẫn): câu trả lời trực tiếp, dữ kiện rõ, JSON-LD đúng &
  `JSON.parse()` được, cập nhật `llms.txt`/`llms-full.txt` khi thêm bài, `dateModified` mới.
- **SEO**: title/description/canonical/OG/Twitter đủ; heading mạch lạc; internal link giữa
  các bài; ảnh có `alt` mô tả thật; `sitemap.xml` + `feed.xml` cập nhật khi thêm/xóa bài.
- **UX/UI**: tốc độ (ảnh optimize, `loading=lazy`), không CLS, không tràn ngang, chạm tốt
  trên mobile, contrast đạt. Ưu tiên trải nghiệm đọc "im lặng mà sang".
