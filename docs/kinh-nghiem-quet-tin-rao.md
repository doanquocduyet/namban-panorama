# Kinh nghiệm quét tin rao từ bộ đo Namban Index — viết cho ô Villas (26/9/2026)

Tài liệu nội bộ. Rút từ `tools/survey/crawl.py`, `tools/survey/aggregate.py` và
`.github/workflows/index-weekly.yml` của Panorama — mọi điều dưới đây là cái bộ đo đang
chạy thật, không phải lý thuyết.

---

## 0. Nói thật trước: vì sao Panorama "ra nhiều tin hơn"

Hai bên **đếm hai thứ khác nhau**, không phải bên nào đọc giỏi hơn:

| | Panorama (Namban Index) | Villas (trang tin rao) |
|---|---|---|
| Đếm gì | Mọi tin **còn đang rao** ngày quét, đăng lúc nào cũng tính | Chỉ tin **đọc được ngày đăng thật**, đã mở lại nguồn kiểm |
| Lượt 25/9/2026 | 634 tin | 318 tin (tháng 6 → 24/9) |
| Mạnh ở | Độ phủ: thấy gần hết hàng đang bày bán | Độ đúng: ngày, giá, khu đã đối chiếu từng tin |

Vì vậy đừng bỏ bước kiểm của Villas để chạy theo số lượng. Cái Villas nên học là **cách
mở rộng độ phủ** (mục 1–4) — rồi vẫn giữ bước kiểm như cũ. Tin nào không kiểm được ngày
thì vẫn có ích: đưa vào nhóm "tin còn đang rao", không đưa vào nhóm "tin theo ngày đăng".

---

## 1. Vào từ đúng cửa: trang danh sách theo TỪNG ĐƠN VỊ CŨ

Các sàn vẫn xếp tin theo **tên hành chính cũ** (trước 1/7/2025). Chỉ tìm "xã Nam Ban
Lâm Hà" là mất phần lớn tin. Bộ đo vào **5 cửa** cho mỗi sàn:

- xã Nam Ban Lâm Hà (tên mới, nếu sàn đã có)
- thị trấn Nam Ban · xã Đông Thanh · xã Mê Linh · xã Gia Lâm (tên cũ)

Cửa nào đã biết là khu gì thì gắn sẵn khu cho mọi tin lấy từ cửa đó (khi tin không tự
ghi khu). Danh sách cửa đang dùng: xem phiếu 25/9 đã gửi (guland, datnenlamdong,
batdongsanonline, thuviennhadat, muaban, mogi).

## 2. Tự dò cách phân trang, đừng viết tay cho từng sàn

Mỗi sàn phân trang một kiểu. Bộ đo thử lần lượt 6 kiểu cho **trang 2**, kiểu nào ra link
mới thì dùng kiểu đó cho trang 3, 4… và **dừng khi một trang không ra link mới** (tối đa
30 trang):

`/trang/2/` · `/page-2/` · `/trang--2.html` · `?page=2` · `?p=2` · `?cp=2`

Lọc link tin bằng mẫu URL riêng của từng sàn (vd guland chỉ lấy link có `/post/`), bỏ
tham số `?…` và `#…` trước khi so trùng.

## 3. Đọc trang chi tiết theo tầng — tầng nào có thì dùng, không có thì xuống tầng dưới

1. **JSON-LD** trong trang (nhiều sàn có sẵn): `datePosted`/`datePublished`, `price`,
   `address`, `floorSize`. Chính xác nhất, ưu tiên số 1.
2. Thẻ `meta article:published_time` hoặc `<time datetime>`.
3. Chữ trong trang: "Ngày đăng …", "Diện tích …", "Mức giá …".
4. Chỗ riêng của từng sàn (vd guland: ô giá `.dtl-prc__ttl`, ô diện tích `.dtl-prc__dtc`).
5. Địa chỉ: breadcrumb, không có thì cụm "xã/thị trấn …" trong tiêu đề.

## 4. Bộ đọc số tiền, diện tích, ngày — chỗ hay sai nhất

- **Tiền:** hiểu `1 tỷ 350 triệu`, `1 tỷ 3`, `1,65 tỷ`, `1.599 tỷ` (dấu chấm hay phẩy sau
  "tỷ" đều là thập phân), `850 triệu`, `850tr`. Phân biệt **giá cả lô / giá mỗi m² /
  giá mỗi sào / giá mỗi lô-nền**. "Thỏa thuận", "liên hệ" không có số → bỏ.
- **Sào = 1.000 m²** (Tây Nguyên). Giá "X/sào" thì chia 1.000 ra giá/m², **không chia
  cho diện tích cả lô**.
- **Diện tích:** m², m2, "mét vuông", ha (×10.000), sào (×1.000); chỉ nhận 10–500.000 m².
- **Ngày:** `dd/mm/yyyy`, `yyyy-mm-dd`, "3 ngày trước", "hôm qua". Ngày suy ra từ
  "… trước" gắn cờ **ước lượng**, không trộn với ngày thật. Guland hay hiện **ngày cập
  nhật** chứ không phải ngày đăng → tách riêng, không đếm là ngày đăng.
- **Chặn số vô lý:** giá/m² ngoài 100 nghìn – 100 triệu, hoặc giá cả lô ngoài 50 triệu –
  200 tỷ → bỏ (thường là gõ nhầm đơn vị).

## 5. Phân khu: địa chỉ trước, tiêu đề sau, có danh sách loại trừ

- Đọc **địa chỉ trước** (đáng tin hơn), tiêu đề sau.
- Danh sách **loại trừ**: Nam Hà, Phi Tô, Tà Nung, Đinh Văn, Đạ Đờn, Tân Hà, Tân Văn,
  Phú Sơn, Liên Hà, Hoài Đức, Phúc Thọ, Đan Phượng, Tân Thanh, Bảo Lộc, Di Linh, Đức
  Trọng, Lạc Dương, Đơn Dương, Cam Ly… Địa chỉ dính một tên loại trừ → ngoài xã.
- Danh sách **nhận**: Đông Thanh, Mê Linh (kể cả Buôn Chuối), Gia Lâm, và các mốc chỉ có
  ở Nam Ban (Thăng Long, Chi Lăng, Bãi Công, Từ Liêm, Thanh Trì, Linh Ẩn, thác Voi, Tổng
  Đội, Ba Đình, ĐT.725…).
- Tiêu đề vừa có tên nhận vừa có tên loại trừ → ghi **"mơ hồ"**, không đoán.

## 6. Gộp tin trùng giữa các sàn

Một lô thường rao trên 2–4 sàn. Coi là **cùng một lô** khi: cùng khu + diện tích lệch
≤ 2 % + giá lệch ≤ 3 %. Giữ bản có URL gốc và ngày chắc nhất. Khi so với nguồn không
ghi khu rõ (vd bản tổng hợp) thì **bỏ điều kiện khu**, chỉ so diện tích + giá.

## 7. Chạy lịch sự để không bị chặn

- Đọc `robots.txt` của **từng URL** trước khi mở; bị cấm thì bỏ, ghi lại.
- Nghỉ **1,5 giây** giữa hai lần mở cùng một trang; tự giới thiệu bằng User-Agent có tên
  web và đường dẫn liên hệ.
- Mỗi nguồn tối đa ~450 tin một lượt.
- **Mỗi nguồn một máy, chạy song song** (GitHub Actions matrix): mỗi máy chỉ gọi một sàn
  nên vẫn lịch sự với từng sàn, mà cả lượt xong trong ~25 phút thay vì ~60.
- Guland chặn một số dải IP (máy trợ lý bị 403) nhưng máy GitHub đọc được — **bị chặn
  thì đổi chỗ chạy**, không vượt Cloudflare/captcha.

## 8. Luật dừng — thà không đăng còn hơn đăng số sai

Bộ đo tự dừng, **không sửa trang**, khi:
- một nguồn tuần trước có tin mà tuần này về 0 (nghi bị chặn hoặc sàn đổi giao diện);
- ít hơn 15 tin mới trong tuần (chỉ xét khi lần đo trước đã cách ≥ 6 ngày);
- trung vị một nhóm (≥ 30 tin cả hai tuần) nhảy quá 25 %;
- tổng dưới 100 tin sau gộp trùng; hoặc lô của chính web mình chiếm quá 40 %.

## 9. Lưu ngay — tin mất rất nhanh

Sàn gỡ tin sau 2–3 tháng. Nên: quét đều (Villas mỗi sáng, Panorama mỗi tuần), và **tháng
đã qua không bao giờ bị tính lại bằng mẫu nhỏ hơn** — nếu không, tháng 6 sẽ tự tụt dần
khi tin tháng 6 biến mất khỏi mạng.

## 10. Chỉ giữ số, không giữ người

Không lưu tiêu đề, mô tả, ảnh, số điện thoại, tên người đăng. Tiêu đề chỉ dùng trong bộ
nhớ để phân khu rồi bỏ. Dòng thô giữ 30 ngày trong artifact của lượt chạy, không vào repo;
danh sách tin đã thấy chỉ lưu mã băm.

---

## 11. Mạng xã hội — nói thẳng cái được và cái không

Bộ đo Panorama **không quét mạng xã hội**. Cho Villas tham khảo:

- **YouTube (video môi giới):** được — trang công khai, Villas đang làm đúng (`yt-dlp`,
  nghỉ ~3 giây, lưu bộ nhớ đệm). Đây là nguồn mạnh nhất cho tháng cũ.
- **Nhóm Facebook, Zalo, TikTok:** phần lớn nằm sau đăng nhập, và điều khoản cấm quét tự
  động. **Không tự động hóa** (sai luật đã chốt: không cào dữ liệu sau đăng nhập, không
  vượt chặn). API chính thức của Facebook/TikTok cho nội dung công khai chỉ cấp cho nhà
  nghiên cứu hoặc qua xét duyệt — không thực tế cho một web nhỏ.
- **Cách hợp lệ để lấy tin mạng xã hội:** mở một "hộp nhận tin" — môi giới, người quen,
  chính Chú gửi **đường dẫn** tin (Zalo/Facebook công khai) vào một chỗ; bộ đọc mở đúng
  link công khai đó, kiểm như mọi tin khác. Người gửi tự nguyện, không cào.

---

*Kèm: phiếu 25/9/2026 "đọc chung nguồn với Namban Index" (danh sách 6 sàn + khuôn trang
tin rao phải giữ để bộ đo Panorama đọc được).*
