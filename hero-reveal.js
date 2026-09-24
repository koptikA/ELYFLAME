// Hero entrance, once per load: the headline rises letter by letter (Serega Gentle), "fire." lands with a spring
// (Serega Emotional) as the gymnast's leg reaches the top, then the copy and the button follow.
// Both libraries render static text when the visitor prefers reduced motion. After each reveal, stop() puts plain text
// back, so browser translation sees words instead of single letters.
import { seregaGentle } from './lib/serega-gentle.js'
import { seregaEmotional } from './lib/serega-emotional.js'

const hero = document.querySelector('.hero')
const lines = [...hero.querySelectorAll('[data-reveal]')]
const accent = hero.querySelector('[data-reveal-accent]')
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
  let delay = 150
  for (const line of lines) {
    // Show the host only when its letters are rendered, so the plain text never flashes first.
    setTimeout(() => { show(line); const c = seregaGentle(line); c.finished.then(() => c.stop()) }, delay)
    delay += line.textContent.length * 15 + 120
  }
  setTimeout(() => { show(accent); const c = seregaEmotional(accent); c.finished.then(() => c.stop()) }, 950)
  setTimeout(() => hero.classList.add('is-in'), 1300)
})
