# Quét câu khai lý lịch — kết quả Việc 1 (9/9/2026)

Phiếu gốc: quét 6 mẫu `tôi ở Nam Ban` · `tôi sống ở Nam Ban` · `mình ở Nam Ban` ·
`mình sống ở Nam Ban` · `tôi đang sống ở Nam Ban` · `tôi ở đây` trong vùng
`.art-body` → `.share-row`. Đã `html.unescape()` + bỏ `\xa0`, case-insensitive.

**Ô Code chỉ đếm và báo. KHÔNG tự viết câu thay thế, KHÔNG sửa gì.**

---

## TRẠNG THÁI SAU ĐỢT SỬA 9/9/2026

**Đã sửa 26 ca** (CA 2 → CA 27) theo bảng Chú duyệt, `str_replace` exact, mỗi
`old_str` khớp đúng một lần, không ca nào phải nới rộng. Kèm 4 sửa ở
`/dat-nam-ban-chua-xay` (B1–B4).

**CA 1 — ĐÓNG, báo động giả.** `/ban-dat-nam-ban`: "lô đất mình" + "ở Nam Ban"
là hai cụm dính nhau trong một câu FAQ, không phải khai lý lịch. Không đụng,
và đợt rà sau đừng mở lại.

### PHẠM VI QUÉT ĐÚNG — SỬA SAU KHI SÓT 3 CA (9/9/2026)

Bộ quét phải dò **toàn bộ text node trong vùng `.art-body` → `.share-row`**, KHÔNG
giới hạn ở `<p> <li> <figcaption> <h2> <h3> <blockquote>`.

Lý do: đợt 9/9/2026 bộ quét chỉ liệt sáu thẻ đó nên **sót 3 ca nằm trong
`<div class="quick-answer">`**. Đó lại đúng là **khối AEO** — khối trả lời nhanh
đầu bài, chỗ Google và AI trích nhiều nhất. Sót ở đó là sót đúng chỗ đắt nhất.
Grep sau sửa ra 4 ca thay vì 1 mới lộ ra lỗi này.

### 6 CA ĐỢT HAI — ĐÃ XỬ 9/9/2026

Bộ quét Việc 1 chỉ dò trong `<p> <li> <figcaption> <h2> <h3> <blockquote>`, nên
**bỏ sót chữ nằm trong `<div class="quick-answer">`**. Đó là lý do lần đầu ra 27
mà grep lại còn 4. Ba ca trong `quick-answer` (QA-1 → QA-3) và ba ca chỉ có trong `llms-full.txt`
(LLM-1 → LLM-3) đã sửa theo bảng Chú duyệt:

- `/len-lam-dong-nen-song-o-dau` — *"Tôi ở Nam Ban, một vùng ven Đà Lạt, nên phần
  cuối tôi kể vùng này rõ hơn; mấy vùng khác tôi chỉ nói trong phạm vi mình đã đi qua."*
  (dạng Ca C — vế sau là moat)
- `/len-lam-dong-song-lam-gi` — *"Tôi ở Nam Ban, vùng Lâm Hà, nên chuyện này tôi
  nhìn khá gần."*
- `/nhan-tien-den-bu-dat-nen-lam-gi` — *"Tôi ở Nam Ban, nên phần cuối tôi kể từ
  chỗ mình đứng."* (dạng Ca C)

Và ba ca **chỉ có trong `llms-full.txt`**, không có trong thân bài HTML:

- *"Nếu Nam Ban với bạn cũng là một nơi để quay về — tôi ở đây."*
- *"Chúng tôi ở đây, qua nhiều mùa được giá lẫn mất giá."*
- *"Đang phân vân giữa hai vùng, hai lô cụ thể — tôi ở đây."*

### llms-full.txt

Không có script sinh file này, và nội dung là tóm tắt biên soạn tay chứ không
trích máy từ HTML — nên "sinh lại từ HTML" không chạy được. Thay vào đó áp lại
**đúng 26 cặp Chú đã duyệt**, thuần cơ học, không viết câu mới: **31 → 7 ca**
(1 báo động giả + 3 ca quick-answer + 3 ca chỉ có ở file này).
`llms.txt` và `feed.xml` vẫn 0.

---


```
QUÉT CÂU KHAI LÝ LỊCH — kết quả Việc 1
Phạm vi: 168 file .html lang=vi, vùng .art-body → .share-row (gồm Nguồn & Đọc gì tiếp).
Đã html.unescape + bỏ \xa0 trước khi so. Case-insensitive.
TỔNG: 27 ca trong HTML

Theo mẫu: tôi ở nam ban = 15 · tôi ở đây = 8 · tôi sống ở nam ban = 3 · mình ở nam ban = 1
Theo vị trí: giữa bài = 15 · MỞ BÀI = 12
Số bài dính: 23

==============================================================================

### CA 1 — /ban-dat-nam-ban · dòng 448 · mẫu «mình ở nam ban» · giữa bài
TRƯỚC : Dấu hiệu rõ nhất: tin đăng im lặng hàng tuần, không một cuộc gọi nào.
CÂU   : Làm sao biết giá thật của lô đất mình ở Nam Ban?
SAU   : Đừng nhìn giá rao — đó là giá người ta muốn, không phải giá người ta được

### CA 2 — /chua-linh-an-nam-ban · dòng 381 · mẫu «tôi ở nam ban» · MỞ BÀI
TRƯỚC : (đầu bài)
CÂU   : Tôi ở Nam Ban, đi ngang chùa gần như mỗi tuần.
SAU   : Viết bài này cho ai đang tính ghé.

### CA 3 — /dat-nguon-goc-lam-nghiep-nam-ban · dòng 555 · mẫu «tôi ở đây» · giữa bài
TRƯỚC : Biết hai thứ có đang kể cùng một câu chuyện hay không mới là chuyện đáng hỏi.
CÂU   : Tôi ở đây nên hồ sơ thì đọc trên bàn, còn đất thì vẫn thích chạy ra ngoài đường nhìn.
SAU   : Sổ nói một chuyện.

### CA 4 — /giu-dat-nam-ban-tu-xa · dòng 376 · mẫu «tôi ở đây» · MỞ BÀI
TRƯỚC : Nói trước cho nhẹ đầu: giữ đất không khó như nhiều người mới mua thường tưởng.
CÂU   : Tôi ở đây, thấy chuyện này hoài, nên viết ra mấy cách người ta đang làm — cho ai vừa mua đất xong đỡ băn khoăn.
SAU   : Đất ở Nam Ban để một thời gian không sao, và cho người khác canh tác cũng không làm mất quyền của mình, miễn là giữ sổ đỏ và thỏa thuận rõ ràng

### CA 5 — /ho-dong-thanh-nam-ban · dòng 371 · mẫu «tôi ở đây» · MỞ BÀI
TRƯỚC : Người thì bảo sắp thành khu du lịch, người thì bảo bỏ hoang rồi.
CÂU   : Tôi ở đây, chạy ngang hoài, nên kể lại cho gọn.
SAU   : Hồ Đông Thanh nhìn từ thân đập — hồ đã có nước, tháp lấy nước và thân đập đã dựng, phần trên tháp còn để thép chờ.

### CA 6 — /lam-dong-co-gi-de-lam-an · dòng 433 · mẫu «tôi ở nam ban» · giữa bài
TRƯỚC : Còn chọn thế nào, dựa vào cái gì mà quyết — cái đó dài, để dành bài sau.
CÂU   : Tôi ở Nam Ban nên câu tôi hay được hỏi tiếp là: vậy nếu lên Lâm Đồng sống, nên chọn vùng nào ?
SAU   : Câu hỏi thường gặp

### CA 7 — /lam-ha-truoc-va-sau-sap-nhap · dòng 375 · mẫu «tôi ở nam ban» · MỞ BÀI
TRƯỚC : (đầu bài)
CÂU   : Tôi ở Nam Ban, một trong sáu xã đó.
SAU   : Mấy chữ "Lâm Hà cũ", "Lâm Hà mới" nghe hoài.

### CA 8 — /lam-ha-truoc-va-sau-sap-nhap · dòng 467 · mẫu «tôi ở đây» · giữa bài
TRƯỚC : Tên thôn trong xã đổi ra sao thì ở bài này .
CÂU   : Tôi ở đây nên thấy chuyện đổi tên diễn ra khá nhẹ nhàng.
SAU   : Giấy tờ đổi trên bàn, còn ngoài đường người ta vẫn gọi như cũ.

### CA 9 — /len-lam-dong-nen-song-o-dau · dòng 398 · mẫu «tôi ở nam ban» · giữa bài
TRƯỚC : Còn tôi thì sao?
CÂU   : Tôi ở Nam Ban rồi nên câu này hơi thiên vị, nhưng tôi kể thật lý do.
SAU   : Tôi cần một chỗ đủ gần Đà Lạt để dùng Đà Lạt như một tiện ích — cần gì thì chạy lên, 25km qua đèo Tà Nung, chừng 45 phút

### CA 10 — /len-lam-dong-nen-song-o-dau · dòng 420 · mẫu «tôi ở nam ban» · giữa bài
TRƯỚC : Anh em muốn hỏi thì hỏi gì?
CÂU   : Tôi ở Nam Ban nên những câu về Nam Ban tôi trả lời dễ hơn mấy vùng khác.
SAU   : Ai đang cân giữa vài vùng thì cứ hỏi thẳng, hỏi câu cụ thể

### CA 11 — /len-lam-dong-song-lam-gi · dòng 396 · mẫu «tôi ở nam ban» · giữa bài
TRƯỚC : Còn mua đất trước, xong mới ngồi nghĩ "ủa mình sống ở đây bằng gì" thì hơi ngược.
CÂU   : Tôi ở Nam Ban, nên câu tiếp theo tôi hay được hỏi là: vậy mỗi vùng Lâm Đồng sống bằng gì , chỗ nào hợp với mình?
SAU   : Cái đó mới là chuyện đáng kể tiếp — để dành bài sau.

### CA 12 — /mua-bo-nam-ban · dòng 437 · mẫu «tôi ở nam ban» · giữa bài
TRƯỚC : Chúng chỉ đang nói về những giống khác nhau, ở những vùng khác nhau, rồi gộp chung lại thành một câu.
CÂU   : Chúng tôi ở Nam Ban — một xã vùng ven Đà Lạt, cách thành phố chừng bốn mươi lăm phút xe qua đèo Tà Nung.
SAU   : Đây là vùng trồng bơ thật, không phải vùng bán bơ.

### CA 13 — /mua-dat-nam-ban-500-trieu-1-ty · dòng 390 · mẫu «tôi ở nam ban» · MỞ BÀI
TRƯỚC : Đó là một trong những khoảng ngân sách được hỏi nhiều nhất khi tìm hiểu đất ở đây, và cũng là lý do nhiều người tìm đất Nam Ban giá rẻ hay bắt đầu từ khoảng này.
CÂU   : Tôi ở Nam Ban, nhìn giá lên xuống hoài, nên viết ra đây cho ai có ngân sách tầm đó — để hình dung trước mình mua được kiểu đất nào, khỏi kỳ vọng lệch rồi hụt hẫng.
SAU   : Ở Nam Ban, tầm 500–800 triệu thường mua được lô nhỏ vài trăm mét vuông, có ít thổ cư, hoặc lô xa trung tâm hơn một chút

### CA 14 — /mua-mua-nam-ban · dòng 359 · mẫu «tôi ở nam ban» · MỞ BÀI
TRƯỚC : (đầu bài)
CÂU   : Tôi ở Nam Ban nên mùa mưa với tôi không phải một dòng trong bản tin thời tiết.
SAU   : Nó là lúc cây cối đổi màu, đường đất khó đi hơn, vườn có việc khác, nhà có việc khác

### CA 15 — /nam-ban-co-sap-nhap-da-lat · dòng 369 · mẫu «tôi ở nam ban» · MỞ BÀI
TRƯỚC : (đầu bài)
CÂU   : Tôi ở Nam Ban, chuyện này nghe hoài.
SAU   : Có người hỏi thẳng: "Nam Ban sáp nhập Đà Lạt hả anh?" Có người lại gõ Google: "Nam Ban sắp nhập Đà Lạt?", "Nam Ban thành Đà Lạt?", "Đà Lạt mở rộng tới Nam Ban?"

### CA 16 — /nam-ban-hay-dran · dòng 453 · mẫu «tôi ở nam ban» · giữa bài
TRƯỚC : Đứng trên đất, hít cái không khí, nhìn cái vườn, tự khắc bạn biết chỗ nào hợp với mình.
CÂU   : Tôi ở Nam Ban nên rành Nam Ban hơn; còn D'ran là một chỗ đáng đi, đáng cân nhắc thật lòng.
SAU   : Câu hỏi thường gặp

### CA 17 — /nam-ban-hay-duc-trong · dòng 350 · mẫu «tôi sống ở nam ban» · MỞ BÀI
TRƯỚC : Nếu đang tìm một vùng quanh Đà Lạt để sống, mua đất, làm một căn nhỏ cuối tuần, hoặc chỉ đơn giản là kiếm chỗ để dành cho vài năm nữa — kiểu gì cũng có lúc bạn đặt Nam Ban cạnh Đức Trọng.
CÂU   : Tôi sống ở Nam Ban, còn Đức Trọng thì đi qua lại nhiều lần, vừa vì đường ra sân bay vừa vì có việc dưới đó.
SAU   : Nên phần Nam Ban tôi nói theo cái mình sống; phần Đức Trọng tôi nói trong phạm vi mình quan sát được, chỗ nào là thông tin chung thì tôi ghi rõ.

### CA 18 — /nam-ban-hay-duc-trong · dòng 438 · mẫu «tôi ở nam ban» · giữa bài
TRƯỚC : Mấy trường hợp đó tôi nói thẳng luôn.
CÂU   : Tôi ở Nam Ban, nhưng khuyên người ta mua chỗ không hợp thì cũng chẳng để làm gì.
SAU   : Nam Ban hợp với ai, và cuối cùng nên chọn đâu

### CA 19 — /nam-ban-hay-lac-duong · dòng 383 · mẫu «tôi sống ở nam ban» · MỞ BÀI
TRƯỚC : Cùng cao nguyên, cùng mát, cùng có đất vườn — mà tính nết khác nhau khá xa.
CÂU   : Tôi sống ở Nam Ban, còn phía Lạc Dương thì đi qua lại nhiều lần vì thích cảnh bên đó.
SAU   : Phần Nam Ban tôi nói theo cái mình sống; phần Lạc Dương tôi nói trong phạm vi mình quan sát được.

### CA 20 — /nam-ban-hay-lac-duong · dòng 471 · mẫu «tôi ở nam ban» · giữa bài
TRƯỚC : Mấy trường hợp đó tôi nói thẳng.
CÂU   : Tôi ở Nam Ban, nhưng khuyên người ta mua chỗ không hợp thì cũng chẳng để làm gì.
SAU   : Chỉ có một điều nên tính khi mua bên đó: vùng nhiều rừng thì cũng nhiều đất thuộc diện bảo vệ, và đất gắn với du lịch thì giá đi theo câu chuyện du lịch

### CA 21 — /nhan-tien-den-bu-dat-nen-lam-gi · dòng 462 · mẫu «tôi sống ở nam ban» · giữa bài
TRƯỚC : Còn tôi, ở Nam Ban thì nhìn chuyện này thế nào?
CÂU   : Tôi sống ở Nam Ban, một vùng ven Đà Lạt, nên gặp khá nhiều người lên đây với một khoản tiền vừa có được từ đất ở nơi khác.
SAU   : Điều tôi để ý: phần lớn họ không lên để kiếm lời nhanh

### CA 22 — /novaland-nam-ban · dòng 361 · mẫu «tôi ở đây» · MỞ BÀI
TRƯỚC : "Novaland vô Nam Ban thật hả?" "Khu nào?" "Nghe nói mấy ngàn hecta?" "Bao giờ làm?"
CÂU   : Tôi ở đây nên cũng tò mò như mọi người, tìm hiểu kỹ rồi kể lại cho anh em.
SAU   : Vì chuyện đang nóng, mà đề xuất với dự án đã duyệt là hai chuyện khác nhau xa.

### CA 23 — /ocop-nam-ban · dòng 444 · mẫu «tôi ở nam ban» · giữa bài
TRƯỚC : Chưa kiểm được thì để đó.
CÂU   : Tôi ở Nam Ban nên mấy chuyện này không cần làm thành báo cáo.
SAU   : Đi một vòng, thấy chuyện đáng kể thì ghi lại.

### CA 24 — /tach-thua-dat-nam-ban · dòng 542 · mẫu «tôi ở nam ban» · giữa bài
TRƯỚC : Nghe câu trả lời là đã hiểu thêm khá nhiều.
CÂU   : Tôi ở Nam Ban, nên mấy chuyện này tôi thường gặp ngay ngoài đất chứ không chỉ đọc trên giấy.
SAU   : Quy định là một chuyện, từng thửa ngoài thực tế lại là một chuyện khác.

### CA 25 — /thon-nam-ban · dòng 657 · mẫu «tôi ở đây» · giữa bài
TRƯỚC : Người có đất, có nhà, có giấy tờ ở đây thì gặp nó rất cụ thể.
CÂU   : Tôi ở đây nên thấy cả hai phía.
SAU   : Hồ sơ thì đọc trên bàn, còn ngoài đường có gì thay đổi thì chạy một vòng là biết.

### CA 26 — /ve-nam-ban-lam-gi · dòng 336 · mẫu «tôi ở đây» · MỞ BÀI
TRƯỚC : Nam Ban không chỉ dành cho người làm vườn.
CÂU   : Tôi ở đây lâu rồi nên bắt đầu thấy một chuyện khác: có những người không cần đổi nghề để đổi nơi sống.
SAU   : Họ chỉ cần một căn nhà nhỏ, một khoảng riêng, internet đủ tốt, một chút cây xanh — rồi tiếp tục công việc của mình ở đây.

### CA 27 — /xay-nha-o-nam-ban · dòng 382 · mẫu «tôi ở đây» · MỞ BÀI
TRƯỚC : Mấy năm nay người ta lên Nam Ban xây nhà nhiều.
CÂU   : Tôi ở đây, nhìn hết — nhà mọc lên từng cái, mà chuyện dở khóc dở cười cũng không ít.
SAU   : Nên viết ra đây cho ai sắp xây, đọc trước một lần đỡ vấp mấy cái người trước đã vấp.


==============================================================================
NGOÀI HTML
  llms.txt         0 ca
  llms-full.txt    31 ca
  feed.xml         0 ca
```


---

## ĐÓNG SỔ (9/9/2026)

**Tổng đã xử: 32 ca** — 26 ca đợt một + 3 ca `quick-answer` + 3 ca `llms-full.txt`.

**CA 1 đóng vĩnh viễn.** `/ban-dat-nam-ban`, câu FAQ *"Làm sao biết giá thật của
lô đất mình ở Nam Ban?"* — "lô đất mình" và "ở Nam Ban" là hai cụm dính nhau,
không phải khai lý lịch. Grep còn bắt được ca này ở cả HTML lẫn `llms-full.txt`,
**đó là con số kỳ vọng, không phải lỗi**. Đợt rà sau gặp lại thì đừng mở lại.

**Còn treo:** entry `llms-full.txt` chứa LLM-2 giờ đọc cụt — câu
*"Qua nhiều mùa được giá lẫn mất giá."* đứng một mình sau *"nhắn chúng tôi một
câu."*, mất chủ ngữ. Phiếu cấm tự nối chữ nên để nguyên, chờ câu thay.
