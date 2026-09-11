# Rà soát mật độ "Nam Ban" — ĐỢT 1, CHỈ ĐẾM

> Sinh bằng `python3 tools/scan-mat-do-nam-ban.py`. **Không sửa một chữ nào.**

> Ngày quét: 11/9/2026 · Ô Code chỉ đếm; cháu đọc từng ca rồi viết câu thay.


## TỔNG — VƯỢT NGƯỠNG, CẦN CHIA ĐỢT

**620 ca.** Phiếu chốt vượt 60 thì dừng, nên file này in ĐẦY ĐỦ nhóm A và B (26 ca, nhóm đáng sửa nhất), còn C/D/E chỉ in **số đếm theo bài** — chưa liệt từng câu.


| nhóm | ca |
|---|---|
| A — `<title>` thiếu | 10 bài |
| B — `<h1>` thiếu | 16 bài |
| C — H2 <50% | 81 bài / **481 câu** |
| D — FAQ <30% | 12 bài / **64 câu** |
| E — mật độ >25 | 49 bài |
| **TỔNG** | **620** |

### Nhãn máy gợi ý trong C và D

| nhãn | C | D |
|---|---|---|
| [KHÔNG SỬA — câu tu từ] | 220 | 11 |
| [KHÔNG SỬA — truy vấn rộng] | 13 | 19 |
| [KHÔNG SỬA? — H1 đã neo] | 217 | 24 |
| _(không nhãn — đáng xét)_ | 31 | 10 |

**450/481 ca C và 54/64 ca D đã có nhãn.** Máy gợi ý thôi — cháu đọc lại, ô Code không tự loại.


## PHẠM VI

Quét 155 bài `lang="vi"`. Loại 18 file:


| file | lý do loại |
|---|---|
| `404.html` | hub / trang chức năng |
| `_mau-bai-viet.html` | hub / trang chức năng |
| `brief.html` | hub / trang chức năng |
| `dat.html` | hub / trang chức năng |
| `dau-tu.html` | hub / trang chức năng |
| `demo-hop-tac.html` | hub / trang chức năng |
| `demo-phuong-phap.html` | hub / trang chức năng |
| `demo-selection.html` | hub / trang chức năng |
| `demo-ve-panorama.html` | hub / trang chức năng |
| `doc-nhanh.html` | hub / trang chức năng |
| `elephant-waterfall-nam-ban.html` | không phải lang="vi" |
| `hoi-nhanh.html` | hub / trang chức năng |
| `index.html` | hub / trang chức năng |
| `living-in-nam-ban.html` | không phải lang="vi" |
| `nam-ban-co-gi-moi.html` | hub / trang chức năng |
| `nam-ban.html` | hub / trang chức năng |
| `namban-index.html` | hub / trang chức năng |
| `trao-doi.html` | hub / trang chức năng |

**Cách khoanh thân bài** — site có hai template (§7.2) nên KHÔNG bám một class. Mốc đầu: `.art-body` → `.body` → `</h1>`. Mốc cuối: `share-row` → `next-read` → `source-box` → `<footer>`. Bỏ H2 "Câu hỏi thường gặp", "Nguồn & lưu ý", "Đọc gì tiếp". Mọi phép so đều `html.unescape()` + bỏ `\xa0` (Luật 13d) và case-insensitive (Luật 4).


## A — `<title>` KHÔNG chứa "Nam Ban" (10 bài)

Nhóm đáng sửa nhất: title là thứ hiện trên SERP.


| slug | title hiện tại | ký tự |
|---|---|---|
| `/cau-tong-doi-nam-ban` | Cầu Tổng Đội xây mới: khởi công 14/7/2026, xong tháng 11/2027 | Namban Panorama | 79 |
| `/dat-the-am-the-duong` | Thế đất âm, thế đất dương là gì? Đất cao hay thấp hơn đường có ảnh hưởng gì? | Namban Panorama | 94 |
| `/dieu-de-lai-cho-con` | Điều để lại cho con, có lẽ không phải một căn nhà | Namban Panorama | 67 |
| `/lam-dong-co-gi-de-lam-an` | Lâm Đồng có gì để làm ăn? Mỗi vùng một kiểu | Namban Panorama | 61 |
| `/lam-ha-truoc-va-sau-sap-nhap` | Lâm Hà trước và sau sáp nhập: huyện cũ nay còn những xã nào? | Namban Panorama | 78 |
| `/len-lam-dong-nen-song-o-dau` | Lên Lâm Đồng nên sống ở đâu? | Namban Panorama | 46 |
| `/len-lam-dong-song-lam-gi` | Lên Lâm Đồng sống: làm gì để có thu nhập? | Namban Panorama | 59 |
| `/mua-vuon-ca-phe-nam-ban` | Mua vườn cà phê có dòng tiền thật không? | Namban Panorama | 58 |
| `/nhan-tien-den-bu-dat-nen-lam-gi` | Nhận tiền đền bù đất rồi nên làm gì? | Namban Panorama | 54 |
| `/phi-to-nam-ha-lam-ha` | Phi Tô ở đâu? Vùng cà phê, thanh long nay thuộc xã Nam Hà Lâm Hà | Namban Panorama | 82 |

## B — `<h1>` KHÔNG chứa "Nam Ban" (16 bài)


| slug | H1 hiện tại |
|---|---|
| `/cau-tong-doi-nam-ban` | Cầu Tổng Đội xây mới: khởi công 14/7/2026, xong tháng 11/2027 |
| `/dat-the-am-the-duong` | Thế đất âm, thế đất dương: đọc đất cao thấp hơn đường thế nào? |
| `/dieu-de-lai-cho-con` | Điều để lại cho con, có lẽ không phải một căn nhà. |
| `/lam-dong-co-gi-de-lam-an` | Lâm Đồng có gì để làm ăn? Mỗi vùng một kiểu |
| `/lam-ha-truoc-va-sau-sap-nhap` | Lâm Hà trước và sau sáp nhập: nay còn những xã nào? |
| `/len-lam-dong-nen-song-o-dau` | Lên Lâm Đồng nên sống ở đâu? |
| `/len-lam-dong-song-lam-gi` | Lên Lâm Đồng sống: làm gì để có thu nhập? |
| `/mua-vuon-ca-phe-nam-ban` | Mua vườn cà phê có dòng tiền thật không? |
| `/nguoi-nam-ban-anh-nam` | Anh Nam, và mùa cà phê khiến anh ở lại |
| `/nguoi-nam-ban-chi-trang` | Chị Trang, và quyết định đổi cả một nếp nhà |
| `/nhan-tien-den-bu-dat-nen-lam-gi` | Nhận tiền đền bù đất rồi nên làm gì? |
| `/phi-to-nam-ha-lam-ha` | Phi Tô ở đâu, giờ thuộc xã nào? |
| `/roi-sai-gon-len-nam-ban` | Người rời Sài Gòn, và mảnh vườn anh không tính trước |
| `/ta-nung-hay-me-linh` | Tà Nung hay Mê Linh? Hai vùng gần Đà Lạt khác nhau thế nào |
| `/vuon-bo-loi-bao-nhieu` | Một sào bơ cho bao nhiêu tiền? Bóc phép tính người ta hay dùng để bán đất. |
| `/xa-nam-ha-lam-ha` | Xã Nam Hà Lâm Hà là vùng thế nào? |

## C — H2 dưới 50% (81 bài, 481 câu) — CHƯA LIỆT TỪNG CÂU


| slug | H2 | câu thiếu |
|---|---|---|
| `/nam-ha-sap-nhap-nam-ban` | 5/17 | 12 |
| `/dat-nam-ban-trong-cay-gi` | 0/11 | 11 |
| `/mua-dat-co-vuon-bo` | 1/12 | 11 |
| `/tach-thua-dat-nam-ban` | 1/12 | 11 |
| `/ho-dong-thanh-nam-ban` | 0/10 | 10 |
| `/mua-dat-co-vuon-ca-phe` | 0/10 | 10 |
| `/ban-dat-nam-ban` | 0/9 | 9 |
| `/len-lam-dong-nen-song-o-dau` | 0/9 | 9 |
| `/len-tho-cu-het-bao-nhieu-tien` | 0/9 | 9 |
| `/mot-ngay-lam-vuon-nam-ban` | 0/9 | 9 |
| `/mua-vuon-ca-phe-nam-ban` | 1/10 | 9 |
| `/nam-ban-mua-nao` | 0/9 | 9 |
| `/ta-nung-hay-me-linh` | 2/11 | 9 |
| `/chi-phi-dat-dai-nam-ban` | 7/15 | 8 |
| `/da-lat-di-nam-ban` | 0/8 | 8 |
| `/dat-nam-ban-cuoi-tuan` | 0/8 | 8 |
| `/dat-the-am-the-duong` | 0/8 | 8 |
| `/do-dac-dat-nam-ban` | 1/9 | 8 |
| `/ho-bai-cong-nam-ban` | 0/8 | 8 |
| `/nam-ban-hay-don-duong` | 2/10 | 8 |
| `/nguoi-ngoai-tinh-mua-dat-nam-ban` | 0/8 | 8 |
| `/thon-nam-ban` | 3/11 | 8 |
| `/truoc-khi-xuong-tien` | 0/8 | 8 |
| `/ca-phe-nam-ban` | 2/9 | 7 |
| `/dat-vuon-nam-ban-xay-duoc-gi` | 0/7 | 7 |
| `/duong-ha-bac-nam-ban` | 3/10 | 7 |
| `/lam-dong-co-gi-de-lam-an` | 1/8 | 7 |
| `/lam-ha-truoc-va-sau-sap-nhap` | 0/7 | 7 |
| `/mua-dat-duong-gia-nam-ban` | 1/8 | 7 |
| `/nhan-tien-den-bu-dat-nen-lam-gi` | 1/8 | 7 |
| `/vuon-bo-loi-bao-nhieu` | 0/7 | 7 |
| `/chuyen-muc-dich-su-dung-dat-nam-ban` | 1/7 | 6 |
| `/dinh-gia-dat-nam-ban` | 4/10 | 6 |
| `/doc-the-dat-nam-ban` | 1/7 | 6 |
| `/giu-dat-nam-ban-tu-xa` | 2/8 | 6 |
| `/homestay-nam-ban-co-lai-khong` | 1/7 | 6 |
| `/kinh-nghiem-mua-dat-nam-ban` | 1/7 | 6 |
| `/len-lam-dong-song-lam-gi` | 1/7 | 6 |
| `/mua-bo-nam-ban` | 1/7 | 6 |
| `/mua-ca-phe-nam-ban` | 1/7 | 6 |
| `/mua-dat-nam-ban-de-lam-gi` | 0/6 | 6 |
| `/quy-trinh-mua-dat-nam-ban` | 2/8 | 6 |
| `/5km-o-nam-ban` | 2/7 | 5 |
| `/ca-phe-nam-ban-ai` | 0/5 | 5 |
| `/chua-linh-an-nam-ban` | 4/9 | 5 |
| `/coc-dat-nam-ban` | 2/7 | 5 |
| `/dat-nguon-goc-lam-nghiep-nam-ban` | 3/8 | 5 |
| `/dau-tam-nam-ban` | 0/5 | 5 |
| `/mot-ngay-o-nam-ban` | 0/5 | 5 |
| `/nam-ban-hay-duc-trong` | 3/8 | 5 |
| `/nam-ban-va-nam-ha` | 2/7 | 5 |
| `/quy-hoach-chung-nam-ban` | 2/7 | 5 |
| `/ram-vu-lan-nam-ban` | 3/8 | 5 |
| `/so-hoa-nam-ban` | 1/6 | 5 |
| `/vua-mua-dat-nam-ban-lam-gi` | 1/6 | 5 |
| `/xay-nha-o-nam-ban` | 1/6 | 5 |
| `/brief-01` | 0/4 | 4 |
| `/kinh-te-so-nam-ban` | 2/6 | 4 |
| `/mua-dat-nam-ban-500-trieu-1-ty` | 1/5 | 4 |
| `/nam-ban-co-dang-song` | 3/7 | 4 |
| `/nam-ban-hay-di-linh` | 1/5 | 4 |
| `/nen-xem-khu-nao-o-nam-ban` | 3/7 | 4 |
| `/pickleball-nam-ban` | 3/7 | 4 |
| `/so-sanh-nam-ban-bao-loc-da-lat` | 0/4 | 4 |
| `/thuy-dien-da-chomo-phi-to` | 3/7 | 4 |
| `/xa-nam-ha-lam-ha` | 2/6 | 4 |
| `/dac-san-nam-ban` | 2/5 | 3 |
| `/duong-di-nam-ban` | 2/5 | 3 |
| `/mua-dat-da-lat-chon-nam-ban` | 1/4 | 3 |
| `/mua-dat-nam-ban` | 2/5 | 3 |
| `/nam-ban-hay-dran` | 2/5 | 3 |
| `/o-thu-nam-ban-truoc-khi-mua-dat` | 1/4 | 3 |
| `/phi-to-nam-ha-lam-ha` | 2/5 | 3 |
| `/roi-sai-gon-len-nam-ban` | 1/4 | 3 |
| `/sap-nhap-nam-ban-dat` | 0/3 | 3 |
| `/thac-voi-nam-ban` | 0/3 | 3 |
| `/tiem-nang-dau-tu` | 2/5 | 3 |
| `/cay-xang-petro-moi-o-nam-ban` | 1/3 | 2 |
| `/doc-lo-dat-02-view-ho` | 0/2 | 2 |
| `/nam-ban-co-hop-voi-ban` | 1/3 | 2 |
| `/san-bay-lien-khuong-mo-lai` | 1/3 | 2 |

## D — FAQ dưới 30% (12 bài, 64 câu) — CHƯA LIỆT TỪNG CÂU


| slug | FAQ | câu thiếu |
|---|---|---|
| `/tach-thua-dat-nam-ban` | 2/12 | 10 |
| `/dat-vuon-nam-ban-xay-duoc-gi` | 3/11 | 8 |
| `/ta-nung-hay-me-linh` | 1/9 | 8 |
| `/lam-ha-truoc-va-sau-sap-nhap` | 1/8 | 7 |
| `/len-lam-dong-song-lam-gi` | 0/6 | 6 |
| `/lam-dong-co-gi-de-lam-an` | 1/6 | 5 |
| `/len-lam-dong-nen-song-o-dau` | 1/6 | 5 |
| `/coc-dat-nam-ban` | 0/3 | 3 |
| `/loi-di-chung-dat-nam-ban` | 0/3 | 3 |
| `/mua-dat-nam-ban-hop-dong-uy-quyen` | 0/3 | 3 |
| `/nha-go-thong-nam-ban` | 1/4 | 3 |
| `/xay-nha-giap-rung-thong-nam-ban` | 1/4 | 3 |

## E — mật độ thân bài VƯỢT 25 (49 bài)

Đếm trong vùng thân bài (gồm cả FAQ hiển thị). Cột `lần/1000 chữ` để thấy bài dài thì 26 lần chưa chắc là nhồi — số tuyệt đối một mình dễ gây báo động giả.


| slug | lần | số chữ | lần/1000 chữ |
|---|---|---|---|
| `/nam-ban-va-nam-ha` | 63 | 2103 | 30.0 |
| `/nam-ban-co-sap-nhap-da-lat` | 62 | 2068 | 30.0 |
| `/nam-ban-hay-lac-duong` | 59 | 3386 | 17.4 |
| `/xa-nam-ban-lam-ha` | 57 | 1381 | 41.3 |
| `/nam-ban-hay-don-duong` | 53 | 2744 | 19.3 |
| `/nam-ban-hay-duc-trong` | 50 | 2480 | 20.2 |
| `/duong-di-nam-ban` | 47 | 1526 | 30.8 |
| `/quy-hoach-2050` | 47 | 2362 | 19.9 |
| `/thon-nam-ban` | 46 | 3166 | 14.5 |
| `/nen-xem-khu-nao-o-nam-ban` | 44 | 2233 | 19.7 |
| `/nam-ha-sap-nhap-nam-ban` | 42 | 2442 | 17.2 |
| `/ocop-nam-ban` | 40 | 1479 | 27.0 |
| `/novaland-nam-ban` | 39 | 2037 | 19.1 |
| `/ai-nam-ban` | 38 | 1413 | 26.9 |
| `/nam-ban-hay-di-linh` | 36 | 1861 | 19.3 |
| `/nam-ban-la-gi` | 36 | 1126 | 32.0 |
| `/cho-nam-ban` | 35 | 975 | 35.9 |
| `/dat-gan-da-lat` | 35 | 1897 | 18.5 |
| `/ho-me-linh-nam-ban-cam-ly-thuong` | 34 | 1865 | 18.2 |
| `/nam-ban-thuoc-xa-nao` | 34 | 1361 | 25.0 |
| `/ta-nung-hay-me-linh` | 34 | 2449 | 13.9 |
| `/tiem-nang-dau-tu` | 34 | 2220 | 15.3 |
| `/dat-me-linh-nam-ban` | 33 | 1111 | 29.7 |
| `/dat-trung-tam-nam-ban` | 33 | 1098 | 30.1 |
| `/quy-hoach-chung-nam-ban` | 33 | 2106 | 15.7 |
| `/khu-nao-o-nam-ban` | 32 | 1437 | 22.3 |
| `/mot-ngay-o-nam-ban` | 32 | 1986 | 16.1 |
| `/mua-dat-nam-ban` | 32 | 1880 | 17.0 |
| `/nam-ban-hay-dran` | 32 | 1253 | 25.5 |
| `/ve-nam-ban-lam-gi` | 32 | 1383 | 23.1 |
| `/xa-nam-ha-lam-ha` | 32 | 1019 | 31.4 |
| `/chua-linh-an-nam-ban` | 31 | 2207 | 14.0 |
| `/co-nen-mua-dat-nam-ban-o-xa` | 31 | 1774 | 17.5 |
| `/dat-gia-lam-nam-ban` | 31 | 1091 | 28.4 |
| `/ca-phe-nam-ban` | 30 | 2500 | 12.0 |
| `/chuyen-len-nam-ban-song` | 30 | 1670 | 18.0 |
| `/so-sanh-nam-ban-bao-loc-da-lat` | 30 | 1171 | 25.6 |
| `/mua-bo-nam-ban` | 29 | 2308 | 12.6 |
| `/phi-to-nam-ha-lam-ha` | 29 | 1070 | 27.1 |
| `/thuong-mai-dien-tu-nam-ban` | 29 | 1173 | 24.7 |
| `/gia-ca-phe-va-gia-dat-nam-ban` | 28 | 1964 | 14.3 |
| `/mua-mua-nam-ban` | 28 | 1367 | 20.5 |
| `/nam-ban-mua-nao` | 28 | 2148 | 13.0 |
| `/nam-ban-co-gi` | 27 | 1015 | 26.6 |
| `/rau-hoa-cay-do-la-nam-ban` | 27 | 2174 | 12.4 |
| `/truoc-khi-xuong-tien` | 27 | 2146 | 12.6 |
| `/dat-dong-thanh-nam-ban` | 26 | 1068 | 24.3 |
| `/lam-ha-truoc-va-sau-sap-nhap` | 26 | 1510 | 17.2 |
| `/nuoc-o-nam-ban` | 26 | 1486 | 17.5 |

## BẢNG TỔNG — 155 bài, thiếu nhiều nhất trước


| slug | title | H1 | H2 | FAQ | mật độ |
|---|---|---|---|---|---|
| `/lam-ha-truoc-va-sau-sap-nhap` | **✗** | **✗** | 0/7 | 1/8 | 26 |
| `/len-lam-dong-nen-song-o-dau` | **✗** | **✗** | 0/9 | 1/6 | 16 |
| `/len-lam-dong-song-lam-gi` | **✗** | **✗** | 1/7 | 0/6 | 6 |
| `/lam-dong-co-gi-de-lam-an` | **✗** | **✗** | 1/8 | 1/6 | 7 |
| `/dat-the-am-the-duong` | **✗** | **✗** | 0/8 | 5/8 | 11 |
| `/mua-vuon-ca-phe-nam-ban` | **✗** | **✗** | 1/10 | 5/10 | 18 |
| `/nhan-tien-den-bu-dat-nen-lam-gi` | **✗** | **✗** | 1/8 | 4/8 | 6 |
| `/phi-to-nam-ha-lam-ha` | **✗** | **✗** | 2/5 | 2/5 | 29 |
| `/cau-tong-doi-nam-ban` | **✗** | **✗** | 3/6 | 3/7 | 14 |
| `/dieu-de-lai-cho-con` | **✗** | **✗** | — | — | 5 |
| `/vuon-bo-loi-bao-nhieu` | ✓ | **✗** | 0/7 | 4/9 | 11 |
| `/ta-nung-hay-me-linh` | ✓ | **✗** | 2/11 | 1/9 | 34 |
| `/xa-nam-ha-lam-ha` | ✓ | **✗** | 2/6 | 2/5 | 32 |
| `/roi-sai-gon-len-nam-ban` | ✓ | **✗** | 1/4 | 6/6 | 10 |
| `/nguoi-nam-ban-anh-nam` | ✓ | **✗** | — | 6/6 | 13 |
| `/nguoi-nam-ban-chi-trang` | ✓ | **✗** | — | 6/6 | 10 |
| `/dat-vuon-nam-ban-xay-duoc-gi` | ✓ | ✓ | 0/7 | 3/11 | 9 |
| `/ho-dong-thanh-nam-ban` | ✓ | ✓ | 0/10 | 3/10 | 15 |
| `/tach-thua-dat-nam-ban` | ✓ | ✓ | 1/12 | 2/12 | 10 |
| `/len-tho-cu-het-bao-nhieu-tien` | ✓ | ✓ | 0/9 | 4/10 | 14 |
| `/ho-bai-cong-nam-ban` | ✓ | ✓ | 0/8 | 4/9 | 17 |
| `/thac-voi-nam-ban` | ✓ | ✓ | 0/3 | 2/4 | 15 |
| `/mua-dat-co-vuon-ca-phe` | ✓ | ✓ | 0/10 | 7/13 | 15 |
| `/coc-dat-nam-ban` | ✓ | ✓ | 2/7 | 0/3 | 2 |
| `/ban-dat-nam-ban` | ✓ | ✓ | 0/9 | 5/8 | 14 |
| `/ca-phe-nam-ban-ai` | ✓ | ✓ | 0/5 | 4/6 | 19 |
| `/do-dac-dat-nam-ban` | ✓ | ✓ | 1/9 | 4/9 | 14 |
| `/mua-dat-co-vuon-bo` | ✓ | ✓ | 1/12 | 8/16 | 22 |
| `/nguoi-ngoai-tinh-mua-dat-nam-ban` | ✓ | ✓ | 0/8 | 7/10 | 9 |
| `/dau-tam-nam-ban` | ✓ | ✓ | 0/5 | 6/8 | 24 |
| `/quy-trinh-mua-dat-nam-ban` | ✓ | ✓ | 2/8 | 2/6 | 10 |
| `/vua-mua-dat-nam-ban-lam-gi` | ✓ | ✓ | 1/6 | 4/8 | 10 |
| `/nam-ban-mua-nao` | ✓ | ✓ | 0/9 | 10/12 | 28 |
| `/mua-ca-phe-nam-ban` | ✓ | ✓ | 1/7 | 4/7 | 14 |
| `/truoc-khi-xuong-tien` | ✓ | ✓ | 0/8 | 7/8 | 27 |
| `/dat-nam-ban-trong-cay-gi` | ✓ | ✓ | 0/11 | 8/9 | 21 |
| `/duong-ha-bac-nam-ban` | ✓ | ✓ | 3/10 | 3/10 | 18 |
| `/mua-dat-duong-gia-nam-ban` | ✓ | ✓ | 1/8 | 5/7 | 11 |
| `/brief-01` | ✓ | ✓ | 0/4 | — | 13 |
| `/da-lat-di-nam-ban` | ✓ | ✓ | 0/8 | 3/3 | 17 |
| `/dat-nam-ban-cuoi-tuan` | ✓ | ✓ | 0/8 | 3/3 | 10 |
| `/doc-lo-dat-02-view-ho` | ✓ | ✓ | 0/2 | 2/2 | 9 |
| `/homestay-nam-ban-co-lai-khong` | ✓ | ✓ | 1/7 | 5/7 | 24 |
| `/mot-ngay-lam-vuon-nam-ban` | ✓ | ✓ | 0/9 | 2/2 | 9 |
| `/mot-ngay-o-nam-ban` | ✓ | ✓ | 0/5 | 7/7 | 32 |
| `/mua-dat-da-lat-chon-nam-ban` | ✓ | ✓ | 1/4 | 2/4 | 19 |
| `/mua-dat-nam-ban-de-lam-gi` | ✓ | ✓ | 0/6 | 2/2 | 6 |
| `/o-thu-nam-ban-truoc-khi-mua-dat` | ✓ | ✓ | 1/4 | 2/4 | 15 |
| `/sap-nhap-nam-ban-dat` | ✓ | ✓ | 0/3 | — | 21 |
| `/so-sanh-nam-ban-bao-loc-da-lat` | ✓ | ✓ | 0/4 | 7/7 | 30 |
| `/doc-the-dat-nam-ban` | ✓ | ✓ | 1/7 | 6/8 | 18 |
| `/nam-ban-hay-don-duong` | ✓ | ✓ | 2/10 | 8/12 | 53 |
| `/mua-bo-nam-ban` | ✓ | ✓ | 1/7 | 11/14 | 29 |
| `/chuyen-muc-dich-su-dung-dat-nam-ban` | ✓ | ✓ | 1/7 | 8/10 | 17 |
| `/kinh-nghiem-mua-dat-nam-ban` | ✓ | ✓ | 1/7 | 4/5 | 9 |
| `/mua-dat-nam-ban-hop-dong-uy-quyen` | ✓ | ✓ | 6/11 | 0/3 | 10 |
| `/xay-nha-o-nam-ban` | ✓ | ✓ | 1/6 | 4/5 | 18 |
| `/ca-phe-nam-ban` | ✓ | ✓ | 2/9 | 7/10 | 30 |
| `/so-hoa-nam-ban` | ✓ | ✓ | 1/6 | 5/6 | 19 |
| `/mua-dat-nam-ban-500-trieu-1-ty` | ✓ | ✓ | 1/5 | 4/5 | 19 |
| `/5km-o-nam-ban` | ✓ | ✓ | 2/7 | 4/6 | 9 |
| `/dinh-gia-dat-nam-ban` | ✓ | ✓ | 4/10 | 4/9 | 14 |
| `/giu-dat-nam-ban-tu-xa` | ✓ | ✓ | 2/8 | 3/4 | 13 |
| `/kinh-te-so-nam-ban` | ✓ | ✓ | 2/6 | 4/6 | 17 |
| `/loi-di-chung-dat-nam-ban` | ✓ | ✓ | 6/9 | 0/3 | 9 |
| `/chua-linh-an-nam-ban` | ✓ | ✓ | 4/9 | 5/11 | 31 |
| `/nam-ban-va-nam-ha` | ✓ | ✓ | 2/7 | 7/9 | 63 |
| `/thon-nam-ban` | ✓ | ✓ | 3/11 | 21/26 | 46 |
| `/thuy-dien-da-chomo-phi-to` | ✓ | ✓ | 3/7 | 2/4 | 21 |
| `/chi-phi-dat-dai-nam-ban` | ✓ | ✓ | 7/15 | 7/15 | 18 |
| `/nam-ban-hay-di-linh` | ✓ | ✓ | 1/5 | — | 36 |
| `/ram-vu-lan-nam-ban` | ✓ | ✓ | 3/8 | 2/3 | 10 |
| `/dat-nguon-goc-lam-nghiep-nam-ban` | ✓ | ✓ | 3/8 | 9/13 | 23 |
| `/cay-xang-petro-moi-o-nam-ban` | ✓ | ✓ | 1/3 | 4/5 | 15 |
| `/quy-hoach-chung-nam-ban` | ✓ | ✓ | 2/7 | 12/12 | 33 |
| `/mua-dat-nam-ban-co-nguoi-dang-canh-tac` | ✓ | ✓ | 5/8 | 1/3 | 8 |
| `/nam-ha-sap-nhap-nam-ban` | ✓ | ✓ | 5/17 | 1/1 | 42 |
| `/nam-ban-hay-dran` | ✓ | ✓ | 2/5 | 6/7 | 32 |
| `/nam-ban-co-hop-voi-ban` | ✓ | ✓ | 1/3 | 7/7 | 24 |
| `/san-bay-lien-khuong-mo-lai` | ✓ | ✓ | 1/3 | — | 12 |
| `/nha-go-thong-nam-ban` | ✓ | ✓ | 5/7 | 1/4 | 10 |
| `/nam-ban-hay-duc-trong` | ✓ | ✓ | 3/8 | 8/8 | 50 |
| `/rau-hoa-cay-do-la-nam-ban` | ✓ | ✓ | 3/6 | 9/12 | 27 |
| `/nen-xem-khu-nao-o-nam-ban` | ✓ | ✓ | 3/7 | 9/10 | 44 |
| `/tra-cuu-dat-nam-ban` | ✓ | ✓ | 3/5 | 3/5 | 10 |
| `/dac-san-nam-ban` | ✓ | ✓ | 2/5 | 4/4 | 20 |
| `/duong-di-nam-ban` | ✓ | ✓ | 2/5 | 7/7 | 47 |
| `/mua-dat-nam-ban` | ✓ | ✓ | 2/5 | — | 32 |
| `/tiem-nang-dau-tu` | ✓ | ✓ | 2/5 | 4/4 | 34 |
| `/xay-nha-nho-nam-ban-bao-nhieu-tien` | ✓ | ✓ | 4/7 | 2/3 | 9 |
| `/nam-ban-hay-lac-duong` | ✓ | ✓ | 6/11 | 8/11 | 59 |
| `/nam-ban-co-dang-song` | ✓ | ✓ | 3/7 | 5/5 | 25 |
| `/o-nam-ban-mot-nam-moi-biet` | ✓ | ✓ | 4/8 | 6/7 | 19 |
| `/pickleball-nam-ban` | ✓ | ✓ | 3/7 | 2/2 | 11 |
| `/nam-ban-sau-6h-toi` | ✓ | ✓ | 4/7 | 5/6 | 19 |
| `/khu-nao-o-nam-ban` | ✓ | ✓ | 4/7 | 6/7 | 32 |
| `/nam-ban-co-gi` | ✓ | ✓ | 3/6 | — | 27 |
| `/quy-hoach-2050` | ✓ | ✓ | 3/6 | 5/5 | 47 |
| `/tour-ca-phe-nam-ban` | ✓ | ✓ | 4/8 | 7/7 | 22 |
| `/ve-nam-ban-lam-gi` | ✓ | ✓ | 4/7 | 6/6 | 32 |
| `/an-gi-o-nam-ban` | ✓ | ✓ | 3/5 | 5/5 | 24 |
| `/google-maps-khong-noi-ve-nam-ban` | ✓ | ✓ | 3/5 | 6/6 | 13 |
| `/duong-nam-ban-phi-to-da-lat` | ✓ | ✓ | 3/4 | 3/4 | 22 |
| `/xay-nha-giap-rung-thong-nam-ban` | ✓ | ✓ | 8/8 | 1/4 | 10 |
| `/ocop-nam-ban` | ✓ | ✓ | 6/8 | 7/9 | 40 |
| `/10-10-1975-nam-ban` | ✓ | ✓ | 7/9 | 3/4 | 21 |
| `/nam-ban-co-sap-nhap-da-lat` | ✓ | ✓ | 5/7 | 9/10 | 62 |
| `/dat-gan-da-lat` | ✓ | ✓ | 4/6 | — | 35 |
| `/dat-giap-rung-thong-nam-ban` | ✓ | ✓ | 7/7 | 1/3 | 16 |
| `/mua-chung-dat-nam-ban` | ✓ | ✓ | 6/9 | 3/3 | 23 |
| `/mua-nha-xay-san-nam-ban` | ✓ | ✓ | 6/9 | — | 12 |
| `/nam-ban-thuoc-xa-nao` | ✓ | ✓ | 2/3 | — | 34 |
| `/dat-nam-ban-chua-xay` | ✓ | ✓ | 5/6 | 4/6 | 12 |
| `/ho-me-linh-nam-ban-cam-ly-thuong` | ✓ | ✓ | 8/9 | 3/5 | 34 |
| `/ho-thanh-tri-nam-ban` | ✓ | ✓ | 6/7 | 2/3 | 16 |
| `/lam-viec-tu-xa-o-nam-ban` | ✓ | ✓ | 5/7 | 6/6 | 20 |
| `/mua-nha-nam-ban-khong-o` | ✓ | ✓ | 4/5 | 5/6 | 19 |
| `/ban-do-quy-hoach-nam-ban` | ✓ | ✓ | 3/4 | 3/3 | 23 |
| `/ho-tron-nam-ban` | ✓ | ✓ | 6/8 | 2/2 | 25 |
| `/view-panorama-nam-ban` | ✓ | ✓ | 9/10 | 3/4 | 22 |
| `/dat-nam-ban-xuong-gia-ban-hay-giu` | ✓ | ✓ | 7/9 | — | 13 |
| `/gia-ca-phe-va-gia-dat-nam-ban` | ✓ | ✓ | 7/9 | — | 28 |
| `/ho-o-nam-ban` | ✓ | ✓ | 7/9 | 3/3 | 21 |
| `/tram-sac-nam-ban` | ✓ | ✓ | 4/5 | 5/5 | 21 |
| `/cho-nam-ban` | ✓ | ✓ | 5/6 | 6/6 | 35 |
| `/dat-trung-tam-nam-ban` | ✓ | ✓ | 5/6 | 5/5 | 33 |
| `/lo-dat-nam-ban-binh-thuong` | ✓ | ✓ | 5/6 | — | 11 |
| `/nuoc-o-nam-ban` | ✓ | ✓ | 5/6 | 10/10 | 26 |
| `/xem-dat-nam-ban-chua-mua-duoc` | ✓ | ✓ | 5/6 | 6/6 | 17 |
| `/ai-nam-ban` | ✓ | ✓ | 6/7 | 6/6 | 38 |
| `/dat-nam-ban-duong-dat` | ✓ | ✓ | 6/7 | — | 11 |
| `/dat-nam-ban-tho-cu-san` | ✓ | ✓ | 6/7 | — | 8 |
| `/ho-tu-liem-nam-ban` | ✓ | ✓ | 6/7 | 3/3 | 16 |
| `/xay-nha-giap-suoi-nam-ban` | ✓ | ✓ | 6/6 | 3/4 | 9 |
| `/dai-hoc-da-lat-nam-ban` | ✓ | ✓ | 4/4 | 4/5 | 19 |
| `/dat-giap-suoi-nam-ban` | ✓ | ✓ | 8/8 | 4/5 | 14 |
| `/novaland-nam-ban` | ✓ | ✓ | 9/10 | 9/9 | 39 |
| `/brief-02` | ✓ | ✓ | 7/7 | — | 17 |
| `/brief-03` | ✓ | ✓ | 8/8 | — | 15 |
| `/cau-chuyen-nam-ban` | ✓ | ✓ | — | — | 8 |
| `/chuan-bi-truoc-khi-ban-dat-nam-ban` | ✓ | ✓ | 10/10 | — | 12 |
| `/chuyen-len-nam-ban-song` | ✓ | ✓ | 7/7 | 11/11 | 30 |
| `/co-nen-mua-dat-nam-ban-o-xa` | ✓ | ✓ | 5/5 | 7/7 | 31 |
| `/dat-dong-thanh-nam-ban` | ✓ | ✓ | 6/6 | 5/5 | 26 |
| `/dat-gia-lam-nam-ban` | ✓ | ✓ | 6/6 | 5/5 | 31 |
| `/dat-giap-ho-nam-ban` | ✓ | ✓ | 8/8 | 4/4 | 16 |
| `/dat-me-linh-nam-ban` | ✓ | ✓ | 6/6 | 5/5 | 33 |
| `/doc-lo-dat` | ✓ | ✓ | — | — | 5 |
| `/hoa-o-nam-ban` | ✓ | ✓ | 9/9 | 4/4 | 18 |
| `/mua-mua-nam-ban` | ✓ | ✓ | 7/7 | 9/9 | 28 |
| `/nam-ban-la-gi` | ✓ | ✓ | 7/7 | 5/5 | 36 |
| `/nha-go-nam-ban` | ✓ | ✓ | 7/7 | 3/3 | 13 |
| `/thuong-mai-dien-tu-nam-ban` | ✓ | ✓ | 5/5 | 6/6 | 29 |
| `/xa-nam-ban-lam-ha` | ✓ | ✓ | 10/10 | 7/7 | 57 |
| `/xay-nha-giap-ho-nam-ban` | ✓ | ✓ | 5/5 | 3/3 | 12 |
