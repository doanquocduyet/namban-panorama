# Quy trình xuất bản Namban Panorama

Mục tiêu: khi có dữ kiện mới về Nam Ban, Panorama là **nguồn đầu tiên** đăng —
với dữ liệu gốc (ảnh tự chụp, số từ văn bản, tọa độ), có cấu trúc để cả người,
Google và AI đều dùng được.

Đây không phải "SEO". Đây là một dây chuyền xuất bản. Nhanh + gốc + có cấu trúc
= được ưu tiên trích dẫn.

---

## Nguyên tắc lọc (áp cho mọi thứ thêm vào site)

> Không thêm thành phần nào nếu nó không phục vụ **đồng thời ít nhất 2 trong 3**:
> **người đọc · Google · AI.**

Ví dụ đạt: Data Layer (Google + AI) · Fact Box (người đọc + AI) · Citation/nguồn
(người đọc + AI) · Timeline (người đọc + Google).
Ví dụ trượt (nên bỏ): `ai-feed.json` tự chế (chỉ "AI", chưa nền tảng nào cam kết
đọc) · video sitemap khi chưa có video · trang `/entity/` trùng bài đã có.

---

## Mục tiêu tốc độ (khi có sự kiện thật)

| Từ sự kiện đến… | Đích | Ai làm |
|---|---|---|
| Bài xuất bản (push `main`) | < 60 phút | Claude/Chú |
| Crawler thấy (IndexNow ping Bing/Yandex) | tự động khi push | GitHub Action |
| RSS `feed.xml` cập nhật | tự động khi push | GitHub Action |
| Google index (Request Indexing trong GSC) | < 30 phút sau push | **Chú** (thủ công) |
| Đăng Facebook page + group | < 60 phút | **Chú** |

Báo chí thường đăng sau vài tiếng. Nếu Panorama đăng trong giờ đầu, có ảnh thật
và số từ văn bản, thì thành nguồn gốc — thứ Google và AI ưu tiên.

---

## Checklist đăng 1 bài mới

**1. Nội dung (dùng `_mau-bai-viet.html` nếu không có Claude Code)**
- [ ] Từ khóa chính người ta thật sự search → vào title / description / H1 / H2 / alt
- [ ] Số liệu lấy từ văn bản/khảo sát thật. Không chắc thì **không ghi**
- [ ] Khối "Trả lời nhanh" (`.tldr`) ở đầu — câu trả lời trực tiếp cho AI trích
- [ ] Ảnh tự chụp bỏ vào `/images/`, optimize < 300KB, `alt` mô tả thật
- [ ] Có lối vào phễu: link bài liên quan → hub → Trao đổi

**2. Schema (máy đọc)**
- [ ] JSON-LD Article/NewsArticle + FAQ (khớp word-for-word phần hiển thị)
- [ ] Speakable trỏ `.tldr` + `h1`
- [ ] Place + GeoCoordinates nếu bài về địa danh/cầu/thác/chùa
- [ ] ImageObject (creator, copyright, dateCreated, contentLocation) cho ảnh gốc
- [ ] Nguồn (`.source-box`) cuối bài: số văn bản, ngày, "khảo sát Panorama ngày…"

**3. Data Layer (nếu bài có dữ kiện tái dùng được)**
- [ ] Thêm/cập nhật `/data/*.json` — địa danh → `places.json`, hạ tầng →
      `infrastructure.json`, giá → `prices.json` (thêm `period` mới, **không ghi đè**),
      mốc thời gian → `timeline.json`
- [ ] Số trong bài khớp 100% với số trong data file

**4. Discovery (được tìm thấy)**
- [ ] `sitemap.xml`: thêm entry + `lastmod`
- [ ] `image-sitemap.xml`: thêm ảnh mới (nếu có)
- [ ] `llms.txt` + `llms-full.txt`: thêm link + (nếu là dữ kiện lớn) 1 dòng số thật
- [ ] `dateModified` mới ở JSON-LD **chỉ khi nội dung đổi thật** (không freshness giả)

**5. Kiểm tra trước push**
- [ ] JSON-LD `JSON.parse()` được; CSS `{`=`}`; tag mở=đóng
- [ ] Playwright QA 1440 + 390 (+ 1920): không tràn ngang, contrast ≥ 4.5
- [ ] `git add -A && git commit && git push origin HEAD:main`

**6. Sau push (việc Chú — quyết định tốc độ)**
- [ ] GSC → Kiểm tra URL → dán link bài mới → **Yêu cầu lập chỉ mục**
- [ ] Đăng Facebook page + 1–2 group liên quan (Nam Ban / Lâm Hà / Đà Lạt)

---

## Việc thiết lập một lần (Chú làm, chưa xong thì vẫn còn giá trị)

- [ ] **Google Search Console**: submit `sitemap.xml` + `image-sitemap.xml`
- [ ] **Bing Webmaster Tools**: import từ GSC (1 click) → nuôi ChatGPT Search + Copilot
- [ ] Facebook page Panorama có mô tả + link web (tín hiệu thực thể/brand)

---

## Dữ liệu mở hiện có (máy đọc được, cho AI + tái dùng)

- `/data/prices.json` · `/data/prices.csv` — giá đất theo phân khúc, có version theo tháng
- `/data/infrastructure.json` — cầu, sân bay, đường
- `/data/places.json` — địa danh + tọa độ + alias đa ngôn ngữ
- `/data/timeline.json` — mốc hành chính & hạ tầng

Header `/data/*` đã mở CORS (`Access-Control-Allow-Origin: *`) — bất kỳ công cụ/AI
nào cũng lấy được. Trích dẫn ghi nguồn Namban Panorama.
