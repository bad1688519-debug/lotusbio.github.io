(() => {
  const product = document.querySelector('.product-order[data-product]');
  const spec = product?.querySelector('#quote-spec');
  const quantity = product?.querySelector('#quote-qty');
  if (!product?.dataset.product || !spec || !quantity) return;

  function updateDocumentLinks() {
    const count = Number(quantity.value);
    const valid = quantity.validity.valid && Number.isInteger(count) && count > 0;
    const selection = product.dataset.product + ' · ' + spec.value
      + (valid ? ' · ' + count + (count === 1 ? ' box' : ' boxes') : '');
    document.querySelectorAll('[data-batch-selection]').forEach(node => {
      node.textContent = 'Selected: ' + selection + '.'
        + (valid ? '' : ' Enter a valid whole-number box quantity to include it in your request.');
    });
    document.querySelectorAll('[data-batch-coa]').forEach(link => {
      link.href = '/coas/?product=' + encodeURIComponent(selection) + '#request-coa';
    });
    const sampleSpecification = spec.value.replace(/\s*×\s*\d+\s*vials\b/i, '');
    const sampleSelection = product.dataset.product + ' · ' + sampleSpecification;
    document.querySelectorAll('[data-test-sample]').forEach(link => {
      link.href = '/wholesale/?inquiry=sample-testing&product=' + encodeURIComponent(sampleSelection) + '#inquiry';
    });
    document.querySelectorAll('[data-selected-quote]').forEach(link => {
      link.href = '/wholesale/?product=' + encodeURIComponent(selection) + '#inquiry';
    });
  }
  spec.addEventListener('change', updateDocumentLinks);
  quantity.addEventListener('input', updateDocumentLinks);
  updateDocumentLinks();
})();
