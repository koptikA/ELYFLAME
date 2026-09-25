# Footer team: responsive layout

For Ivan, September 25, 2026. This note covers the "team" at the bottom of the footer: `.footer-team`, `layoutTeam()` in `site.js`, and the sprite `assets/gymnast/team.svg`. The prototype still uses two fixed steps. Below is the target layout for production. I checked it in the browser by swapping in the reference code from this note: 320–1920 px, no console errors, no horizontal scroll.

## What's wrong now

Up to 760 px the row has 6 girls, 120 px tall. Above 760 px it has 12 girls, 240 px tall. The space between girls is the container width minus the girls, split evenly, so it goes negative when they don't fit:

| Viewport | Container | Girls | Overlap |
|---|---|---|---|
| 320 px | 282 px | 6 | 8 px |
| 600–760 px | 528–669 px | 6 | none, but the row looks sparse |
| 800 px | 704 px | 12 | 55 px |
| 1024 px | 901 px | 12 | 37 px |
| 1280 px | 1126 px | 12 | 16 px |
| 1440 px | 1267 px | 12 | 4 px |

Overlap is the largest overlap between neighboring sprite boxes. On tablets and small laptops, the girls stand on top of each other.

## Target rule

`W` is the content width of `.footer-team`.

1. **Height follows width:** `kidH = clamp(120, 0.19 × W, 240)` px. It reaches 240 px at `W` ≈ 1263 px (a 1440 px viewport), so the desktop from 1440 px up looks the same as now.
2. **Count:** as many girls as fit, from 4 to 12. Take them in priority order `12, 6, 1, 3, 10, 5, 7, 2, 8, 11, 4, 9` and pick the largest `n` where the sum of their widths + `2 × pad` − `(n − 1) × 0.035 × kidH` ≤ `W`. Neighbors may overlap by up to 3.5% of `kidH`: the sprite boxes include empty space around arms and apparatus, so at most an arm or a hoop touches the next girl.
3. **Order, left to right:** `12, 1, 3, 7, 10, 2, 5, 8, 11, 4, 9, 6`, keeping only the chosen girls. Girl 12 always stands far left and girl 6 far right: they hold the sticks the ribbon hangs from.
4. **Spacing:** `pad = kidH / 20` on each side. The remaining space is split evenly between the girls.
5. **Ribbon:** it runs from the tip of girl 6's stick to the tip of girl 12's, waving above the heads through the middle girls' centers, alternating between `top / 2 + amp` and `top / 2 − 0.4 × amp`. The band above the heads is `top = 0.15 × kidH`, the wave is `amp = 0.075 × kidH`, and the SVG height is `kidH + top + 4`.

What this gives:

| Viewport | Girl height | Girls |
|---|---|---|
| 320 px | 120 px | 5 |
| 390 px | 120 px | 6, the same set as now |
| 430 px | 120 px | 7 |
| 600 px | 120 px | 9 |
| 760–1280 px | 127–214 px | 12 |
| 1440 px and up | 240 px | 12, as now |

## What stays the same

- The sprite `assets/gymnast/team.svg` with symbols `kid-1` … `kid-12`. All girls share one scale (745 units is the tallest girl), and each symbol's bottom edge is the floor. Widths, heights, and stick tips are in `KIDS` in `site.js`.
- The satin ribbon (`paintSatin()`, the thin version up to 760 px), the reveal mask, and the scroll animation: the girls rise in one by one and the ribbon draws from right to left. With "reduce motion" on, the row is static.
- The block is decorative (`aria-hidden="true"`) and is laid out again on resize.

## Reference code

A drop-in replacement for `layoutTeam()` in `site.js`. Everything after the ribbon's through-points is unchanged.

```js
const TEAM_PRIORITY=[12,6,1,3,10,5,7,2,8,11,4,9],TEAM_ORDER=[12,1,3,7,10,2,5,8,11,4,9,6];
function layoutTeam(){
  if(!team)return;
  const W=team.clientWidth,mobile=innerWidth<=760;
  const kidH=Math.min(240,Math.max(120,.19*W)),sc=kidH/745,pad=kidH/20,overlap=.035*kidH;
  // As many girls as fit (4–12); the two holding sticks always stand at the ends.
  let n=4;
  for(let m=4;m<=12;m++)if(TEAM_PRIORITY.slice(0,m).reduce((a,k)=>a+KIDS[k][0]*sc,0)+2*pad-(m-1)*overlap<=W)n=m;
  const order=TEAM_PRIORITY.slice(0,n).sort((a,b)=>TEAM_ORDER.indexOf(a)-TEAM_ORDER.indexOf(b));
  const top=.15*kidH,H=kidH+top+4,floor=H-2,amp=.075*kidH;
  const widths=order.map(k=>KIDS[k][0]*sc),gap=(W-2*pad-widths.reduce((a,b)=>a+b,0))/(order.length-1);
  let x=pad;const kids=order.map(k=>{const[w,h,tx,ty]=KIDS[k],kid={k,x,y:floor-h*sc,w:w*sc,h:h*sc,tip:tx===undefined?null:[x+tx*sc,floor-h*sc+ty*sc]};x+=w*sc+gap;return kid;});
  const tipL=kids[0].tip,tipR=kids[kids.length-1].tip;
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
}
```

## How to check

- At every width from 320 to 1920 px, no girl covers another girl's body. At most an arm or an apparatus touches a neighbor.
- Both ribbon ends sit on the stick tips.
- No horizontal scroll. The footer's height follows the row: about 142 px for the row on phones and 280 px on desktop.
- The same footer is on `/ru/` and `/uk/`; check them too.

## Figma

The Figma file shows two states of the row: Desktop with 12 girls and Mobile with 6. Figma can't change the count by width, so for widths in between, the rule above is the source of truth.
