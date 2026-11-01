# Chánh Điện LIVE — bản riêng cho kênh TikTok

Màn hình chánh điện 9:16 để phát TikTok LIVE. Người xem bình luận là được vào ngồi bồ đoàn. Ai tặng quà thì được xướng tên hồi hướng bằng giọng đọc tiếng Việt. Có nhạc thiền, chuông, mõ, tự đọc kinh định kỳ.

Dựa trên mã nguồn mở **Chánh Điện Online** của Kent Juno (giấy phép MIT, xem `LICENSE`): https://github.com/kentjuno/chanh-dien-online

## Bản riêng này khác bản gốc ở đâu

| Thêm | Để làm gì |
|---|---|
| Nút chạy một chạm `BAM-DE-CHAY-WINDOWS.bat` (Mac: `BAM-DE-CHAY-MAC.command`) | Tự kiểm Node.js, tự cài thư viện lần đầu, tự mở bảng điều khiển. Không phải gõ lệnh. |
| Nút cập nhật `CAP-NHAT-WINDOWS.bat` | Bấm một lần là lấy bản sửa mới nhất từ GitHub, không mất cấu hình, sổ công đức, ảnh và bài giảng của chú. |
| Cửa sổ live dọc mở sẵn | Nút chạy tự mở cửa sổ live bằng Edge: tự phát tiếng, không bị Windows làm chậm khi bị che. |
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
4. Lần đầu sẽ thấy cửa sổ đen chạy chữ 1–2 phút (đang cài thư viện).
5. Xong thì tự mở **hai cửa sổ**: Bảng điều khiển (trình duyệt thường) và **cửa sổ live dọc** (Microsoft Edge, tiêu đề "Overlay 9:16 · Chánh Điện LIVE"). Cửa sổ dọc tự phát tiếng, không cần bấm gì.
6. **Không tắt cửa sổ đen** trong lúc live. Tắt nó là tắt chương trình.

Từ lần sau chỉ cần bấm đúp `BAM-DE-CHAY-WINDOWS.bat`.

## Lên sóng TikTok LIVE

**Trước hết, tài khoản phải được phép LIVE từ máy tính.** Điều kiện do TikTok đặt (tuổi, số người theo dõi…) và mỗi nguồn nói một số khác nhau. Cách chắc nhất: tải TikTok LIVE Studio, đăng nhập, nó báo ngay tài khoản có dùng được không.

**Bước 1 · Cài TikTok LIVE Studio (làm một lần)**
1. Vào https://www.tiktok.com/studio/download → bấm **Tải xuống cho Windows**. Chỉ tải từ trang của TikTok.
2. Mở file vừa tải → cài như phần mềm thường.
3. Mở TikTok LIVE Studio → **Đăng nhập** bằng tài khoản TikTok của kênh (quét mã QR bằng điện thoại: ứng dụng TikTok → ô tìm kiếm có biểu tượng quét, hoặc **Hồ sơ → ☰ → Quét mã**).
4. Nếu LIVE Studio báo tài khoản chưa đủ điều kiện, dừng ở đây: phải nuôi kênh tới khi TikTok mở quyền.

**Bước 2 · Đưa chánh điện vào khung live (làm một lần, LIVE Studio tự nhớ)**
1. Bấm đúp `BAM-DE-CHAY-WINDOWS.bat`, chờ cửa sổ live dọc hiện ra. **Đừng thu nhỏ cửa sổ này** (được phép để nó nằm sau cửa sổ khác).
2. Trong LIVE Studio, chuyển khung hình sang **Dọc** (nút đổi hướng ngay trên khung xem trước).
3. Bấm **Thêm nguồn** (Add source) → **Chụp cửa sổ** (Window capture) → chọn cửa sổ **Overlay 9:16 · Chánh Điện LIVE** → **Xác nhận**.
4. Kéo các góc khung cho phủ kín khung dọc.
5. Nếu khung chỉ thấy màu đen: xóa nguồn đó, thêm lại bằng **Chụp màn hình** (Display capture) rồi cắt lấy vùng cửa sổ dọc.
6. Âm thanh: trong phần âm thanh của LIVE Studio, bật **âm thanh máy tính / hệ thống** (Desktop audio) để người xem nghe nhạc, mõ, lời giảng. Tắt micro nếu không nói.

**Bước 3 · Lên sóng (mỗi lần live)**
1. Bấm đúp `BAM-DE-CHAY-WINDOWS.bat`.
2. Mở TikTok LIVE Studio → gõ tiêu đề live, ví dụ "Tụng kinh an yên mỗi tối · bình luận để vào thiền" → chọn chủ đề → bấm **Phát LIVE** (Go LIVE).
3. Trên Bảng điều khiển, ô **Username kênh đang live** gõ `@tenkenhcuachu` → bấm **Kết nối**. Thấy chữ xanh `TikTok: @… ✓` là xong. Lần sau nó tự kết nối, không phải gõ lại.
4. Dùng điện thoại khác vào live của chính mình, bình luận "nam" để thấy mình vào ngồi. Có tiếng, có người vào là chạy đúng.
5. Kết thúc: bấm **Kết thúc LIVE** trong LIVE Studio, rồi tắt cửa sổ đen.

Chưa live vẫn thử được: mục **Thử tương tác**, **Đổ người mẫu**, **Bot mô phỏng**. Bot chỉ hiện trên máy mình, không phải người xem thật.

**Đừng để live chạy một mình suốt đêm.** Các hướng dẫn về TikTok LIVE đều cho thấy TikTok hạn chế đề xuất, có khi chặn kiếm tiền, với live chỉ có màn hình chạy sẵn, giọng máy, không người thật tương tác. Nên có người ngồi live: bật micro chào người mới vào, đọc lời nguyện của người tặng quà, hoặc gắn thêm một camera nhỏ quay tay gõ mõ.

## Cập nhật bản mới

Mỗi khi Claude sửa xong và báo "đã cập nhật":
1. Tắt cửa sổ đen nếu đang chạy.
2. Bấm đúp `CAP-NHAT-WINDOWS.bat` → bấm phím bất kỳ → chờ chữ "Xong".
3. Bấm đúp `BAM-DE-CHAY-WINDOWS.bat` để chạy lại.

Nút cập nhật luôn thay file chương trình bằng bản mới. Nó **không đụng** tới `cau-hinh.json`, sổ công đức, nhạc chú tự thêm. Ảnh, nhạc và bài giảng đã có trên máy thì giữ nguyên (chú sửa `hall.jpg` hay một bài giảng thì không bị ghi đè). GitHub cần khoảng 5 phút để có bản mới, cập nhật sớm quá thì bấm lại.

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

Ghi chú kỹ thuật: thêm hoặc bớt file thì chạy `python3 tao-cap-nhat.py` để làm mới `cap-nhat.txt` (danh sách cho nút cập nhật) rồi commit. Thư mục này tạm nằm trên nhánh `claude/chua-online-tiktok-bzmruf` của kho Namban Panorama. **Không gộp vào `main`**, vì `main` tự đăng lên nambanpanorama.com. Nên chuyển sang một kho GitHub riêng.
