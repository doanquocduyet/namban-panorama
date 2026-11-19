// Chấm bot hỏi–đáp (chat-bot.js) trên bộ câu thử tools/chat-eval.json — chạy SAU MỖI LẦN sửa chat-bot.js
// hoặc gen-chat-index.py:   node tools/chat-eval.js [-v]
// Bộ "chinh" (112 câu) đã dùng để chỉnh ngưỡng; bộ "giu-lai" (52 câu) chưa dùng để chỉnh — số của bộ này mới
// là số thật. Mốc 19/11/2026: chinh 93/100 đúng ngay câu đầu, 0 trả bừa · giu-lai 35/44, 1 sai bài, 2/8 trả bừa.
// Sửa xong mà số tụt (nhất là "sai bài", "trả bừa") thì đừng đẩy lên.
const path = require('path'), fs = require('fs'), ROOT = path.join(__dirname, '..');
const B = require(path.join(ROOT, 'chat-bot.js'));
B.build(JSON.parse(fs.readFileSync(path.join(ROOT, 'chat-index.json'), 'utf8')));
const all = JSON.parse(fs.readFileSync(path.join(__dirname, 'chat-eval.json'), 'utf8')), verbose = process.argv.includes('-v');
const base = u => (u || '').split('#')[0].replace(/\/$/, '') || '/';
for (const bo of ['chinh', 'giu-lai']) {
  let n = 0, top1 = 0, inMore = 0, wrong = 0, miss = 0, negOk = 0, negBad = 0, nNeg = 0; const fails = [];
  for (const it of all.filter(x => x.bo === bo)) {
    const r = B.ask(it.q), ok = new Set(it.ok_urls.map(base));
    if (!ok.size) { nNeg++; if (!r.ok) negOk++; else { negBad++; fails.push(['TRẢ BỪA', it.q, r.top.d.q]); } continue; }
    n++;
    if (!r.ok) { miss++; fails.push(['BÁO CHƯA CÓ', it.q, r.top ? r.top.d.q : '—']); continue; }
    const t = base(r.top.d.u);
    if (ok.has(t)) top1++;
    else if (r.more.some(m => ok.has(base(m.d.u)))) { inMore++; fails.push(['ĐÚNG Ở GỢI Ý', it.q, r.top.d.q]); }
    else { wrong++; fails.push(['SAI BÀI', it.q, r.top.d.q]); }
  }
  const pct = x => (100 * x / Math.max(n, 1)).toFixed(0) + '%';
  console.log(`[${bo}] có bài ${n}: đúng ngay câu đầu ${top1} (${pct(top1)}) · đúng ở gợi ý ${inMore} · sai bài ${wrong} · báo nhầm "chưa có" ${miss}` +
    ` | không có bài ${nNeg}: nói đúng "chưa có" ${negOk} · trả bừa ${negBad}`);
  if (verbose) fails.forEach(f => console.log('  -', f[0], '|', f[1], '| bot:', f[2]));
}
