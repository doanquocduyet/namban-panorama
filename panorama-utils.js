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
