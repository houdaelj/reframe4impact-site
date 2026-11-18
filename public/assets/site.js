(function(){
  var nav=document.getElementById('nav'), burger=document.getElementById('burger');
  if(burger&&nav){burger.addEventListener('click',function(){var o=nav.classList.toggle('open');burger.setAttribute('aria-expanded',String(o))});}
  var mz=document.getElementById('mosaic');
  if(mz){setTimeout(function(){mz.classList.add('framed')},700);}
  var cp=document.getElementById('copy-mail');
  if(cp){cp.addEventListener('click',function(){
    var el=document.getElementById('mail'), t=el.textContent, btn=this, old=btn.innerHTML;
    function done(){btn.textContent=document.documentElement.lang==='en'?'Copied':'Copié';setTimeout(function(){btn.innerHTML=old},1500)}
    function sel(){var r=document.createRange();r.selectNodeContents(el);var s=getSelection();s.removeAllRanges();s.addRange(r)}
    if(navigator.clipboard){navigator.clipboard.writeText(t).then(done,sel)}else sel();
  });}
})();
