/* Optional, consent-gated measurement. Never send inquiry field values. */
(() => {
  'use strict';
  if (window.lotusAnalytics) return;
  const id = 'G-RG2DB32WR9';
  const consentKey = 'lotusbio-analytics-consent-v1';
  const maxAge = 180 * 86400000;
  const production = location.hostname === 'lbiopeptides.com';
  let choice = null, loaded = false;
  try { const saved = JSON.parse(localStorage.getItem(consentKey)); if (saved && Date.now() - saved.at < maxAge && ['granted','denied'].includes(saved.value)) choice = saved.value; } catch {}
  const disabledKey = 'ga-disable-' + id;
  window[disabledKey] = choice !== 'granted';
  function safeReferrer() { try { return new URL(document.referrer).origin + '/'; } catch { return ''; } }
  function page() { return {page_location: location.origin + location.pathname, page_referrer: safeReferrer(), page_title: document.title}; }
  function start() {
    if (!production || choice !== 'granted') return;
    window[disabledKey] = false;
    const firstLoad = !loaded;
    loaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('consent', 'default', {analytics_storage:'denied', ad_storage:'denied', ad_user_data:'denied', ad_personalization:'denied'});
    window.gtag('consent', 'update', {analytics_storage:'granted'});
    window.gtag('js', new Date());
    window.gtag('config', id, {...page(), send_page_view:false, allow_google_signals:false, allow_ad_personalization_signals:false, cookie_expires:15552000});
    window.gtag('event', 'page_view', {...page(), send_to:id});
    if (firstLoad) { const script = document.createElement('script'); script.async = true; script.src = 'https://www.googletagmanager.com/gtag/js?id=' + id; script.id = 'lotus-ga4'; document.head.append(script); }
  }
  function track(name, details = {}) {
    if (!production || choice !== 'granted' || !loaded || window[disabledKey]) return;
    if (!['contact_whatsapp','contact_email','view_coa','generate_lead','begin_inquiry'].includes(name)) return;
    const params = {...page(), send_to:id};
    if (['form','quote_list'].includes(details.method)) params.method = details.method;
    if (['pdf','report_page','verification'].includes(details.document_type)) params.document_type = details.document_type;
    window.gtag('event', name, params);
  }
  function removeCookies() {
    document.cookie.split(';').forEach(item => { const name = item.trim().split('=')[0]; if (!/^_ga(?:_|$)/.test(name)) return;
      ['', location.hostname, '.' + location.hostname].forEach(domain => { document.cookie = name + '=; Max-Age=0; path=/; SameSite=Lax' + (domain ? '; domain=' + domain : ''); });
    });
  }
  function choose(value) {
    choice = value;
    try { localStorage.setItem(consentKey, JSON.stringify({value, at:Date.now()})); } catch {}
    window[disabledKey] = value !== 'granted';
    if (value === 'granted') {
      start();
    } else {
      // Drop queued commands as well as disabling future measurement.
      if (window.dataLayer) window.dataLayer.length = 0;
      removeCookies();
    }
    panel.hidden = true;
  }
  const style = document.createElement('style'); style.textContent = '.lb-consent{position:fixed;bottom:18px;left:18px;right:18px;max-width:640px;padding:20px;background:#fff;color:#12313a;border:1px solid #b9d6ce;border-radius:12px;box-shadow:0 6px 30px #102b3326;z-index:9999;font:14px/1.5 Arial,sans-serif}.lb-consent[hidden]{display:none}.lb-consent p{margin:0 0 14px}.lb-consent-actions{display:flex;gap:10px;flex-wrap:wrap}.lb-consent button{background:#176b51;color:#fff;border:1px solid #176b51;border-radius:6px;padding:10px 16px;font:inherit;cursor:pointer}.lb-consent a{color:#176b51;text-decoration:underline}.lb-consent-links{display:flex;gap:14px;flex-wrap:wrap;align-items:center;padding:12px 0}.lb-consent-links button{font:inherit;color:inherit;background:none;border:0;padding:0;text-decoration:underline;cursor:pointer}@media(max-width:600px){.lb-consent{bottom:10px;left:10px;right:10px;padding:16px}.lb-consent-actions button{flex:1}}'; document.head.append(style);
  const panel = document.createElement('section'); panel.className = 'lb-consent'; panel.setAttribute('aria-label','Analytics privacy choice'); panel.hidden = choice !== null;
  panel.innerHTML = '<p><strong>Optional analytics</strong><br>With your permission, we use Google Analytics to understand visits and inquiry actions. We do not send your form entries to Analytics. You can change your choice at any time. <a href="/privacy/">Privacy details</a></p><div class="lb-consent-actions"><button type="button" data-consent="denied">Reject analytics</button><button type="button" data-consent="granted">Allow analytics</button></div>';
  panel.querySelectorAll('[data-consent]').forEach(button => button.addEventListener('click', () => choose(button.dataset.consent)));
  document.body.append(panel);
  const settings = document.createElement('div'); settings.className = 'lb-consent-links'; settings.innerHTML = '<a href="/privacy/">Privacy</a><button type="button">Analytics preferences</button>';
  settings.querySelector('button').addEventListener('click', () => { panel.hidden = false; panel.querySelector('button').focus(); });
  (document.querySelector('footer') || document.body).append(settings);
  document.addEventListener('click', event => {
    const link = event.target.closest && event.target.closest('a[href]'); if (!link) return;
    let url; try { url = new URL(link.href, location.href); } catch { return; }
    if (['wa.me','api.whatsapp.com','web.whatsapp.com'].includes(url.hostname)) track('contact_whatsapp');
    else if (url.protocol === 'mailto:') track('contact_email');
    else if (url.hostname === 'janoshik.com') track('view_coa',{document_type:'verification'});
    else if (url.origin === location.origin && /(?:\/coas?\/|\/reports\/|\.pdf$)/i.test(url.pathname)) track('view_coa',{document_type:/\.pdf$/i.test(url.pathname)?'pdf':'report_page'});
  });
  document.addEventListener('lotus:inquiry-accepted', () => track('generate_lead',{method:'form'}));
  window.lotusAnalytics = {track};
  start();
})();
