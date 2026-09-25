async (sel) => {
  const root = getComputedStyle(document.documentElement), tokens = {};
  for (const n of ['paper','paper-raised','sand','blush','cream','placeholder','ink','ink-muted','line','line-strong','pink','pink-deep','pink-soft','pink-tint','brand-magenta','brand-orange','stage','on-stage','on-stage-muted','peach','decor','decor-soft','error','white']) {
    let v = root.getPropertyValue('--' + n).trim().toLowerCase();
    if (v.length === 4) v = '#' + [...v.slice(1)].map(c => c + c).join('');
    if (v) tokens[v] = n;
  }
  const col = c => {
    let p;
    const m1 = c.match(/^rgba?\(([^)]+)\)/), m2 = c.match(/^color\(srgb ([^)]+)\)/);
    if (m1) p = m1[1].split(/[ ,/]+/).filter(Boolean).map(Number);
    else if (m2) { const q = m2[1].split(/[ /]+/).filter(Boolean).map(Number); p = [q[0] * 255, q[1] * 255, q[2] * 255, q[3] ?? 1]; }
    else return null;
    const a = p[3] ?? 1;
    if (a === 0) return null;
    const hex = '#' + p.slice(0, 3).map(v => Math.round(v).toString(16).padStart(2, '0')).join('');
    return {hex, a: +a.toFixed(3), token: tokens[hex] || null};
  };
  const sec = document.querySelector(sel), sr = sec.getBoundingClientRect(), sx = sr.left, sy = sr.top;
  const box = e => {
    const r = e.getBoundingClientRect(), w = e.offsetWidth || r.width, h = e.offsetHeight || r.height;
    return {x: +(r.left + r.width / 2 - w / 2 - sx).toFixed(1), y: +(r.top + r.height / 2 - h / 2 - sy).toFixed(1), w: +w.toFixed(1), h: +h.toFixed(1)};
  };
  const vis = e => { const c = getComputedStyle(e); return c.display !== 'none' && c.visibility !== 'hidden' && +c.opacity > 0 && e.getClientRects().length > 0; };
  const sprite = new DOMParser().parseFromString(await (await fetch('/assets/gymnast/team.svg')).text(), 'image/svg+xml');
  const svgOut = svg => {
    const clone = svg.cloneNode(true), a = [svg, ...svg.querySelectorAll('*')], c = [clone, ...clone.querySelectorAll('*')];
    a.forEach((e, i) => {
      const cs = getComputedStyle(e), t = c[i];
      for (const p of ['fill', 'stroke', 'stroke-width', 'opacity', 'stroke-linecap', 'stroke-linejoin', 'fill-rule']) { const v = cs.getPropertyValue(p); if (v && !t.hasAttribute(p)) t.setAttribute(p, v); }
      t.removeAttribute('class'); t.removeAttribute('style'); t.removeAttribute('mask');
    });
    clone.querySelectorAll('use').forEach(u => {
      const id = (u.getAttribute('href') || '').split('#')[1], sym = sprite.getElementById(id);
      if (!sym) return;
      const s = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      for (const k of ['x', 'y', 'width', 'height']) if (u.getAttribute(k)) s.setAttribute(k, u.getAttribute(k));
      s.setAttribute('viewBox', sym.getAttribute('viewBox'));
      for (const p of sym.children) { const q = p.cloneNode(true); q.setAttribute('fill', u.getAttribute('fill') || 'rgb(37, 33, 30)'); s.appendChild(q); }
      u.replaceWith(s);
    });
    const b = box(svg);
    clone.setAttribute('width', b.w); clone.setAttribute('height', b.h); clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    clone.removeAttribute('aria-hidden'); clone.removeAttribute('focusable');
    return new XMLSerializer().serializeToString(clone);
  };
  const satinOnly = (svg, b) => {
    const g = svg.querySelector('.apparatus-satin'), clone = g.cloneNode(true), a = [g, ...g.querySelectorAll('*')], c = [clone, ...clone.querySelectorAll('*')];
    a.forEach((e, i) => { const cs = getComputedStyle(e), t = c[i]; for (const p of ['fill', 'stroke', 'stroke-width', 'opacity']) { const v = cs.getPropertyValue(p); if (v && !t.hasAttribute(p)) t.setAttribute(p, v); } t.removeAttribute('class'); t.removeAttribute('data-d'); });
    const vb = svg.getAttribute('viewBox');
    return `<svg xmlns="http://www.w3.org/2000/svg" width="${b.w}" height="${b.h}" viewBox="${vb}" preserveAspectRatio="xMidYMax meet">${clone.outerHTML}</svg>`;
  };
  const out = [];
  const walk = e => {
    for (const el of e.children) {
      if (!vis(el) || ['SCRIPT', 'TEMPLATE'].includes(el.tagName)) continue;
      const cs = getComputedStyle(el), b = box(el), name = (el.getAttribute('class') || el.tagName.toLowerCase()).split(' ')[0];
      const rot = cs.rotate && cs.rotate !== 'none' ? parseFloat(cs.rotate) : 0;
      if (el.tagName.toLowerCase() === 'svg' && el.classList.contains('apparatus-kid')) {
        const u = el.querySelector('use'), vb = el.viewBox.baseVal, s = Math.min(b.w / vb.width, b.h / vb.height);
        const ox = b.x + (b.w - vb.width * s) / 2, oy = b.y + (b.h - vb.height * s);
        const kid = {k: +u.getAttribute('href').split('kid-')[1], x: +(ox + u.x.baseVal.value * s).toFixed(1), y: +(oy + u.y.baseVal.value * s).toFixed(1), w: +(u.width.baseVal.value * s).toFixed(1), h: +(u.height.baseVal.value * s).toFixed(1)};
        const g = el.querySelector('.apparatus-satin');
        let satin = null;

        out.push({t: 'kid', ...kid, satin: g ? {x: b.x, y: b.y, w: b.w, h: b.h} : null, satinSvg: g ? satinOnly(el, b) : null});
        continue;
      }
      if (el.tagName.toLowerCase() === 'svg') { out.push({t: 'svg', name, ...b, rot, svg: svgOut(el)}); continue; }
      const bg = col(cs.backgroundColor), bw = ['Top', 'Right', 'Bottom', 'Left'].map(s => parseFloat(cs['border' + s + 'Width']) || 0);
      const bc = bw.some(v => v) ? col(bw[0] ? cs.borderTopColor : bw[2] ? cs.borderBottomColor : cs.borderLeftColor) : null;
      const shadow = cs.boxShadow !== 'none';
      if (bg || bc || shadow || el.classList.contains('is-empty')) out.push({t: 'rect', name, ...b, rot, bg, bc, bw, shadow, radius: parseFloat(cs.borderTopLeftRadius) || 0, mono: el.classList.contains('is-empty')});
      if (el.tagName === 'IMG') out.push({t: 'img', name, ...b, rot, src: el.getAttribute('src')});
      const direct = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
      const blockKids = [...el.children].some(k => vis(k) && k.tagName !== 'BR' && ['block', 'flex', 'grid', 'list-item', 'table'].includes(getComputedStyle(k).display));
      if (direct && !blockKids) {
        for (const s of el.querySelectorAll('svg')) if (vis(s)) out.push({t: 'svg', name: 'icon', ...box(s), rot: 0, svg: svgOut(s)});
        const em = el.querySelector('em');
        out.push({t: 'text', name, ...b, rot, text: el.innerText.replace(/ /g, ' '), fam: cs.fontFamily.split(',')[0].replace(/"/g, '').trim(),
          size: parseFloat(cs.fontSize), weight: +cs.fontWeight, lh: parseFloat(cs.lineHeight) || null, ls: parseFloat(cs.letterSpacing) || 0,
          upper: cs.textTransform === 'uppercase', align: cs.textAlign, color: col(cs.color), emColor: em ? col(getComputedStyle(em).color) : null,
          deco: cs.textDecorationLine});
        continue;
      }
      if (direct) for (const tn of el.childNodes) {
        if (tn.nodeType !== 3 || !tn.textContent.trim()) continue;
        const rg = document.createRange(); rg.selectNodeContents(tn); const rr = rg.getBoundingClientRect();
        out.push({t: 'text', name, x: +(rr.left - sx).toFixed(1), y: +(rr.top - sy).toFixed(1), w: +rr.width.toFixed(1), h: +rr.height.toFixed(1), rot: 0,
          text: tn.textContent.trim().replace(/ /g, ' '), fam: cs.fontFamily.split(',')[0].replace(/"/g, '').trim(), size: parseFloat(cs.fontSize), weight: +cs.fontWeight,
          lh: parseFloat(cs.lineHeight) || null, ls: parseFloat(cs.letterSpacing) || 0, upper: false, align: 'start', color: col(cs.color), emColor: null, deco: cs.textDecorationLine});
      }
      walk(el);
    }
  };
  walk(sec);
  const scs = getComputedStyle(sec);
  return {sel, w: +sr.width.toFixed(1), h: +sr.height.toFixed(1), bg: col(scs.backgroundColor), bgi: scs.backgroundImage !== 'none' ? scs.backgroundImage.slice(0, 200) : null, nodes: out};
}
