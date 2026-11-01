# Chánh Điện LIVE — bản riêng cho kênh TikTok

Màn hình chánh điện 9:16 để phát TikTok LIVE. Người xem bình luận là được vào ngồi bồ đoàn. Ai tặng quà thì được xướng tên hồi hướng bằng giọng đọc tiếng Việt. Có nhạc thiền, chuông, mõ, tự đọc kinh định kỳ.

Dựa trên mã nguồn mở **Chánh Điện Online** của Kent Juno (giấy phép MIT, xem `LICENSE`): https://github.com/kentjuno/chanh-dien-online

## Bản riêng này khác bản gốc ở đâu

| Thêm | Để làm gì |
|---|---|
| Nút chạy một chạm `BAM-DE-CHAY-WINDOWS.bat` (Mac: `BAM-DE-CHAY-MAC.command`) | Tự kiểm Node.js, tự cài thư viện lần đầu, tự mở bảng điều khiển. Không phải gõ lệnh. |
| File `cau-hinh.json` tự lưu | Tên thiền đường, dòng phụ, giọng đọc, nhịp mõ, username kênh… sửa trên bảng điều khiển là lưu luôn. Tắt máy mở lại không mất. |
| Tự kết nối lại TikTok | Nhớ username kênh. Mở chương trình trước khi bật LIVE cũng được: cứ 60 giây nó thử vào phòng một lần, rớt mạng cũng tự vào lại. Bấm **Ngắt** thì dừng hẳn. |
| Lời giảng liên tục | Đọc lần lượt các bài trong thư mục `bai-giang` (12 bài soạn sẵn), có phụ đề trên màn hình. Quà luôn được đọc trước lời giảng. |
| Nhạc nền tự xếp danh sách | Mọi file `.mp3` bỏ vào `assets/music` tự vào danh sách, phát ngẫu nhiên. Chỉnh âm lượng, chuyển bài trên bảng điều khiển. |
| Sổ công đức theo ngày | Bảng Công Đức trên màn hình hiện 6 người dâng nhiều nhất trong ngày và 3 người vừa dâng. Bảng điều khiển hiện đủ danh sách. Lưu vào thư mục `cong-duc`, khởi động lại không mất. |
| Lọc từ bậy | Bình luận có từ chửi tục không hiện lên màn hình. Lời hồi hướng chỉ đọc bình luận có ý cầu nguyện, không đọc link hay số điện thoại. Thêm từ cấm trong `cau-hinh.json`, mục `tuCam`. |
| Dòng ghi công hiện rõ | Bản gốc giấu một dòng "Mã nguồn được chia sẻ bởi Kent Juno" hiện 7 giây mỗi 5–10 phút, viết bằng mã làm rối. Bản này viết lại cho rõ và có công tắc bật/tắt. |
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

## Nhạc nền

- Bỏ file `.mp3` vào thư mục `assets/music`. Khoảng 2 phút sau tự vào danh sách, hoặc bấm **Nạp lại bài giảng + nhạc**.
- Hai bài có sẵn do tác giả gốc làm bằng Gemini.
- **Không dùng bài hát Phật giáo đang thịnh hành tải trên mạng.** Các bài đó đều có bản quyền. TikTok quét âm thanh trên LIVE: phát nhạc không có quyền dễ bị tắt tiếng, dừng live, nặng thì khóa tài khoản. Thư viện nhạc của TikTok cũng không dùng được khi đang LIVE.
- Nhạc an toàn: nhạc chú tự làm hoặc đặt người làm, nhạc mua giấy phép có ghi rõ được phát trực tiếp, nhạc tự tạo bằng công cụ AI cho phép dùng thương mại.

## Lời giảng

- Mỗi file `.txt` trong thư mục `bai-giang` là một bài. Dòng đầu ghi `# Tên bài`. Các đoạn cách nhau một dòng trống.
- 12 bài có sẵn do Claude soạn theo giáo lý căn bản: Tứ Diệu Đế, Bát Chánh Đạo, Năm giới, Từ bi hỷ xả, Vô thường, Nhân quả, Chánh niệm hơi thở, Hiếu hạnh, Tham sân si, Công đức không nằm ở món quà, Nhẫn nhục, Tam Bảo. Một vòng đọc hết khoảng 25–30 phút rồi xáo thứ tự đọc lại.
- Muốn thêm bài: mở Notepad, gõ bài, lưu vào `bai-giang` với đuôi `.txt` và chọn mã **UTF-8**. Bấm **Nạp lại bài giảng + nhạc**.
- Giọng đọc là giọng máy. Không chép nguyên văn bài giảng của một vị thầy rồi cho máy đọc như của thầy: vừa vi phạm bản quyền, vừa dễ bị coi là mạo danh.

## Nhận quà của người xem

Code này **không đụng tới tiền**. Nó chỉ đọc tên người tặng và tên quà để xướng tên, ghi sổ công đức.

- Quà người xem tặng tự vào tài khoản TikTok của chú dưới dạng kim cương. Rút tiền làm trong ứng dụng TikTok, không qua chương trình này.
- Muốn nhận quà, tài khoản phải bật tính năng nhận quà LIVE. Điều kiện do TikTok đặt và đổi theo từng thời kỳ, ít nhất phải từ 18 tuổi. Xem điều kiện mới nhất ngay trong ứng dụng, thường nằm ở **Hồ sơ → ☰ → Công cụ dành cho nhà sáng tạo**.
- Đừng treo số tài khoản ngân hàng hay mã QR xin tiền trên màn hình live. Đừng nhân danh một ngôi chùa để kêu gọi đóng góp. Hai việc này dễ vi phạm luật lệ TikTok và quy định về quyên góp, hoạt động tôn giáo.

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

- Sổ công đức (`cong-duc/`) và `cau-hinh.json` có tên người xem, username kênh: không được đưa lên GitHub (đã chặn sẵn trong `.gitignore`).
- Server chỉ mở trên chính máy mình (`127.0.0.1`). Máy khác trong mạng không vào được.
- Trang web lạ đang mở cùng trình duyệt không điều khiển được (kiểm `Origin` và `Host`).
- Chỉ phục vụ thư mục `assets` và `live`. Mã server, `package.json`, `cau-hinh.json`, `.git` đều trả 404.
- Tên, bình luận của người xem bị cắt độ dài và chỉ hiện như chữ thường, không chạy được mã.

## Giấy phép

MIT. Giữ nguyên file `LICENSE` (ghi tên tác giả gốc Kent Juno) khi chia sẻ lại.

---

Ghi chú kỹ thuật: thư mục này tạm nằm trên nhánh `claude/chua-online-tiktok-bzmruf` của kho Namban Panorama. **Không gộp vào `main`**, vì `main` tự đăng lên nambanpanorama.com. Nên chuyển sang một kho GitHub riêng.
