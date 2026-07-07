# PHIẾU CHỈ THỊ TỔNG — CLAUDE CODE
## Repo: Panorama (nambanpanorama.com)
## Người giao: ô Content (thay Chú D). Làm xong commit + push, báo link lại.

────────────────────────────────────────
## PHẦN 0 — NGUYÊN TẮC AN TOÀN (đọc trước)
────────────────────────────────────────
- Sửa file: str_replace EXACT, KHÔNG regex DOTALL.
- Không đụng nội dung/schema/layout ngoài đúng dòng được chỉ.
- Trước push mỗi file: kiểm div mở/đóng cân, braces CSS cân, JSON-LD parse được, WCAG ≥4.5 (số/giá không gold-trên-trắng).
- Slug đặt đúng tuyệt đối (case-sensitive, có gạch).
- File nguồn 15 bài HTML: nằm cùng thư mục phiếu này (thư mục PANORAMA-DANG trong outputs). Thiếu file nào → dừng, báo, KHÔNG tự chế nội dung.
- QA screenshot thật desktop + mobile 1 bài mỗi ngôn ngữ.

────────────────────────────────────────
## PHẦN 1 — SỬA 2 BÀI ĐÃ LIVE (chỉ đổi footer)
────────────────────────────────────────
2 bài ĐÃ live, KHÔNG đăng lại. Chỉ thay chữ trong dòng footer.
File trên repo: `sap-nhap-nam-ban-dat` và `nam-ban-thuoc-xa-nao`.
Tìm `<div class="foot-note">...</div>`, thay chữ bên trong thành:
```
Đất Nam Ban, vùng ven Đà Lạt — hiểu vùng đất trước khi hiểu giá đất.
```
Giữ nguyên thẻ + class. Chỉ đổi chữ. Không đụng gì khác.

────────────────────────────────────────
## PHẦN 2 — SỬA BÀI ANH ĐÃ LIVE "living-in-nam-ban" (4 việc)
────────────────────────────────────────
Bài `living-in-nam-ban` ĐÃ live. Sửa 4 chỗ, KHÔNG đăng lại:

**2.1 — SAI ĐƠN VỊ HÀNH CHÍNH (quan trọng nhất).**
Bài đang ghi "Lam Ha District" / "huyện Lâm Hà". SAI — từ 1/7/2025 bỏ cấp huyện.
Thay MỌI chỗ "Lam Ha District" → "Nam Ban Lam Ha commune" (và nếu có "District" đứng cạnh Lam Ha ở chỗ khác cũng sửa). Có ở ~3 chỗ: thân bài, đoạn "Where is Nam Ban", và FAQ. Đọc kỹ từng chỗ, chỉ sửa khi nói đơn vị hành chính hiện tại.

**2.2 — SAI KHOẢNG CÁCH.**
Bài ghi "25–30 km from Da Lat". Thay thành "about 27 km from Da Lat" (khớp chuẩn toàn hệ thống). Sửa cả trong FAQ nếu có.

**2.3 — CHÈN HREFLANG** (nối bộ đa ngữ). Trong `<head>`, nếu có `<link rel="canonical">` thì chèn ngay sau; nếu chưa có thì chèn cả canonical:
```html
<link rel="canonical" href="https://nambanpanorama.com/living-in-nam-ban">
<link rel="alternate" hreflang="en" href="https://nambanpanorama.com/living-in-nam-ban">
<link rel="alternate" hreflang="vi" href="https://nambanpanorama.com/nam-ban-co-dang-song">
<link rel="alternate" hreflang="fr" href="https://nambanpanorama.com/fr/vivre-a-nam-ban">
<link rel="alternate" hreflang="zh-Hans" href="https://nambanpanorama.com/zh/zai-nam-ban-shenghuo">
<link rel="alternate" hreflang="ko" href="https://nambanpanorama.com/ko/nam-ban-salm">
<link rel="alternate" hreflang="ja" href="https://nambanpanorama.com/ja/nam-ban-kurashi">
<link rel="alternate" hreflang="x-default" href="https://nambanpanorama.com/living-in-nam-ban">
```
Nếu đã có hreflang lẻ → thay hết bằng khối 8 dòng trên. Không nhân đôi canonical.

**2.4 — SLOGAN FOOTER.** Tìm footer, thay chữ thành:
```
Nam Ban, Da Lat highlands — understand the land before you hear the price.
```

────────────────────────────────────────
## PHẦN 3 — ĐĂNG 15 BÀI MỚI
────────────────────────────────────────
Thêm 15 file HTML mới theo đúng slug. Footer các file này ĐÃ có slogan chuẩn — không sửa.

### 3A. Panorama Việt (4 bài)
| File nguồn | Slug |
|---|---|
| dieu-de-lai-cho-con.html | `/dieu-de-lai-cho-con` |
| mua-bo-nam-ban.html | `/mua-bo-nam-ban` |
| vuon-bo-loi-bao-nhieu.html | `/vuon-bo-loi-bao-nhieu` |
| nam-ban-hay-di-linh.html | `/nam-ban-hay-di-linh` |

### 3B. Cụm "Sống ở Nam Ban" (5 bài — bản Anh đã live ở Phần 2)
| File nguồn | Slug |
|---|---|
| vi-nam-ban-co-dang-song.html | `/nam-ban-co-dang-song` |
| fr-vivre-a-nam-ban.html | `/fr/vivre-a-nam-ban` |
| zh-zai-nam-ban-shenghuo.html | `/zh/zai-nam-ban-shenghuo` |
| ko-nam-ban-salm.html | `/ko/nam-ban-salm` |
| ja-nam-ban-kurashi.html | `/ja/nam-ban-kurashi` |

### 3C. Cụm "Thác Voi" (6 bài)
| File nguồn | Slug |
|---|---|
| vi-thac-voi-nam-ban.html | `/thac-voi-nam-ban` |
| en-elephant-waterfall-nam-ban.html | `/elephant-waterfall-nam-ban` |
| fr-cascade-des-elephants-nam-ban.html | `/fr/cascade-des-elephants-nam-ban` |
| zh-nam-ban-daxiang-pubu.html | `/zh/nam-ban-daxiang-pubu` |
| ko-nam-ban-kokkiri-pokpo.html | `/ko/nam-ban-kokkiri-pokpo` |
| ja-nam-ban-zou-no-taki.html | `/ja/nam-ban-zou-no-taki` |

────────────────────────────────────────
## PHẦN 4 — SITEMAP (để Google tìm hết)
────────────────────────────────────────
Cập nhật sitemap.xml: thêm 15 slug mới ở Phần 3 + 5 slug đã sửa/live (living-in-nam-ban, sap-nhap-nam-ban-dat, nam-ban-thuoc-xa-nao). TẤT CẢ bài đều index (không noindex bài nào). Ping Google Search Console nếu có quyền.

────────────────────────────────────────
## PHẦN 5 — MENU ĐIỀU HƯỚNG 2 TẦNG (chống rối)
────────────────────────────────────────
QUAN TRỌNG: KHÔNG nhồi hết 20 bài lên menu. Chia 2 tầng:

**TẦNG 1 — Lên menu chính (giữ gọn 5-6 mục, đúng gu tối giản):**
- Sống ở Nam Ban (`/nam-ban-co-dang-song`)
- Giá đất (`/namban-index`)
- Quy hoạch (`/quy-hoach` hoặc trang quy hoạch hiện có)
- Sáp nhập & vùng đất (`/sap-nhap-nam-ban-dat`)
- Trao đổi (`/trao-doi`)

**TẦNG 2 — KHÔNG lên menu, vẫn index + vào từ search/link nội bộ:**
- 12 bài đa ngữ (thác Voi + sống các tiếng nước ngoài): người nước ngoài vào từ Google, KHÔNG bày lên menu tiếng Việt. Chỉ nối nhau qua hreflang + nút chuyển ngôn ngữ trong bài.
- Bài bơ, "điều để lại", "Nam Ban vs Di Linh": vào từ search + khối "Đọc tiếp" cuối bài khác.

**LIÊN KẾT NỘI BỘ (giữ người trong phễu):** mỗi bài Việt có khối "Đọc tiếp" trỏ 1-2 bài Việt liên quan. Cụm thác Voi mỗi bản trỏ bản "sống" cùng tiếng (đã có sẵn trong file). KHÔNG cross-link lộn xộn tất cả với tất cả.

**Trang chủ:** nếu có khu "bài mới/nổi bật", đưa 3-4 bài trụ tiếng Việt. Bài ngoại KHÔNG lên trang chủ tiếng Việt.

────────────────────────────────────────
## PHẦN 6 — KIỂM TRA SAU (bắt buộc trước khi báo xong)
────────────────────────────────────────
- 15 slug mới mở được, không 404, không vỡ layout (mobile + desktop).
- Bài Anh living: "District" đã hết, khoảng cách = 27km, đúng 1 canonical + 7 alternate, footer slogan Anh.
- 2 bài live kia: footer đã đổi, phần còn lại nguyên.
- Mỗi cụm đa ngữ: mở 1 bản, hreflang trỏ đúng các bản kia.
- Menu chính: đúng 5-6 mục, KHÔNG tràn bài ngoại.
- Báo lại: tổng trang thêm/sửa + link 3 bài bất kỳ để ô Content check.

KHÔNG dùng file `fr-vivre-hauts-plateaux-nam-ban.html` (bản Pháp cũ, bỏ).
