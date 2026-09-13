# Rà khối liên hệ cuối bài — đếm và phân loại

Chạy 13/9/2026. **Chỉ đếm và phân loại, không gắn khối nào, không sửa file nào.**

## Cách quét — đọc trước khi tin con số

**Khối liên hệ KHÔNG nằm trong HTML.** Nó do `panorama-utils.js` chèn lúc chạy, theo danh
sách slug `IN` ở đầu file. Nên grep markup sẽ ra 0 ở mọi bài — phải đọc danh sách `IN`.

**Ba hệ template, không bám một class.** Mốc dự phòng dùng để nhận ra một trang là bài viết:
`<div class="art-body"` · `<div class="body"` · `<article` · `<div class="tldr"` · `class="share-row"`.
Bản quét đầu chỉ có ba mốc đầu và **loại nhầm `/doc-lo-dat`** — bài đó dùng
`<section class="wrap">` + `.idx-list`, là hệ thứ ba. Đã nới mốc.

## Phạm vi

- File `.html` toàn repo: **189**
- Trong phạm vi (bài viết `lang="vi"`, có index): **156**
- Bị loại: **33**

| File bị loại | Lý do |
|---|---|
| `nam-ban-co-gi-moi` | hub/chức năng — dòng thời gian tin |
| `nam-ban` | hub/chức năng — hub Về Nam Ban |
| `dat` | hub/chức năng — hub Về Đất |
| `hoi-nhanh` | hub/chức năng — hub hỏi-đáp |
| `dau-tu` | hub/chức năng — hub Đầu tư |
| `nam-ban-co-gi` | hub/chức năng — hub điểm đến |
| `namban-index` | hub/chức năng — trang chỉ số giá |
| `index` | hub/chức năng — trang chủ |
| `trao-doi` | hub/chức năng — trang liên hệ |
| `cau-chuyen-nam-ban` | hub/chức năng — trang tuyển tập |
| `doc-nhanh` | hub/chức năng — trang tuyển tập |
| `elephant-waterfall-nam-ban` | không phải lang="vi" |
| `living-in-nam-ban` | không phải lang="vi" |
| `en/foreigners-buying-land-nam-ban` | không phải lang="vi" |
| `en/index` | không phải lang="vi" |
| `en/land-prices-nam-ban` | không phải lang="vi" |
| `en/nam-ban-master-plan-2050` | không phải lang="vi" |
| `en/nam-ban` | không phải lang="vi" |
| `en/trao-doi` | không phải lang="vi" |
| `fr/cascade-des-elephants-nam-ban` | không phải lang="vi" |
| `fr/vivre-a-nam-ban` | không phải lang="vi" |
| `ja/nam-ban-kurashi` | không phải lang="vi" |
| `ja/nam-ban-zou-no-taki` | không phải lang="vi" |
| `ko/nam-ban-kokkiri-pokpo` | không phải lang="vi" |
| `ko/nam-ban-salm` | không phải lang="vi" |
| `zh/nam-ban-daxiang-pubu` | không phải lang="vi" |
| `zh/zai-nam-ban-shenghuo` | không phải lang="vi" |
| `404` | noindex |
| `_mau-bai-viet` | noindex |
| `demo-hop-tac` | noindex |
| `demo-phuong-phap` | noindex |
| `demo-selection` | noindex |
| `demo-ve-panorama` | noindex |

> `namban-index` nằm trong `IN` nhưng bị loại khỏi phạm vi vì là trang chỉ số giá, không phải bài.
> Nó có khối liên hệ và điều đó đúng — chỉ là không đếm vào hai danh sách dưới.

---

## A1 — Đã có khối liên hệ (78 bài)

| slug | H1 |
|---|---|
| `10-10-1975-nam-ban` | 10/10/1975: ngày người Hà Nội bắt đầu câu chuyện Nam Ban |
| `ban-dat-nam-ban` | Bán đất Nam Ban: vì sao lô này ra hàng, lô kia nằm mãi |
| `ban-do-quy-hoach-nam-ban` | Bản đồ quy hoạch Nam Ban đến 2050: vùng nào nên, vùng nào không nên xuống tiền |
| `brief-02` | Ở Nam Ban, loại đất nào đang có người mua thật? |
| `brief-03` | Đất 1.000m² ở Nam Ban: vì sao lô nào cũng chừng đó? |
| `cau-tong-doi-nam-ban` | Cầu Tổng Đội Nam Ban xây mới: khởi công 14/7/2026, xong tháng 11/2027 |
| `cay-xang-petro-moi-o-nam-ban` | 2 cây xăng Petro mới trên trục 725 Nam Ban — một tín hiệu nhỏ đáng chú ý |
| `chi-phi-dat-dai-nam-ban` | Chi phí đất đai ở Nam Ban: những khoản tiền có thể phát sinh |
| `chuan-bi-truoc-khi-ban-dat-nam-ban` | Bán đất Nam Ban: cần làm gì trước khi rao? |
| `coc-dat-nam-ban` | Cọc đất Nam Ban: cọc bao nhiêu, giấy viết thế nào cho chắc |
| `dai-hoc-da-lat-nam-ban` | Nam Ban và Đại học Đà Lạt ngồi lại với nhau |
| `dat-gan-da-lat` | Đất gần Đà Lạt: vì sao nhiều người tìm về Nam Ban |
| `dat-giap-ho-nam-ban` | Mua đất giáp hồ ở Nam Ban: cần xem gì trước khi xuống tiền? |
| `dat-giap-rung-thong-nam-ban` | Mua đất giáp rừng thông ở Nam Ban: được gì, mất gì |
| `dat-giap-suoi-nam-ban` | Mua đất giáp suối ở Nam Ban: cần xem gì trước khi xuống tiền? |
| `dat-nam-ban-chua-xay` | Có đất Nam Ban nhưng chưa xây nhà |
| `dat-nam-ban-cuoi-tuan` | Mua đất Nam Ban để cuối tuần lên chơi chọn khác gì mua để ở? |
| `dat-nam-ban-duong-dat` | Đất Nam Ban đường đất, view đẹp: mua rồi làm đường có đáng không? |
| `dat-nam-ban-kinh-doanh-gi` | Mua đất Nam Ban kinh doanh gì? |
| `dat-nam-ban-tho-cu-san` | Lô Nam Ban đã làm đẹp, thổ cư sẵn, tách sẵn: có đáng trả thêm không? |
| `dat-nam-ban-trong-cay-gi` | Đất Nam Ban trồng cây gì có dòng tiền? |
| `dat-nam-ban-xuong-gia-ban-hay-giu` | Mua đất Nam Ban rồi giá xuống: nên bán hay giữ? |
| `dau-tam-nam-ban` | Vì sao trên đất Nam Ban có nhiều vườn dâu tằm |
| `dinh-gia-dat-nam-ban` | Định giá đất Nam Ban: vì sao hai lô đất lại khác giá? |
| `doc-lo-dat` | Thẩm định lô đất Nam Ban: đọc pháp lý, giá, rủi ro |
| `doc-lo-dat-02-view-ho` | 2.300m² view hồ, 5,75 tỷ: đọc thẳng một lô đất Nam Ban |
| `doc-the-dat-nam-ban` | Đọc thế đất Nam Ban: dốc, taluy, và chỗ nước từng chảy qua |
| `duong-ha-bac-nam-ban` | Đường nhựa Hà Bắc Nam Ban – Mê Linh (tuyến T-20) |
| `giu-dat-nam-ban-tu-xa` | Mua đất Nam Ban xong, ở xa thì giữ đất kiểu gì |
| `ho-bai-cong-nam-ban` | Hồ Bãi Công ở Nam Ban |
| `ho-me-linh-nam-ban-cam-ly-thuong` | Hồ Mê Linh Nam Ban – đập Cam Ly Thượng: góc hồ giáp Tà Nung Đà Lạt |
| `ho-o-nam-ban` | Hồ ở Nam Ban: những cái có tên trong hồ sơ |
| `ho-thanh-tri-nam-ban` | Hồ Thanh Trì ở Nam Ban: thật ra là hai hồ |
| `ho-tu-liem-nam-ban` | Hồ Từ Liêm ở Nam Ban: đường vào, khu dân cư quanh hồ và đất khu này |
| `hoa-o-nam-ban` | Nam Ban trồng được hoa gì? |
| `homestay-nam-ban-co-lai-khong` | Kinh doanh homestay ở Nam Ban có lãi không? |
| `khu-nao-o-nam-ban` | Khu nào ở Nam Ban? Cách đọc một địa chỉ trước khi đi xem đất |
| `kinh-nghiem-mua-dat-nam-ban` | Kinh nghiệm mua đất Nam Ban: những điều nên biết trước khi quyết định mua |
| `len-tho-cu-het-bao-nhieu-tien` | Lên thổ cư ở Nam Ban hết bao nhiêu tiền? |
| `lo-dat-nam-ban-binh-thuong` | Lô đất Nam Ban bình thường, không có gì nổi bật: hợp với ai? |
| `loi-di-chung-dat-nam-ban` | Đất Nam Ban có lối đi chung, đất đi nhờ đường: mua thì cần nhìn gì |
| `mua-chung-dat-nam-ban` | Mua chung đất Nam Ban có nên không? |
| `mua-dat-co-vuon-bo` | Mua đất có sẵn vườn bơ ở Nam Ban: cây bơ tính thế nào? |
| `mua-dat-co-vuon-ca-phe` | Mua đất có sẵn vườn cà phê ở Nam Ban: cây tính thế nào? |
| `mua-dat-da-lat-chon-nam-ban` | Nhiều người tính mua đất Đà Lạt, cuối cùng lại dừng ở Nam Ban |
| `mua-dat-duong-gia-nam-ban` | Mua đất dưỡng già ở Nam Ban: nhà vườn cho vợ chồng về hưu |
| `mua-dat-nam-ban` | Mua đất Nam Ban: những câu hỏi thường gặp |
| `mua-dat-nam-ban-co-nguoi-dang-canh-tac` | Mua đất Nam Ban đang có người canh tác: cần nhìn gì trước khi xuống tiền |
| `mua-dat-nam-ban-de-lam-gi` | Mua đất Nam Ban để làm gì? |
| `mua-dat-nam-ban-hop-dong-uy-quyen` | Mua đất Nam Ban bằng hợp đồng ủy quyền: cần biết gì? |
| `mua-mua-nam-ban` | Mùa mưa Nam Ban ra sao? |
| `mua-nha-nam-ban-khong-o` | Mua nhà Nam Ban xong mà không lên ở |
| `mua-nha-xay-san-nam-ban` | Mua nhà xây sẵn ở Nam Ban: nhìn gì ngoài phần hoàn thiện? |
| `mua-vuon-ca-phe-nam-ban` | Mua vườn cà phê Nam Ban có dòng tiền thật không? |
| `nam-ban-hay-di-linh` | Nam Ban hay Di Linh? Nếu hỏi một người đã đi về nhiều năm. |
| `nam-ban-hay-don-duong` | Nam Ban hay Đơn Dương? |
| `nam-ban-thuoc-xa-nao` | Nam Ban thuộc xã nào sau sáp nhập? |
| `nam-ban-va-nam-ha` | Nam Ban và Nam Hà: khác nhau ở đâu? |
| `nha-go-nam-ban` | Xây nhà gỗ làm second home ở Nam Ban: những điều cần biết |
| `nha-go-thong-nam-ban` | Nhà gỗ thông ở Nam Ban: vì sao chỗ rẻ chỗ đắt, và có nên làm thép tiền chế? |
| `quy-hoach-2050` | Quy hoạch Lâm Đồng 2050: Nam Ban nằm ở đâu trên bản đồ mới? |
| `quy-trinh-mua-dat-nam-ban` | Quy trình mua đất Nam Ban đi qua những bước nào? |
| `rau-hoa-cay-do-la-nam-ban` | Rau, hoa và cây đô la ở Nam Ban |
| `san-bay-lien-khuong-mo-lai` | Sân bay Liên Khương mở lại 19/8/2026: Nam Ban được gì, không được gì |
| `sap-nhap-nam-ban-dat` | Sáp nhập ảnh hưởng gì tới giá đất Nam Ban? |
| `so-sanh-nam-ban-bao-loc-da-lat` | Nam Ban hay Bảo Lộc, Đà Lạt? |
| `tiem-nang-dau-tu` | Tiềm năng đầu tư Nam Ban: đọc cơ hội qua lăng kính toàn cảnh |
| `tram-sac-nam-ban` | Nam Ban có mấy trạm sạc VinFast? |
| `truoc-khi-xuong-tien` | Mua đất Nam Ban cần lưu ý gì: 6 điều người ở đây thấy, người mới không thấy |
| `vi-sao-nam-ban-nhieu-giao-dich` | Vì sao đất Nam Ban nhiều người mua bán hơn các vùng ven Đà Lạt khác? |
| `view-panorama-nam-ban` | View Panorama Nam Ban: view hồ, view suối, view rừng thông khác nhau thế nào? |
| `vua-mua-dat-nam-ban-lam-gi` | Vừa mua đất Nam Ban xong — làm gì tiếp |
| `vuon-bo-loi-bao-nhieu` | Một sào bơ ở Nam Ban cho bao nhiêu tiền? Bóc phép tính người ta hay dùng để… |
| `xay-nha-giap-ho-nam-ban` | Xây nhà giáp hồ ở Nam Ban: những điều cần biết |
| `xay-nha-giap-rung-thong-nam-ban` | Xây nhà giáp rừng thông ở Nam Ban: những chỗ phải tính khác |
| `xay-nha-giap-suoi-nam-ban` | Xây nhà giáp suối ở Nam Ban: điều cần biết |
| `xay-nha-nho-nam-ban-bao-nhieu-tien` | Xây một căn nhỏ ở Nam Ban hết bao nhiêu tiền? |
| `xem-dat-nam-ban-chua-mua-duoc` | Đi xem đất Nam Ban nhiều lần mà chưa mua được |

---

## A2 — Chưa có khối liên hệ (78 bài)

Nhãn gắn bằng tiêu chí máy đếm được trên slug + H1, **không phán đoán nội dung**.
Bài rơi vào hai nhóm thì ghi cả hai.

| slug | nhãn | chuyên mục | H1 | câu mở bài |
|---|---|---|---|---|
| `chuyen-muc-dich-su-dung-dat-nam-ban` | **ĐẤT** | Về Đất | Chuyển mục đích sử dụng đất Nam Ban 2026: lúc nhiều,… | Tôi ngồi rà hồ sơ đất đai của xã mấy tháng nay, thấy một quãng ký dày bất thường. Rồi ngừng. Rồi lại ký. Nhìn từng cái chẳng ra gì — xếp theo thời… |
| `co-nen-mua-dat-nam-ban-o-xa` | **ĐẤT + VÙNG** | Về Nam Ban | Có nên mua đất Nam Ban để ở? Điều nhiều người chỉ hiểu… | Có nên mua đất Nam Ban để ở? Có, nếu bạn tìm một nơi ở lâu dài, gần Đà Lạt nhưng yên tĩnh, khí hậu ôn hòa quanh năm và có thể sống thật. Không phù… |
| `dat-dong-thanh-nam-ban` | **ĐẤT** | Về Đất | Đất Đông Thanh ở Nam Ban thế nào? | Chạy về phía Đông Thanh, đường có đoạn mở rộng ra, rồi thi thoảng lại có một khúc nhìn xuống được cả một vùng thung lũng phía dưới. Cảnh đổi liên tục. |
| `dat-gia-lam-nam-ban` | **ĐẤT** | Về Đất | Đất Gia Lâm ở Nam Ban thế nào? | Chạy vào Gia Lâm, thứ đập vào mắt trước tiên không phải nhà cửa, mà là vườn. Vườn dâu, vườn cà phê, rồi sân phơi trải dọc đường, thi thoảng một… |
| `dat-me-linh-nam-ban` | **ĐẤT** | Về Đất | Đất Mê Linh ở Nam Ban thế nào? | Đi từ Đà Lạt qua đèo Tà Nung, chỗ đầu tiên của Nam Ban mà mình chạm tới là Mê Linh. Đường nhỏ hơn, đồi nhiều hơn, cà phê trải dài, và cái không khí… |
| `dat-nguon-goc-lam-nghiep-nam-ban` | **ĐẤT + VÙNG** | Về Đất | Mua đất rừng ở Nam Ban được không? Đất có nguồn gốc… | Không phải để dọa. Cũng không phải cứ nghe chữ "lâm nghiệp" là tránh. |
| `dat-the-am-the-duong` | **ĐẤT + VÙNG** | Về Đất | Thế đất âm, thế đất dương: đọc đất cao thấp hơn đường… | Tôi đi xem đất nhiều, nên có một thói quen: chưa hỏi giá, tôi đi hết lô một vòng trước. Đất đang nghiêng về đâu, đường ở đâu, nước sẽ chạy về đâu —… |
| `dat-trung-tam-nam-ban` | **ĐẤT** | Về Đất | Đất khu trung tâm Nam Ban thế nào? | Ai lên Nam Ban lần đầu thường đặt chân tới khu trung tâm trước. Đây là chỗ có chợ, có hàng ăn, cà phê, xe cộ qua lại — cái nhịp của một thị trấn nhỏ… |
| `dat-vuon-nam-ban-xay-duoc-gi` | **ĐẤT** | Về Đất | Đất vườn Nam Ban xây được gì? Quy định mới từ 20/8/2026 | Đứng trong vườn, câu anh em hỏi tôi nhiều nhất là: "Miếng này làm cái chòi được không anh?" |
| `do-dac-dat-nam-ban` | **ĐẤT + VÙNG** | Về Đất | Đo đạc đất Nam Ban: đất ngoài đường có giống trên sổ… | Tôi để ý chuyện này vì nó chạm đúng một việc rất đời: mình đứng trên đất mỗi ngày, nhưng lúc mở sổ ra chưa chắc hai bên đã nói cùng một con số. |
| `gia-ca-phe-va-gia-dat-nam-ban` | **ĐẤT + VÙNG** | Về Đất | Giá cà phê tăng thì giá đất Nam Ban có tăng theo không? | Có liên quan, nhưng không phải cứ giá cà phê tăng là giá đất Nam Ban tăng ngay. Ở một vùng nông nghiệp như Nam Ban, cà phê được giá làm dòng tiền… |
| `ho-tron-nam-ban` | **ĐẤT + VÙNG** | Về Nam Ban | Hồ Tròn ở Nam Ban: trong giấy nó tên là hồ Ba Đình | Người mới lên hay hỏi: sao giữa cao nguyên lại có Ba Đình, Đống Đa, Gia Lâm, Đông Anh, Thanh Trì, Từ Liêm. |
| `mua-dat-nam-ban-500-trieu-1-ty` | **ĐẤT + VÙNG** | Đầu tư | Mua đất Nam Ban: 500 triệu đến 1 tỷ mua được gì? | Người hỏi mua đất Nam Ban, câu hay gặp nhất không phải “có lô vài tỷ nào đẹp”, mà là “tầm năm trăm, một tỷ thì mua được gì”. Đó là một trong những… |
| `nam-ban-hay-duc-trong` | **ĐẤT + VÙNG + SO SÁNH** | Về Đất | Nam Ban hay Đức Trọng: nên sống và mua đất ở đâu? | Nếu đang tìm một vùng quanh Đà Lạt để sống, mua đất, làm một căn nhỏ cuối tuần, hoặc chỉ đơn giản là kiếm chỗ để dành cho vài năm nữa — kiểu gì cũng… |
| `nam-ban-hay-lac-duong` | **ĐẤT + VÙNG + SO SÁNH** | Về Đất | Nam Ban hay Lạc Dương: nên chọn vùng nào để ở và mua… | Ai tìm đất vùng ven Đà Lạt, sớm muộn cũng đặt hai cái tên này cạnh nhau. Cùng cao nguyên, cùng mát, cùng có đất vườn — mà tính nết khác nhau khá xa. |
| `nen-xem-khu-nao-o-nam-ban` | **ĐẤT** | Về Đất | Nam Ban, Đông Thanh, Mê Linh, Gia Lâm: nên xem khu nào… | Người mới lên Nam Ban hay tưởng đây là một chỗ. Chạy vài vòng mới vỡ ra: trong cùng cái tên Nam Ban có tới bốn vùng, mỗi vùng một tính nết. |
| `nguoi-ngoai-tinh-mua-dat-nam-ban` | **ĐẤT + VÙNG** | Về Đất | Người ở tỉnh khác mua đất Nam Ban: có sổ và chưa có sổ… | Chuyện này tôi hay phải nói lại với người dưới phố lên. Đọc trên mạng thấy "luật mới bỏ điều kiện hộ khẩu rồi" nên yên tâm. Đúng — nhưng đúng ở một… |
| `nhan-tien-den-bu-dat-nen-lam-gi` | **ĐẤT** | Về Đất | Nhận tiền đền bù đất rồi nên làm gì? | Tôi không có lời khuyên chung cho mọi người. Vì mỗi khoản tiền đến từ một câu chuyện khác nhau. |
| `o-thu-nam-ban-truoc-khi-mua-dat` | **ĐẤT + VÙNG** | Về Đất | Ở thử Nam Ban trước khi mua đất | Tôi để ý mấy năm nay có một kiểu người khôn: chưa vội mua đất, mà lên thuê ở vài tháng cho biết trước đã. Ban đầu tôi thấy lạ, sau mới thấy đó là… |
| `quy-hoach-chung-nam-ban` | **ĐẤT + VÙNG** | Đầu tư | Quy hoạch chung Nam Ban Lâm Hà đến 2050: 7 khu vực… | Mấy hôm nay anh em hỏi tôi về bản quy hoạch mới. Có người xuống xem đất, mở bản đồ lên, thấy màu xanh màu vàng rồi bắt đầu tính giá. |
| `tach-thua-dat-nam-ban` | **ĐẤT** | Về Đất | Tách thửa đất Nam Ban: diện tích tối thiểu từ 20/8/2026 | Đứng ngoài đất, câu anh em hỏi tôi nhiều nhất vẫn là: "Miếng này có tách được không?" |
| `tra-cuu-dat-nam-ban` | **ĐẤT** | Về Đất | Tra cứu thông tin thửa đất Nam Ban thế nào? | Đi coi đất với khách, kiểu gì cũng có người vừa đứng ở lô vừa rút điện thoại ra: “thửa này tra được thông tin gì không anh?”. Ngày trước câu đó phải… |
| `xay-nha-o-nam-ban` | **ĐẤT** | Về Đất | Xây nhà ở Nam Ban, mấy điều nên biết trước khi khởi công | Mấy năm nay người ta lên Nam Ban xây nhà nhiều. Nhà mọc lên từng cái, mà chuyện dở khóc dở cười cũng không ít. Nên viết ra đây cho ai sắp xây, đọc… |
| `5km-o-nam-ban` | **KHÁC** | Về Nam Ban | Ở Nam Ban, 5 km có gần không? | Có một lỗi rất dễ mắc khi nhìn Nam Ban trên bản đồ. |
| `ai-nam-ban` | **KHÁC** | Về Nam Ban | AI Nam Ban: Nam Ban có AI không? | Nghe “AI Nam Ban” là thấy hơi buồn cười. Một vùng trồng cà phê, sáng ra sương còn đọng trên lá, thì AI ở chỗ nào? |
| `an-gi-o-nam-ban` | **KHÁC** | Về Nam Ban | Ăn gì ở Nam Ban? | Người mới tới Nam Ban hay hỏi: ở đây ăn uống có gì? |
| `brief` | **KHÁC** | Brief | Panorama Brief | Bản tin về đất và vùng Nam Ban. Không định kỳ — ra khi có đủ thứ đáng nói. |
| `brief-01` | **KHÁC** | Đầu tư | Nam Ban không còn là Nam Ban? Bản đồ vừa được vẽ lại | Nếu trong sáu tháng qua có ai chào bạn một lô đất "ở thị trấn Nam Ban", họ đang nói về một nơi không còn tồn tại trên giấy tờ hành chính. |
| `ca-phe-nam-ban` | **VÙNG** | Về Nam Ban | Nam Ban trồng được những loại cà phê nào? | Nam Ban trồng được cả Robusta lẫn Arabica — hai loài cà phê chính, và không nhiều vùng có cả hai. Lý do nằm ở độ cao: vườn cà phê ở đây quanh… |
| `ca-phe-nam-ban-ai` | **VÙNG** | Về Nam Ban · Cập nhật | Cà phê Nam Ban và AI: King Coffee khảo sát số hóa vùng… | Trong năm 2026, lãnh đạo xã Nam Ban Lâm Hà làm việc với Công ty TNHH TNI King Coffee và Học viện AI Coffee Academy về ứng dụng trí tuệ nhân tạo trên… |
| `cho-nam-ban` | **VÙNG** | Về Nam Ban | Chợ Nam Ban ở đâu, họp lúc nào? | Có một chỗ ở Nam Ban lúc nào cũng có người: cái chợ. |
| `chua-linh-an-nam-ban` | **VÙNG** | Về Nam Ban | Chùa Linh Ẩn (Thiền viện Linh Ẩn) Nam Ban: đi thế nào… | Đi ngang chùa gần như mỗi tuần. Viết bài này cho ai đang tính ghé. |
| `chuyen-len-nam-ban-song` | **VÙNG** | Về Nam Ban | Chuyển lên Nam Ban sống: trường, y tế, internet, và… | Nam Ban có đủ trường từ mầm non đến trung học phổ thông ngay tại chỗ. Y tế có trạm y tế xã và phòng khám đa khoa; cần bệnh viện thì đi Đà Lạt chừng… |
| `da-lat-di-nam-ban` | **KHÁC** | Về Nam Ban | Đà Lạt đi Nam Ban bằng cách nào? | Trục chính là tỉnh lộ ĐT.725. Từ trung tâm chạy hướng thác Cam Ly, tới ngã ba Suối Vàng thấy bảng Tà Nung thì quẹo vào. Qua đèo, tới Mê Linh, rồi… |
| `dac-san-nam-ban` | **KHÁC** | Về Nam Ban | Nam Ban có đặc sản gì? | Nam Ban có cà phê, bơ 034 (vụ chính cuối tháng 5, tháng 6), hồng, chuối laba, và tơ tằm — nghề từ thời người Hà Nội vào lập nghiệp. Đặc sản thật của… |
| `dieu-de-lai-cho-con` | **VÙNG** | — | Điều để lại cho con, có lẽ không phải một căn nhà. | Hôm rồi ngồi uống cà phê ở Nam Ban với vài anh chị bạn. Lạ một chỗ, cứ gặp nhau là kiểu gì câu chuyện cũng quay về đất. |
| `duong-di-nam-ban` | **VÙNG** | Về Nam Ban | Sài Gòn đi lên Nam Ban bằng đường nào | Google Maps sẽ đưa bạn tới nơi. Bài này giúp bạn biết nên đi đường nào, lúc nào nên tránh, và vì sao có hai lối vào Nam Ban. |
| `duong-nam-ban-phi-to-da-lat` | **VÙNG** | Về Nam Ban | Đường mới từ Nam Ban lên Đà Lạt qua Phi Tô | Ở Nam Ban lâu thì quen với một câu mặc định: muốn lên Đà Lạt thì đi đèo Tà Nung. Đường đó đẹp, nhưng bao năm nó gần như là lối duy nhất. |
| `google-maps-khong-noi-ve-nam-ban` | **KHÁC** | Về Nam Ban | Những điều Google Maps không nói về Nam Ban | Có tiếng xe công nông buổi sáng. Có tiếng chó sủa buổi tối. Có tiếng mưa trên mái tôn, tiếng máy cắt cỏ, đôi khi tiếng máy ươm tơ. Đây là những âm… |
| `ho-dong-thanh-nam-ban` | **VÙNG** | Về Nam Ban | Hồ Đông Thanh ở Nam Ban: hồ này làm tới đâu rồi? | Anh em lên xem đất kiểu gì cũng hỏi tôi câu này. "Nghe nói dưới đó có cái hồ lớn hả anh?" |
| `kinh-te-so-nam-ban` | **KHÁC** | Về Nam Ban | Nông sản Nam Ban có bán online không? | Ra chợ Nam Ban buổi sáng, hay bắt gặp người bán vừa cân hàng vừa cúi xuống nhắn tin. Hỏi ra mới biết đang chốt đơn cho khách dưới Sài Gòn. |
| `lam-dong-co-gi-de-lam-an` | **KHÁC** | Lâm Đồng | Lâm Đồng có gì để làm ăn? Mỗi vùng một kiểu | Có lần một anh bạn dưới Sài Gòn lên chơi, ngồi sau xe tôi chạy một vòng, được chừng nửa tiếng thì hỏi: "Ủa sao nãy giờ thấy cây khác rồi?" |
| `lam-ha-truoc-va-sau-sap-nhap` | **KHÁC** | Về Nam Ban | Lâm Hà trước và sau sáp nhập: nay còn những xã nào? | Nam Ban giờ là một trong sáu xã đó. Mấy chữ "Lâm Hà cũ", "Lâm Hà mới" nghe hoài. Riêng phần lịch sử, diện tích và địa giới của xã tôi ở, tôi gom ở… |
| `lam-viec-tu-xa-o-nam-ban` | **VÙNG** | Về Nam Ban | Làm việc từ xa ở Nam Ban: giữ công việc, đổi nơi sống | Ở Nam Ban thấy một điều khá thú vị: công nghệ làm khoảng cách giữa thành phố và một vùng ven ngắn đi rất nhiều. |
| `len-lam-dong-nen-song-o-dau` | **VÙNG** | Lâm Đồng | Lên Lâm Đồng nên sống ở đâu? | Hai bài trước tôi kể ở Lâm Đồng người ta kiếm sống bằng gì, rồi mỗi vùng làm ăn một kiểu ra sao. Đọc xong thì câu tiếp theo trong đầu ai cũng giống… |
| `len-lam-dong-song-lam-gi` | **VÙNG** | Lâm Đồng | Lên Lâm Đồng sống: làm gì để có thu nhập? | Tôi hay gặp câu hỏi này khi ngồi cà phê với mấy anh em dưới phố lên chơi. Ngồi một hồi, thế nào cũng có người thở dài: "Hay là mình lên đây sống… |
| `mot-ngay-lam-vuon-nam-ban` | **VÙNG** | Về Nam Ban | Một ngày của người làm vườn ở Nam Ban | Ai đang tính lên đây sống thì câu đáng hỏi không phải người ta làm nông thế nào. Mà là: một ngày ở đây trôi qua ra sao, và mình có sống nổi kiểu đó… |
| `mot-ngay-o-nam-ban` | **VÙNG** | Về Nam Ban | Nếu chỉ có một ngày ở Nam Ban | Một ngày ở Nam Ban đủ để đi hết những điểm có tên: Thác Voi, chùa Linh Ẩn, làng dệt tơ tằm, vài quán cà phê nhìn ra đồi. Nhưng bài này không viết để… |
| `mua-bo-nam-ban` | **VÙNG** | Về Nam Ban | Mùa bơ Nam Ban tháng mấy? | Mùa bơ Nam Ban: hai giống, hai mùa, cách nhau ba tháng. Bơ 034 có trái từ tháng 4 đến tháng 6, rộ nhất cuối tháng 5 đầu tháng 6. Bơ Booth chín muộn… |
| `mua-ca-phe-nam-ban` | **VÙNG** | Về Nam Ban | Mùa cà phê Nam Ban tháng mấy? Mùa hoa và mùa thu hoạch | Nam Ban có hai mùa cà phê. Mùa hoa từ tháng 2 đến tháng 4, rộ nhất tháng 3 — hoa trắng nở thành đợt, mỗi đợt chỉ 7 đến 10 ngày. Mùa thu hoạch từ… |
| `nam-ban-co-dang-song` | **VÙNG** | — | Sống ở Nam Ban thực sự như thế nào? | Một cái nhìn thành thật về nhịp sống, những đánh đổi, và kiểu người thật sự thấy thuộc về nơi thị trấn cao nguyên yên tĩnh này, cạnh Đà Lạt — không… |
| `nam-ban-co-hop-voi-ban` | **VÙNG** | Về Nam Ban | Có nên chuyển lên Nam Ban sống? Ai hợp, ai không | Có những người tới Nam Ban một lần, rồi vài năm sau vẫn quay lại. Có những người tới Nam Ban ba lần trong một tháng, rồi không bao giờ quay lại nữa.… |
| `nam-ban-co-sap-nhap-da-lat` | **KHÁC** | Đầu tư | Nam Ban sáp nhập Đà Lạt không? | Chuyện này nghe hoài. Có người hỏi thẳng: "Nam Ban sáp nhập Đà Lạt hả anh?" Có người lại gõ Google: "Nam Ban sắp nhập Đà Lạt?", "Nam Ban thành Đà… |
| `nam-ban-hay-dran` | **SO SÁNH** | Về Nam Ban | Nam Ban hay D'ran | Tôi sống và làm việc ở Nam Ban nên gần như tuần nào cũng đi thực địa các khu đất trong vùng. D'ran tôi cũng đã ghé nhiều lần để tự mình quan sát và… |
| `nam-ban-la-gi` | **KHÁC** | Về Nam Ban | Nam Ban là gì, ở đâu? | Nhiều người nghe tên Nam Ban lần đầu từ một người bạn, hoặc từ một video bỏ phố về rừng, rồi lên mạng tra thử. Bài này viết cho đúng lúc đó — chưa… |
| `nam-ban-mua-nao` | **VÙNG** | Về Nam Ban | Nên đi Nam Ban mùa nào? | Cùng một mảnh đất, mùa khô với mùa mưa cho thấy hai chuyện khác nhau. Có thứ chỉ mùa khô mới thấy. Có thứ phải đợi một trận mưa lớn mới lộ ra. |
| `nam-ban-sau-6h-toi` | **KHÁC** | Về Nam Ban | Nam Ban sau 6 giờ tối có gì? | Ban ngày nhìn Nam Ban rất dễ. Chợ, quán, xe cộ, người ra vườn, người đi làm. |
| `nam-ha-sap-nhap-nam-ban` | **KHÁC** | Hỏi nhiều | Nếu Nam Hà sáp nhập Nam Ban thì đổi gì? | Chưa. Tới lúc tôi viết dòng này thì chưa có văn bản nào. |
| `nguoi-nam-ban-anh-nam` | **VÙNG + CHÂN DUNG** | Về Nam Ban | Anh Nam, và mùa cà phê khiến anh ở lại | Một người đến Nam Ban định ở thử một mùa. Rồi anh không về nữa. |
| `nguoi-nam-ban-chi-trang` | **CHÂN DUNG** | Về Nam Ban | Chị Trang, và quyết định đổi cả một nếp nhà | Chị không rời phố để trốn. Chị rời phố vì muốn con mình lớn lên khác đi. |
| `novaland-nam-ban` | **VÙNG** | Đầu tư | Novaland Nam Ban: ở đâu, bao nhiêu ha, đã triển khai… | Mấy hôm nay anh em hỏi tôi hoài. "Novaland vô Nam Ban thật hả?" "Khu nào?" "Nghe nói mấy ngàn hecta?" "Bao giờ làm?" |
| `nuoc-o-nam-ban` | **VÙNG** | Về Đất | Nước ở Nam Ban: có nước máy không, khoan giếng bao sâu? | Đi xem đất với người ta nhiều, tôi để ý: ai cũng hỏi view, hỏi đường vào, hỏi thổ cư. Chuyện nước để sau cùng, có người tới lúc tính xây mới nhớ ra. |
| `o-nam-ban-mot-nam-moi-biet` | **KHÁC** | Về Nam Ban | Ở Nam Ban một năm rồi mới biết gì? | Có những chuyện đi xem đất một buổi không thấy. Ở vài tháng bắt đầu thấy. Ở đủ một năm, đi qua các mùa, mới hiểu vì sao người sống lâu ở một vùng… |
| `ocop-nam-ban` | **VÙNG** | Về Nam Ban | OCOP Nam Ban: sản phẩm, nông sản và những gì đang thay… | Nếu hỏi Nam Ban làm ra gì, cà phê là câu trả lời dễ thấy nhất. Nhưng đi trong vùng còn gặp dâu tằm, bơ, rau và những khu vườn mỗi nhà làm một kiểu. |
| `phi-to-nam-ha-lam-ha` | **KHÁC** | Về Nam Ban | Phi Tô ở đâu, giờ thuộc xã nào? | Từ Nam Ban đi về hướng Phi Tô, cảnh gần như chỉ có một màu: cà phê. Đồi này qua đồi khác, cà phê trải kín, thi thoảng xen một vạt thanh long. |
| `pickleball-nam-ban` | **KHÁC** | Về Nam Ban | Nam Ban có sân pickleball không? | Một điểm bên thôn 4. Một điểm nữa mang tên Mai Vàng, cũng trong xã. Đi Đinh Văn chừng hai mươi phút thì có thêm hai chỗ, một trong đó có sân trong… |
| `ram-vu-lan-nam-ban` | **KHÁC** | Về Nam Ban | Rằm và Vu Lan ở Nam Ban | Không hoàn toàn, và chỗ này nhiều người lẫn. |
| `roi-sai-gon-len-nam-ban` | **KHÁC** | Về Nam Ban | Người rời Sài Gòn, và mảnh vườn anh không tính trước | Buổi sáng ở vườn của anh bắt đầu sớm hơn anh từng nghĩ một con người có thể tự nguyện thức dậy. Năm giờ rưỡi, sương còn nằm trên tán cà phê, anh đã… |
| `so-hoa-nam-ban` | **KHÁC** | Về Nam Ban | Số hóa Nam Ban là gì? | Mấy năm nay nghe “chuyển đổi số” nhiều đến mức thành sáo. Ở phố thì còn thấy được — app gọi xe, ví điện tử, camera khắp ngã tư. Còn ở một xã trồng… |
| `ta-nung-hay-me-linh` | **SO SÁNH** | Về Đất | Tà Nung hay Mê Linh? Hai vùng gần Đà Lạt khác nhau thế… | Ai từ Đà Lạt về Nam Ban đều đi qua con đèo này. Tôi đi hoài. |
| `thac-voi-nam-ban` | **VÙNG** | — | Thác Voi, Nam Ban: những điều nên biết trước khi đi | Phần lớn người tìm "Nam Ban" thật ra đang tìm một thứ: dòng thác. Đây là hướng dẫn thành thật về Thác Voi — đi thế nào, đi mùa nào, thực sự ra sao —… |
| `thon-nam-ban` | **KHÁC** | Về Nam Ban | Nam Ban có những thôn nào? Tên thôn mới và tên thôn cũ | Chuyện này rất đời. Đất vẫn ở đó, nhà vẫn ở đó, đường vẫn là con đường ấy. Chỉ có cách gọi một địa chỉ đang chạy hai nhịp khác nhau. |
| `thuong-mai-dien-tu-nam-ban` | **VÙNG** | Về Nam Ban | Thương mại điện tử Nam Ban: mua bán online thế nào? | Ra Nam Ban một thời gian thì thấy chuyện bán hàng qua mạng ở đây chẳng có gì lạ. Người có cà phê thì đăng cà phê, có bơ thì đăng bơ, chụp cái ảnh… |
| `thuy-dien-da-chomo-phi-to` | **VÙNG** | Về Nam Ban | Thủy điện Đạ Chomo ở Phi Tô: có phải Nam Ban không | Từ hồi có tuyến mới chạy Nam Ban – Mê Linh – Hang Hớt – Phi Tô rồi ra Đà Lạt, người đi ngang hay hỏi lại: "Dưới đó có cái thủy điện phải không anh?" |
| `tour-ca-phe-nam-ban` | **VÙNG** | Về Nam Ban | Tour cà phê Nam Ban: đi đâu, làm gì | Nam Ban có hai kiểu trải nghiệm cà phê. Tám Trình Coffee làm tour trong ngày — từ nửa tiếng đến tám tiếng, khoảng 170 đến 200 nghìn một khách, có… |
| `ve-nam-ban-lam-gi` | **KHÁC** | Về Nam Ban | Về Nam Ban làm gì? | Nam Ban không chỉ dành cho người làm vườn. |
| `xa-nam-ban-lam-ha` | **KHÁC** | Tra cứu | Xã Nam Ban Lâm Hà: lịch sử, diện tích, dân số | Hội đồng Bộ trưởng ra Quyết định 77-HĐBT, lập thị trấn Nông trường Nam Ban — trung tâm Vùng kinh tế mới Hà Nội tại Lâm Đồng, lúc đó thuộc huyện Đức… |
| `xa-nam-ha-lam-ha` | **KHÁC** | Về Nam Ban | Xã Nam Hà Lâm Hà là vùng thế nào? | Nam Hà với Nam Ban là hàng xóm sát vách, mà lại hay bị nhầm là một, chắc tại tên gần giống. Thật ra đây là hai xã khác nhau, và Nam Hà có cái chất… |

---

## C — Ba con số

| | |
|---|---|
| Tổng bài A2 | **78** |
| A2 mang nhãn `[ĐẤT]` | **23** |
| Trong `[ĐẤT]` còn mang nhãn khác | **12** |

Phân bố đầy đủ:

| tổ hợp nhãn | số bài |
|---|---|
| VÙNG | 26 |
| KHÁC | 25 |
| ĐẤT | 11 |
| ĐẤT + VÙNG | 10 |
| SO SÁNH | 2 |
| ĐẤT + VÙNG + SO SÁNH | 2 |
| VÙNG + CHÂN DUNG | 1 |
| CHÂN DUNG | 1 |

Nhóm phải đọc tay là 12 bài `[ĐẤT]` kiêm nhãn khác:

- `co-nen-mua-dat-nam-ban-o-xa` — ĐẤT + VÙNG — Có nên mua đất Nam Ban để ở? Điều nhiều người chỉ hiểu sau khi lên ở…
- `dat-nguon-goc-lam-nghiep-nam-ban` — ĐẤT + VÙNG — Mua đất rừng ở Nam Ban được không? Đất có nguồn gốc lâm nghiệp
- `dat-the-am-the-duong` — ĐẤT + VÙNG — Thế đất âm, thế đất dương: đọc đất cao thấp hơn đường ở Nam Ban thế…
- `do-dac-dat-nam-ban` — ĐẤT + VÙNG — Đo đạc đất Nam Ban: đất ngoài đường có giống trên sổ không?
- `gia-ca-phe-va-gia-dat-nam-ban` — ĐẤT + VÙNG — Giá cà phê tăng thì giá đất Nam Ban có tăng theo không?
- `ho-tron-nam-ban` — ĐẤT + VÙNG — Hồ Tròn ở Nam Ban: trong giấy nó tên là hồ Ba Đình
- `mua-dat-nam-ban-500-trieu-1-ty` — ĐẤT + VÙNG — Mua đất Nam Ban: 500 triệu đến 1 tỷ mua được gì?
- `nam-ban-hay-duc-trong` — ĐẤT + VÙNG + SO SÁNH — Nam Ban hay Đức Trọng: nên sống và mua đất ở đâu?
- `nam-ban-hay-lac-duong` — ĐẤT + VÙNG + SO SÁNH — Nam Ban hay Lạc Dương: nên chọn vùng nào để ở và mua đất?
- `nguoi-ngoai-tinh-mua-dat-nam-ban` — ĐẤT + VÙNG — Người ở tỉnh khác mua đất Nam Ban: có sổ và chưa có sổ khác nhau thế…
- `o-thu-nam-ban-truoc-khi-mua-dat` — ĐẤT + VÙNG — Ở thử Nam Ban trước khi mua đất
- `quy-hoach-chung-nam-ban` — ĐẤT + VÙNG — Quy hoạch chung Nam Ban Lâm Hà đến 2050: 7 khu vực phát triển và…

---

## D — SĐT trong footer

Quét `0978 758 788` và `0978758788` trong khối `<footer>` toàn repo: **96 bài, 185 lần**.

**Vi phạm §2.2 (có khối liên hệ mà footer vẫn còn SĐT): 1 ca.**

| slug | chuyên mục | số lần |
|---|---|---|
| `10-10-1975-nam-ban` | Về Nam Ban | 2 |

95 bài còn lại **không** nằm trong `IN` — tức chưa có khối liên hệ, nên footer
giữ SĐT là **đúng luật**, không phải lỗi.

> Phiếu nhắc `/dat-nguon-goc-lam-nghiep-nam-ban` có SĐT footer. File đó có thật, nhưng nó
> **không nằm trong `IN`** nên chưa có khối liên hệ — footer giữ SĐT là đúng §2.2. Không phải ca lỗi.
