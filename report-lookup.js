/* LotusBio report access v1. Each random code supplies its own decryption key.
   Only encrypted payloads are public; no code directory or decryption keys ship. */
(() => {
  'use strict';
  const form = document.getElementById('report-lookup');
  if (!form) return;
  const field = document.getElementById('report-code');
  const button = form.querySelector('button[type="submit"]');
  const status = document.getElementById('lookup-status');
  const result = document.getElementById('lookup-result');
  const open = document.getElementById('result-open');
  const download = document.getElementById('result-download');
  const encoder = new TextEncoder();
  const decoder = new TextDecoder('utf-8', { fatal: true });
  let objectUrl = null;
  let requestVersion = 0;
  let controller = null;
  const hex = bytes => Array.from(new Uint8Array(bytes), b => b.toString(16).padStart(2, '0')).join('');
  const digest = text => crypto.subtle.digest('SHA-256', encoder.encode(text));
  function clear() {
    if (objectUrl) URL.revokeObjectURL(objectUrl);
    objectUrl = null;
    result.hidden = true;
    open.removeAttribute('href');
    download.removeAttribute('href');
    ['result-group','result-title','result-id','result-date','result-note'].forEach(id => {
      document.getElementById(id).textContent = '';
    });
  }
  document.getElementById('result-clear').addEventListener('click', () => {
    requestVersion++;
    if (controller) controller.abort();
    clear(); field.value = ''; status.textContent = 'Report closed.'; field.focus();
  });
  form.addEventListener('submit', async event => {
    event.preventDefault();
    const version = ++requestVersion;
    if (controller) controller.abort();
    controller = new AbortController();
    clear();
    const code = field.value.toUpperCase().replace(/[\s-]/g, '');
    if (!/^LB[A-Z2-7]{24}$/.test(code)) {
      status.textContent = 'Enter the complete LotusBio access code, including its LB prefix.';
      field.focus(); return;
    }
    if (!crypto.subtle) {
      status.textContent = 'Your browser cannot unlock this report. Use a current browser over HTTPS or contact our team.';
      return;
    }
    button.disabled = true;
    status.textContent = 'Checking your code…';
    try {
      const path = hex(await digest('LotusBio report lookup v1:' + code));
      const response = await fetch('/assets/report-vault/' + path + '.bin', {
        credentials: 'omit', cache: 'no-store', signal: controller.signal
      });
      if (!response.ok) throw new Error('Unavailable');
      const bytes = new Uint8Array(await response.arrayBuffer());
      if (bytes.length < 40 || decoder.decode(bytes.slice(0, 8)) !== 'LBENC001') throw new Error('Invalid payload');
      const key = await crypto.subtle.importKey('raw', await digest('LotusBio report key v1:' + code), {name:'AES-GCM'}, false, ['decrypt']);
      const plain = new Uint8Array(await crypto.subtle.decrypt({
        name:'AES-GCM', iv:bytes.slice(8,20), additionalData:encoder.encode('LotusBio report v1'), tagLength:128
      }, key, bytes.slice(20)));
      const length = new DataView(plain.buffer).getUint32(0, false);
      if (length > 16384 || length + 4 > plain.length) throw new Error('Invalid record');
      const meta = JSON.parse(decoder.decode(plain.slice(4, 4 + length)));
      const pdf = plain.slice(4 + length);
      if (meta.mime === 'application/pdf') {
        if (decoder.decode(pdf.slice(0,5)) !== '%PDF-' || hex(await crypto.subtle.digest('SHA-256', pdf)) !== meta.sha256) throw new Error('Invalid PDF');
        if (version !== requestVersion) return;
        objectUrl = URL.createObjectURL(new Blob([pdf], {type:'application/pdf'}));
        open.href = objectUrl; open.textContent = 'Open PDF report ↗';
        download.href = objectUrl; download.download = meta.filename;
        download.hidden = false;
      } else {
        const url = new URL(meta.verification_url);
        if (url.protocol !== 'https:' || url.hostname !== 'verify.janoshik.com' || !/^\/tests\/\d+_[A-Z0-9]+$/.test(url.pathname)) throw new Error('Invalid source');
        if (version !== requestVersion) return;
        open.href = url.href; open.textContent = 'Open official Janoshik report ↗';
        download.hidden = true;
      }
      document.getElementById('result-group').textContent = meta.group;
      document.getElementById('result-title').textContent = meta.product;
      document.getElementById('result-id').textContent = meta.original_report_id;
      document.getElementById('result-date').textContent = meta.date ? 'Report date: ' + meta.date : '';
      document.getElementById('result-note').textContent = meta.note;
      result.hidden = false;
      status.textContent = 'One matching report unlocked. Check the original identifiers and test scope.';
      field.value = '';
    } catch (error) {
      if (version === requestVersion) {
        clear();
        status.textContent = error.name === 'AbortError' ? 'Lookup cancelled.' : 'Report could not be opened. Check the complete code and your connection, or contact LotusBio.';
      }
    } finally {
      if (version === requestVersion) button.disabled = false;
    }
  });
  button.disabled = false;
  window.addEventListener('pagehide', clear);
})();


