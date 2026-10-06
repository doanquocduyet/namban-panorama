# Video nền trang chủ

Thả đúng **một** file tên `hero.mp4` vào thư mục này là trang chủ tự bật video nền.
Không có file → trang giữ nguyên như hiện tại, không lỗi.

## Yêu cầu file

| | |
|---|---|
| Tên file | `hero.mp4` (đúng tên, chữ thường) |
| Dung lượng | **≤ 3 MB** — quá nặng sẽ hại tốc độ và thứ hạng Google |
| Độ dài | **8–12 giây**, cắt sao cho lặp lại không thấy điểm nối |
| Khung hình | 1920×1080 (16:9), 24–30 fps |
| Âm thanh | **XOÁ HẲN** — video tự chạy nên bắt buộc không tiếng |

## Quay thế nào cho đúng tông Panorama

Nguyên tắc: **một cú máy, gần như đứng yên.** Không zoom, không cắt cảnh, không lia nhanh.
Người xem phải cảm thấy "đang nhìn ra cửa sổ", không phải "đang xem quảng cáo".

Nên quay:
- Sương trôi qua đồi cà phê (đặt điện thoại lên chỗ cố định, quay 30 giây, cắt lấy 10 giây đẹp nhất)
- Mặt hồ Bãi Công gợn nhẹ lúc chiều
- Lá cà phê lay trong gió, hậu cảnh là thung lũng
- Mây chạy trên dãy núi nhìn từ đài ngắm

Tránh: người đi lại, xe chạy, cảnh có dây điện hoặc cột đèn, cảnh cắt nhanh, bất cứ thứ gì nhấp nháy.

## Xuất file nhẹ

Nếu có ffmpeg trên máy:

```
ffmpeg -i goc.mp4 -t 10 -an -vf "scale=1920:-2" -c:v libx264 -crf 30 -preset slow -movflags +faststart hero.mp4
```

- `-an` xoá tiếng · `-crf 30` nén mạnh · `-movflags +faststart` cho video chạy ngay khi chưa tải xong
- Xuất xong kiểm dung lượng; còn trên 3 MB thì tăng `-crf` lên 32 rồi xuất lại

Không có ffmpeg: dùng CapCut hoặc VN Video Editor trên điện thoại — cắt 10 giây, tắt tiếng,
xuất 1080p, rồi nén qua trang freeconvert.com/video-compressor về dưới 3 MB.

## Khi nào video KHÔNG chạy (cố ý)

- Trên điện thoại → dùng bản tĩnh, không tốn dung lượng mạng của người đọc
- Máy bật chế độ giảm chuyển động
- Mạng 2G hoặc đang bật tiết kiệm dữ liệu

## Muốn video hiện RÕ thay vì mờ sau lớp giấy

Mặc định video nằm mờ phía sau, chữ giữ màu tối — hợp tông trầm.
Muốn video nổi hẳn, chữ chuyển trắng: sửa `index.html`, đổi `<header>` thành `<header class="video-bold">`.

## Bản điện thoại `hero-m.mp4` (6/10/2026)

Điện thoại (≤ 440px) tải `hero-m.mp4` thay cho `hero.mp4`: cắt sẵn 1344×1080 ở giữa (bỏ hai bên vốn không bao giờ lọt
khung hero dọc), thu về 672×540, H.264 CRF 27, không tiếng — **~0,7 MB thay vì 3 MB**. Khung nhìn y hệt bản gốc (tính
bằng hình học object-fit:cover; khung hero ≤ 440px có tỷ lệ rộng/cao ≤ 1,24). Video chỉ tải sau sự kiện `load` của
trang. Thay `hero.mp4` thì làm lại bản này:

    ffmpeg -i hero.mp4 -an -vf "crop=1344:1080:288:0,scale=672:540:flags=lanczos" -c:v libx264 -preset veryslow \
      -crf 27 -profile:v high -pix_fmt yuv420p -movflags +faststart hero-m.mp4
