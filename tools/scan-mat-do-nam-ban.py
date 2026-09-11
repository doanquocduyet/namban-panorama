# -*- coding: utf-8 -*-
"""Rà mật độ "Nam Ban" ở 4 chỗ: title · H1 · H2 nội dung · câu hỏi FAQ.
CHỈ ĐẾM VÀ BÁO — không sửa gì.

Bài học đã vá (đừng lặp lại):
  - KHÔNG bám một class duy nhất để khoanh thân bài. Site có hai template
    (§7.2) nên container là .art-body HOẶC .body, và vài bài không có cả hai.
    Mốc kết thúc cũng ba dạng: share-row / share-row fu / không có.
    Dùng CHUỖI MỐC DỰ PHÒNG, và in danh sách file bị loại để người đọc soi lại.
  - Luật 13d: html.unescape() rồi bỏ \xa0 TRƯỚC khi so chuỗi.
  - Luật 4: so case-insensitive.
"""
import re, html, glob, json

HUB = {'index.html','404.html','_mau-bai-viet.html','brief.html','trao-doi.html',
       'nam-ban.html','dat.html','dau-tu.html','hoi-nhanh.html','namban-index.html',
       'doc-nhanh.html','nam-ban-co-gi-moi.html'}
SKIP_H = ('câu hỏi thường gặp','nguồn & lưu ý','nguồn và lưu ý','đọc gì tiếp',
          'câu hỏi nhanh','hỏi nhanh','đọc thêm','chia sẻ')

flat  = lambda s: html.unescape(s).replace('\xa0', ' ')
strip = lambda s: re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s)).strip()
has   = lambda s: 'nam ban' in strip(flat(s)).lower()

def zone(raw):
    """Khoanh thân bài bằng chuỗi mốc dự phòng."""
    st = None
    for pat in (r'<div class="art-body"', r'<div class="body"', r'</h1>'):
        m = re.search(pat, raw)
        if m: st = m.end(); break
    if st is None: return None
    en = len(raw)
    for pat in (r'<div class="share-row', r'<div class="next-read',
                r'<div class="source-box', r'<footer'):
        m = re.search(pat, raw[st:])
        if m: en = st + m.start(); break
    return raw[st:en]

def scan(path):
    raw = open(path, encoding='utf-8').read()
    if path in HUB or path.startswith('demo-'): return None, 'hub / trang chức năng'
    if 'lang="vi"' not in raw[:300]:            return None, 'không phải lang="vi"'
    if '<h1' not in raw:                        return None, 'không có <h1>'
    body = zone(raw)
    if body is None:                            return None, 'không khoanh được thân bài'

    t  = re.search(r'<title>(.*?)</title>', raw, re.S)
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', raw, re.S)
    h2 = [strip(flat(x)) for x in re.findall(r'<h2[^>]*>(.*?)</h2>', body, re.S)]
    h2 = [x for x in h2 if x and x.lower() not in SKIP_H]

    faq, mq = [], re.search(r'<h2[^>]*>\s*Câu hỏi thường.*?</h2>', body, re.S | re.I)
    if mq:
        sb = body.find('<div class="source-box"', mq.end())
        faq = [strip(flat(x)) for x in
               re.findall(r'<h3[^>]*>(.*?)</h3>', body[mq.end(): sb if sb > 0 else len(body)], re.S)]
        faq = [x for x in faq if x and x.lower() not in SKIP_H]

    # bài không có H2/FAQ vẫn phải tính cho nhóm A và B (title, H1)
    return dict(slug=path[:-5],
                title=strip(flat(t.group(1))) if t else '',
                h1=strip(flat(h1.group(1))) if h1 else '',
                h2=h2, faq=faq,
                dens=strip(flat(body)).lower().count('nam ban'),
                words=len(strip(flat(body)).split())), None

DOMAIN = ('đất','nhà','giá','hồ','đường','cà phê','dâu tằm','bơ','vườn','thác','chùa','cầu',
          'sân bay','quy hoạch','sổ','thửa','lô','khu','xã','view','rừng','thông','suối','mưa',
          'nắng','mùa','homestay','farmstay','chợ','điện','nước','thuế','phí','tằm','tơ','dân')
BROAD  = ('lâm đồng','toàn quốc','cả nước','luật ','nghị định','nghị quyết','thông tư',
          'bảng giá đất','vi bằng','công chứng','thuế','lệ phí','trước bạ','sổ chung','sổ đỏ')

def tag(s, h1_has):
    l = s.lower()
    if any(k in l for k in BROAD):        return '[KHÔNG SỬA — truy vấn rộng]'
    if not any(k in l for k in DOMAIN):   return '[KHÔNG SỬA — câu tu từ]'
    if h1_has:                            return '[KHÔNG SỬA? — H1 đã neo]'
    return ''

if __name__ == '__main__':
    rows, skip = [], []
    for f in sorted(glob.glob('*.html')):
        d, why = scan(f)
        rows.append(d) if d else skip.append((f, why))
    A = [r for r in rows if not has(r['title'])]
    B = [r for r in rows if not has(r['h1'])]
    C = [r for r in rows if r['h2'] and sum(map(has, r['h2']))/len(r['h2']) < .5]
    D = [r for r in rows if r['faq'] and sum(map(has, r['faq']))/len(r['faq']) < .3]
    E = [r for r in rows if r['dens'] > 25]
    nC = sum(sum(1 for x in r['h2'] if not has(x)) for r in C)
    nD = sum(sum(1 for x in r['faq'] if not has(x)) for r in D)
    print('bài quét: %d | loại: %d' % (len(rows), len(skip)))
    for f, w in skip: print('   loại  %-38s %s' % (f, w))
    print('A title thiếu : %d' % len(A))
    print('B H1 thiếu    : %d' % len(B))
    print('C H2 <50%%     : %d bài / %d câu' % (len(C), nC))
    print('D FAQ <30%%    : %d bài / %d câu' % (len(D), nD))
    print('E dens >25    : %d bài' % len(E))
    print('TỔNG CA =', len(A)+len(B)+nC+nD+len(E))
    json.dump(dict(rows=rows, skip=skip), open('/tmp/scan.json','w'), ensure_ascii=False)
