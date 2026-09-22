document.querySelectorAll('form[data-inquiry]').forEach(form => {
  const params = new URLSearchParams(location.search);
  if (form.elements.product && params.get('product')) form.elements.product.value = params.get('product');
  if (form.elements.requirements && params.get('report')) form.elements.requirements.value = 'Please confirm the batch documentation associated with Janoshik report #' + params.get('report') + '.';
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const data = new FormData(form);
    const labels = {company:'Company / name',email:'Email',country:'Destination country',product:'Product / specification',quantity:'Estimated quantity',frequency:'Purchase frequency',whatsapp:'WhatsApp',requirements:'Requirements'};
    const body = Object.entries(labels).filter(([key])=>data.has(key)).map(([key,label])=>label+': '+data.get(key)).join('\n');
    const subject = data.get('request_type') === 'COA documentation request' ? 'LotusBio COA documentation request' : 'LotusBio wholesale inquiry';
    let panel = form.querySelector('#email-fallback');
    if (!panel) {panel=document.createElement('div');panel.id='email-fallback';form.append(panel);}
    panel.replaceChildren();
    const status=document.createElement('p');status.setAttribute('role','status');status.textContent='Sending your inquiry…';panel.append(status);
    const email=document.createElement('a');email.className='button';email.textContent='Open email draft';email.href='mailto:info@lotusbio.cn?subject='+encodeURIComponent(subject)+'&body='+encodeURIComponent(body);
    const whatsapp=document.createElement('a');whatsapp.className='button';whatsapp.textContent='Open WhatsApp draft';whatsapp.href='https://wa.me/85292734987?text='+encodeURIComponent(body);whatsapp.target='_blank';whatsapp.rel='noopener';
    const copy=document.createElement('button');copy.type='button';copy.className='button';copy.textContent='Copy inquiry';copy.onclick=async()=>{try{await navigator.clipboard.writeText(body);status.textContent='Copied. Paste into an email to info@lotusbio.cn.';}catch{status.textContent='Copy is unavailable. Use the email or WhatsApp draft, or copy the fields manually.';}};
    panel.append(email,whatsapp,copy);
    const submit=form.querySelector('[type="submit"]');submit.disabled=true;
    const payload={subject,company:data.get('company'),email:data.get('email'),_replyto:data.get('email'),requirements:body};
    try {await window.sendLotusInquiry(payload);status.textContent='Your inquiry was accepted for delivery. Reply email: '+data.get('email')+'.';}
    catch {status.textContent='We could not confirm delivery. Your details remain in the form. Use an email or WhatsApp draft below.';}
    finally {submit.disabled=false;}
  });
});

// Native dialog keeps confirmation independent of any framework or hydration.
const gate = document.querySelector('#age-confirmation');
let accepted = false;
try { accepted = sessionStorage.getItem('lotusbio-rebuild-age') === 'accepted'; } catch {}
if (gate && !accepted) gate.showModal();
document.querySelector('#age-continue')?.addEventListener('click', () => {
  try { sessionStorage.setItem('lotusbio-rebuild-age', 'accepted'); } catch {}
  gate.close();
});
document.querySelector('#age-leave')?.addEventListener('click', () => { location.href = 'https://www.google.com/'; });
gate?.addEventListener('cancel', event => event.preventDefault());

