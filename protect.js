// ── Namban Panorama · Content Protection ──────────────────────────
(function(){
  // 1. Tắt chuột phải
  document.addEventListener('contextmenu', function(e){ e.preventDefault(); });

  // 2. Tắt kéo ảnh
  document.addEventListener('dragstart', function(e){ e.preventDefault(); });

  // 3. Tắt chọn văn bản bằng chuột (vẫn cho scroll)
  document.addEventListener('selectstart', function(e){ e.preventDefault(); });

  // 4. Tắt tổ hợp phím copy / save / print / inspect
  document.addEventListener('keydown', function(e){
    var c = e.key.toLowerCase();
    // Ctrl/Cmd + C, A, S, P, U, I, J, F12
    if((e.ctrlKey || e.metaKey) && ['c','a','s','p','u','i','j','x'].includes(c)){
      e.preventDefault(); return false;
    }
    if(e.key === 'F12'){ e.preventDefault(); return false; }
    if(e.key === 'PrintScreen'){ e.preventDefault(); return false; }
  });

  // 5. Phủ overlay trong suốt lên toàn bộ ảnh
  function protectImages(){
    document.querySelectorAll('img').forEach(function(img){
      if(img.dataset.protected) return;
      img.dataset.protected = '1';
      var wrap = img.parentNode;
      // Chỉ wrap nếu chưa có lớp bảo vệ
      if(!wrap.classList.contains('img-protect-wrap')){
        var div = document.createElement('div');
        div.className = 'img-protect-wrap';
        div.style.cssText = 'position:relative;display:inline-block;width:100%;';
        wrap.insertBefore(div, img);
        div.appendChild(img);
        wrap = div;
      }
      var shield = document.createElement('div');
      shield.style.cssText = [
        'position:absolute','top:0','left:0','width:100%','height:100%',
        'z-index:10','cursor:default',
        'user-select:none','-webkit-user-select:none',
      ].join(';');
      shield.addEventListener('contextmenu', function(e){ e.preventDefault(); });
      shield.addEventListener('dragstart',   function(e){ e.preventDefault(); });
      wrap.appendChild(shield);
    });
  }

  // Chạy ngay + chạy lại khi DOM thay đổi
  protectImages();
  var mo = new MutationObserver(protectImages);
  mo.observe(document.body, {childList:true, subtree:true});

  // 6. CSS: tắt pointer-events trên img, tắt user-select toàn trang
  var style = document.createElement('style');
  style.textContent = [
    'img{pointer-events:none!important;-webkit-user-drag:none!important;}',
    'body{-webkit-user-select:none!important;-moz-user-select:none!important;user-select:none!important;}',
    '.img-protect-wrap{position:relative;display:block;}',
  ].join('');
  document.head.appendChild(style);

})();
