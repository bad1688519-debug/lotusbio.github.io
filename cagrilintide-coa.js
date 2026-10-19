(() => {
 const spec=document.querySelector('#quote-spec'), qty=document.querySelector('#quote-qty');
 if(!spec||!qty)return;
 function update(){
   const valid=qty.validity.valid && Number(qty.value)>0;
   const selection='Cagrilintide · '+spec.value+(valid?' · '+qty.value+' box(es)':'');
   document.querySelector('[data-batch-selection]').textContent='Selected: '+selection;
   document.querySelectorAll('[data-batch-coa]').forEach(a=>{a.href='/coas/?product='+encodeURIComponent(selection)+'#request-coa';});
 }
 spec.addEventListener('change',update);qty.addEventListener('input',update);update();
})();