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
