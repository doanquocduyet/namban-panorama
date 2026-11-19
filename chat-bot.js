/* Hỏi–đáp MIỄN PHÍ của Nam Ban Panorama (thêm 19/11/2026).
 * Không dùng AI viết câu: chạy trong trình duyệt, so câu hỏi với chat-index.json
 * (hỏi–đáp FAQ + mục bài) rồi trả lại NGUYÊN VĂN câu trả lời đã có trên web, kèm link bài.
 * Không máy chủ, không khoá API, không phí. Chạy được cả trong Node để kiểm thử.
 * Kho sinh bằng tools/gen-chat-index.py. Dùng ở ô tìm kiếm (panorama-utils.js) và đầu /hoi-nhanh.
 *
 * Cách so: BM25 trên ba trường (câu hỏi · tựa bài · câu trả lời), hai bộ thống kê (giữ dấu / bỏ dấu),
 * chuẩn hoá chữ gõ tắt (ko, bn, dl, 500tr…), sửa lỗi gõ một chữ, tách câu hỏi hai ý, khớp hai chiều
 * (câu hỏi có sẵn phải nằm gần trọn trong câu người gõ), phạt khi câu có sẵn nói một địa danh khác. */
(function (root) {
  'use strict';

  // Số và đơn vị viết như nhau ở hai phía: "1.000 m²" = "1000m2", "500tr" = "500 tr".
  function pre(s) {
    s = String(s || '').toLowerCase().replace(/²/g, '2').replace(/³/g, '3');
    for (var i = 0; i < 2; i++) s = s.replace(/(\d)\.(\d{3})(?!\d)/g, '$1$2');
    return s.replace(/(\d)(m2|m|ha|km|tr|ty|tỷ|triệu|trieu|ngàn|nghìn)(?![a-zà-ỹđ0-9])/g, '$1 $2');
  }
  function fold(s) {
    s = pre(s).replace(/đ/g, 'd');
    s = s.normalize ? s.normalize('NFD').replace(/[̀-ͯ]/g, '') : s;
    return s.replace(/[^a-z0-9]+/g, ' ').trim();
  }
  function lowerToks(s) {
    return pre(s).replace(/[^0-9a-zà-ỹđ]+/g, ' ').trim().split(/\s+/).filter(Boolean);
  }
  var HAS_MARK = /[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]/;

  // Từ đệm viết CÓ dấu: chỉ bỏ khi người gõ có dấu (gõ không dấu thì "cho" có thể là "chợ").
  var STOP_MARK = new Set(('là gì có không thì và của cho ở thế nào như một những các được để với về tôi mình em anh chị ' +
    'ơi à nhé ạ vậy rồi sao hay hoặc tại từ đến này đó kia mà ra vào cũng còn hơn nhất rất quá làm bị nên cần muốn ' +
    'bạn ai cái con người đi xem hỏi biết giúp xin giờ bây khoảng chừng tầm đang lúc thật nhỉ đâu hiện nay đây ' +
    'mấy bao nhiêu').split(' '));
  // Từ đệm khi gõ KHÔNG dấu: bỏ những chữ trùng với từ có nghĩa ("chi" phí, đất "nen", đầu "tu", "lam" đồng, "cho" chợ).
  var STOP_FOLD = new Set(('la gi co khong thi va cua o the nao nhu mot nhung cac duoc voi toi minh em oi a nhe vay roi ' +
    'sao hay hoac ma cung rat qua bi muon ban ai cai xem hoi biet giup xin khoang luc nhi may bao nhieu gio hien nay').split(' '));
  // Cố ý KHÔNG bỏ: "dau" (đâu/đầu tư/dâu tằm), "tam" (tằm), "chung" (sổ chung), "dang" (đáng sống), "bay" (sân bay), "gio" (gió).
  // "ban" bị bỏ khi gõ không dấu vì trùng "bán" — nhưng "nam ban" vẫn được tính nhờ cặp chữ.
  // "bao nhiêu", "mấy" là chữ hỏi số lượng: không tính vào độ phủ, vẫn được cộng điểm qua cặp chữ ("bao nhiêu km").

  // Chữ gõ tắt / gõ nói → chữ đủ. Chỉ áp cho câu người gõ, không áp cho kho.
  var ABBR = {
    ko: 'không', k: 'không', khg: 'không', kh: 'không', hok: 'không', hông: 'không', khum: 'không', hem: 'không',
    bn: 'bao nhiêu', bnh: 'bao nhiêu', baonhieu: 'bao nhiêu', nhiu: 'nhiêu',
    dc: 'được', đc: 'được', dk: 'được', đk: 'được',
    dl: 'đà lạt', đl: 'đà lạt', dalat: 'đà lạt',
    sg: 'sài gòn', hcm: 'sài gòn', tphcm: 'sài gòn', saigon: 'sài gòn',
    nb: 'nam ban', namban: 'nam ban',
    vs: 'hay', tr: 'triệu', j: 'gì', z: 'vậy', v: 'vậy', ntn: 'như thế nào', lm: 'làm', mn: 'mọi người',
    ng: 'người', r: 'rồi', vô: 'vào', zô: 'vào', nhâp: 'nhập', thổcư: 'thổ cư'
  };

  // Gõ khác chữ nhưng cùng ý (đã bỏ dấu). Chỉ THÊM từ, không thay từ người gõ.
  var SYN = [
    [/\bbao xa\b|\bbao nhieu km\b|\bmay km\b|\bmay cay\b|\bbao nhieu cay so\b/, 'cach km'],
    [/\bso hong\b/, 'so do giay chung nhan'],
    [/\bso do\b/, 'so hong'],
    [/\btho cu\b/, 'dat o'],
    [/\bdat o\b/, 'tho cu'],
    [/\blen tho cu\b|\bchuyen tho cu\b/, 'chuyen muc dich'],
    [/\bsan bay\b/, 'lien khuong'],
    [/\bchi phi\b|\bton bao nhieu\b|\bhet bao nhieu\b|\bbao nhieu tien\b/, 'tien phi gia'],
    [/\bgia dat\b/, 'index trung vi'],
    [/\bthoi tiet\b/, 'khi hau nhiet do'],
    [/\bdan so\b|\bbao nhieu dan\b|\bbao nhieu nguoi\b/, 'bao nhieu dan nguoi'],
    [/\bdien tich\b/, 'km2 ha'],
    [/\bsap nhap\b|\bsat nhap\b/, 'sap nhap sat nhap 1 7 2025'],
    [/\blinh an\b/, 'chua linh an thac voi'],
    [/\bdo cao\b|\bcao bao nhieu\b/, 'cao bao nhieu met'],
    [/\bxe buyt\b|\bxe bus\b|\bxe khach\b/, 'xe buyt xe khach'],
    [/\btaxi\b|\bgrab\b|\bxe om\b/, 'taxi grab'],
    [/\binternet\b|\bwifi\b|\bcap quang\b/, 'internet wifi cap quang'],
    [/\bremote\b|\blam tu xa\b|\bwfh\b/, 'lam viec tu xa'],
    [/\bcap 3\b/, 'cap ba'],
    [/\bmon ngon\b|\bquan an\b|\ban uong\b/, 'an gi quan'],
    [/\blen gia\b/, 'tang gia'],
    [/\bsang ten\b/, 'chuyen nhuong'],
    [/\bsai gon\b/, 'tp hcm'],
    [/\btrieu m2\b|\btrieu 1 m2\b|\btrieu met\b/, 'gia trieu m2']
  ];

  // Địa danh: câu có sẵn nói Nam Hà mà người gõ hỏi Nam Ban → hạ điểm (Nam Hà là xã riêng, xem CLAUDE.md §5).
  var ENT = ['nam ha', 'phi to', 'ta nung', 'duc trong', 'di linh', 'lac duong', 'd ran', 'dran', 'don duong', 'bao loc',
    'lien nghia', 'thac voi', 'linh an', 'cam ly', 'lien khuong', 'tan ha', 'dinh van', 'phu son', 'dan phuong'];

  var D = null;

  function build(json) {
    var pages = json.pages, rows = json.rows, N = rows.length;
    // Hai bộ thống kê: chữ bỏ dấu (F) cho người gõ không dấu, chữ giữ dấu (A) cho người gõ có dấu
    // ("mưa" hiếm hơn hẳn "mua"; gộp chung thì "mùa mưa" khớp nhầm "mùa bơ").
    var docs = [], dfF = Object.create(null), dfA = Object.create(null), sum = { F: [0, 0, 0], A: [0, 0, 0] };
    var pF = Object.create(null), pA = Object.create(null); // chữ → các dòng có chữ đó (chỉ chấm dòng có chung chữ hiếm)
    for (var i = 0; i < N; i++) {
      var r = rows[i], pg = pages[r[3]], ans = r[2].slice(0, 500);
      var F = [fold(r[1]).split(' '), fold(pg[1]).split(' '), fold(ans).split(' ')];
      var A = [lowerToks(r[1]), lowerToks(pg[1]), lowerToks(ans)];
      count(F, dfF); count(A, dfA); post(F, pF, i); post(A, pA, i);
      for (var j = 0; j < 3; j++) { sum.F[j] += F[j].length; sum.A[j] += A[j].length; }
      var qc = [], seen = Object.create(null);
      A[0].forEach(function (w) { if (!STOP_MARK.has(w)) { var f = fold(w); if (f && !seen[f] && !STOP_FOLD.has(f)) { seen[f] = 1; qc.push(f); } } });
      var fq = ' ' + F[0].join(' ') + ' ';
      docs.push({ k: r[0], q: r[1], a: r[2], u: pg[0] + (r[4] ? '#' + r[4] : ''), p: pg[0], t: pg[1], qc: qc,
        ents: ENT.filter(function (e) { return fq.indexOf(' ' + e + ' ') >= 0; }),
        F: { tf: F.map(tf), len: F.map(lenOf), sq: ' ' + F[0].join(' ') + ' ', st: ' ' + F[1].join(' ') + ' ' },
        A: { tf: A.map(tf), len: A.map(lenOf), sq: ' ' + A[0].join(' ') + ' ', st: ' ' + A[1].join(' ') + ' ' } });
    }
    function idfOf(df) {
      var o = Object.create(null), mx = 0;
      for (var w in df) { o[w] = Math.log(1 + (N - df[w] + 0.5) / (df[w] + 0.5)); if (o[w] > mx) mx = o[w]; }
      return { m: o, max: mx, df: df };
    }
    D = { docs: docs, N: N, F: idfOf(dfF), A: idfOf(dfA), post: { F: pF, A: pA },
      avg: { F: sum.F.map(function (x) { return x / N; }), A: sum.A.map(function (x) { return x / N; }) } };
    D.byLen = Object.create(null); // từ điển chữ bỏ dấu theo độ dài, để sửa lỗi gõ
    for (var w in dfF) (D.byLen[w.length] = D.byLen[w.length] || []).push(w);
    // toàn văn đã bỏ dấu (mỗi dòng ngăn bằng "|") để dò cặp chữ có từng xuất hiện trên web không
    D.all = ' ' + docs.map(function (d) { return d.F.sq + d.F.st + fold(d.a); }).join(' | ') + ' ';
    return D;
  }
  function count(fields, df) {
    var seen = Object.create(null);
    fields.forEach(function (arr) { arr.forEach(function (w) { if (w && !seen[w]) { seen[w] = 1; df[w] = (df[w] || 0) + 1; } }); });
  }
  function post(fields, P, i) {
    var seen = Object.create(null);
    fields.forEach(function (arr) { arr.forEach(function (w) { if (w && !seen[w]) { seen[w] = 1; (P[w] = P[w] || []).push(i); } }); });
  }
  function tf(arr) { var m = Object.create(null); arr.forEach(function (w) { if (w) m[w] = (m[w] || 0) + 1; }); return m; }
  function lenOf(x) { return x.length; }

  // Sửa lỗi gõ một chữ ("intenet" → "internet"): chỉ cho chữ dài ≥ 5, không có trong kho.
  function near(a, b) {
    var la = a.length, lb = b.length;
    if (Math.abs(la - lb) > 1) return false;
    var i = 0, j = 0, diff = 0;
    while (i < la && j < lb) {
      if (a[i] === b[j]) { i++; j++; continue; }
      if (++diff > 1) return false;
      if (la > lb) i++; else if (lb > la) j++;
      else if (a[i + 1] === b[j] && a[i] === b[j + 1]) { i += 2; j += 2; } else { i++; j++; }
    }
    return diff + (la - i) + (lb - j) <= 1;
  }
  function fix(w) {
    if (w.length < 5 || D.F.m[w] !== undefined) return w;
    var best = null, bd = 0;
    [w.length - 1, w.length, w.length + 1].forEach(function (L) {
      (D.byLen[L] || []).forEach(function (c) { if (near(w, c) && D.F.df[c] > bd) { bd = D.F.df[c]; best = c; } });
    });
    return best || w;
  }

  // Cặp chữ chỉ "bây giờ / hiện nay": bỏ cả cặp ("bay" đứng một mình vẫn là sân bay).
  var NOW = { 'bay gio': 1, 'hien nay': 1, 'hien tai': 1, 'luc nay': 1, 'dao nay': 1, 'gio day': 1 };
  function normalize(query) {
    var out = [];
    lowerToks(query).forEach(function (t) { (ABBR[t] !== undefined ? ABBR[t] : t).split(' ').forEach(function (x) { out.push(x); }); });
    for (var i = out.length - 2; i >= 0; i--) if (NOW[fold(out[i] + ' ' + out[i + 1])]) out.splice(i, 2);
    return out.join(' ');
  }

  function parse(query) {
    var q = normalize(query), marked = HAS_MARK.test(q);
    var raw = q.split(' ').filter(Boolean), keep = [], accSeq = [];
    raw.forEach(function (t) {
      var ft = fold(t);
      if (!ft) return;
      accSeq.push(t);
      if (marked ? (STOP_MARK.has(t) || (!HAS_MARK.test(t) && STOP_FOLD.has(ft))) : STOP_FOLD.has(ft)) return;
      if (HAS_MARK.test(t) && D.A.m[t] !== undefined) keep.push({ m: 'A', w: t });
      else keep.push({ m: 'F', w: fix(ft) }); // chữ không dấu, hoặc chữ có dấu gõ lệch dấu ("thổ cử") → so theo bộ bỏ dấu
    });
    var all = keep.length ? fold(q) : '', extra = [];
    SYN.forEach(function (s) { if (s[0].test(all)) extra = extra.concat(s[1].split(' ')); });
    var pairs = [], fs = fold(q).split(' ').filter(Boolean).map(fix);
    if (marked) for (var i = 0; i + 1 < accSeq.length; i++) pairs.push({ m: 'A', p: accSeq[i] + ' ' + accSeq[i + 1] });
    for (var k = 0; k + 1 < fs.length; k++) pairs.push({ m: 'F', p: fs[k] + ' ' + fs[k + 1], soft: marked });
    var set = Object.create(null);
    fs.concat(extra).forEach(function (w) { set[w] = 1; });
    // Cặp hai chữ có nghĩa đứng liền nhau mà KHÔNG trang nào có ("chung cư", "hồ bơi", "dù lượn"):
    // gần như chắc là một khái niệm web chưa nói tới → tính vào độ phủ như một chữ không khớp.
    var novel = 0, fk = fold(q).split(' ').filter(Boolean).map(fix);
    for (var n = 0; n + 1 < fk.length; n++) {
      var a = fk[n], b = fk[n + 1];
      if (STOP_FOLD.has(a) || STOP_FOLD.has(b) || D.F.m[a] === undefined || D.F.m[b] === undefined) continue;
      if (D.all.indexOf(' ' + a + ' ' + b + ' ') < 0) novel += (D.F.m[a] + D.F.m[b]) / 2;
    }
    return { terms: keep, extra: extra, pairs: pairs, marked: marked, set: set, novel: novel,
      flat: ' ' + fs.concat(extra).join(' ') + ' ' };
  }

  var W = [3, 1.5, 1]; // trọng số: câu hỏi/tiêu đề mục · tựa bài · câu trả lời

  function bm25(tfm, len, avg, w, idf) {
    var f = tfm[w]; if (!f) return 0;
    return idf * (f * 2.2) / (f + 1.2 * (0.25 + 0.75 * len / avg));
  }

  function score(doc, P) {
    var s = 0, hit = 0, tot = P.novel, rareI = -1, rareHit = false;
    P.terms.forEach(function (t) {
      var M = D[t.m], st = doc[t.m], avg = D.avg[t.m];
      var i = M.m[t.w] !== undefined ? M.m[t.w] : M.max; // chữ không có trong kho = hiếm nhất (câu ngoài chủ đề sẽ hụt độ phủ)
      tot += i;
      var v0 = W[0] * bm25(st.tf[0], st.len[0], avg[0], t.w, i), v1 = W[1] * bm25(st.tf[1], st.len[1], avg[1], t.w, i),
        v2 = W[2] * bm25(st.tf[2], st.len[2], avg[2], t.w, i);
      s += v0 + v1 + v2;
      if (v0 > 0 || v1 > 0) hit += i; else if (v2 > 0) hit += 0.6 * i; // chữ chỉ nằm trong câu trả lời: tính một phần
      if (i > rareI) { rareI = i; rareHit = v0 + v1 + v2 > 0; } // chữ hiếm nhất của câu hỏi có khớp không
    });
    P.extra.forEach(function (w) {
      var i = (D.F.m[w] || 0) * 0.6;
      s += 1.5 * bm25(doc.F.tf[0], doc.F.len[0], D.avg.F[0], w, i) + 0.5 * bm25(doc.F.tf[2], doc.F.len[2], D.avg.F[2], w, i);
    });
    P.pairs.forEach(function (pp) {
      var M = D[pp.m], st = doc[pp.m], ws = pp.p.split(' ');
      // lấy chữ hiếm hơn trong cặp: "có lạnh", "lạnh không" gõ không dấu vẫn tách được "lạnh" khỏi "chữa lành"
      var i = Math.max(M.m[ws[0]] || 0, M.m[ws[1]] || 0) * (pp.soft ? 0.4 : 1);
      if (st.sq.indexOf(' ' + pp.p + ' ') >= 0) s += 1.6 * i;
      else if (st.st.indexOf(' ' + pp.p + ' ') >= 0) s += 1.0 * i;
    });
    // khớp chiều ngược: câu hỏi có sẵn nằm trọn trong câu người gõ thì chắc là đúng câu
    var dw = 0, dh = 0;
    doc.qc.forEach(function (w) { var i = D.F.m[w] || 0; dw += i; if (P.set[w]) dh += i; });
    var dcov = dw ? dh / dw : 0;
    s *= 0.45 + 0.55 * dcov;
    for (var e = 0; e < doc.ents.length; e++) {
      if (P.flat.indexOf(' ' + doc.ents[e] + ' ') < 0) { s *= 0.55; break; }
    }
    if (doc.k === 0) s *= 1.12; // hỏi–đáp viết sẵn được ưu tiên hơn mục bài
    if (doc.p === '/hoi-nhanh') s *= 0.9; // cùng câu có ở bài chuyên sâu thì dẫn về bài đó (hub ↔ spoke, §7.3)
    return { s: s, cov: tot ? hit / tot : 0, dcov: dcov, dw: dw, rare: rareHit };
  }

  // Ngưỡng chọn 19/11/2026 trên 164 câu thử (112 câu chỉnh + 52 câu giữ lại), ưu tiên ít trả sai hơn ít "chưa có".
  var OPT = { minScore: 8, minCov: 0.5, minCov2: 0.35, minDcov: 0.7, minCov3: 0.25 };

  function run(query, o) {
    var P = parse(query);
    if (!P.terms.length) return { ok: false, res: [], P: P };
    // chỉ chấm những dòng có ít nhất một chữ "hiếm" của câu hỏi (chữ như "nam", "đất" có ở gần như mọi dòng)
    var cand = null, mark = Object.create(null);
    P.terms.forEach(function (t) {
      var M = D[t.m]; if (M.m[t.w] === undefined || M.m[t.w] < 0.8) return;
      (D.post[t.m][t.w] || []).forEach(function (i) { if (!mark[i]) { mark[i] = 1; (cand = cand || []).push(i); } });
    });
    if (!cand) cand = D.docs.map(function (_, i) { return i; });
    var res = [];
    for (var c = 0; c < cand.length; c++) {
      var r = score(D.docs[cand[c]], P);
      if (r.s > 0) res.push({ d: D.docs[cand[c]], s: r.s, cov: r.cov, dcov: r.dcov, dw: r.dw, rare: r.rare });
    }
    res.sort(function (a, b) { return b.s - a.s; });
    var t = res[0];
    // nhận khi: phủ gần hết câu người gõ · hoặc câu có sẵn nằm gần trọn trong câu người gõ ·
    // hoặc câu có sẵn nằm TRỌN trong câu người gõ và có ít nhất một chữ mang nghĩa ("Ăn gì ở Nam Ban?" ← "an gi o nam ban ngon")
    // (đường thứ hai đòi chữ hiếm nhất của câu hỏi phải khớp: "sổ đỏ và sổ hồng khác nhau" không được trả bằng câu "có sổ / chưa có sổ")
    var ok = !!t && t.s >= o.minScore && (t.cov >= o.minCov || (t.dcov >= o.minDcov && t.cov >= o.minCov2 && t.rare) ||
      (t.dcov >= 0.99 && t.dw >= 2 && t.cov >= o.minCov3));
    return { ok: ok, res: res, P: P };
  }

  // Câu hai ý ("…có sáp nhập không? nếu có thì đất có lên giá không") → hỏi từng ý.
  function clauses(query) {
    var parts = String(query).split(/[?!;]+|,\s|\.\s|\s(?:nếu|neu|với lại|voi lai)\s/i)
      .map(function (x) { return (x || '').trim(); }).filter(Boolean);
    var out = [];
    parts.forEach(function (p) {
      var n = parse(p).terms.length;
      if (out.length && n < 3) out[out.length - 1] += ' ' + p; else if (n) out.push(p);
      else if (out.length) out[out.length - 1] += ' ' + p;
    });
    return out;
  }

  function ask(query, opts) {
    if (!D) throw new Error('chưa nạp chat-index');
    var o = {}; for (var k in OPT) o[k] = (opts && opts[k] != null) ? opts[k] : OPT[k];
    var full = run(query, o), cs = clauses(query), parts = cs.length > 1 ? cs.map(function (c) { return run(c, o); }) : [];
    var main = full, extraTops = [];
    if (parts.length) {
      var first = null;
      parts.forEach(function (p) { if (p.ok && !first) first = p; });
      if (!full.ok && first) main = first; // cả câu khớp được thì giữ cả câu; không thì lấy ý đầu tiên khớp được
      parts.forEach(function (p) { if (p.ok && p !== main) extraTops.push(p.res[0]); });
      if (main !== full && full.ok) extraTops.push(full.res[0]);
    }
    var top = main.res[0], ok = main.ok;
    var seen = new Set(), more = [];
    if (top) seen.add(top.d.p);
    extraTops.forEach(function (x) { if (!seen.has(x.d.p) && more.length < 3) { seen.add(x.d.p); more.push(x); } });
    for (var j = ok ? 1 : 0; j < main.res.length && more.length < 3; j++) {
      var x = main.res[j];
      if (seen.has(x.d.p)) continue;
      if (x.s < (ok ? top.s * 0.45 : 4)) break;
      seen.add(x.d.p); more.push(x);
    }
    return { ok: ok, top: top, more: more, parsed: main.P };
  }

  // Câu người gõ có dáng câu hỏi không (ô tìm kiếm chỉ hiện thẻ trả lời cho câu hỏi, không cho một hai chữ).
  function isQuestion(q) {
    var f = fold(normalize(q)), n = f.split(' ').filter(Boolean).length;
    return /\?/.test(q) || n >= 4 ||
      (n >= 2 && /\b(bao nhieu|bao xa|bao lau|o dau|the nao|khong|may|nao|gi|sao|co nen|duoc khong|la gi)\b/.test(f));
  }

  var api = { fold: fold, build: build, ask: ask, parse: parse, isQuestion: isQuestion, OPT: OPT };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.NBBot = api;

  // Chạy nền (Web Worker): trang nạp file này bằng new Worker(...) → dựng kho và chấm câu ngoài luồng chính,
  // gõ không bao giờ bị khựng. Kết quả gửi về đã gọn (bỏ bảng đếm chữ).
  if (typeof WorkerGlobalScope !== 'undefined' && root instanceof WorkerGlobalScope) {
    var slim = function (x) { return x && { d: { k: x.d.k, q: x.d.q, a: x.d.a, u: x.d.u, p: x.d.p, t: x.d.t }, s: x.s, cov: x.cov, dcov: x.dcov }; };
    root.onmessage = function (e) {
      var m = e.data || {};
      if (m.type === 'load') {
        fetch(m.url).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
          .then(function (j) { build(j); root.postMessage({ type: 'ready' }); })
          .catch(function () { root.postMessage({ type: 'fail' }); });
      } else if (m.type === 'ask' && D) {
        var r = ask(m.q);
        root.postMessage({ type: 'ans', id: m.id, q: m.q, question: isQuestion(m.q), ok: r.ok, top: slim(r.top), more: r.more.map(slim) });
      }
    };
  }
})(typeof window !== 'undefined' ? window : this);
