# Facebook cho Panorama — bộ vận hành

Bản dựng 9/9/2026. Chuyển bộ 7 prompt Chú đưa sang chất liệu Panorama.

**Trang: [facebook.com/nambanpanorama](https://facebook.com/nambanpanorama)**

Đăng tự động đã dựng xong: `tools/fb-post.py` + `.github/workflows/fb-post.yml`,
hàng đợi ở `data/fb-queue.json`. Chạy trên runner GitHub (phiên Claude bị chặn
`graph.facebook.com`). **Chỉ cần một secret `FB_PAGE_TOKEN`** — page token tự gắn
với đúng một Trang nên script hỏi `GET /me` ra Page ID, rồi đối chiếu username với
`nambanpanorama`; lệch thì dừng, không đăng. Chốt này có thật vì Chú quản ba Trang
(Panorama · Villas · Greenspacers), bấm nhầm ở bước lấy token là bài Panorama rơi
lên tường Trang bán đất. Chưa cấp token thì workflow chạy khô, in bài ra, thoát sạch.

Đọc `CLAUDE.md` §2 trước khi viết bất cứ dòng nào lên Facebook. Trang Facebook là
**cánh tay của publication**, không phải kênh bán. Người ta đọc xong phải thấy
"chỗ này biết chuyện", không phải "chỗ này đang gạ mình".

---

## 0-A. LẤY `FB_PAGE_TOKEN` — HƯỚNG DẪN TỪNG NÚT CHO CHÚ

Đây là **việc duy nhất Chú phải tự tay làm**. Làm một lần, xong là hệ thống tự chạy.
Mất khoảng 15 phút. Không cần cài gì, không cần trả tiền.

**Trước khi bắt đầu, kiểm một chuyện:** Chú phải là **Quản trị viên (Admin)** của
Trang `facebook.com/nambanpanorama`. Vào Trang → nếu thấy nút **"Chuyển vào Bảng tin
chuyên nghiệp"** hoặc vào được **Meta Business Suite** thì Chú là admin, đi tiếp được.

---

### BƯỚC 1 — Tạo một App trên Meta (5 phút)

App này chỉ là cái "giấy thông hành" để Facebook cấp token. Không ai nhìn thấy nó,
không cần duyệt, không cần công khai.

1. Mở **https://developers.facebook.com/apps/**
2. Đăng nhập bằng đúng tài khoản Facebook đang quản Trang Panorama.
3. Lần đầu vào Facebook hỏi *"Bạn có phải nhà phát triển không"* → bấm
   **"Bắt đầu" / "Get Started"**, xác nhận số điện thoại hoặc email nếu nó hỏi.
4. Bấm nút xanh **"Tạo ứng dụng" / "Create App"** (góc trên bên phải).
5. **Giao diện Meta đổi tháng 9/2026** — giờ nó hỏi **"Trường hợp sử dụng"**
   (Use case) với một cột lọc bên trái. Màn hình mặc định mở ở **"Đáng chú ý (6)"**,
   và **cả sáu mục ở đó đều SAI** (API Marketing · Trình quản lý quảng cáo ·
   API Threads · Trò chơi tức thì · Đăng nhập bằng Facebook · WhatsApp).
   **Đừng tick cái nào.**

   Bấm **"Quản lý nội dung (5)"** ở cột trái. Năm mục hiện ra, tick **đúng mục
   cuối cùng: "Quản lý mọi thứ trên Trang"** — mô tả của nó là *"Đăng nội dung
   và video, kiểm duyệt bài viết và bình luận của người theo dõi trên Trang,
   đồng thời xem thông tin chi tiết về hoạt động tương tác."* Đó là use case
   cấp đúng ba quyền `pages_show_list` · `pages_read_engagement` ·
   `pages_manage_posts`.

   Bốn mục còn lại trong nhóm đó **bỏ qua**: API Threads · Instagram ·
   Video trực tiếp · oEmbed — không cái nào đăng được lên Trang Facebook.

   Bấm **Tiếp / Next**.
6. Màn **"Doanh nghiệp"** hỏi kết nối hồ sơ doanh nghiệp nào. Chọn
   **"Tôi chưa muốn kết nối hồ sơ doanh nghiệp."** → **Tiếp / Next**.

   **KHÔNG gắn vào hồ sơ Tân Hưng Realty.** Ba lý do, ghi lại để đợt sau đừng
   quyết lại: (a) hệ thống chỉ cần Page Access Token của chính admin Trang —
   app ở chế độ Development vẫn đăng được lên Trang mà admin đó quản, business
   portfolio chỉ cần cho System User token hoặc app phát hành công khai;
   (b) gắn vào là dính quy trình **xác minh doanh nghiệp**, thêm một vòng giấy
   tờ cho thứ không dùng tới; (c) Tân Hưng Realty là lane bán đất, Panorama là
   publication — §1 tách ba web ra chính vì vậy.

   Vướng về sau thì gắn sau ở **Cài đặt app → Cơ bản → Business Account**,
   không phải làm lại từ đầu.
7. Hai màn **"Yêu cầu"** và **"Tổng quan"** chỉ bấm xác nhận, không điền gì.
8. Điền:
   - **Tên ứng dụng:** gõ `Namban Panorama Auto Post` (tên gì cũng được, chỉ mình thấy)
   - **Email liên hệ:** `nambanpanorama@gmail.com`
   - **Tài khoản doanh nghiệp:** để trống cũng được
9. Bấm **"Tạo ứng dụng" / "Create App"**. Facebook hỏi lại mật khẩu → nhập.

Xong bước 1. Giờ Chú đang ở trang quản lý App.

---

### BƯỚC 2 — Lấy token trong Graph API Explorer (5 phút)

1. Mở **https://developers.facebook.com/tools/explorer/**
2. Góc **trên bên phải** có ô **"Ứng dụng Meta" / "Meta App"** → bấm vào, chọn
   đúng app `Namban Panorama Auto Post` vừa tạo.
3. Ngay dưới đó, ô **"Người dùng hoặc Trang" / "User or Page"** → bấm →
   chọn **"Nhận mã truy cập của Trang" / "Get Page Access Token"**.
4. Facebook mở cửa sổ hỏi chọn Trang. **ĐÂY LÀ CHỖ QUAN TRỌNG NHẤT** — Chú quản
   ba Trang, phải tick **đúng `Namban Panorama`**, bỏ tick hai Trang kia.
   Bấm **Tiếp / Continue** → **Lưu / Save** → **Xong / Done**.
5. Quay lại Explorer, ở khung **"Quyền" / "Permissions"**, bấm
   **"Thêm quyền" / "Add a Permission"**. Danh sách gom theo nhóm —
   **nhóm cần là "Events Groups Pages"**, mọi quyền `pages_*` nằm trong đó.

   **Tick đủ TÁM quyền, cấp một lần cho xong** (Chú chốt 16/9/2026 — đừng để
   sau phải quay lại làm lại):

   *Bốn quyền script cần ngay:*
   | Quyền | Để làm gì |
   |---|---|
   | `pages_show_list` | Liệt kê Trang — script dùng để biết token thuộc Trang nào |
   | `pages_read_engagement` | Đọc tên và username Trang — chốt chặn chống đăng nhầm Trang |
   | `pages_manage_posts` | Đăng bài, sửa, xoá — `POST /{page}/feed` |
   | `pages_manage_engagement` | Đăng comment thay mặt Trang — `POST /{post}/comments`, chỗ script để link bài |

   *Bốn quyền mở sẵn cho sau này:*
   | Quyền | Dùng khi nào |
   |---|---|
   | `pages_read_user_content` | Đọc comment người khác — cần khi muốn tự trả lời comment |
   | `pages_manage_metadata` | Webhook, cài đặt Trang — cần khi muốn nhận thông báo comment mới |
   | `read_insights` | Số liệu tiếp cận, tương tác — mục 1.10 theo dõi Insights 90 ngày |
   | `pages_messaging` | Trả lời inbox — nếu sau này làm auto reply |

   **Có quyền ≠ app tự làm.** Script chỉ chạy đúng thứ đã code: một bài, một
   comment. Bốn quyền sau chỉ mở sẵn cửa, không có rủi ro khi tick thừa.

   **Đừng tick:** `publish_to_groups` và `groups_access_member_info` (Panorama
   không đăng nhóm) · mọi quyền có tiền tố `ads_` (lane quảng cáo, sai việc).
6. Bấm nút xanh **"Tạo mã truy cập" / "Generate Access Token"**. Facebook hỏi
   xác nhận lần nữa → đồng ý hết.

   **LỖI HAY GẶP Ở ĐÂY — `Invalid Scopes: manage_pages`.** Gặp thật 16/9/2026.
   Explorer tự nhét quyền `manage_pages` vào danh sách; đó là **quyền cũ Meta đã
   bỏ từ 2021**, thay bằng ba quyền hẹp hơn (`pages_show_list` ·
   `pages_read_engagement` · `pages_manage_posts`). Thông báo ghi rõ *"chỉ hiển
   thị cho nhà phát triển"* nên nó **không chặn** việc lấy token — nhưng để lại
   thì lần nào bấm cũng báo đỏ, dễ tưởng hỏng.

   Dọn: ở khung **"Quyền"**, góc trên bên phải có icon **🗑** → bấm để xoá sạch
   danh sách → bấm **"Thêm quyền"** tick lại đúng ba quyền trên → rồi mới chọn
   lại **"Nhận mã truy cập Trang"**. Không thấy thùng rác thì tìm dòng
   `manage_pages` trong danh sách và bấm dấu **×** bên cạnh nó.
7. Ô **"Mã truy cập" / "Access Token"** ở trên giờ có một chuỗi dài loằng ngoằng.
   **Copy cả chuỗi đó.** Đây là token **ngắn hạn** (hết hạn sau ~1 giờ) — bước 3
   sẽ đổi nó thành loại không hết hạn.

---

### BƯỚC 3 — Đổi thành token KHÔNG HẾT HẠN (3 phút)

Bỏ qua bước này là một tháng sau hệ thống chết, mà không ai biết.

1. Mở **https://developers.facebook.com/tools/debug/accesstoken/**
2. Dán chuỗi token vừa copy vào ô, bấm **"Gỡ lỗi" / "Debug"**.
3. Kéo xuống cuối trang, bấm nút **"Gia hạn mã truy cập" / "Extend Access Token"**.
   Facebook hỏi mật khẩu → nhập.
4. Xuất hiện một chuỗi **mới** ở dưới. Copy chuỗi mới này.
5. Dán chuỗi mới vào Debugger lần nữa, bấm **Debug**, và **nhìn hai dòng**
   (Chú hỏi 16/9/2026: *"làm sao biết mã vĩnh viễn hay có hạn 2–3 tháng"*):
   - **"Hết hạn" / "Expires"** phải ghi **"Không bao giờ" / "Never"**
   - **"Loại" / "Type"** phải ghi **"Trang" / "Page"**

   Nếu **Expires** vẫn ghi một ngày cụ thể, hoặc **Type** ghi "User" → làm lại
   bước 2 và nhớ chọn **"Get Page Access Token"**, đừng lấy token người dùng.

   **Vì sao hay gặp con số "2–3 tháng":** token *người dùng* dài hạn sống đúng
   **60 ngày**. Page token **dẫn xuất từ** token người dùng dài hạn đó mới là
   loại không hết hạn. Lấy nhầm một bậc là hai tháng sau hệ thống chết lặng lẽ —
   workflow vẫn xanh vì không có bài đến hạn, tới khi có bài mới đỏ.

   **Không phải nhớ đi kiểm thủ công.** `tools/fb-post.py` tự gọi
   `GET /debug_token` mỗi lần chạy và in ngay đầu log:

   ```
   Token: loại PAGE · KHÔNG HẾT HẠN
   ```

   Thấy dòng đó là yên tâm. Nếu token có hạn, log in thẳng số ngày còn lại và
   trỏ về đúng mục này. Nếu token không phải loại PAGE, log in cảnh báo riêng.
   Kiểm token hỏng cũng **không chặn việc đăng** — chỉ in ra rồi chạy tiếp.

**Chuỗi cuối cùng đó chính là `FB_PAGE_TOKEN`.** Giữ kỹ — ai có nó là đăng được
lên Trang.

---

### BƯỚC 4 — Dán vào GitHub (2 phút)

1. Mở thẳng link này:
   **https://github.com/doanquocduyet/namban-panorama/settings/secrets/actions/new**
2. Ô **Name** gõ chính xác: `FB_PAGE_TOKEN`
   (viết hoa hết, có gạch dưới, không có khoảng trắng)
3. Ô **Secret** dán chuỗi token dài ở bước 3.
4. Bấm **"Add secret"**.

Xong. Không phải làm gì thêm.

---

### BƯỚC 5 — Chạy thử trước khi cho nó tự đăng

**Chạy khô trước** — in bài ra màn hình, không đăng lên Facebook:

1. Mở **https://github.com/doanquocduyet/namban-panorama/actions/workflows/fb-post.yml**
2. Bấm **"Run workflow"** (nút xám bên phải).
3. Ô **"Chạy khô — in bài ra, không đăng"** để nguyên **true**.
4. Bấm **"Run workflow"** xanh.
5. Đợi khoảng 30 giây, bấm vào run vừa hiện, xem log. Phải thấy bài sắp đăng in ra.

**Rồi mới đăng thật:** làm lại từ đầu, nhưng đổi ô chạy khô thành **false**.

Log sẽ in `Đăng lên Trang: Namban Panorama (nambanpanorama)`. Nếu nó in tên Trang
khác thì script **tự dừng, không đăng** — lúc đó quay lại bước 2 chọn lại Trang.

Sau lần đầu thành công, workflow tự chạy **11h trưa và 20h tối giờ Việt Nam** mỗi
ngày, mỗi lần một bài, theo hàng đợi `data/fb-queue.json`.

---

### KHI NÀO PHẢI LÀM LẠI

Page token loại này **không tự hết hạn**, nhưng sẽ chết nếu:
- Chú **đổi mật khẩu Facebook**
- Chú **gỡ app** khỏi tài khoản (Cài đặt → Ứng dụng và trang web)
- Chú **rời quyền admin** của Trang

Dấu hiệu chết: workflow `fb-post` bắt đầu đỏ, log ghi `LỖI GRAPH API 190`.
Chữa: làm lại từ **bước 2**, rồi cập nhật secret ở bước 4 (bấm **Update** thay vì
Add).

---

### CHỐT AN TOÀN ĐÃ DỰNG SẴN — Chú không cần lo

| Rủi ro | Đã chặn thế nào |
|---|---|
| Token cấp nhầm Trang Villas / Greenspacers | Script hỏi `GET /me`, đối chiếu username với `nambanpanorama`, lệch thì **dừng, không đăng** |
| Bài có chữ CTA bán (§2.1) | 12 chuỗi cấm kiểm **trước khi gọi API** — `liên hệ ngay`, `mua ngay`, `chốt ngay`, `nhanh tay`… dính một chữ là dừng |
| Đăng nhầm bài chưa có trên web | Kiểm `slug` có file `.html` thật không, không có thì dừng |
| Link ngoài làm tụt tiếp cận | Link bài **luôn nằm ở comment 1**, không nằm trong caption |
| Đăng trùng | Đăng xong ghi `posted: true` vào hàng đợi, commit lại |
| Chưa cấp token mà workflow chạy | Tự chuyển sang chạy khô, in bài ra, thoát sạch — **không run nào đỏ** |

---

## 0-B. INSTAGRAM — HƯỚNG DẪN TỪNG NÚT

Instagram **dùng chung token với Facebook**, không phải lấy token mới. Nhưng Chú
phải làm ba việc trên điện thoại trước, nếu chưa làm thì API không thấy tài khoản.

### BƯỚC 1 — Kiểm loại tài khoản Instagram (3 phút, trên điện thoại)

Tài khoản cá nhân thường **không đăng được bằng API**. Phải là Professional.

⚠️ **Tên mục trong app đổi theo từng bản.** Bản Chú dùng (16/9/2026) KHÔNG có
mục "Dành cho chuyên gia" như tài liệu Meta ghi. Đường đúng trên máy Chú:

1. Mở app **Instagram** → bấm **ảnh đại diện** góc dưới phải.
2. Bấm **☰** góc trên phải → **Cài đặt và hoạt động**.
3. Kéo xuống gần cuối, tới mục **Thông tin chi tiết và công cụ**.
4. Bấm **Công cụ và loại tài khoản**.
5. Dòng đầu **Loại tài khoản** cho biết đang là gì:
   - Ghi **Cá nhân** → bấm dòng ngay dưới, **"Chuyển sang tài khoản công
     việc"**. (Bản cũ gọi là *"tài khoản chuyên nghiệp"* — cùng một thứ,
     Instagram đổi tên. Đừng đi tìm chữ "chuyên nghiệp" nữa.)
   - Ghi **Công việc** / **Doanh nghiệp** → xong rồi, khỏi làm gì.
6. Trong luồng chuyển:
   - **Danh mục** → chọn **Nhà xuất bản kỹ thuật số** (không có thì **Blogger
     cá nhân** hoặc **Trang web tin tức**). **ĐỪNG chọn "Bất động sản"** —
     Panorama là publication (§1 CLAUDE.md); chọn vậy là tự dán nhãn sai lane
     và Instagram xếp nội dung vào nhóm tin rao.
   - Hỏi **Doanh nghiệp** hay **Nhà sáng tạo** → chọn **Doanh nghiệp**.
     Nhà sáng tạo bị giới hạn vài API đăng bài.
   - Hỏi nối Trang Facebook → **Bỏ qua**, nối ở bước 2 trên máy tính cho chắc.
7. Quay lại màn hình cũ, dòng **Loại tài khoản** phải đổi thành **Công việc**.
   Thấy vậy mới là xong bước 1.

Tiện kiểm luôn: **Cài đặt và hoạt động → Quyền riêng tư của tài khoản** phải
là **Công khai**.

### BƯỚC 2 — Nối Instagram với Trang Facebook (2 phút, LÀM TRÊN MÁY TÍNH)

Đây là chỗ hay sót nhất. API tìm Instagram **qua Trang**, không nối thì
script báo *"Trang chưa gắn tài khoản Instagram chuyên nghiệp"*.

**Làm trên máy tính, đừng làm trong app.** Đường trong app đổi liên tục, mỗi
bản một chỗ; đường Business Suite thì ổn định.

1. Mở https://business.facebook.com/latest/settings/instagram_accounts
2. Nếu nó hỏi chọn Trang → chọn **NamBan Panorama**.
3. Bấm **Kết nối tài khoản** (hoặc **Thêm**).
4. Đăng nhập Instagram `nambanpanorama` → xác nhận.
5. Xong thì màn hình đó hiện tên tài khoản Instagram nằm dưới Trang NamBan
   Panorama. Đó là thứ cần thấy.

Cẩn thận chỗ chọn Trang — Chú quản nhiều Trang, bấm nhầm là bài Panorama rơi
lên Instagram của Trang khác. Script có chốt chặn đối chiếu username nên nó
dừng chứ không đăng bừa, nhưng bấm đúng ngay từ đầu vẫn hơn.

### BƯỚC 3 — Thêm sản phẩm Instagram vào app TRƯỚC (5 phút)

⚠️ **Gõ `instagram` vào ô Thêm quyền mà không ra dòng nào — đó KHÔNG phải
lỗi.** Quyền `instagram_*` chỉ hiện trong Explorer **sau khi** app được gắn
sản phẩm Instagram. Giống hệt Threads: chưa thêm Threads API thì trong ô
chọn không có dòng Threads. Vấp thật 16/9/2026, mất một vòng đi tìm.

1. Mở https://developers.facebook.com/apps/ → bấm vào app đã tạo ở mục 0-A.
2. Menu trái, kéo xuống cuối → **Thêm sản phẩm** (*Add Product*).
3. Tìm ô **Instagram** → **Thiết lập** (*Set up*).
4. Hỏi kiểu thiết lập → chọn **API thiết lập bằng đăng nhập Facebook**
   (*Instagram API setup with Facebook Login*).
   **ĐỪNG chọn** *"Instagram API với đăng nhập Instagram"* — đường đó dùng
   token riêng của Instagram, không dùng được Page token mình đang có.
5. Menu trái không có **Thêm sản phẩm** mà có **Trường hợp sử dụng**
   (*Use cases*) → app dựng theo kiểu mới. Khi đó: **Trường hợp sử dụng** →
   **Thêm trường hợp sử dụng** → chọn cái có chữ **Instagram** → **Thiết lập**.
   Kết quả như nhau.

### BƯỚC 4 — Lấy token có quyền Instagram (3 phút)

Token cũ chưa có quyền Instagram, phải lấy lại **một lần**.

Giao diện tiếng Việt đặt tên ô khác tài liệu Meta — đối chiếu cho khỏi lẫn:
**Meta App** = *Ứng dụng trên Meta* · **User or Page** = *Người dùng hoặc
Trang* · **Permissions** = *Quyền* · **Add a Permission** = *Thêm quyền*.

1. Mở https://developers.facebook.com/tools/explorer/ và **tải lại trang**
   (F5) nếu vừa làm bước 3 xong — không tải lại thì quyền mới chưa hiện.
2. Ô **Ứng dụng trên Meta** chọn đúng app đã tạo ở mục 0-A.
3. Trong ô **Quyền**, bấm **Thêm quyền** → tìm và tick thêm:
   - `instagram_basic`
   - `instagram_content_publish`
   - `instagram_manage_comments` *(để thả link vào comment 1)*
4. Ô **Người dùng hoặc Trang** — mặc định là **Mã người dùng**, SAI loại.
   Đổi thành **Mã truy cập Trang** → chọn **NamBan Panorama**.
5. Bấm **Generate Access Token** → duyệt lại → **Continue**.

**Thứ tự bắt buộc:** thêm sản phẩm → tải lại trang → tick quyền → đổi sang
mã Trang → Generate. Sai thứ tự thì mã sinh ra thiếu quyền, phải làm lại.
6. Đem token mới qua https://developers.facebook.com/tools/debug/accesstoken/
   → dán → **Debug** → bấm **Extend Access Token** (nút *"Gia hạn"*).
7. Kiểm hai dòng: **Expires** phải ghi **Never**, **Type** phải ghi **Page**.
   Sai một trong hai thì làm lại bước 4.
8. Dán đè vào secret cũ: https://github.com/doanquocduyet/namban-panorama/settings/secrets/actions
   → bấm `FB_PAGE_TOKEN` → **Update secret**.

### MỘT ĐIỀU PHẢI BIẾT TRƯỚC VỀ INSTAGRAM

**Instagram không cho link bấm được** — không trong caption, không trong comment.
Link duy nhất bấm được là link ở **bio**. Nên Instagram **không kéo người về web**
như Facebook; nó chỉ để nhận diện. Chú vào bio đặt sẵn `nambanpanorama.com`.

**Caption Instagram trần 2.200 ký tự.** Bài ngắn nhất của site đã 5.700 ký tự, nên
**không bài nào đăng đủ được trên Instagram**. Script tự lùi về câu mồi viết tay
trong hàng đợi và ghi rõ lý do trong log — không cắt ngang giữa câu.

**Ảnh dùng luôn tấm og 1200×630.** Tỷ lệ 1,905:1, vừa sát trần 1,91:1 của
Instagram nên lọt, không phải cắt lại bộ ảnh vuông.

---

## 0-C. THREADS — HƯỚNG DẪN TỪNG NÚT

Threads **có token riêng**, không dùng chung với Facebook. Đây là chỗ khác biệt
lớn nhất so với Instagram, đừng nhầm.

### BƯỚC 1 — Bật Threads cho tài khoản (2 phút)

Không cần cài app riêng. Mở thẳng từ trong Instagram:

1. **Instagram → ☰ → Cài đặt và hoạt động** → kéo xuống mục **Cũng của Meta**
   → bấm **Threads**.
2. Hoặc cài app **Threads** rồi đăng nhập bằng đúng tài khoản Instagram
   `nambanpanorama`.
3. Bảo đảm tài khoản **công khai** (không khoá). Tài khoản khoá thì API đăng
   được nhưng không ai ngoài người theo dõi thấy — mất sạch ý nghĩa.

### BƯỚC 2 — Thêm Threads vào app Meta (5 phút)

1. Mở https://developers.facebook.com/apps/ → bấm vào app đã tạo ở mục 0-A.
2. Menu trái → **Thêm sản phẩm** (*Add Product*).
3. Tìm ô **Threads API** → bấm **Thiết lập** (*Set up*).
4. Vào **Threads API** → **Cài đặt** (*Settings*).
5. Ô **Redirect Callback URLs** phải điền gì đó thì mới lưu được. Điền:
   `https://nambanpanorama.com/` — mình không dùng đường quay lại này, nhưng
   Meta bắt buộc có.
6. Bấm **Lưu thay đổi**.

### BƯỚC 3 — MỜI TÀI KHOẢN LÀM NGƯỜI KIỂM THỬ (bắt buộc, 5 phút)

⚠️ **Bỏ bước này thì bấm Generate sẽ ra lỗi:**
`{"error_message":"Invalid Request: The user has not accepted the invite to
test the app.","error_code":1349245}` — vấp thật 17/9/2026.

App ở chế độ phát triển thì tài khoản Threads phải được **mời** và phải
**bấm nhận lời mời**. **Facebook KHÔNG cần bước này** (admin Trang là đủ),
Threads thì cần — đây là chỗ hai bên khác nhau, đừng suy từ bên kia sang.

*Trên máy tính:*
1. Mở https://developers.facebook.com/apps/1057590477249015/roles/roles/
2. Kéo tới mục **Người kiểm thử Threads** (*Threads Testers*) — nằm dưới
   Quản trị viên / Nhà phát triển / Người kiểm thử.
3. **Thêm người** → gõ `namban.panorama` → **Gửi**.

*Trên điện thoại:*
4. App **Threads** → **☰** → **Cài đặt** → **Tài khoản**
5. **Quyền trên trang web** (*Website permissions*) → **Lời mời** (*Invites*)
6. Thấy lời mời từ app → bấm **Chấp nhận**.

### BƯỚC 4 — Lấy token Threads (5 phút)

1. Mở https://developers.facebook.com/tools/explorer/
2. Góc phải trên: ô **Ứng dụng trên Meta** chọn đúng app.
3. Ô nhỏ bên trái ô địa chỉ đang ghi **`graph.facebook.com`** → đổi thành
   **`graph.threads.net`**. *Không thấy dòng đó thì bước 2 (mục 0-C) chưa xong.*
4. Bấm **Generate Threads Access Token**.
5. Chọn tài khoản Threads → duyệt quyền → **Tiếp tục**.
6. Copy chuỗi trong ô **Mã truy cập**.

**Nhận biết đúng token:** mã Facebook bắt đầu bằng `EAA`, mã Threads bắt đầu
bằng `TH`. Còn thấy `EAA` là chưa lấy được, đừng đem đi dùng.

### BƯỚC 5 — Đổi thành token 60 ngày (3 phút)

Token Explorer vừa cấp **chỉ sống 1 giờ**. Phải đổi, không thì mai đã chết.

1. Mở https://developers.facebook.com/apps/1057590477249015/settings/basic/
2. Dòng **Khóa bí mật của ứng dụng** → **Hiển thị** → copy.
3. Mở tab mới, dán địa chỉ này, thay hai chỗ IN HOA:
   `https://graph.threads.net/access_token?grant_type=th_exchange_token&client_secret=KHOA_BI_MAT&access_token=MA_TH_NGAN_HAN`
4. Trang trả về `{"access_token":"THQ...","expires_in":5183944}` — copy chuỗi
   sau `"access_token":`. **Đó mới là token 60 ngày.**

### BƯỚC 6 — Dán vào GitHub (2 phút)

1. Mở https://github.com/doanquocduyet/namban-panorama/settings/secrets/actions/new
2. Ô **Name** gõ đúng: `THREADS_TOKEN`
3. Ô **Secret** dán token ở bước 5.
4. Bấm **Add secret**.

`tools/social-post.py` tự in số ngày còn lại mỗi lần chạy và kêu to khi còn
dưới 14 ngày. Tới lúc đó chỉ làm lại bước 4–6, không phải làm lại từ đầu.

### ⚠️ TOKEN THREADS SỐNG 60 NGÀY — KHÁC HẲN FACEBOOK

Đây là điểm phải nhớ. Token Facebook không hết hạn; **token Threads thì hết hạn
sau 60 ngày**, và Meta chưa cho loại vĩnh viễn. Hai tháng một lần phải làm lại
**bước 3 và 4**.

Dấu hiệu chết: workflow `social-post` đỏ ở nhánh `threads`, log ghi lỗi mã 190.

### MỘT ĐIỀU PHẢI BIẾT TRƯỚC VỀ THREADS

**Threads trần 500 ký tự một bài.** Nên script đăng nguyên bài bằng **chuỗi trả
lời nối nhau** — đúng nếp Threads, người ta vẫn đọc kiểu đó. Bài đầu có ảnh, các
bài sau là chữ, bài chót là link.

Bài của site ra **12–18 mắt xích** một chuỗi. Dài, nhưng đó là cái giá của "đăng
100% nội dung". Muốn một bài nào đó chỉ đăng câu mồi thì thêm `"full": false`
vào bài đó trong `data/fb-queue.json`.

---

## 0-D. ĐĂNG 100% NỘI DUNG — ĐÃ BẬT, VÀ MỘT CHỖ CẦN NÓI THẲNG

Chú chốt 16/9/2026: đăng **nguyên văn bài web**, không đăng câu mồi cụt. Đã bật,
mặc định cho mọi bài. Script bóc lời bài bằng đúng bộ bóc của audio
(`scripts/gen_audio_edge.py`, hàm `narration`) nên nó tự bỏ `<figure>`, khối
Nguồn, khối liên hệ, nút Nghe bài, mục "Đọc gì tiếp" — còn lại đúng phần người
đọc đọc trên web.

Tắt cho một bài: thêm `"full": false` vào bài đó trong `data/fb-queue.json`.

**Chỗ phải nói thẳng, vì nó là dữ kiện chứ không phải ý kiến:** việc này **không
đem lại SEO**. Ba lý do, kiểm được:

1. **Link từ Facebook là `nofollow`** — không truyền giá trị xếp hạng sang site.
2. **Google gần như không index bài Facebook.** Nội dung Trang chỉ hiện đầy đủ
   với người đã đăng nhập, Googlebot đọc được rất ít.
3. **Các bộ thu thập của AI bị Meta chặn.** Nên chữ đăng lên Facebook gần như
   vô hình với ChatGPT, Perplexity, Gemini — tức là **không giúp AEO/GEO**.

Cái đăng đủ nội dung **thật sự** đem lại là **thời gian đọc trên bài**, và đó là
thứ Facebook đo để quyết định cho bao nhiêu người thấy. Bài dài giữ người ở lại
lâu hơn câu mồi ba dòng, nên tiếp cận lên. Đó là lợi ích thật, đo được, nằm gọn
**bên trong Facebook**.

Cái nó lấy đi là **cú bấm sang web**. Đọc hết trên Facebook rồi thì ít ai bấm
link nữa. Mà phễu của Panorama nằm ở web (§0.6 CLAUDE.md), không nằm ở Facebook.

**Nên cách dùng đúng:** để `full: true` cho bài **kể chuyện, dữ kiện vùng, sửa
hiểu nhầm** — loại đọc xong là xong, mục tiêu là người ta nhớ tới Panorama. Để
`full: false` cho bài **tra cứu có bảng, có số, có FAQ dài** — loại người ta cần
mở lại nhiều lần, và mỗi lần mở lại là một lần vào web.

SEO vẫn là việc của web, không phải việc của Facebook. Cái web đang làm đúng
hướng rồi: `llms.txt`, JSON-LD, `sitemap.xml`, IndexNow, tầng `/data/*.json`.

---

## 0. GIỮ GÌ, BỎ GÌ CỦA 7 PROMPT

7 prompt Chú đưa là công thức bán hàng viral. **Cơ chế thì đúng, chất liệu thì sai
lane.** Bảng đổi:

| Prompt gốc bảo | Panorama làm |
|---|---|
| "Hook gây shock, gây tò mò tột độ" | Hook bằng **một dữ kiện cụ thể ít người biết**. Tò mò tới từ chỗ lạ mà thật, không từ chữ in hoa. |
| "Đánh vào nỗi đau khách hàng" | Nói thẳng **rủi ro có thật**, kể cả rủi ro khiến người ta không mua. §2.8. |
| "CTA seeding, kêu gọi inbox" | Không CTA. Kết bằng **một câu hỏi thật** hoặc để trống. Link bài ở comment 1. |
| "Khan hiếm: chỉ còn 3 lô" | Cấm tuyệt đối. Đây là chữ của tin rao. |
| "Chốt sale trong comment" | Comment chỉ trả lời đúng câu hỏi. Ai hỏi khu cụ thể → chỉ sang bài, không báo giá lô. |
| Lịch 30 ngày | **Giữ nguyên.** Đây là phần giá trị nhất. |
| Ngân hàng 30 hook | **Giữ nguyên cơ chế**, viết lại bằng giọng mình. |
| 1 ý → 7 góc | **Giữ nguyên.** Đúng với kho 163 bài. |
| Phân tích bài top | **Giữ**, cần Chú dán số thật. |

**Một luật riêng cho Facebook, không có trong `CLAUDE.md`:** bài Facebook **không được
là bản tóm tắt của bài web**. Tóm tắt thì người đọc đọc xong ở lại Facebook, không sang
web — phễu đứt ngay chỗ đó. Bài Facebook phải là **một lát cắt trọn vẹn** (đọc xong
thấy đủ), và bài web là **chỗ trả lời câu hỏi mà lát cắt đó mở ra**.

---

## 1. KỸ THUẬT FACEBOOK — CÁI GÌ ĐANG THẬT SỰ CHẠY

Phần này là kỹ thuật thuần, không dính giọng. Áp được cho mọi trang.

**1.1 Hai dòng đầu là tất cả.** Facebook cắt caption ở khoảng **125 ký tự** trên mobile
rồi hiện "Xem thêm". Người ta quyết định đọc tiếp hay không ở đúng chỗ đó. Nên:
- Dữ kiện mạnh nhất nằm ở **dòng 1**, không nằm ở dòng 3.
- Không mở bài bằng "Chào cả nhà", "Hôm nay Panorama xin chia sẻ" — đốt sạch 125 ký tự.
- Xuống dòng sau câu đầu. Một câu một dòng ở phần đầu, dễ liếc.

**1.2 Link ngoài làm tụt tiếp cận — nhưng đừng giấu link.** Cách đang chạy tốt:
viết đủ giá trị trong caption, **link đặt ở comment đầu tiên do chính Trang đăng**,
rồi ghim comment đó. Trong caption ghi một dòng cuối: *"Bản đầy đủ ở comment."*
Không viết "link ở cmt nhé cả nhà" — chữ đó là chữ seeding.

**1.2b Bài = ẢNH + caption, link nằm dưới comment (Chú chốt 16/9/2026).** Không đăng
bài chữ trơn, cũng không để link trên bài. `tools/fb-post.py` làm ba việc theo thứ tự:
gọi `POST /{page}/photos` với `url` ảnh + `caption` → lấy `post_id` trong kết quả →
gọi `POST /{post_id}/comments` để thả link. Comment phải gắn vào `post_id` (bài trên
tường), không gắn vào `id` (node ảnh).

**Ảnh không phải khai tay.** Script tự lấy theo thứ tự: trường `image` của bài trong
`data/fb-queue.json` → `og:image` đọc thẳng từ `<slug>.html`. Mọi bài đã có og cắt
chuẩn 1200×630 (§3 CLAUDE.md) nên mặc định là đúng tấm. Muốn đổi tấm khác cho một bài
thì thêm `"image": "/images/ten-anh.jpg"` vào entry đó. Script kiểm file có thật trong
repo trước khi đưa cho Graph — Graph tự đi tải URL đó, đưa nhầm đường dẫn thì nó báo
lỗi mơ hồ, khó dò.

**Chốt chặn kèm theo:** caption chứa `http` hoặc `nambanpanorama.com` là script DỪNG,
không đăng. Link chỉ được nằm ở comment.

**1.3 Bình luận trong 60 phút đầu quyết định bài sống hay chết.** Nên:
- Đăng lúc mình rảnh trả lời, đừng đăng rồi đi ngủ.
- Trả lời **mọi** bình luận trong giờ đầu, kể cả bình luận một chữ.
- Trả lời bằng **thêm dữ kiện**, không bằng "cảm ơn anh/chị ạ". Mỗi câu trả lời là một
  bài viết nhỏ — đó là chỗ Facebook đo là "cuộc trò chuyện".

**1.4 Câu hỏi cuối bài phải trả lời được bằng một câu.** "Anh chị thấy sao ạ?" không ai
trả lời. "Nhà mình ai từng đi Nam Ban mùa mưa chưa, đường Tà Nung lúc đó thế nào?" thì
có người trả lời — vì họ có sẵn câu chuyện.

**1.5 Định dạng, theo thứ tự tiếp cận hiện tại:**
1. **Reels** (video dọc 15–40 giây) — tiếp cận cao nhất, tới người chưa follow.
2. **Ảnh đơn + caption dài** — tốt nhất cho bài dữ kiện. Đây là xương sống của Panorama.
3. **Carousel ảnh** (3–5 tấm) — hợp bài so sánh, bài "đọc lô đất".
4. **Chỉ chữ, không ảnh** — thấp nhất, nhưng dùng được cho tin cập nhật ngắn.

**1.6 Hashtag: 3–5, bám địa danh, đặt cuối.** `#NamBan #LamHa #LamDong #DatNamBan`
và một cái theo chủ đề bài. Đừng nhồi 30 cái — Facebook không thưởng, người đọc thấy rẻ.

**1.7 Không sửa caption trong 24 giờ đầu.** Sửa bài đang phân phối thì phân phối bị
tính lại. Sai chính tả nhỏ thì để đó, hôm sau sửa.

**1.8 Đăng đều quan trọng hơn đăng nhiều.** 4 bài/tuần đều đặn tốt hơn 12 bài một tuần
rồi im hai tuần. Lịch dưới đây là **5 bài/tuần**, cắt xuống 3 cũng được, miễn đừng đứt.

**1.9 Ảnh phải là ảnh mình chụp.** Cùng luật với web (§3 Luật 19–20): không ảnh có vạch
khoanh ranh, không ảnh mạng, không ảnh có chữ tin rao. Ảnh thật của vùng là **tài sản
phân biệt Panorama với 200 trang môi giới** — đừng đổi nó lấy một tấm đẹp trên mạng.

**1.10 Giờ đăng cho tệp này.** Người mua đất Nam Ban phần lớn ở Sài Gòn, đi làm.
Hai khung tốt: **11h30–12h30** (nghỉ trưa) và **20h30–22h00** (tối, nằm lướt).
Bài dữ kiện dài → khung tối. Tin cập nhật ngắn → khung trưa.

---

## 2. NGÂN HÀNG 30 MỞ ĐẦU

Mỗi hook dưới đây bám một bài có thật trong repo. Không hook nào bịa số.
Dùng làm **dòng 1**, tức phần nằm trên nếp gấp "Xem thêm".

**Nhóm A — dữ kiện lạ mà thật (mạnh nhất, dùng nhiều nhất)**

1. Hồ Tròn ở Nam Ban, trong hồ sơ nó tên là hồ Ba Đình. → `/ho-tron-nam-ban`
2. Hồ Thanh Trì thật ra là hai cái hồ, không phải một. → `/ho-thanh-tri-nam-ban`
3. Ở Nam Ban, 5 km không phải lúc nào cũng là 5 km. → `/5km-o-nam-ban`
4. Nam Ban có 17 thôn. Phần lớn người bán đất gọi tên thôn cũ. → `/thon-nam-ban`
5. Năm nay riêng khu này có 206 quyết định cho chuyển mục đích sử dụng đất. → `/chuyen-muc-dich-su-dung-dat-nam-ban`
6. Từ 20/8/2026, diện tích tối thiểu để tách thửa ở Lâm Đồng đã đổi. → `/tach-thua-dat-nam-ban`
7. Cầu Tổng Đội khởi công 14/7/2026. Dự kiến xong 10/11/2027 — mười sáu tháng. → `/cau-tong-doi-nam-ban`
8. Sân bay Liên Khương bay lại từ 19/8/2026. Nam Ban cách đó khoảng 20 km. → `/san-bay-lien-khuong-mo-lai`
9. Trên trục 725 vừa mọc thêm hai cây xăng Petro. → `/cay-xang-petro-moi-o-nam-ban`
10. Người Hà Nội bắt đầu câu chuyện Nam Ban vào ngày 10/10/1975. → `/10-10-1975-nam-ban`
11. Quy hoạch Nam Ban tới 2050 chia vùng này làm 7 khu vực phát triển. → `/quy-hoach-chung-nam-ban`
12. Rừng thông ở Nam Ban ít hơn nhiều người tưởng — và phần nhiều là thông dân tự trồng. → `/dat-giap-rung-thong-nam-ban`

**Nhóm B — sửa một hiểu nhầm phổ biến**

13. Chùa Linh Ẩn không nằm trong thành phố Đà Lạt. → `/chua-linh-an-nam-ban`
14. Nam Hà không thuộc Nam Ban. Đó là hai xã. → `/nam-ban-va-nam-ha`
15. Thủy điện Đạ Chomo không nằm ở Nam Ban. → `/thuy-dien-da-chomo-phi-to`
16. Tà Nung không thuộc Lâm Hà — nó thuộc Đà Lạt. → `/ta-nung-hay-me-linh`
17. "Lên thổ cư được giảm 70%" — cái giảm đó không phải như nhiều người hiểu. → `/len-tho-cu-het-bao-nhieu-tien`
18. Đất đo ngoài đường và đất ghi trên sổ thường không bằng nhau. → `/do-dac-dat-nam-ban`
19. Nam Ban chưa sáp nhập vào Đà Lạt. → `/nam-ban-co-sap-nhap-da-lat`

**Nhóm C — câu hỏi người ta thật sự gõ**

20. 500 triệu tới 1 tỷ ở Nam Ban mua được gì? → `/mua-dat-nam-ban-500-trieu-1-ty`
21. Một sào bơ ở Nam Ban cho bao nhiêu tiền một năm? → `/vuon-bo-loi-bao-nhieu`
22. Xây một căn nhỏ ở Nam Ban hết bao nhiêu? → `/xay-nha-nho-nam-ban-bao-nhieu-tien`
23. Nam Ban có nước máy không, khoan giếng sâu bao nhiêu mét? → `/nuoc-o-nam-ban`
24. Đất vườn ở Nam Ban xây được cái gì, không xây được cái gì? → `/dat-vuon-nam-ban-xay-duoc-gi`
25. Nam Ban sau 6 giờ tối sống thế nào? → `/nam-ban-sau-6h-toi`

**Nhóm D — nói ngược, chỗ Panorama khác mọi trang khác**

26. Có những lô đất ở Nam Ban tôi sẽ khuyên đừng mua. → `/truoc-khi-xuong-tien`
27. Homestay ở Nam Ban: nói thẳng về dòng tiền, kể cả phần không vui. → `/homestay-nam-ban-co-lai-khong`
28. Mua đất Nam Ban rồi giá xuống thì nên bán hay giữ? → `/dat-nam-ban-xuong-gia-ban-hay-giu`
29. Đừng hỏi lô nào đẹp. Hỏi lô này hỏng ở đâu. → `/kinh-nghiem-mua-dat-nam-ban`
30. Một lô bình thường, không view, không gì nổi bật — hợp với ai? → `/lo-dat-nam-ban-binh-thuong`

**Cách dùng ngân hàng này:** mỗi tuần lấy **2 hook nhóm A, 1 nhóm B, 1 nhóm C, 1 nhóm D**.
Nhóm A kéo người lạ, nhóm B tạo uy tín, nhóm C bắt đúng từ khoá, nhóm D là chỗ người ta
nhớ mình. Đừng dùng liền hai hook cùng nhóm — trang sẽ thành một giọng.

---

## 3. LỊCH 30 NGÀY

5 bài/tuần, nghỉ thứ Bảy và Chủ Nhật (hoặc để một bài nhẹ cuối tuần).
Mỗi ngày ghi: **định dạng · hook · bài web dẫn tới**.

Nhịp tuần cố định — cứ lặp, người đọc quen giờ:

| Thứ | Vai trò | Định dạng |
|---|---|---|
| Hai | Dữ kiện vùng (nhóm A) | Ảnh đơn + caption dài |
| Ba | Sửa hiểu nhầm (nhóm B) | Ảnh đơn |
| Tư | Câu hỏi tiền bạc (nhóm C) | Carousel hoặc ảnh đơn |
| Năm | Đời sống / con người | Reels hoặc ảnh đơn |
| Sáu | Nói ngược, rủi ro (nhóm D) | Chỉ chữ hoặc ảnh đơn |

### Tuần 1 — vùng đất là gì

| Ngày | Định dạng | Hook | Bài dẫn |
|---|---|---|---|
| 1 (Hai) | Ảnh | Hồ Tròn, trong hồ sơ tên là hồ Ba Đình | `/ho-tron-nam-ban` |
| 2 (Ba) | Ảnh | Chùa Linh Ẩn không nằm trong Đà Lạt | `/chua-linh-an-nam-ban` |
| 3 (Tư) | Carousel | 500 triệu tới 1 tỷ mua được gì | `/mua-dat-nam-ban-500-trieu-1-ty` |
| 4 (Năm) | Reels | Một ngày của người làm vườn | `/mot-ngay-lam-vuon-nam-ban` |
| 5 (Sáu) | Chữ | Có lô tôi sẽ khuyên đừng mua | `/truoc-khi-xuong-tien` |

### Tuần 2 — đường sá và hạ tầng

| Ngày | Định dạng | Hook | Bài dẫn |
|---|---|---|---|
| 8 | Ảnh | Cầu Tổng Đội: khởi công 14/7/2026, xong 10/11/2027 | `/cau-tong-doi-nam-ban` |
| 9 | Ảnh | Tà Nung thuộc Đà Lạt, không thuộc Lâm Hà | `/ta-nung-hay-me-linh` |
| 10 | Ảnh | Nam Ban có nước máy không | `/nuoc-o-nam-ban` |
| 11 | Reels | Đường Tà Nung mùa mưa | `/mua-mua-nam-ban` |
| 12 | Chữ | Đừng hỏi lô nào đẹp | `/kinh-nghiem-mua-dat-nam-ban` |

### Tuần 3 — pháp lý và tiền

| Ngày | Định dạng | Hook | Bài dẫn |
|---|---|---|---|
| 15 | Ảnh | 206 quyết định chuyển mục đích | `/chuyen-muc-dich-su-dung-dat-nam-ban` |
| 16 | Ảnh | "Giảm 70%" không phải như nhiều người hiểu | `/len-tho-cu-het-bao-nhieu-tien` |
| 17 | Carousel | Xây căn nhỏ hết bao nhiêu | `/xay-nha-nho-nam-ban-bao-nhieu-tien` |
| 18 | Ảnh | Người rời Sài Gòn lên đây làm cà phê | `/roi-sai-gon-len-nam-ban` |
| 19 | Chữ | Mua rồi giá xuống: bán hay giữ | `/dat-nam-ban-xuong-gia-ban-hay-giu` |

### Tuần 4 — chọn khu, chọn kiểu sống

| Ngày | Định dạng | Hook | Bài dẫn |
|---|---|---|---|
| 22 | Ảnh | Ở Nam Ban, 5 km không phải lúc nào cũng là 5 km | `/5km-o-nam-ban` |
| 23 | Ảnh | Nam Hà không thuộc Nam Ban | `/nam-ban-va-nam-ha` |
| 24 | Carousel | Nên xem khu nào ở Nam Ban | `/nen-xem-khu-nao-o-nam-ban` |
| 25 | Reels | Nam Ban sau 6 giờ tối | `/nam-ban-sau-6h-toi` |
| 26 | Chữ | Lô bình thường hợp với ai | `/lo-dat-nam-ban-binh-thuong` |

### Hai ngày lẻ (29, 30)

| Ngày | Định dạng | Hook | Bài dẫn |
|---|---|---|---|
| 29 | Ảnh | Rừng thông ở Nam Ban ít hơn người ta tưởng | `/dat-giap-rung-thong-nam-ban` |
| 30 | Chữ | 5 bài được đọc nhiều nhất tháng này | `/doc-nhanh` |

**Tháng sau đổi gì:** giữ nguyên nhịp tuần, thay hook. Ngân hàng 30 hook trên đủ cho
**hai tháng** nếu mỗi tháng dùng 15 cái. Sang tháng thứ ba thì viết ngân hàng mới —
lúc đó đã có số thật để biết nhóm nào chạy.

---

## 4. MỘT Ý → BẢY GÓC

Đây là kỹ thuật đáng giá nhất trong bộ 7 prompt. Làm mẫu trên một ý:

> **Ý gốc: đường mới Nam Ban đi Đà Lạt qua Phi Tô vừa thông.** (`/duong-nam-ban-phi-to-da-lat`)

| Góc | Hook | Ai đọc |
|---|---|---|
| **Dữ kiện** | Có một tuyến đèo nữa nối Nam Ban với Đà Lạt, không phải Tà Nung. | Người chưa biết vùng |
| **So sánh** | Đi Đà Lạt bằng đường mới hay đèo Tà Nung: khác nhau chỗ nào | Người sắp lên xem đất |
| **Ảnh hưởng tới đất** | Đường mới mở thì đất khu nào đổi giá, khu nào không | Người đang cân nhắc |
| **Cảnh báo** | Đường mới không tự làm lô của bạn có giá | Người đang bị chào bán |
| **Trải nghiệm** | Chạy thử tuyến đó một chiều mưa | Người đọc vì thích vùng |
| **Hỏi đáp** | Xe con đi được không, mùa mưa có sạt không | Người sắp đi |
| **Lịch sử** | Trước khi có đường này, người Nam Ban lên Đà Lạt bằng gì | Người ở lâu, thích chuyện cũ |

Bảy góc này **không đăng liền bảy ngày**. Rải trong 3–4 tuần, mỗi góc dẫn về cùng
một bài web. Facebook không phạt trùng chủ đề nếu góc khác nhau — nó phạt trùng chữ.

**Ý gốc khác đủ sức tách 7 góc:** cầu Tổng Đội · sân bay Liên Khương mở lại · tách
thửa từ 20/8/2026 · quy hoạch 2050 · mùa cà phê · hồ Bãi Công.

---

## 5. BỐN BÀI VIẾT SẴN — DÁN THẲNG

Viết đúng giọng, đúng luật. Chú đổi tên khu, đổi ảnh cho khớp thực tế rồi đăng.

---

### Bài 1 — dữ kiện (Thứ Hai tuần 1)

> Hồ Tròn ở Nam Ban, trong hồ sơ nó tên là hồ Ba Đình.
>
> Không ai gọi vậy. Người ở đây gọi Hồ Tròn, người bán đất cũng gọi Hồ Tròn. Nhưng
> khi ra xã hỏi giấy tờ, tra quy hoạch, hay đọc quyết định thì phải tìm chữ "Ba Đình"
> mới ra.
>
> Chuyện này không lạ ở Nam Ban. Vùng này do người miền Bắc lên lập từ 1975, nên
> tên trong hồ sơ mang tên quê cũ — Ba Đình, Từ Liêm, Thanh Trì, Gia Lâm, Đông Anh,
> Mê Linh. Còn tên người ta gọi hằng ngày thì mọc theo hình dáng, theo thói quen.
>
> Nó thành một cái bẫy nhỏ khi đi xem đất: người môi giới nói "lô này gần Hồ Tròn",
> mình lên bản đồ quy hoạch tìm Hồ Tròn không thấy, tưởng họ nói sai. Thật ra là hai
> tên của một chỗ.
>
> Nhà mình ai từng gặp trường hợp tên gọi và tên giấy tờ khác nhau ở Nam Ban chưa?
>
> Bản đầy đủ ở comment.
>
> #NamBan #LamHa #LamDong #HoTron

*Comment 1 (Trang tự đăng, ghim):* Hồ Tròn ở Nam Ban: trong giấy nó tên là hồ Ba Đình —
https://nambanpanorama.com/ho-tron-nam-ban

---

### Bài 2 — sửa hiểu nhầm (Thứ Ba)

> Chùa Linh Ẩn không nằm trong thành phố Đà Lạt.
>
> Rất nhiều người gọi là "chùa Linh Ẩn Đà Lạt", kể cả mấy trang du lịch lớn. Nhưng
> chùa nằm ở Nam Ban, cách trung tâm Đà Lạt khoảng 25 km, đi qua đèo Tà Nung chừng
> 45 phút.
>
> Chuyện này quan trọng với người đi chơi hơn là nghe qua. Có nhà đặt phòng ở Đà Lạt,
> sáng tính "ghé chùa rồi về ăn trưa", tới nơi mới biết là một chuyến đèo cả đi cả về
> gần hai tiếng chưa kể dừng.
>
> Đi thì nên gộp: chùa Linh Ẩn và thác Voi nằm sát nhau, cùng khu, thêm chợ Nam Ban
> nếu đi buổi sáng. Một buổi là đủ, không cần vội.
>
> Bản đầy đủ ở comment — có đường đi, giờ, và mấy chỗ hay bị nhầm.
>
> #NamBan #ChuaLinhAn #ThacVoi #LamDong

*Comment 1:* https://nambanpanorama.com/chua-linh-an-nam-ban

---

### Bài 3 — tiền (Thứ Tư)

> 500 triệu tới 1 tỷ ở Nam Ban mua được gì?
>
> Câu hay gặp nhất không phải "có lô vài tỷ nào đẹp", mà đúng là câu này. Không phải
> vài tỷ như nhiều người tưởng khi nghĩ tới đất ven Đà Lạt.
>
> Nói gọn, đây là mặt bằng tham khảo, không phải giá cố định:
>
> — **500 tới 800 triệu**: lô vài trăm mét vuông hoặc tính theo sào, ít thổ cư, xa
> trung tâm hơn một chút. Hợp người vốn chưa nhiều, mua mảnh đầu tiên, để dành, hoặc
> làm một mảnh vườn nhỏ.
>
> — **Khoảng 1 tỷ**: lô rộng hơn, thổ cư nhiều hơn, gần hơn. Nhiều lô ở tầm này có sẵn
> vườn cà phê trên đất, mua vô là có bóng mát, khỏi gây vườn từ đầu.
>
> Điều nên nhớ nằm ở chỗ khác: cùng một tầm tiền, cái mình đang chọn thật ra là **chọn
> bỏ cái gì** — rộng hay gần, nhiều thổ cư hay ít, có vườn sẵn hay đất trống. Không lô
> nào được hết mọi thứ trong tầm tiền đó. Càng xa trục ĐT.725, càng ít thổ cư, thì giá
> càng mềm — và đó là lý do người tìm đất rẻ hay phải lùi ra xa hơn.
>
> Biết trước mình bỏ cái nào thì đi xem đất nhẹ hơn nhiều.
>
> Anh chị đang tính tầm tiền này thì ưu tiên cái gì trước — rộng, gần, hay nhiều thổ cư?
>
> Bản đầy đủ ở comment.
>
> #NamBan #DatNamBan #LamHa #MuaDat

*Comment 1:* https://nambanpanorama.com/mua-dat-nam-ban-500-trieu-1-ty

---

### Bài 4 — nói ngược (Thứ Sáu)

> Có những lô đất ở Nam Ban tôi sẽ khuyên đừng mua.
>
> Không phải vì lô xấu. Vì nó không hợp với người đang hỏi.
>
> Lô rộng, view thung lũng, đường đất một quãng dài, giá mềm — đẹp thật. Nhưng nếu
> người hỏi là người tính lên ở hẳn, tuổi đã cao, không tự chạy xe được, thì cái đường
> đất đó sẽ trả lời thay cho mọi thứ còn lại ngay mùa mưa đầu tiên.
>
> Ngược lại, lô vuông vức sát đường nhựa mà không có view gì cả — nhiều người chê nhạt.
> Với đúng người thì đó lại là lô ít phải hối tiếc nhất.
>
> Chỗ dễ nhầm nằm ở câu hỏi: người ta hay hỏi "lô này có tốt không", còn câu dẫn tới
> quyết định đúng là "lô này tốt cho ai". Hai câu nghe giống nhau nhưng đi về hai phía
> khác hẳn.
>
> Nên khi có ai bảo lô nào cũng tốt, cũng tăng giá, cũng "để đâu chẳng lời" — chỗ đó
> chưa hỏi bạn định làm gì với miếng đất.
>
> Bản đầy đủ ở comment: 6 điều người ở đây thấy mà người mới thường bỏ qua.
>
> #NamBan #DatNamBan #LamDong

*Comment 1:* https://nambanpanorama.com/truoc-khi-xuong-tien

---

## 6. BA VIỆC CẦN CHÚ ĐƯA SỐ THẬT

Prompt 1, 6, 7 trong bộ Chú gửi đều cần dữ liệu của trang. Em không bịa số được.
Khi Chú dán mấy thứ dưới đây vào một lượt chat, em chạy tiếp:

1. **Ảnh chụp Meta Business Suite → Insights → 90 ngày.** Cần: tiếp cận, tương tác,
   follow tăng/giảm, và **giờ người theo dõi online**. Giờ online quyết định mục 1.10
   ở trên — hiện em đang dùng suy đoán theo tệp, có số thật thì chỉnh lại cho đúng.
2. **5 bài có tiếp cận cao nhất và 5 bài thấp nhất** — dán nguyên caption. Có đủ 10 bài
   thì tìm ra được **mẫu chung**: hook kiểu nào chạy, độ dài nào chạy, ảnh kiểu nào chạy.
   Đó là prompt 6, và nó chỉ có giá trị khi so bài thật của trang mình.
3. **Trang đang có bao nhiêu follow, mục tiêu bao nhiêu, trong bao lâu.** Không có mốc
   thì không đo được, mà không đo được thì tháng sau vẫn đăng theo cảm tính.

---

## 7. ĐO GÌ, VÀ ĐỪNG ĐO GÌ

**Đo ba con số này thôi:**
- **Số người mới theo dõi mỗi tuần** — trang có lớn không.
- **Số click sang web mỗi tuần** — phễu có chảy không. Xem ở Search Console, nguồn
  giới thiệu Facebook.
- **Số bình luận là câu hỏi thật** (không tính "hay quá", "quan tâm") — trang có tạo
  ra người đang thật sự cân nhắc không.

**Đừng đo lượt thích.** Nó lên xuống theo phân phối chứ không theo chất lượng bài, và
đuổi theo nó sẽ kéo giọng trang về phía viral — đúng chỗ mình đang tránh.

**Ngưỡng để đổi hướng:** chạy đủ **4 tuần** rồi mới đọc số. Dưới 4 tuần thì cái mình
nhìn thấy là nhiễu, không phải xu hướng.

---

## 8. BA CHỖ DỄ TRƯỢT LANE

Ghi lại để lượt sau không phải nghĩ lại:

1. **Có người inbox hỏi giá lô cụ thể.** Trả lời được, nhưng trả lời **trong inbox**,
   không kéo ra bài đăng. Trên tường thì chỉ dẫn sang bài web. Tường là mặt publication.
2. **Có bài lên tự nhiên, nhiều người vào.** Cám dỗ là đăng liền một bài bán ngay sau
   đó để "tận dụng". Đừng. Đăng bài dữ kiện tiếp theo như lịch — người mới vào cần
   thấy trang này đều đặn là chỗ đọc, không phải chỗ chốt.
3. **Có người bình luận sai dữ kiện.** Sửa bằng dữ kiện, có nguồn, một câu, không gắt.
   Đây là chỗ người lạ nhìn vào để quyết định có tin trang này không — quan trọng hơn
   cả bài đăng.
