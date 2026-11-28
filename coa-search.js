(() => {
 const input=document.getElementById('coa-search');
 if(!input)return;
 const cards=[...document.querySelectorAll('.coa-card')];
 const groups=[...document.querySelectorAll('[data-coa-group]')];
 const normalize=value=>String(value||'').toLowerCase()
  .replace(/[\-\u2010-\u2015]/g,'')
  .replace(/[^a-z0-9]+/g,' ').trim();
 const searchable=new Map(cards.map(card=>[card,normalize(card.textContent)]));
 function update(){
  const query=normalize(input.value);
  const terms=query?query.split(/\s+/):[];
  let count=0;
  for(const card of cards){
   card.hidden=!terms.every(term=>searchable.get(card).includes(term));
   if(!card.hidden)count++;
  }
  for(const group of groups){
   const visible=[...group.querySelectorAll('.coa-card')].filter(card=>!card.hidden).length;
   group.hidden=visible===0;
   group.querySelector('[data-group-count]').textContent=visible+' reports';
  }
  document.getElementById('coa-count').textContent=count+' reports';
  document.getElementById('coa-empty').hidden=count>0;
 }
 input.addEventListener('input',update);
 document.querySelectorAll('.coa-categories a').forEach(link=>link.addEventListener('click',()=>{input.value='';update();}));
 update();
})();
