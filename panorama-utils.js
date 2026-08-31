/* KHỐI LIÊN HỆ TRẦM CUỐI BÀI — chỉ bài đất/mua bán/thị trường/BĐS/index.
   Đặt sau nội dung, trước footer. Chữ trầm, không nút, không "ngay".
   Chạy TRƯỚC bước rewrite tel→Zalo bên dưới để số trong khối cũng được rewrite. */
(function(){
  try{
    var IN=["namban-index","tiem-nang-dau-tu","quy-hoach-2050","ban-do-quy-hoach-nam-ban",
      "truoc-khi-xuong-tien","so-sanh-nam-ban-bao-loc-da-lat","doc-lo-dat","doc-lo-dat-02-view-ho",
      "khu-nao-o-nam-ban","doc-the-dat-nam-ban","len-tho-cu-het-bao-nhieu-tien","ban-dat-nam-ban",
      "mua-dat-nam-ban","mua-dat-co-vuon-ca-phe","mua-dat-co-vuon-bo","mua-dat-duong-gia-nam-ban",
      "mua-vuon-ca-phe-nam-ban","vua-mua-dat-nam-ban-lam-gi","sap-nhap-nam-ban-dat","nam-ban-thuoc-xa-nao",
      "dat-gan-da-lat","nam-ban-hay-di-linh","dau-tam-nam-ban","cau-tong-doi-nam-ban",
      "cay-xang-petro-moi-o-nam-ban","san-bay-lien-khuong-mo-lai","homestay-nam-ban-co-lai-khong",
      "vuon-bo-loi-bao-nhieu","dat-nam-ban-trong-cay-gi","rau-hoa-cay-do-la-nam-ban",
      "ho-bai-cong-nam-ban","nam-ban-hay-don-duong","duong-ha-bac-nam-ban","nam-ban-va-nam-ha",
      "mua-dat-da-lat-chon-nam-ban","quy-trinh-mua-dat-nam-ban","tram-sac-nam-ban",
      "dinh-gia-dat-nam-ban","mua-mua-nam-ban","mua-dat-nam-ban-de-lam-gi","dat-nam-ban-cuoi-tuan"];
    var slug=(location.pathname||"").replace(/\/+$/,"").split("/").pop().replace(/\.html$/,"");
    if(slug===""||IN.indexOf(slug)===-1)return;
    if(document.getElementById("pm-endcontact"))return;
    var st=document.createElement("style");
    st.textContent=
      ".pm-endcontact{max-width:720px;margin:38px auto 8px;padding:22px 24px 0;border-top:1px solid var(--line,#e1d9c8);}"+
      ".pm-endcontact .pm-ec-q{font-size:14px;color:var(--muted,#6e6759);margin:0 0 6px;letter-spacing:.2px;line-height:1.55;}"+
      ".pm-endcontact .pm-ec-a{font-family:'Fraunces',serif;font-size:18px;color:var(--forest,#2f4034);margin:0;letter-spacing:.3px;}"+
      ".pm-endcontact .pm-ec-a a{color:var(--forest,#2f4034);text-decoration:none;border-bottom:1px solid var(--line,#e1d9c8);padding-bottom:1px;transition:color .2s;}"+
      ".pm-endcontact .pm-ec-a a:hover{color:var(--clay,#9d5d38);}"+
      ".pm-endcontact .pm-ec-dot{color:var(--stone-text,#726a5c);margin:0 8px;}"+
      ".art-body .pm-endcontact{margin-left:0;margin-right:0;padding-left:0;padding-right:0;}";
    document.head.appendChild(st);
    var block=document.createElement("div");
    block.id="pm-endcontact"; block.className="pm-endcontact";
    block.innerHTML='<p class="pm-ec-q">Có câu hỏi về một khu cụ thể ở Nam Ban?</p>'+
      '<p class="pm-ec-a"><a href="tel:0978758788">0978 758 788</a>'+
      '<span class="pm-ec-dot">·</span>'+
      '<a href="https://zalo.me/0978758788" target="_blank" rel="noopener">Zalo</a></p>';
    var body=document.querySelector(".art-body");
    if(body){ body.appendChild(block); }
    else{
      var footer=document.querySelector("footer");
      if(footer){ var w=document.createElement("div"); w.className="wrap"; w.appendChild(block); footer.parentNode.insertBefore(w,footer); }
    }
  }catch(e){}
})();

/* LIÊN HỆ: email → Gmail (mọi máy); số điện thoại → Zalo trên PC (mobile giữ gọi) */
(function(){
  try{
    /* mailto: → Gmail cho MỌI thiết bị. Universal link: iPhone/Android có Gmail app
       sẽ mở thẳng app soạn thư; không có app thì mở Gmail web. PC mở Gmail web.
       mailto: trong HTML giữ làm fallback nếu JS tắt. */
    var GMAIL='https://mail.google.com/mail/?view=cm&fs=1&to=nambanpanorama@gmail.com';
    var mails=document.querySelectorAll('a[href^="mailto:nambanpanorama@gmail.com"]');
    for(var j=0;j<mails.length;j++){
      var m=mails[j];
      m.setAttribute('href',GMAIL);
      m.setAttribute('target','_blank');
      m.setAttribute('rel','noopener');
      m.setAttribute('title','Soạn mail gửi Namban Panorama');
    }
    /* tel: → Zalo CHỈ trên PC; điện thoại giữ tel: để bấm gọi */
    var isPhone=/Android|iPhone|iPod|Windows Phone|BlackBerry|IEMobile|Opera Mini|Mobile/i.test(navigator.userAgent||'');
    if(isPhone)return;
    var ZALO='https://zalo.me/0978758788';
    var links=document.querySelectorAll('a[href^="tel:0978758788"]');
    for(var i=0;i<links.length;i++){
      var a=links[i];
      a.setAttribute('href',ZALO);
      a.setAttribute('target','_blank');
      a.setAttribute('rel','noopener');
      a.setAttribute('title','Nhắn Zalo 0978 758 788');
    }
  }catch(e){}
})();

/* "CẬP NHẬT LẦN CUỐI" — lấy ngày THẬT từ JSON-LD dateModified (không thể lùi khống) */
(function(){
  try{
    if(document.getElementById('pm-updated'))return;
    var pub=null, mod=null;
    var S=document.querySelectorAll('script[type="application/ld+json"]');
    for(var i=0;i<S.length;i++){
      var d; try{d=JSON.parse(S[i].textContent);}catch(e){continue;}
      var arr=d['@graph']?d['@graph']:[d];
      for(var j=0;j<arr.length;j++){
        var o=arr[j], ty=o&&o['@type'];
        if(ty==='Article'||ty==='NewsArticle'||ty==='BlogPosting'){
          if(o.datePublished) pub=String(o.datePublished).slice(0,10);
          if(o.dateModified) mod=String(o.dateModified).slice(0,10);
        }
      }
    }
    if(!mod) return;                 /* không có ngày sửa → không hiện */
    if(pub && mod<=pub) return;       /* chưa sửa sau khi đăng → chỉ giữ ngày đăng */
    var p=mod.split('-');
    var label='Cập nhật '+parseInt(p[2],10)+'/'+parseInt(p[1],10)+'/'+p[0];
    var idate=document.querySelector('.issue-date');
    if(idate){
      var s=document.createElement('span');
      s.id='pm-updated'; s.textContent=label;
      s.style.cssText='font-size:11px;letter-spacing:2px;text-transform:uppercase;color:var(--clay,#9d5d38);margin-left:14px;';
      idate.parentNode.insertBefore(s, idate.nextSibling);
      return;
    }
    var h1=document.querySelector('.art-header h1,.idx-header h1,h1');
    if(h1){
      var dv=document.createElement('div');
      dv.id='pm-updated'; dv.textContent=label;
      dv.style.cssText='font-size:12px;letter-spacing:1px;text-transform:uppercase;color:var(--stone,#a79c87);margin-top:8px;';
      h1.parentNode.insertBefore(dv, h1.nextSibling);
    }
  }catch(e){}
})();

(function(){
  if(!document.querySelector('.art-body'))return;

  /* 1. READING PROGRESS BAR */
  var bar=document.getElementById('reading-progress')||document.querySelector('.read-progress');
  if(!bar){bar=document.createElement('div');bar.id='reading-progress';document.body.prepend(bar);}
  function updateBar(){
    var st=window.scrollY||document.documentElement.scrollTop;
    var dh=document.documentElement.scrollHeight-window.innerHeight;
    bar.style.width=(dh>0?Math.min(st/dh*100,100):0)+'%';
  }
  window.addEventListener('scroll',updateBar,{passive:true});
  updateBar();

  /* 2. BREADCRUMB from JSON-LD BreadcrumbList */
  var scripts=document.querySelectorAll('script[type="application/ld+json"]');
  var bc=null;
  for(var i=0;i<scripts.length;i++){
    try{var d=JSON.parse(scripts[i].textContent);if(d['@type']==='BreadcrumbList'){bc=d;break;}}catch(e){}
  }
  if(bc&&bc.itemListElement&&bc.itemListElement.length&&!document.querySelector('.crumb')){
    var items=bc.itemListElement.slice().sort(function(a,b){return a.position-b.position;});
    var html=items.map(function(it,idx){
      var sep=idx>0?'<span class="sep">›</span>':'';
      if(idx<items.length-1)return sep+'<a href="'+(it.item||'/')+'">'+it.name+'</a>';
      return sep+'<span>'+it.name+'</span>';
    }).join('');
    var el=document.createElement('div');
    el.className='art-breadcrumb';
    el.innerHTML=html;
    var body=document.querySelector('.art-body');
    if(body)body.insertBefore(el,body.firstChild);
  }
})();

/* MENU MOBILE ĐỒNG BỘ — nâng nav cũ (bật/tắt inline) thành panel trượt xịn.
   Chạy trên MỌI trang: trang đã có panel (#mobileMenu) thì bỏ qua; trang nav cũ
   có .hamburger + link nav thì tự dựng panel, đọc đúng link/nhãn (kể cả ngoại ngữ). */
(function(){
  try{
    var stat=document.getElementById('mobileMenu');
    if(stat){                                                   /* đã có panel tĩnh trong trang */
      /* Một số trang có panel + onclick="toggleMenu()" nhưng QUÊN định nghĩa hàm
         -> menu chết im lặng. Vá tại đây cho cả lớp lỗi này, không sửa tay từng trang. */
      if(typeof window.toggleMenu!=='function'){
        var sov=document.getElementById('menuOverlay'),
            scl=document.getElementById('mobileClose'),
            sham=document.querySelector('.hamburger');
        window.toggleMenu=function(){
          var open=stat.classList.toggle('open');
          if(sov)sov.classList.toggle('open',open);
          if(scl)scl.classList.toggle('open',open);
          if(sham)sham.classList.toggle('is-open',open);
          document.body.style.overflow=open?'hidden':'';
        };
        document.addEventListener('keydown',function(e){
          if(e.key==='Escape'&&stat.classList.contains('open'))window.toggleMenu();
        });
      }
      return;
    }
    var ham=document.querySelector('.hamburger');
    var srcLinks=document.querySelectorAll('.nav-links a, .navlinks a');
    if(!ham||!srcLinks.length)return;                           /* không có nav để nâng */

    var css=[
"@media(prefers-reduced-motion:no-preference){.hamburger span{transition:transform .3s ease,opacity .2s ease;}}",
".hamburger.is-open span:nth-child(1){transform:translateY(6.5px) rotate(45deg);}",
".hamburger.is-open span:nth-child(2){opacity:0;}",
".hamburger.is-open span:nth-child(3){transform:translateY(-6.5px) rotate(-45deg);}",
".pm-menu-overlay{position:fixed;inset:0;background:rgba(26,24,21,.28);backdrop-filter:blur(2px);-webkit-backdrop-filter:blur(2px);z-index:999;opacity:0;visibility:hidden;transition:opacity .4s ease,visibility .4s;}",
".pm-menu-overlay.open{opacity:1;visibility:visible;}",
".pm-mobile-menu{position:fixed;top:0;right:0;bottom:0;width:72%;max-width:340px;height:100vh;height:100dvh;background:rgba(244,240,232,.92);backdrop-filter:blur(22px) saturate(1.2);-webkit-backdrop-filter:blur(22px) saturate(1.2);border-left:1px solid rgba(157,93,56,.14);box-shadow:-18px 0 50px rgba(26,24,21,.16);z-index:1000;display:flex;flex-direction:column;align-items:flex-start;justify-content:center;padding:0 0 0 40px;visibility:hidden;transform:translateX(100%);transition:transform .44s cubic-bezier(.22,.61,.36,1),visibility .44s;}",
".pm-mobile-menu.open{visibility:visible;transform:translateX(0);}",
".pm-mobile-menu a{font-family:'Fraunces',serif;font-size:25px;font-weight:300;color:var(--ink,#1a1815);text-decoration:none;letter-spacing:.2px;padding:15px 0;opacity:0;transform:translateX(18px);transition:opacity .5s ease,transform .5s cubic-bezier(.22,.61,.36,1),color .2s;}",
".pm-mobile-menu.open a{opacity:1;transform:translateX(0);}",
".pm-mobile-menu.open a:nth-of-type(1){transition-delay:.14s;}.pm-mobile-menu.open a:nth-of-type(2){transition-delay:.20s;}.pm-mobile-menu.open a:nth-of-type(3){transition-delay:.26s;}.pm-mobile-menu.open a:nth-of-type(4){transition-delay:.32s;}.pm-mobile-menu.open a:nth-of-type(5){transition-delay:.38s;}.pm-mobile-menu.open a:nth-of-type(6){transition-delay:.44s;}",
".pm-mobile-menu a:active,.pm-mobile-menu a:hover{color:var(--clay,#9d5d38);}",
".pm-mobile-close{position:fixed;top:20px;right:22px;width:42px;height:42px;font-size:26px;color:var(--ink,#1a1815);cursor:pointer;background:rgba(244,240,232,.6);border:1px solid rgba(157,93,56,.18);border-radius:50%;line-height:0;padding:0;z-index:1001;display:flex;align-items:center;justify-content:center;opacity:0;visibility:hidden;transition:opacity .4s ease .1s,visibility .4s;}",
".pm-mobile-close.open{opacity:1;visibility:visible;}"
    ].join("");
    var st=document.createElement('style');st.textContent=css;document.head.appendChild(st);

    /* thay hamburger để bỏ listener cũ (bật/tắt .nav-links) */
    var ham2=ham.cloneNode(true);ham.parentNode.replaceChild(ham2,ham);

    var ov=document.createElement('div');ov.className='pm-menu-overlay';ov.id='menuOverlay';
    var cl=document.createElement('button');cl.className='pm-mobile-close';cl.id='mobileClose';cl.setAttribute('aria-label',{vi:'Đóng',en:'Close',fr:'Fermer',zh:'关闭',ko:'닫기',ja:'閉じる'}[(document.documentElement.getAttribute('lang')||'vi').slice(0,2).toLowerCase()]||'Close');cl.textContent='×';
    var mm=document.createElement('div');mm.className='pm-mobile-menu';mm.id='mobileMenu';
    function closeMenu(){mm.classList.remove('open');ov.classList.remove('open');cl.classList.remove('open');ham2.classList.remove('is-open');document.body.style.overflow='';}
    function openMenu(){mm.classList.add('open');ov.classList.add('open');cl.classList.add('open');ham2.classList.add('is-open');document.body.style.overflow='hidden';}
    function toggle(){(mm.classList.contains('open')?closeMenu:openMenu)();}

    var seen={},n=0;
    for(var i=0;i<srcLinks.length&&n<6;i++){
      var a=srcLinks[i],href=a.getAttribute('href'),txt=(a.textContent||'').trim();
      if(!href||!txt)continue;var k=href+'|'+txt;if(seen[k])continue;seen[k]=1;n++;
      var na=document.createElement('a');na.setAttribute('href',href);na.textContent=txt;
      na.addEventListener('click',closeMenu);mm.appendChild(na);
    }

    document.body.appendChild(ov);document.body.appendChild(cl);document.body.appendChild(mm);
    ov.addEventListener('click',closeMenu);
    cl.addEventListener('click',closeMenu);
    ham2.addEventListener('click',function(e){e.preventDefault();toggle();});
    document.addEventListener('keydown',function(e){if(e.key==='Escape'&&mm.classList.contains('open'))closeMenu();});
    if(typeof window.toggleMenu!=='function')window.toggleMenu=toggle;
  }catch(e){}
})();

/* NGHE BÀI (đọc audio) — dùng Web Speech API của trình duyệt, miễn phí, không backend.
   Chèn nút trầm ở đầu bài; đọc H1 + thân bài, giọng theo ngôn ngữ trang.
   Đọc theo từng câu (chunk) để tránh lỗi cắt của Chrome; có tạm dừng + đổi tốc độ. */
(function(){
  try{
    if(!('speechSynthesis' in window))return;                 /* trình duyệt không hỗ trợ → ẩn */
    var body=document.querySelector('.art-body')||document.querySelector('article')||document.querySelector('.idx-body');
    if(!body)return;
    if(document.getElementById('pm-audio'))return;

    var lang=(document.documentElement.getAttribute('lang')||'vi').slice(0,2).toLowerCase();
    if(lang!=='vi')return;                                     /* bài ngoại ngữ không cần voice */
    var L={
      vi:{play:'Nghe bài',pause:'Tạm dừng',reading:'Đang đọc',replay:'Nghe lại',unit:'phút',aria:'Nghe bài viết'},
      en:{play:'Listen',pause:'Pause',reading:'Playing',replay:'Replay',unit:'min',aria:'Listen to article'},
      fr:{play:'Écouter',pause:'Pause',reading:'Lecture',replay:'Réécouter',unit:'min',aria:'Écouter l’article'},
      zh:{play:'朗读',pause:'暂停',reading:'播放中',replay:'重听',unit:'分钟',aria:'朗读文章'},
      ko:{play:'듣기',pause:'일시정지',reading:'재생 중',replay:'다시 듣기',unit:'분',aria:'기사 듣기'},
      ja:{play:'記事を聴く',pause:'一時停止',reading:'再生中',replay:'もう一度',unit:'分',aria:'記事を聴く'}
    }[lang]||null;
    if(!L)L={play:'Nghe bài',pause:'Tạm dừng',reading:'Đang đọc',replay:'Nghe lại',unit:'phút',aria:'Nghe bài viết'};

    /* --- gom văn bản: H1 + các đoạn trong thân bài --- */
    var chunks=[];
    function pushText(t){
      t=(t||'').replace(/\s+/g,' ').trim(); if(!t)return;
      /* tách câu để mỗi utterance ngắn, đọc mượt + tránh lỗi cắt */
      var s=t.match(/[^.!?…。！？]+[.!?…。！？]*\s*/g)||[t];
      for(var i=0;i<s.length;i++){var c=s[i].trim(); if(c)chunks.push(c);}
    }
    var h1=document.querySelector('.art-header h1')||body.querySelector('h1')||document.querySelector('h1');
    if(h1)pushText(h1.textContent);
    var nodes=body.querySelectorAll('h2,h3,p,li,blockquote');
    for(var i=0;i<nodes.length;i++){
      var n=nodes[i];
      if(n.closest('.pm-endcontact,.art-breadcrumb,.pm-audio,figure'))continue;
      if(n.tagName==='LI'&&n.querySelector('a'))continue;         /* bỏ list link "Đọc gì tiếp" */
      var t=(n.textContent||'').trim();
      if(!t||t==='Đọc gì tiếp:'||/^Đọc gì tiếp/i.test(t))continue;
      pushText(t);
    }
    if(chunks.length<2)return;

    /* ước lượng phút đọc (CJK tính theo ký tự vì không tách bằng dấu cách) */
    var mins;
    if(lang==='zh'||lang==='ja'||lang==='ko'){
      var ch=0; for(var w=0;w<chunks.length;w++)ch+=chunks[w].length;
      mins=Math.max(1,Math.round(ch/380));
    } else {
      var words=0; for(var w2=0;w2<chunks.length;w2++)words+=chunks[w2].split(/\s+/).length;
      mins=Math.max(1,Math.round(words/170));
    }

    /* --- CSS --- */
    var st=document.createElement('style');
    st.textContent=[
".pm-audio{display:inline-flex;align-items:center;gap:11px;margin:2px 0 26px;padding:7px 8px 7px 7px;border:1px solid var(--line,#e1d9c8);border-radius:999px;background:var(--card,#faf6ee);}",
".pm-audio-btn{flex:0 0 auto;width:38px;height:38px;border-radius:50%;border:none;cursor:pointer;background:var(--forest,#2f4034);display:flex;align-items:center;justify-content:center;transition:background .2s,transform .15s;padding:0;}",
".pm-audio-btn:hover{background:var(--forest-deep,#1e2a20);}",
".pm-audio-btn:active{transform:scale(.94);}",
".pm-audio-btn svg{width:15px;height:15px;display:block;fill:#f1ece2;}",
".pm-audio-lbl{font-size:13.5px;color:var(--ink,#1a1815);letter-spacing:.2px;font-weight:500;}",
".pm-audio-time{font-size:12px;color:var(--muted,#6e6759);}",
".pm-audio-speed{font-family:'Fraunces',serif;font-size:12.5px;color:var(--muted,#6e6759);background:none;border:1px solid var(--line,#e1d9c8);border-radius:20px;padding:2px 9px;margin-left:2px;margin-right:4px;cursor:pointer;transition:color .2s,border-color .2s;}",
".pm-audio-speed:hover{color:var(--clay,#9d5d38);border-color:var(--clay-soft,#bb8862);}",
".pm-audio.pm-on .pm-audio-lbl{color:var(--forest,#2f4034);}"
    ].join("");
    document.head.appendChild(st);

    /* --- UI --- */
    var ICON_PLAY='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>';
    var ICON_PAUSE='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 5h4v14H6zM14 5h4v14h-4z"/></svg>';
    var wrap=document.createElement('div');
    wrap.className='pm-audio'; wrap.id='pm-audio'; wrap.setAttribute('role','group'); wrap.setAttribute('aria-label',L.aria);
    wrap.innerHTML=
      '<button class="pm-audio-btn" type="button" aria-label="'+L.play+'">'+ICON_PLAY+'</button>'+
      '<span class="pm-audio-lbl">'+L.play+'</span>'+
      '<span class="pm-audio-time">~'+mins+' '+L.unit+'</span>'+
      '<button class="pm-audio-speed" type="button" aria-label="Tốc độ đọc">1×</button>';
    body.insertBefore(wrap, body.firstChild);

    var btn=wrap.querySelector('.pm-audio-btn'),
        lbl=wrap.querySelector('.pm-audio-lbl'),
        spd=wrap.querySelector('.pm-audio-speed'),
        timeEl=wrap.querySelector('.pm-audio-time');
    var ICON_PLAY2=ICON_PLAY, ICON_PAUSE2=ICON_PAUSE;
    function setIcon(playing){ btn.innerHTML=playing?ICON_PAUSE2:ICON_PLAY2; }
    var rate=1;
    function cycleRate(){ rate=(rate===1)?1.25:(rate===1.25?1.5:1); spd.textContent=(rate===1?'1×':(rate===1.25?'1.25×':'1.5×')); return rate; }

    /* ƯU TIÊN MP3 giọng thật (khai báo bằng <meta name="pm-audio" content="/audio/slug.mp3">) */
    var mp3=(document.querySelector('meta[name="pm-audio"]')||{}).content||'';

    if(mp3){
      /* ---- CHẾ ĐỘ MP3: phát thật, chạy nền/màn hình khoá ---- */
      var audio=new Audio(); audio.preload='metadata'; audio.src=mp3;
      function fmt(s){ if(!isFinite(s))return ''; s=Math.round(s); return Math.floor(s/60)+':'+('0'+(s%60)).slice(-2); }
      audio.addEventListener('loadedmetadata',function(){ if(audio.duration)timeEl.textContent=fmt(audio.duration); });
      audio.addEventListener('timeupdate',function(){ if(audio.duration)timeEl.textContent=fmt(audio.duration-audio.currentTime); });
      audio.addEventListener('play',function(){ setIcon(true); lbl.textContent=L.reading; wrap.classList.add('pm-on'); });
      audio.addEventListener('pause',function(){ if(!audio.ended){ setIcon(false); lbl.textContent=L.pause; } });
      audio.addEventListener('ended',function(){ setIcon(false); wrap.classList.remove('pm-on'); lbl.textContent=L.replay; if(audio.duration)timeEl.textContent=fmt(audio.duration); });
      btn.addEventListener('click',function(){ if(audio.paused){ if(audio.ended)audio.currentTime=0; audio.play(); } else audio.pause(); });
      spd.addEventListener('click',function(){ audio.playbackRate=cycleRate(); });
      if('mediaSession' in navigator){
        try{
          navigator.mediaSession.metadata=new MediaMetadata({
            title:(h1?h1.textContent.trim():document.title),
            artist:'Đoàn Quốc Duyệt — Namban Panorama',
            album:'Namban Panorama'
          });
          navigator.mediaSession.setActionHandler('play',function(){ audio.play(); });
          navigator.mediaSession.setActionHandler('pause',function(){ audio.pause(); });
          navigator.mediaSession.setActionHandler('seekbackward',function(){ audio.currentTime=Math.max(0,audio.currentTime-15); });
          navigator.mediaSession.setActionHandler('seekforward',function(){ audio.currentTime=Math.min(audio.duration||1e9,audio.currentTime+15); });
        }catch(e){}
      }
      return;
    }

    /* ---- CHẾ ĐỘ FALLBACK: giọng máy trình duyệt (Web Speech API) ---- */
    var synth=window.speechSynthesis;
    var state='idle', idx=0, voice=null, keepAlive=null;
    function pickVoice(){
      var vs=synth.getVoices()||[]; var cand=[];
      for(var i=0;i<vs.length;i++){ var vl=(vs[i].lang||'').toLowerCase().replace('_','-'); if(vl.indexOf(lang)===0)cand.push(vs[i]); }
      if(!cand.length)return null;
      function score(v){
        var n=((v.name||'')+' '+(v.voiceURI||'')).toLowerCase(), s=0;
        if(/male|\bnam\b|nathan|david|minh|quan|khanh|william|daniel|liam|george|thomas/.test(n))s+=3; /* gợi ý nam */
        if(/female|\bn[uữ]\b|linh|hoai|hoài|mai|\bthu\b|karen|samantha|victoria/.test(n))s-=2;         /* gợi ý nữ */
        if(/google|natural|enhanced|premium|neural|wavenet|siri/.test(n))s+=2;                          /* chất lượng cao */
        if(v.localService===false)s+=1;                                                                /* giọng cloud thường hay hơn */
        return s;
      }
      cand.sort(function(a,b){return score(b)-score(a);});
      return cand[0];
    }
    function speakNext(){
      if(idx>=chunks.length){ stopAll(true); return; }
      var text=chunks[idx];
      var u=new SpeechSynthesisUtterance(text);
      u.lang=document.documentElement.getAttribute('lang')||'vi';
      if(voice)u.voice=voice;
      u.rate=Math.max(0.5,rate*0.95);   /* chậm nhẹ cho êm */
      u.pitch=0.9;                        /* trầm hơn, bớt chát */
      var gap=/[.!?…。！？]$/.test(text)?260:480;   /* câu: nghỉ ngắn; tiêu đề: nghỉ dài hơn */
      u.onend=function(){ if(state==='playing'){ idx++; setTimeout(speakNext,gap); } };
      u.onerror=function(){ if(state==='playing'){ idx++; setTimeout(speakNext,gap); } };
      synth.speak(u);
    }
    function startKeepAlive(){ stopKeepAlive(); keepAlive=setInterval(function(){ if(state==='playing'&&synth.speaking){ synth.pause(); synth.resume(); } },9000); }
    function stopKeepAlive(){ if(keepAlive){clearInterval(keepAlive);keepAlive=null;} }
    function play(){ if(!voice)voice=pickVoice(); synth.cancel(); state='playing'; setIcon(true); lbl.textContent=L.reading; wrap.classList.add('pm-on'); speakNext(); startKeepAlive(); }
    function pause(){ state='paused'; try{synth.pause();}catch(e){} setIcon(false); lbl.textContent=L.pause; stopKeepAlive(); }
    function resume(){ state='playing'; setIcon(true); lbl.textContent=L.reading; try{synth.resume();}catch(e){} if(!synth.speaking)speakNext(); startKeepAlive(); }
    function stopAll(done){ state='idle'; stopKeepAlive(); try{synth.cancel();}catch(e){} setIcon(false); wrap.classList.remove('pm-on'); lbl.textContent=done?L.replay:L.play; if(done)idx=0; }
    btn.addEventListener('click',function(){
      if(state==='idle'){ idx=(lbl.textContent===L.replay)?0:idx; play(); }
      else if(state==='playing'){ pause(); }
      else { resume(); }
    });
    spd.addEventListener('click',function(){ cycleRate(); if(state==='playing'){ synth.cancel(); speakNext(); } });
    window.addEventListener('beforeunload',function(){ try{synth.cancel();}catch(e){} });
    if(synth.getVoices().length===0 && typeof synth.addEventListener==='function'){
      synth.addEventListener('voiceschanged',function(){ if(!voice)voice=pickVoice(); },{once:true});
    }
  }catch(e){}
})();

/* CHỐNG COPY CHỮ & LƯU HÌNH — mức vừa phải:
   chặn bôi đen/copy chữ + kéo/chuột phải/long-press lưu ảnh trên TOÀN site,
   NHƯNG CHỪA liên hệ (SĐT/email/Zalo ở footer, khối liên hệ cuối bài, trang Trao đổi)
   và các ô nhập form — để khách vẫn copy được số mà liên hệ (giữ phễu).
   Lưu ý: chỉ chặn người dùng phổ thông; KHÔNG ảnh hưởng Google/AI (đọc thẳng HTML nguồn). */
(function(){
  try{
    var EXEMPT='input,textarea,select,[contenteditable="true"],.pm-selectable,'
      +'footer,footer *,.pm-endcontact,.pm-endcontact *,.contact,.contact *,'
      +'a[href^="tel:"],a[href^="mailto:"],a[href*="zalo"],a[href*="mail.google.com"]';
    function exempt(node){
      for(var el=node; el && el.nodeType; el=(el.parentElement||el.parentNode)){
        if(el.matches && el.matches(EXEMPT)) return true;
      }
      return false;
    }
    var css=
      'body{-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none;}'
      +'img,figure,picture,svg,video{-webkit-user-drag:none;-khtml-user-drag:none;-moz-user-drag:none;-o-user-drag:none;user-drag:none;-webkit-touch-callout:none;}'
      +EXEMPT+'{-webkit-user-select:text!important;-moz-user-select:text!important;-ms-user-select:text!important;user-select:text!important;-webkit-touch-callout:default!important;}';
    var st=document.createElement('style'); st.id='pm-protect'; st.textContent=css;
    (document.head||document.documentElement).appendChild(st);

    document.addEventListener('contextmenu',function(e){
      var t=e.target;
      var onImg = t && (t.tagName==='IMG'||t.tagName==='VIDEO'||(t.closest&&t.closest('img,picture,video')));
      if(onImg) e.preventDefault();   /* chặn chuột phải trên ẢNH (không cho "lưu ảnh"); CHỮ vẫn mở menu để dịch */
    },{capture:true});
    document.addEventListener('dragstart',function(e){
      var t=e.target;
      if(t && (t.tagName==='IMG' || (t.closest && t.closest('img,figure,picture')))) e.preventDefault();
    },{capture:true});
    ['copy','cut'].forEach(function(ev){
      document.addEventListener(ev,function(e){
        var s=window.getSelection&&window.getSelection();
        var node=(s&&s.anchorNode)?s.anchorNode:e.target;
        if(!exempt(node)) e.preventDefault();
      },{capture:true});
    });
    document.addEventListener('keydown',function(e){
      var k=(e.key||'').toLowerCase();
      if((e.ctrlKey||e.metaKey)&&k==='s') e.preventDefault();   /* chặn lưu trang (kèm ảnh) */
    },{capture:true});
    function markImgs(){ var im=document.querySelectorAll('img'); for(var i=0;i<im.length;i++) im[i].setAttribute('draggable','false'); }
    if(document.readyState!=='loading') markImgs();
    else document.addEventListener('DOMContentLoaded',markImgs);
  }catch(e){}
})();
