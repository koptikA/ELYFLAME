// Hero entrance, once per load: the headline rises letter by letter (Serega Gentle), "fire." lands with a spring
// (Serega Emotional) as the gymnast's leg reaches the top, then the copy and the button follow.
// Both libraries render static text when the visitor prefers reduced motion. Browser translation would translate the split
// letters one by one, so the headline is translate="no" while it animates; afterwards stop() writes plain text back and the
// translator picks up the whole words.
import { seregaGentle } from './lib/serega-gentle.js'
import { seregaEmotional } from './lib/serega-emotional.js'

const hero = document.querySelector('.hero')
const lines = [...hero.querySelectorAll('[data-reveal]')]
const accent = hero.querySelector('[data-reveal-accent]')
const title = hero.querySelector('h1')
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches
const show = el => { el.style.opacity = '1' }

document.fonts.ready.then(() => {
  // The gymnast's leg starts with the headline, so "fire." lands as the leg reaches the top.
  document.documentElement.classList.add('play')
  if (reduced) {
    for (const el of [...lines, accent]) show(el)
    hero.classList.add('is-in')
    return
  }
  // Show the host only when its letters are rendered, so the plain text never flashes first.
  const reveal = (el, effect, at) => new Promise(done => setTimeout(() => { show(el); const c = effect(el); c.finished.then(() => done(c)) }, at))
  title.translate = false
  let delay = 150
  const runs = lines.map(line => { const run = reveal(line, seregaGentle, delay); delay += line.textContent.length * 15 + 120; return run })
  runs.push(reveal(accent, seregaEmotional, 950))
  Promise.all(runs).then(all => { title.removeAttribute('translate'); for (const c of all) c.stop() })
  setTimeout(() => hero.classList.add('is-in'), 1300)
})
