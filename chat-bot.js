/* Bot hỏi–đáp MIỄN PHÍ của Nam Ban Panorama (bản thử, 19/11/2026).
 * Không dùng AI viết câu: chạy trong trình duyệt, so câu hỏi với chat-index.json
 * (hỏi–đáp FAQ + mục bài) rồi trả lại NGUYÊN VĂN câu trả lời đã có trên web, kèm link bài.
 * Không máy chủ, không khoá API, không phí. Chạy được cả trong Node để kiểm thử.
 * Kho sinh bằng tools/gen-chat-index.py. */
(function (root) {
  'use strict';

  function fold(s) {
    s = String(s || '').toLowerCase().replace(/đ/g, 'd').replace(/²/g, '2').replace(/³/g, '3');
    s = s.normalize ? s.normalize('NFD').replace(/[̀-ͯ]/g, '') : s;
    return s.replace(/[^a-z0-9]+/g, ' ').trim();
  }
  function lowerToks(s) {
    return String(s || '').toLowerCase().replace(/²/g, '2').replace(/[^0-9a-zà-ỹđ]+/g, ' ').trim().split(/\s+/).filter(Boolean);
  }
  var HAS_MARK = /[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]/;

  // Từ đệm, viết CÓ dấu: chỉ bỏ khi người gõ có dấu (gõ không dấu thì "cho" có thể là "chợ").
  var STOP_MARK = new Set(('là gì có không thì và của cho ở thế nào như một những các được để với về tôi mình em anh chị ' +
    'ơi à nhé ạ vậy rồi sao hay hoặc tại từ đến này đó kia mà ra vào cũng còn hơn nhất rất quá làm bị nên cần muốn ' +
    'bạn ai cái con người đi xem hỏi biết cho tôi giúp xin').split(' '));
  // Từ đệm khi gõ KHÔNG dấu: bỏ những chữ trùng với từ có nghĩa ("chi" phí, đất "nen", đầu "tu", "lam" đồng, "cho" chợ).
  var STOP_FOLD = new Set(('la gi co khong thi va cua o the nao nhu mot nhung cac duoc voi toi minh em oi a nhe vay roi ' +
    'sao hay hoac ma cung rat qua bi muon ban oi ai cai xem hoi biet giup xin').split(' '));
  // "ban" bị bỏ khi gõ không dấu vì trùng "bán" — nhưng "nam ban" vẫn được tính nhờ cặp chữ (bigram).

  // Gõ khác chữ nhưng cùng ý (đã bỏ dấu). Chỉ thêm từ, không thay từ người gõ.
  var SYN = [
    [/\bbao xa\b|\bmay km\b|\bbao nhieu km\b|\bmay cay\b|\bbao nhieu cay so\b/, 'cach km'],
    [/\bdalat\b/, 'da lat'],
    [/\bso hong\b/, 'so do giay chung nhan'],
    [/\bso do\b/, 'so hong'],
    [/\btho cu\b/, 'dat o'],
    [/\bdat o\b/, 'tho cu'],
    [/\bsan bay\b/, 'lien khuong'],
    [/\bchi phi\b|\bton bao nhieu\b|\bhet bao nhieu\b/, 'tien phi gia'],
    [/\bgia dat\b/, 'index trung vi'],
    [/\bthoi tiet\b/, 'khi hau nhiet do'],
    [/\bdan so\b|\bbao nhieu dan\b|\bbao nhieu nguoi\b/, 'bao nhieu dan nguoi'],
    [/\bdien tich\b/, 'km2 ha'],
    [/\bsap nhap\b|\bsat nhap\b/, 'sap nhap sat nhap 1 7 2025'],
    [/\bchua linh an\b|\blinh an\b/, 'chua linh an thac voi'],
    [/\bdo cao\b|\bcao bao nhieu\b/, 'cao bao nhieu met'],
  ];

  var D = null; // dữ liệu đã dựng

  function build(json) {
    var pages = json.pages, rows = json.rows, N = rows.length;
    // Hai bộ thống kê: chữ đã bỏ dấu (F) cho người gõ không dấu, chữ giữ dấu (A) cho người gõ có dấu
    // ("mưa" hiếm hơn hẳn "mua"; gộp chung thì "mùa mưa" khớp nhầm "mùa bơ", "mùa hoa").
    var docs = [], dfF = Object.create(null), dfA = Object.create(null), sum = { F: [0, 0, 0], A: [0, 0, 0] };
    for (var i = 0; i < N; i++) {
      var r = rows[i], pg = pages[r[3]], ans = r[2].slice(0, 500);
      var F = [fold(r[1]).split(' '), fold(pg[1]).split(' '), fold(ans).split(' ')];
      var A = [lowerToks(r[1]), lowerToks(pg[1]), lowerToks(ans)];
      count(F, dfF); count(A, dfA);
      for (var j = 0; j < 3; j++) { sum.F[j] += F[j].length; sum.A[j] += A[j].length; }
      docs.push({ k: r[0], q: r[1], a: r[2], u: pg[0] + (r[4] ? '#' + r[4] : ''), t: pg[1],
        F: { tf: F.map(tf), len: F.map(function (x) { return x.length; }), sq: ' ' + F[0].join(' ') + ' ', st: ' ' + F[1].join(' ') + ' ' },
        A: { tf: A.map(tf), len: A.map(function (x) { return x.length; }), sq: ' ' + A[0].join(' ') + ' ', st: ' ' + A[1].join(' ') + ' ' } });
    }
    function idfOf(df) {
      var o = Object.create(null), mx = 0;
      for (var w in df) { o[w] = Math.log(1 + (N - df[w] + 0.5) / (df[w] + 0.5)); if (o[w] > mx) mx = o[w]; }
      return { m: o, max: mx };
    }
    D = { docs: docs, N: N, F: idfOf(dfF), A: idfOf(dfA),
      avg: { F: sum.F.map(function (x) { return x / N; }), A: sum.A.map(function (x) { return x / N; }) } };
    return D;
  }
  function count(fields, df) {
    var seen = Object.create(null);
    fields.forEach(function (arr) { arr.forEach(function (w) { if (w && !seen[w]) { seen[w] = 1; df[w] = (df[w] || 0) + 1; } }); });
  }
  function tf(arr) { var m = Object.create(null); arr.forEach(function (w) { if (w) m[w] = (m[w] || 0) + 1; }); return m; }

  function bm25(tfm, len, avg, w, idf) {
    var f = tfm[w]; if (!f) return 0;
    var k1 = 1.2, b = 0.75;
    return idf * (f * (k1 + 1)) / (f + k1 * (1 - b + b * len / avg));
  }
  var W = [3, 1.5, 1]; // trọng số: câu hỏi/tiêu đề mục · tựa bài · câu trả lời

  function parse(query) {
    var marked = HAS_MARK.test(query);
    var raw = lowerToks(query), keep = [], accSeq = [];
    raw.forEach(function (t) {
      var ft = fold(t);
      if (!ft) return;
      accSeq.push(t);
      if (marked ? STOP_MARK.has(t) : STOP_FOLD.has(ft)) return;
      // chữ có dấu → so theo bộ giữ dấu; chữ không dấu (nam, ban, km, 2025, hoặc gõ lười dấu) → bộ bỏ dấu
      keep.push(HAS_MARK.test(t) ? { m: 'A', w: t } : { m: 'F', w: ft });
    });
    var all = fold(query), extra = [];
    SYN.forEach(function (s) { if (s[0].test(all)) extra = extra.concat(s[1].split(' ')); });
    var pairs = [], fs = all.split(' ').filter(Boolean);
    if (marked) for (var i = 0; i + 1 < accSeq.length; i++) pairs.push({ m: 'A', p: accSeq[i] + ' ' + accSeq[i + 1] });
    else for (var k = 0; k + 1 < fs.length; k++) pairs.push({ m: 'F', p: fs[k] + ' ' + fs[k + 1] });
    return { terms: keep, extra: extra, pairs: pairs, marked: marked };
  }

  function score(doc, P) {
    var s = 0, hit = 0, tot = 0;
    P.terms.forEach(function (t) {
      var M = D[t.m], st = doc[t.m], avg = D.avg[t.m];
      var i = M.m[t.w] !== undefined ? M.m[t.w] : M.max; // chữ không có trong kho = hiếm nhất (câu ngoài chủ đề sẽ hụt độ phủ)
      tot += i;
      var v = 0;
      for (var j = 0; j < 3; j++) v += W[j] * bm25(st.tf[j], st.len[j], avg[j], t.w, i);
      if (v > 0) { s += v; hit += i; }
    });
    P.extra.forEach(function (w) {
      var i = (D.F.m[w] || 0) * 0.6;
      s += 1.5 * bm25(doc.F.tf[0], doc.F.len[0], D.avg.F[0], w, i) + 0.5 * bm25(doc.F.tf[2], doc.F.len[2], D.avg.F[2], w, i);
    });
    P.pairs.forEach(function (pp) {
      var M = D[pp.m], st = doc[pp.m], ws = pp.p.split(' ');
      var i = ((M.m[ws[0]] || 0) + (M.m[ws[1]] || 0)) / 2;
      if (st.sq.indexOf(' ' + pp.p + ' ') >= 0) s += 1.6 * i;
      else if (st.st.indexOf(' ' + pp.p + ' ') >= 0) s += 1.0 * i;
    });
    if (doc.k === 0) s *= 1.12; // hỏi–đáp viết sẵn được ưu tiên hơn mục bài
    return { s: s, cov: tot ? hit / tot : 0 };
  }

  function ask(query, opts) {
    opts = opts || {};
    if (!D) throw new Error('chưa nạp chat-index');
    var P = parse(query);
    if (!P.terms.length) return { ok: false, reason: 'trống', more: [] };
    var res = [];
    for (var i = 0; i < D.docs.length; i++) {
      var r = score(D.docs[i], P);
      if (r.s > 0) res.push({ d: D.docs[i], s: r.s, cov: r.cov });
    }
    res.sort(function (a, b) { return b.s - a.s; });
    var top = res[0];
    var minScore = opts.minScore || 9, minCov = opts.minCov || 0.55;
    var ok = !!top && top.s >= minScore && top.cov >= minCov;
    var seen = new Set(), more = [];
    for (var j = ok ? 1 : 0; j < res.length && more.length < 3; j++) {
      var d = res[j].d, key = d.u.split('#')[0];
      if (seen.has(key) || (top && key === top.d.u.split('#')[0])) continue;
      if (res[j].s < (ok ? top.s * 0.45 : 4)) break;
      seen.add(key); more.push(res[j]);
    }
    return { ok: ok, top: top, more: more, parsed: P };
  }

  var api = { fold: fold, build: build, ask: ask, parse: parse };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.NBBot = api;
})(typeof window !== 'undefined' ? window : this);
