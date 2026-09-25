async ([sel, kind]) => {
  const src = document.querySelector(sel), clone = src.cloneNode(true);
  const a = [src, ...src.querySelectorAll('*')], c = [clone, ...clone.querySelectorAll('*')];
  const props = ['fill', 'stroke', 'stroke-width', 'opacity', 'fill-opacity', 'stroke-opacity', 'stop-color', 'stop-opacity', 'stroke-linecap', 'stroke-linejoin', 'filter', 'fill-rule'];
  a.forEach((e, i) => {
    const cs = getComputedStyle(e), t = c[i];
    if (!['defs', 'mask', 'linearGradient', 'radialGradient', 'filter', 'feGaussianBlur'].includes(e.tagName)) for (const p of props) { const v = cs.getPropertyValue(p); if (v && v !== 'none' || p === 'fill') if (!t.hasAttribute(p)) t.setAttribute(p, v || 'none'); }
    if (['stop'].includes(e.tagName)) { t.setAttribute('stop-color', cs.getPropertyValue('stop-color')); t.setAttribute('stop-opacity', cs.getPropertyValue('stop-opacity')); }
    const cls = e.getAttribute && e.getAttribute('class'); if (cls && !t.id) t.id = cls.split(' ')[0];
    t.removeAttribute('class'); t.removeAttribute('style'); t.removeAttribute('mask'); t.removeAttribute('pathLength');
  });
  clone.querySelectorAll('mask').forEach(m => m.remove());
  const vb = src.getAttribute('viewBox').split(' ').map(Number);
  clone.setAttribute('width', vb[2]); clone.setAttribute('height', vb[3]); clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
  clone.removeAttribute('aria-hidden'); clone.removeAttribute('focusable');
  if (kind === 'team') {
    const doc = new DOMParser().parseFromString(await (await fetch('/assets/gymnast/team.svg')).text(), 'image/svg+xml');
    clone.querySelectorAll('use').forEach(u => {
      const id = u.getAttribute('href').split('#')[1], sym = doc.getElementById(id);
      const s = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      for (const k of ['x', 'y', 'width', 'height']) s.setAttribute(k, u.getAttribute(k));
      s.setAttribute('viewBox', sym.getAttribute('viewBox')); s.setAttribute('id', id);
      for (const p of sym.children) { const q = p.cloneNode(true); q.setAttribute('fill', u.getAttribute('fill')); q.setAttribute('opacity', u.getAttribute('opacity') || '1'); s.appendChild(q); }
      u.replaceWith(s);
    });
    const r = clone.querySelector('#team-ribbon'); if (r) r.id = 'ribbon';
  }
  return new XMLSerializer().serializeToString(clone);
}
