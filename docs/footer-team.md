# «Команда» в подвале: адаптивная раскладка

Для Ивана, 25 сентября 2026. Заметка про «команду» внизу подвала: `.footer-team`, `layoutTeam()` в `site.js`, спрайт `assets/gymnast/team.svg`. До 25 сентября в прототипе были две фиксированные ступени, теперь он работает по правилу ниже, а код для образца — это `layoutTeam()` из прототипа. Проверено на 320–1920 px: без ошибок в консоли и горизонтального скролла.

## Что было не так

До 760 px в ряду было 6 девочек высотой 120 px, шире — 12 девочек высотой 240 px. Расстояние между девочками — ширина контейнера минус девочки, поделённая поровну. Когда девочки не помещались, оно уходило в минус:

| Экран | Контейнер | Девочек | Наложение |
|---|---|---|---|
| 320 px | 282 px | 6 | 8 px |
| 600–760 px | 528–669 px | 6 | нет, но ряд выглядит пустым |
| 800 px | 704 px | 12 | 55 px |
| 1024 px | 901 px | 12 | 37 px |
| 1280 px | 1126 px | 12 | 16 px |
| 1440 px | 1267 px | 12 | 4 px |

Наложение — наибольшее перекрытие соседних рамок спрайта. На планшетах и небольших ноутбуках девочки стояли друг на друге.

## Правило

`W` — ширина содержимого `.footer-team`.

1. **Рост зависит от ширины:** `kidH = clamp(120, 0.19 × W, 240)` px. 240 px получается при `W` ≈ 1263 px (экран 1440 px), так что десктоп от 1440 px выглядит как сейчас.
2. **Одинаковые ячейки:** у каждой девочки ячейка одной ширины, не меньше `0.42 × kidH`, девочка стоит в ней по центру, ногами на полу. Отсюда число девочек `n = floor((W − 2 × pad) / (0.42 × kidH))`, от 4 до 12, а ширина ячейки `(W − 2 × pad) / n`. Девочки разной ширины (обруч или поднятая рука делают спрайт шире), поэтому ровный ритм дают одинаковые ячейки, а не одинаковые промежутки. В соседнюю ячейку заходит максимум рука или предмет.
3. **Какие девочки:** первые `n` в порядке приоритета `12, 6, 1, 3, 10, 5, 7, 2, 8, 11, 4, 9`.
4. **Порядок слева направо:** `12, 1, 3, 7, 10, 2, 5, 8, 11, 4, 9, 6`, из него остаются только выбранные девочки. Девочка 12 всегда крайняя слева, 6 — крайняя справа: у них палочки, на которых держится лента.
5. **Боковые отступы:** `pad = kidH / 20` с каждой стороны.
6. **Лента:** идёт от кончика палочки девочки 6 к кончику палочки девочки 12 волной над головами через центры средних девочек, попеременно на высоте `top / 2 + amp` и `top / 2 − 0.4 × amp`. Полоса над головами `top = 0.15 × kidH`, размах волны `amp = 0.075 × kidH`, высота SVG `kidH + top + 4`.

Что получается:

| Экран | Рост девочек | Девочек |
|---|---|---|
| 320 px | 120 px | 5 |
| 390 px | 120 px | 6, тот же набор, что сейчас |
| 430 px | 120 px | 7 |
| 600 px | 120 px | 10 |
| 760–1280 px | 127–214 px | 12 |
| от 1440 px | 240 px | 12, как сейчас |

## Что не меняется

- Спрайт `assets/gymnast/team.svg` с символами `kid-1` … `kid-12`. У всех девочек общий масштаб (745 единиц — самая высокая), нижний край символа — пол. Ширины, высоты и кончики палочек — в `KIDS` в `site.js`.
- Атласная лента (`paintSatin()`, тонкий вариант до 760 px), маска проявления и анимация при прокрутке: девочки по очереди поднимаются, лента прорисовывается справа налево. При включённом «уменьшении движения» ряд статичный.
- Блок декоративный (`aria-hidden="true"`) и пересобирается при изменении размера окна.

## Код для образца

То же, что `layoutTeam()` в `site.js`.

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

## Как проверить

- На любой ширине от 320 до 1920 px ни одна девочка не закрывает тело соседки. Касаться могут только рука или предмет.
- Оба конца ленты — на кончиках палочек.
- Нет горизонтального скролла. Высота подвала меняется вместе с рядом: ряд около 142 px на телефоне и 280 px на десктопе.
- Тот же подвал на `/ru/` и `/uk/` — проверить и там.

## Figma

В Figma у ряда два состояния: Desktop с 12 девочками и Mobile с 6. Менять число девочек по ширине Figma не умеет, поэтому для промежуточных ширин источник правды — правило выше.
