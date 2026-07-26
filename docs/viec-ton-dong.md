# Việc tồn đọng — Namban Panorama

Ghi để phiên sau KHỎI rà lại toàn site (tiết kiệm token/time). Rà lần cuối: 26/7/2026.
Làm xong mục nào thì xoá mục đó khỏi đây.

---

## 1. 15 bài thiếu `og:image` (thẻ chia sẻ Facebook/Zalo trống) — Chú CHỐT "để đó, chưa làm"

Ảnh hưởng phễu: share link lên Zalo/FB không có ảnh → ít người bấm.
23 bài thiếu `twitter:image` song song. 8 bài còn dòng `<!-- TODO: og:image -->` để lại — làm xong thì gỡ.

**Nhóm A — 11 bài ĐÃ có ảnh hero (thêm og được ngay, cơ học):**

| Bài | Ảnh hero dùng làm og |
|---|---|
| ca-phe-nam-ban | ca-phe-nam-ban.webp |
| mua-ca-phe-nam-ban | ca-phe-trai-chin.webp |
| tour-ca-phe-nam-ban | quan-ca-phe-nam-ban.webp |
| doc-the-dat-nam-ban | do-dat-giu-ranh.webp |
| khu-nao-o-nam-ban | nam-ban-thung-lung.jpg |
| chuyen-len-nam-ban-song | duong-doi-view-thung-lung.jpg |
| homestay-nam-ban-co-lai-khong | villa-khung-go-rung-thong.jpg |
| mua-bo-nam-ban | mua-bo-thu-hoach.jpg |
| mua-dat-co-vuon-ca-phe | nam-ban-thung-lung.jpg |
| mua-dat-duong-gia-nam-ban | me-linh-rung-thong-duong-dat.webp |
| mua-vuon-ca-phe-nam-ban | gia-lam-ca-phe-chin.webp |

**Nhóm B — 4 bài CHƯA có ảnh nào (phải chọn ảnh trước rồi mới thêm og):**
`ban-dat-nam-ban` · `len-tho-cu-het-bao-nhieu-tien` · `mua-dat-co-vuon-bo` · `vua-mua-dat-nam-ban-lam-gi`

**Điểm cần Chú quyết khi làm:** vài ảnh nhóm A là `.webp`, chuẩn site là `og:image=.jpg` (56 trang).
→ Hoặc (a) dùng thẳng webp làm og (gọn, Zalo/FB nay đọc được), hoặc (b) tạo bản `.jpg` riêng cho og.

---

## 2. ~10 bài chưa có audio giọng NAM

53/63 bài đã có nút nghe giọng thật (MP3 trong `/audio/` + `<meta name="pm-audio">`).
CLAUDE.md chốt: bài mới mặc định giọng nam. ~10 bài cũ còn dùng giọng máy (fallback).
→ Cần Chú chạy ElevenLabs tạo MP3 (giọng thật), Claude không tạo MP3 thay được.
Thêm giọng cho 1 bài = bỏ MP3 vào `/audio/<slug>.mp3` + thêm 1 dòng `<meta name="pm-audio" content="/audio/<slug>.mp3">`.
