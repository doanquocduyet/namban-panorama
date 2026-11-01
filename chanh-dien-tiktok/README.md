# Chánh Điện LIVE — bản riêng cho kênh TikTok

Màn hình chánh điện 9:16 để phát TikTok LIVE. Người xem bình luận là được vào ngồi bồ đoàn. Ai tặng quà thì được xướng tên hồi hướng bằng giọng đọc tiếng Việt. Có nhạc thiền, chuông, mõ, tự đọc kinh định kỳ.

Dựa trên mã nguồn mở **Chánh Điện Online** của Kent Juno (giấy phép MIT, xem `LICENSE`): https://github.com/kentjuno/chanh-dien-online

## Bản riêng này khác bản gốc ở đâu

| Thêm | Để làm gì |
|---|---|
| Nút chạy một chạm `BAM-DE-CHAY-WINDOWS.bat` (Mac: `BAM-DE-CHAY-MAC.command`) | Tự kiểm Node.js, tự cài thư viện lần đầu, tự mở bảng điều khiển. Không phải gõ lệnh. |
| File `cau-hinh.json` tự lưu | Tên thiền đường, dòng phụ, giọng đọc, nhịp mõ, username kênh… sửa trên bảng điều khiển là lưu luôn. Tắt máy mở lại không mất. |
| Tự kết nối lại TikTok | Nhớ username kênh. Mở chương trình trước khi bật LIVE cũng được: cứ 60 giây nó thử vào phòng một lần, rớt mạng cũng tự vào lại. Bấm **Ngắt** thì dừng hẳn. |
| Tên mặc định "Thiền Đường An Nhiên" | Khác bản gốc "Chánh Điện Tịnh Tâm" mà nhiều kênh đang dùng. Đổi tên thì gõ ở ô **Tên thiền đường** trên bảng điều khiển. |

`cau-hinh.mau.json` là bản mẫu. Chương trình tự tạo `cau-hinh.json` lần đầu bấm lưu. File này không bị đưa lên GitHub và không mở ra ngoài mạng.

## Cài và chạy trên Windows (làm một lần)

1. **Cài Node.js.** Vào https://nodejs.org/en/download → bấm nút tải bản **LTS** cho Windows → mở file vừa tải → bấm **Next** liên tục → **Install** → **Finish**.
2. **Tải bộ này về máy.** Giải nén ra một thư mục dễ tìm, ví dụ `D:\chanh-dien-tiktok`.
3. **Bấm đúp `BAM-DE-CHAY-WINDOWS.bat`.** Windows có thể hiện khung xanh "Windows protected your PC" → bấm **More info** → **Run anyway**.
4. Lần đầu sẽ thấy cửa sổ đen chạy chữ 1–2 phút (đang cài thư viện). Xong thì trình duyệt tự mở **Bảng điều khiển**.
5. **Không tắt cửa sổ đen** trong lúc live. Tắt nó là tắt chương trình.

Từ lần sau chỉ cần bấm đúp `BAM-DE-CHAY-WINDOWS.bat`.

## Lên sóng TikTok LIVE

1. Trên **Bảng điều khiển**, bấm **Mở màn hình overlay 9:16**. Một cửa sổ dọc hiện ra.
2. Trong cửa sổ dọc đó, bấm nút **Bấm để bật âm thanh** một lần (trình duyệt chặn tự phát tiếng).
3. Mở **TikTok LIVE Studio** → **Add source** (Thêm nguồn) → **Window capture** (Chụp cửa sổ) → chọn cửa sổ có chữ "Overlay 9:16". Kéo cho vừa khung dọc.
   - Dùng OBS thì chọn **Browser source**, URL `http://localhost:3000/live/overlay.html`, rộng 1080, cao 1920.
4. Trong LIVE Studio, chọn âm thanh để người xem nghe được tiếng của trình duyệt (nhạc, mõ, giọng đọc).
5. Bấm **Go LIVE** trên TikTok.
6. Quay lại **Bảng điều khiển**, ô **Username kênh đang live** gõ `@tenkenhcuachu` → bấm **Kết nối**. Thấy chữ xanh `TikTok: @… ✓` là xong. Username được nhớ, lần sau tự vào.

Chưa live vẫn thử được: mục **Thử tương tác**, **Đổ người mẫu**, **Bot mô phỏng**. Bot chỉ hiện trên máy mình, không phải người xem thật.

## Làm cho kênh của mình khác các kênh khác

Mã này được chia sẻ công khai nên sẽ có nhiều kênh dùng y hệt hình. Ba chỗ nên đổi:

1. **Tên thiền đường và dòng phụ**: gõ trên bảng điều khiển, mục **Cảnh**.
2. **Ảnh nền**: thay file `assets/hall.jpg` bằng ảnh của mình, đúng cỡ **1080 × 1920** (dọc), giữ nguyên tên file. Bàn thờ nên nằm khoảng giữa ảnh vì người ngồi được xếp ở nửa dưới.
3. **Giọng đọc**: chọn Nam Minh (nam) hoặc Hoài My (nữ), chỉnh độ trầm và tốc độ trong mục **Giọng đọc**.

## Người xem làm được gì

- **Bình luận bất kỳ**: vào ngồi bồ đoàn (tối đa 100 chỗ, tự mở rộng 24 → 36 → 64 → 100). Đầy chỗ thì người im lâu nhất mà chưa tặng quà nhường chỗ.
- **Bình luận đúng một từ** `nam`, `nữ`, `sư`, `ni`, `tiểu`, `bà`, `cao tăng`: đổi hình nhân vật.
- **Tặng quà**: banner xướng tên, giọng đọc hồi hướng (lấy lời nguyện từ bình luận gần nhất), cộng điểm vào bảng Công Đức.
- **Thả tim**: tim bay trên đầu nhân vật.

## Lưu ý trước khi dùng

- `tiktok-live-connector` là thư viện cộng đồng, **không phải công cụ chính thức của TikTok**. TikTok đổi hệ thống thì nó có thể ngừng chạy. Nó chỉ đọc sự kiện công khai của phòng live, không cần mật khẩu, không đăng nhập thay mình.
- Giọng đọc dùng dịch vụ đọc của Microsoft Edge qua mạng. Máy phát cần Internet.
- Hình trong `assets/` tác giả gốc làm bằng Google Flow, nhạc nền bằng Gemini. Muốn nhận quà, kiếm tiền thì nên thay bằng hình, nhạc của mình.
- Nội dung liên quan Phật giáo: giữ sự tôn kính, không dùng vào việc lừa đảo, trục lợi. Người phát tự chịu trách nhiệm về nội dung, quà tặng và việc tuân thủ điều khoản TikTok, pháp luật Việt Nam (xem phần miễn trừ của tác giả gốc trong `LICENSE` và kho gốc).

## Bảo mật (giữ nguyên từ bản gốc)

- Server chỉ mở trên chính máy mình (`127.0.0.1`). Máy khác trong mạng không vào được.
- Trang web lạ đang mở cùng trình duyệt không điều khiển được (kiểm `Origin` và `Host`).
- Chỉ phục vụ thư mục `assets` và `live`. Mã server, `package.json`, `cau-hinh.json`, `.git` đều trả 404.
- Tên, bình luận của người xem bị cắt độ dài và chỉ hiện như chữ thường, không chạy được mã.

## Giấy phép

MIT. Giữ nguyên file `LICENSE` (ghi tên tác giả gốc Kent Juno) khi chia sẻ lại.

---

Ghi chú kỹ thuật: thư mục này tạm nằm trên nhánh `claude/chua-online-tiktok-bzmruf` của kho Namban Panorama. **Không gộp vào `main`**, vì `main` tự đăng lên nambanpanorama.com. Nên chuyển sang một kho GitHub riêng.
