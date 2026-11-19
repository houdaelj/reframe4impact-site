(function(){
  var nav=document.getElementById('nav'), burger=document.getElementById('burger');
  if(burger&&nav){burger.addEventListener('click',function(){var o=nav.classList.toggle('open');burger.setAttribute('aria-expanded',String(o))});}
  var mz=document.getElementById('mosaic');
  if(mz){var rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;setTimeout(function(){mz.classList.add('framed')},rm?0:800);}
  (function(){var hd=document.querySelector('header.top');function sc(){hd&&hd.classList.toggle('scrolled',scrollY>8)}addEventListener('scroll',sc,{passive:true});sc();
    if(!('IntersectionObserver' in window)||matchMedia('(prefers-reduced-motion: reduce)').matches)return;
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
    window.r4iReveal=function(root){(root||document).querySelectorAll('.head,.pillar,.svc,.step,.acad-band,.course,.chips,.cta,.deliv>div,.values>div,.ft-top,.ft-cols>div').forEach(function(el){
      if(el.classList.contains('in'))return;var r=el.getBoundingClientRect();if(r.top<innerHeight&&r.bottom>0)return;
      var sib=el.parentElement?[].indexOf.call(el.parentElement.children,el):0;el.style.setProperty('--i',Math.min(sib,5));el.classList.add('reveal');io.observe(el)})};
    window.r4iReveal();})();
  var cp=document.getElementById('copy-mail');
  if(cp){cp.addEventListener('click',function(){
    var el=document.getElementById('mail'), t=el.textContent, btn=this, old=btn.innerHTML;
    function done(){btn.textContent=document.documentElement.lang==='en'?'Copied':'Copié';setTimeout(function(){btn.innerHTML=old},1500)}
    function sel(){var r=document.createRange();r.selectNodeContents(el);var s=getSelection();s.removeAllRanges();s.addRange(r)}
    if(navigator.clipboard){navigator.clipboard.writeText(t).then(done,sel)}else sel();
  });}
})();
