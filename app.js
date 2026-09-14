document.querySelector('form')?.addEventListener('submit', function (event) {
  event.preventDefault();
  const data = new FormData(this);
  const body = `Company / name: ${data.get('company')}\nEmail: ${data.get('email')}\n\nRequirements:\n${data.get('requirements')}`;
  const subject = 'LotusBio wholesale inquiry';
  let panel = document.querySelector('#email-fallback');
  if (!panel) { panel = document.createElement('div'); panel.id = 'email-fallback'; this.append(panel); }
  panel.innerHTML = '<strong>Sending your inquiry…</strong><p id="copy-status" role="status"></p>';
  const payload = { subject, company: data.get('company'), email: data.get('email'), requirements: data.get('requirements'), _replyto: data.get('email') };
  const submit=this.querySelector('[type="submit"]');submit.disabled=true;
  window.sendLotusInquiry(payload)
    .then(() => { panel.querySelector('strong').textContent = 'Your inquiry was accepted for delivery.'; panel.querySelector('#copy-status').textContent = 'Reply email: ' + data.get('email') + '.'; })
    .catch(() => { panel.querySelector('strong').textContent = 'We could not confirm delivery.'; panel.querySelector('#copy-status').textContent = 'Your details remain in the form. Please contact info@lotusbio.cn or use WhatsApp.'; })
    .finally(()=>{submit.disabled=false;});
  panel.insertAdjacentHTML('beforeend', '<button type="button" class="button" id="copy-email">Copy inquiry</button>');
  panel.querySelector('#copy-email').onclick = async () => {
    try { await navigator.clipboard.writeText(body); panel.querySelector('#copy-status').textContent = 'Copied. Paste it into an email to info@lotusbio.cn.'; }
    catch { panel.querySelector('#copy-status').textContent = 'Please copy the inquiry manually.'; }
  };
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
