(() => {
  const input = document.querySelector('#catalog-search');
  if (!input) return;
  const normalize = value => String(value || '').toLowerCase()
    .replace(/(\d)\s+(mg|mcg|g|ml)\b/g, '$1$2')
    .replace(/[-\u2010-\u2015]/g, '')
    .replace(/[^a-z0-9]+/g, ' ').trim();
  const cards = [...document.querySelectorAll('[data-catalog-item]')].map(card => ({
    card,
    searchable: normalize([
      card.dataset.search,
      card.querySelector('h2')?.textContent,
      card.querySelector('.catalog-formats')?.textContent
    ].filter(Boolean).join(' '))
  }));
  const update = () => {
    const terms = normalize(input.value).split(' ').filter(Boolean);
    let count = 0;
    cards.forEach(({ card, searchable }) => {
      const match = terms.every(term => searchable.includes(term));
      card.hidden = !match;
      if (match) count++;
    });
    const status = document.querySelector('#catalog-count');
    const empty = document.querySelector('#catalog-empty');
    if (status) status.textContent = `Showing ${count} of ${cards.length} products`;
    if (empty) empty.hidden = count !== 0;
  };
  input.addEventListener('input', update);
  update();
})();
