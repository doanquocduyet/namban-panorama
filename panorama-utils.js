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
      "vuon-bo-loi-bao-nhieu"];
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
      ".pm-endcontact .pm-ec-dot{color:var(--stone,#a79c87);margin:0 8px;}"+
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
  var bar=document.getElementById('reading-progress');
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
