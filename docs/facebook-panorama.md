# Facebook cho Panorama — bộ vận hành

Bản dựng 9/9/2026. Chuyển bộ 7 prompt Chú đưa sang chất liệu Panorama.

Đọc `CLAUDE.md` §2 trước khi viết bất cứ dòng nào lên Facebook. Trang Facebook là
**cánh tay của publication**, không phải kênh bán. Người ta đọc xong phải thấy
"chỗ này biết chuyện", không phải "chỗ này đang gạ mình".

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
