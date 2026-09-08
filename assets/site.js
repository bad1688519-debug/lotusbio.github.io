
(()=>{
 const gate=document.getElementById('ageGate');
 if(gate && localStorage.getItem('lotusbio-age-ok')!=='1') gate.hidden=false;
 const accept=document.getElementById('ageAccept'); if(accept) accept.addEventListener('click',()=>{localStorage.setItem('lotusbio-age-ok','1'); gate.hidden=true;});
 const mb=document.querySelector('.menu-btn'), nav=document.querySelector('header nav'); if(mb&&nav) mb.addEventListener('click',()=>nav.classList.toggle('open'));
 document.querySelectorAll('[data-quote-form]').forEach(form=>form.addEventListener('submit',e=>{e.preventDefault();const d=new FormData(form);const lines=[...d.entries()].filter(([,v])=>String(v).trim()).map(([k,v])=>k+': '+v);const subject=encodeURIComponent('LotusBio wholesale inquiry');const body=encodeURIComponent(lines.join('\n'));location.href='mailto:info@lotusbio.cn?subject='+subject+'&body='+body;}));
 document.querySelectorAll('[data-wa-form]').forEach(btn=>btn.addEventListener('click',()=>{const form=btn.closest('form');const d=new FormData(form);const lines=[...d.entries()].filter(([,v])=>String(v).trim()).map(([k,v])=>k+': '+v);window.open('https://wa.me/85292734987?text='+encodeURIComponent('LotusBio wholesale inquiry\n'+lines.join('\n')),'_blank');}));
})();
