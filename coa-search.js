(() => {
 const input=document.getElementById('coa-search');
 if(!input)return;
 const cards=[...document.querySelectorAll('.coa-card')];
 const groups=[...document.querySelectorAll('[data-coa-group]')];
 function update(){
  const q=input.value.trim().toLowerCase();let count=0;
  for(const card of cards){card.hidden=!card.textContent.toLowerCase().includes(q);if(!card.hidden)count++;}
  for(const group of groups){const visible=[...group.querySelectorAll('.coa-card')].filter(c=>!c.hidden).length;group.hidden=visible===0;group.querySelector('[data-group-count]').textContent=visible+' reports';}
  document.getElementById('coa-count').textContent=count+' reports';
  document.getElementById('coa-empty').hidden=count>0;
 }
 input.addEventListener('input',update);
 document.querySelectorAll('.coa-categories a').forEach(link=>link.addEventListener('click',()=>{input.value='';update();}));update();
})();