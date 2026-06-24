/* ===== Hydrovac Pro — front-end behavior ===== */
(function(){
  'use strict';

  /* ---------- mobile nav ---------- */
  var burger = document.getElementById('burger');
  var navLinks = document.getElementById('navLinks');
  if (burger && navLinks){
    burger.addEventListener('click', function(){
      var open = navLinks.classList.toggle('open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    navLinks.querySelectorAll('a').forEach(function(a){
      a.addEventListener('click', function(){
        navLinks.classList.remove('open');
        burger.setAttribute('aria-expanded','false');
      });
    });
  }

  /* ---------- reveal on scroll ---------- */
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && reveals.length){
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(en){
        if (en.isIntersecting){ en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, {threshold:.12, rootMargin:'0px 0px -8% 0px'});
    reveals.forEach(function(el){ io.observe(el); });
  } else {
    reveals.forEach(function(el){ el.classList.add('in'); });
  }

  /* ---------- back to top ---------- */
  var totop = document.getElementById('totop');
  if (totop){
    window.addEventListener('scroll', function(){
      totop.classList.toggle('show', window.scrollY > 600);
    }, {passive:true});
    totop.addEventListener('click', function(){ window.scrollTo({top:0, behavior:'smooth'}); });
  }

  /* ---------- language switcher (Google Translate, headless) ---------- */
  var langBtn = document.getElementById('langBtn');
  var langPop = document.getElementById('langPop');
  var langList = document.getElementById('langList');
  var langSearch = document.getElementById('langSearch');
  var langCur = document.getElementById('langCur');

  function setCookie(name, val){
    var host = location.hostname;
    document.cookie = name+'='+val+';path=/';
    document.cookie = name+'='+val+';path=/;domain='+host;
    if (host.indexOf('.') > -1){
      document.cookie = name+'='+val+';path=/;domain=.'+host.split('.').slice(-2).join('.');
    }
  }
  function currentLang(){
    var m = document.cookie.match(/googtrans=\/[a-z-]+\/([a-zA-Z-]+)/);
    return m ? m[1] : 'en';
  }
  function applyLang(code, label){
    if (code === 'en'){
      setCookie('googtrans', '');
      document.cookie = 'googtrans=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/';
    } else {
      setCookie('googtrans', '/en/'+code);
    }
    location.reload();
  }
  if (langBtn && langPop){
    // reflect current selection
    (function(){
      var cur = currentLang();
      var li = langList.querySelector('[data-code="'+cur+'"]');
      if (li){ langCur.textContent = li.textContent; li.classList.add('sel'); }
    })();
    langBtn.addEventListener('click', function(e){
      e.stopPropagation();
      var open = langPop.classList.toggle('open');
      langBtn.setAttribute('aria-expanded', open?'true':'false');
      if (open){ langSearch.value=''; filterLangs(''); langSearch.focus(); }
    });
    document.addEventListener('click', function(e){
      if (!langPop.contains(e.target) && e.target!==langBtn){
        langPop.classList.remove('open'); langBtn.setAttribute('aria-expanded','false');
      }
    });
    langList.addEventListener('click', function(e){
      var li = e.target.closest('li'); if (!li) return;
      applyLang(li.getAttribute('data-code'), li.textContent);
    });
    function filterLangs(q){
      q = q.toLowerCase();
      var first = null;
      langList.querySelectorAll('li').forEach(function(li){
        var match = li.textContent.toLowerCase().indexOf(q) > -1;
        li.style.display = match ? '' : 'none';
        li.classList.remove('hl');
        if (match && !first) first = li;
      });
      if (first) first.classList.add('hl');
    }
    langSearch.addEventListener('input', function(){ filterLangs(this.value); });
    langSearch.addEventListener('keydown', function(e){
      if (e.key === 'Enter'){
        var hl = langList.querySelector('li.hl');
        if (hl){ e.preventDefault(); applyLang(hl.getAttribute('data-code'), hl.textContent); }
      }
    });
  }
  // load Google Translate element + hide its UI
  window.googleTranslateElementInit = function(){
    try{
      new google.translate.TranslateElement({pageLanguage:'en', autoDisplay:false}, 'google_translate_element');
    }catch(err){}
  };
  (function(){
    var s = document.createElement('script');
    s.src = '//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
    s.async = true; document.head.appendChild(s);
    var css = document.createElement('style');
    css.textContent =
      '.goog-te-banner-frame,.skiptranslate{display:none!important}'+
      'body{top:0!important;position:static!important}'+
      '#goog-gt-tt,.goog-te-balloon-frame{display:none!important}'+
      '.goog-text-highlight{background:none!important;box-shadow:none!important}'+
      'font[style]{background:none!important;box-shadow:none!important}';
    document.head.appendChild(css);
  })();

  /* ---------- contact form: file chips + validation ---------- */
  var form = document.getElementById('bidForm');
  if (form){
    var drop = document.getElementById('drop');
    var fileInput = form.querySelector('input[type=file]');
    var filesOut = document.getElementById('files');
    var status = document.getElementById('formStatus');

    if (fileInput && filesOut){
      fileInput.addEventListener('change', renderFiles);
      ['dragenter','dragover'].forEach(function(ev){
        drop.addEventListener(ev, function(e){ e.preventDefault(); drop.classList.add('drag'); });
      });
      ['dragleave','drop'].forEach(function(ev){
        drop.addEventListener(ev, function(e){ e.preventDefault(); drop.classList.remove('drag'); });
      });
      drop.addEventListener('drop', function(e){
        if (e.dataTransfer && e.dataTransfer.files.length){ fileInput.files = e.dataTransfer.files; renderFiles(); }
      });
      function renderFiles(){
        filesOut.innerHTML = '';
        var files = Array.prototype.slice.call(fileInput.files);
        files.slice(0,8).forEach(function(f){
          var s = document.createElement('span');
          s.className = 'upload-chip';
          s.textContent = f.name.length>26 ? f.name.slice(0,24)+'…' : f.name;
          filesOut.appendChild(s);
        });
        if (files.length>8){
          var more = document.createElement('span');
          more.className='upload-chip'; more.textContent='+'+(files.length-8)+' more';
          filesOut.appendChild(more);
        }
      }
    }

    form.addEventListener('submit', function(e){
      // honeypot
      var honey = form.querySelector('[name=_honey]');
      if (honey && honey.value){ e.preventDefault(); return; }
      var ok = true;
      form.querySelectorAll('[required]').forEach(function(f){
        if (!f.value.trim()){ ok=false; f.style.borderColor='#c0392b'; }
        else { f.style.borderColor=''; }
      });
      var email = form.querySelector('[name=email]');
      if (email && email.value && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email.value)){
        ok=false; email.style.borderColor='#c0392b';
      }
      if (!ok){
        e.preventDefault();
        if (status){ status.className='form-status err'; status.textContent='Please complete the required fields so we can reach you.'; }
        return;
      }
      // native submit to FormSubmit proceeds
      var btn = form.querySelector('button[type=submit]');
      if (btn){ btn.disabled=true; btn.textContent='Sending…'; }
      if (status){ status.className='form-status ok'; status.textContent='Sending your request…'; }
    });
  }
})();
