const page = await figma.getNodeByIdAsync(PAGE); await figma.setCurrentPageAsync(page);
const W = await figma.getNodeByIdAsync(WRAP);
const vars = await figma.variables.getLocalVariablesAsync('COLOR'); const VAR = {}; for (const v of vars) VAR[v.name.split('/').pop()] = v;
const hex = h => ({r: parseInt(h.slice(1, 3), 16) / 255, g: parseInt(h.slice(3, 5), 16) / 255, b: parseInt(h.slice(5, 7), 16) / 255});
const P = c => { let tok = null, a = 1, h = '#000000'; if (typeof c === 'string') tok = c; else if (c[0][0] === '#') { h = c[0]; a = c[1]; } else { tok = c[0]; a = c[1]; }
  if (tok && VAR[tok]) { const p = figma.variables.setBoundVariableForPaint({type: 'SOLID', color: {r: 0, g: 0, b: 0}}, 'color', VAR[tok]); return a < 1 ? {...p, opacity: a} : p; }
  return {type: 'SOLID', color: hex(h), opacity: a}; };
const ST = {400: 'Regular', 500: 'Medium', 600: 'SemiBold', 700: 'Bold'};
const font = (fam, w) => ({family: fam, style: fam === 'Cinzel' ? (w >= 700 ? 'Bold' : 'Regular') : (ST[w] || 'Regular')});
const styles = await figma.getLocalTextStylesAsync();
const fonts = new Map(); for (const s of styles) fonts.set(s.fontName.family + s.fontName.style, s.fontName);
for (const s of DATA) for (const n of s.nodes) if (n[0] === 'T') { const f = font(n[6], n[8]); fonts.set(f.family + f.style, f); }
await Promise.all([...fonts.values()].map(f => figma.loadFontAsync(f)));
const lhOf = s => s.lineHeight.unit === 'PERCENT' ? s.lineHeight.value / 100 * s.fontSize : s.lineHeight.value;
const styleFor = (fam, size, w, lh) => styles.find(s => s.fontName.family === fam && s.fontName.style === font(fam, w).style && Math.abs(s.fontSize - size) < .6 && Math.abs(lhOf(s) - lh) < 1.5);
const shadow = (await figma.getLocalEffectStylesAsync()).find(s => s.name === 'Shadow/Dropdown');
const tilt = (n, deg) => { const a = deg * Math.PI / 180, c = Math.cos(a), s = Math.sin(a), x = n.x, y = n.y, w = n.width, h = n.height;
  n.relativeTransform = [[c, -s, x + w / 2 - (c * w / 2 - s * h / 2)], [s, c, y + h / 2 - (s * w / 2 + c * h / 2)]]; };
const [btn, linkIn, linkEx, medal, shield, arrowR, arrowE, team] = await Promise.all(['4:47', '4:63', '4:67', '39:65', '39:71', '4:11', '4:15', '30:190'].map(id => figma.getNodeByIdAsync(id)));
const label = (inst, text) => { const k = Object.keys(inst.componentProperties).find(q => q.startsWith('Label')); if (k) inst.setProperties({[k]: text}); };
const LOGO = '23d9942a4d230088962c3cdfe12c315a9c60c52a';
const made = [];
for (const s of DATA) {
  const f = figma.createFrame(); W.appendChild(f); f.name = s.n; f.resize(s.w, s.h); f.fills = s.bg ? [P(s.bg)] : []; f.clipsContent = true; f.layoutSizingHorizontal = 'FIXED';
  const N = s.nodes;
  for (let i = 0; i < N.length; i++) {
    const n = N[i], next = N[i + 1] || [], after = N[i + 2] || [];
    if (n[0] === 'R' && n[6] === 'pink' && next[0] === 'T') {  // primary button
      const b = btn.createInstance(); f.appendChild(b); label(b, next[5]); b.x = n[1]; b.y = n[2]; i += (after[0] === 'T' && /^[→↗]$/.test(after[5])) ? 2 : 1; continue; }
    if (n[0] === 'R' && next[0] === 'T' && /USA Gymnastics/.test(next[5]) && n[8].every(v => v === 1)) {  // credential badge
      const b = (/judge/i.test(next[5]) ? medal : shield).createInstance(); f.appendChild(b); label(b, next[5]); b.x = n[1]; b.y = n[2]; i += after[0] === 'S' ? 2 : 1; continue; }
    if (n[0] === 'R' && n[8].join() === '0,0,1,0' && next[0] === 'T' && after[0] === 'T' && /^[→↗]$/.test(after[5])) {  // text link
      const b = (after[5] === '↗' ? linkEx : linkIn).createInstance(); f.appendChild(b); label(b, next[5]); b.x = n[1]; b.y = n[2]; i += 2; continue; }
    if (n[0] === 'T') {
      const [, x, y, w, h, text, fam, size, wt, lh, ls, color, al, ul] = n; if (!text.trim()) continue;
      if (/^[→↗]$/.test(text)) { const a = (text === '↗' ? arrowE : arrowR).createInstance(); f.appendChild(a); a.x = x; a.y = y + (h - a.height) / 2; continue; }
      const t = figma.createText(); f.appendChild(t); const st = styleFor(fam, size, wt, lh);
      if (st) await t.setTextStyleIdAsync(st.id); else { t.fontName = font(fam, wt); t.fontSize = size; t.lineHeight = {unit: 'PIXELS', value: lh}; if (ls) t.letterSpacing = {unit: 'PIXELS', value: ls}; }
      t.characters = text; t.fills = [P(color)]; t.textAutoResize = 'HEIGHT'; t.resize(w + 2, h); t.x = x; t.y = y; t.name = text.split('\n')[0].slice(0, 32);
      if (al === 'c') t.textAlignHorizontal = 'CENTER'; if (al === 'r' || al === 'e') t.textAlignHorizontal = 'RIGHT'; if (ul) t.textDecoration = 'UNDERLINE';
    } else if (n[0] === 'R') {
      const [, x, y, w, h, rot, bg, bc, bw, sh, rad, mono] = n; const r = figma.createFrame(); f.appendChild(r);
      r.name = mono ? 'Portrait (monogram until the photo; drop the photo here)' : 'Box'; r.resize(w, h); r.x = x; r.y = y; r.fills = bg ? [P(bg)] : []; r.clipsContent = false;
      if (bc) { r.strokes = [P(bc)]; r.strokeAlign = 'INSIDE'; r.strokeTopWeight = bw[0]; r.strokeRightWeight = bw[1]; r.strokeBottomWeight = bw[2]; r.strokeLeftWeight = bw[3]; }
      if (rad) r.cornerRadius = rad; if (sh) await r.setEffectStyleIdAsync(shadow.id);
      if (mono) { const m = figma.createRectangle(); r.appendChild(m); m.name = 'Monogram'; const mw = w * .34, mh = mw * 632 / 540; m.resize(mw, mh); m.x = (w - mw) / 2; m.y = (h - mh) / 2; m.fills = [{type: 'IMAGE', imageHash: LOGO, scaleMode: 'FIT'}]; }
      if (rot) tilt(r, rot);
    } else if (n[0] === 'S') { const v = figma.createNodeFromSvg(n[6]); f.appendChild(v); v.x = n[1]; v.y = n[2]; v.name = 'Icon'; if (n[5]) tilt(v, n[5]);
    } else if (n[0] === 'K') { const src = team.findOne(q => q.name === 'Kid ' + n[1]); const c = src.clone(); f.appendChild(c); c.rescale(n[5] / c.height); c.x = n[2]; c.y = n[3]; c.name = 'Girl ' + n[1] + ' (footer sprite)';
      for (const v of c.findAll(q => 'fills' in q && Array.isArray(q.fills) && q.fills.length > 0)) v.fills = [P('ink')];
    } else if (n[0] === 'A') { const v = figma.createNodeFromSvg(n[5]); f.appendChild(v); v.x = n[1]; v.y = n[2]; v.name = 'Satin ribbon';
    } else if (n[0] === 'I') { const r = figma.createRectangle(); f.appendChild(r); r.resize(n[3], n[4]); r.x = n[1]; r.y = n[2]; r.fills = [P('placeholder')]; r.name = 'Image ' + n[6]; }
  }
  made.push(`${f.id} ${s.n} ${Math.round(f.height)} nodes=${f.children.length}`);
}
return made;
