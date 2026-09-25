# Footer team: responsive layout

For Ivan, September 25, 2026. This note covers the "team" at the bottom of the footer: `.footer-team`, `layoutTeam()` in `site.js`, and the sprite `assets/gymnast/team.svg`. Until September 25 the prototype used two fixed steps; now it follows the rule below, and the reference code is the prototype's `layoutTeam()`. Checked at 320–1920 px: no console errors, no horizontal scroll.

## What was wrong

Up to 760 px the row had 6 girls, 120 px tall. Above 760 px it had 12 girls, 240 px tall. The space between girls is the container width minus the girls, split evenly, so it went negative when they didn't fit:

| Viewport | Container | Girls | Overlap |
|---|---|---|---|
| 320 px | 282 px | 6 | 8 px |
| 600–760 px | 528–669 px | 6 | none, but the row looks sparse |
| 800 px | 704 px | 12 | 55 px |
| 1024 px | 901 px | 12 | 37 px |
| 1280 px | 1126 px | 12 | 16 px |
| 1440 px | 1267 px | 12 | 4 px |

Overlap is the largest overlap between neighboring sprite boxes. On tablets and small laptops, the girls stood on top of each other.

## The rule

`W` is the content width of `.footer-team`.

1. **Height follows width:** `kidH = clamp(120, 0.19 × W, 240)` px. It reaches 240 px at `W` ≈ 1263 px (a 1440 px viewport), so the desktop from 1440 px up looks the same as now.
2. **Equal cells:** every girl gets a cell of the same width, at least `0.42 × kidH`, and stands centered in it, feet on the floor. So the count is `n = floor((W − 2 × pad) / (0.42 × kidH))`, from 4 to 12, and the cell is `(W − 2 × pad) / n`. Girls differ in width (a hoop or a raised arm makes a sprite wider), so equal cells, not equal gaps, keep the rhythm even. At most an arm or an apparatus reaches into the next cell.
3. **Which girls:** the first `n` in priority order `12, 6, 1, 3, 10, 5, 7, 2, 8, 11, 4, 9`.
4. **Order, left to right:** `12, 1, 3, 7, 10, 2, 5, 8, 11, 4, 9, 6`, keeping only the chosen girls. Girl 12 always stands far left and girl 6 far right: they hold the sticks the ribbon hangs from.
5. **Side padding:** `pad = kidH / 20` on each side.
6. **Ribbon:** it runs from the tip of girl 6's stick to the tip of girl 12's, waving above the heads through the middle girls' centers, alternating between `top / 2 + amp` and `top / 2 − 0.4 × amp`. The band above the heads is `top = 0.15 × kidH`, the wave is `amp = 0.075 × kidH`, and the SVG height is `kidH + top + 4`.

What this gives:

| Viewport | Girl height | Girls |
|---|---|---|
| 320 px | 120 px | 5 |
| 390 px | 120 px | 6, the same set as now |
| 430 px | 120 px | 7 |
| 600 px | 120 px | 10 |
| 760–1280 px | 127–214 px | 12 |
| 1440 px and up | 240 px | 12, as now |

## What stays the same

- The sprite `assets/gymnast/team.svg` with symbols `kid-1` … `kid-12`. All girls share one scale (745 units is the tallest girl), and each symbol's bottom edge is the floor. Widths, heights, and stick tips are in `KIDS` in `site.js`.
- The satin ribbon (`paintSatin()`, the thin version up to 760 px), the reveal mask, and the scroll animation: the girls rise in one by one and the ribbon draws from right to left. With "reduce motion" on, the row is static.
- The block is decorative (`aria-hidden="true"`) and is laid out again on resize.

## Reference code

The same as `layoutTeam()` in `site.js`.

```js
const TEAM_PRIORITY=[12,6,1,3,10,5,7,2,8,11,4,9],TEAM_ORDER=[12,1,3,7,10,2,5,8,11,4,9,6];
function layoutTeam(){
  if(!team)return;
  const W=team.clientWidth,mobile=innerWidth<=760;
  const kidH=Math.min(240,Math.max(120,.19*W)),sc=kidH/745,pad=kidH/20;
  // Equal cells, at least 0.42 of a girl's height wide: as many as fit (4–12), each girl centred in hers.
  // The two holding sticks always stand at the ends.
  const n=Math.max(4,Math.min(12,Math.floor((W-2*pad)/(.42*kidH)))),cell=(W-2*pad)/n;
  const order=TEAM_PRIORITY.slice(0,n).sort((a,b)=>TEAM_ORDER.indexOf(a)-TEAM_ORDER.indexOf(b));
  const top=.15*kidH,H=kidH+top+4,floor=H-2,amp=.075*kidH;
  const kids=order.map((k,i)=>{const[w,h,tx,ty]=KIDS[k],x=pad+i*cell+(cell-w*sc)/2;return{k,x,y:floor-h*sc,w:w*sc,h:h*sc,tip:tx===undefined?null:[x+tx*sc,floor-h*sc+ty*sc]};});
  const tipL=kids[0].tip,tipR=kids[kids.length-1].tip;
  // Through-points right to left: a wave above the heads, dipping in the gaps between the girls.
  const P=[tipR];
  for(let i=kids.length-2;i>=1;i--){const k=kids[i];P.push([k.x+k.w/2,top*.5+(i%2?amp:-amp*.4)]);}
  P.push(tipL);
  let d=`M ${P[0][0].toFixed(1)} ${P[0][1].toFixed(1)}`;
  for(let i=0;i<P.length-1;i++){const a=P[Math.max(0,i-1)],b=P[i],c=P[i+1],e=P[Math.min(P.length-1,i+2)];
    d+=` C ${(b[0]+(c[0]-a[0])/6).toFixed(1)} ${(b[1]+(c[1]-a[1])/6).toFixed(1)} ${(c[0]-(e[0]-b[0])/6).toFixed(1)} ${(c[1]-(e[1]-b[1])/6).toFixed(1)} ${c[0].toFixed(1)} ${c[1].toFixed(1)}`;}
  team.innerHTML=`<svg class="team" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" aria-hidden="true" focusable="false">
    <defs><mask id="team-reveal" maskUnits="userSpaceOnUse" x="-80" y="-80" width="${W+160}" height="${H+160}"><path class="team-reveal" pathLength="1" d="${d}"/></mask></defs>
    ${kids.map((k,i)=>`<use class="team-kid" href="assets/gymnast/team.svg#kid-${k.k}" x="${k.x.toFixed(1)}" y="${k.y.toFixed(1)}" width="${k.w.toFixed(1)}" height="${k.h.toFixed(1)}" style="animation-range:entry ${10+i*4}% entry ${45+i*4}%"/>`).join('')}
    <g class="team-ribbon" mask="url(#team-reveal)"></g></svg>`;
  paintSatin(team.querySelector('.team-ribbon'),d,mobile,false);
}```

## How to check

- At every width from 320 to 1920 px, no girl covers another girl's body. At most an arm or an apparatus touches a neighbor.
- Both ribbon ends sit on the stick tips.
- No horizontal scroll. The footer's height follows the row: about 142 px for the row on phones and 280 px on desktop.
- The same footer is on `/ru/` and `/uk/`; check them too.

## Figma

The Figma file shows two states of the row: Desktop with 12 girls and Mobile with 6. Figma can't change the count by width, so for widths in between, the rule above is the source of truth.
