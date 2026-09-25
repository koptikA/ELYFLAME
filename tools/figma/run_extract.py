"""Figma sync: turn a page of the prototype into editable Figma layers.

Needs the preview server (python tools/serve.py) and Playwright. Run from tools/figma/:

    python run_extract.py about/ '#about,#the-sport' about   # -> about-1440.json, about-390.json
    python compact.py about 1440 '#about,#the-sport' g1-1440.json
    python shrink.py g1-1440.json g1-1440.min.json

Then paste `const PAGE = "<page id>", WRAP = "<wrapper id>"; const DATA = <g1-1440.min.json>;` in front of builder.js
and run it with the Figma MCP use_figma tool. builder.js makes one frame per section: texts with the matching text
style, boxes with token colors, Button / Text link / Badge instances where it recognizes them, footer girls cloned
from the footer team (Kid N), and the satin ribbon as SVG. export.js exports the page ribbon or the footer team as a
flat SVG for upload_assets. use_figma accepts 50,000 characters of code: send one section group per call.
The extractor also reads CSS ::after glyphs (the page-index arrow, the audience star, FAQ +/-), input placeholders,
<use> symbols from any sprite (team.svg, split.svg), skips the content of closed <details>, and turns an iframe into an
"Image Google Map" holder: screenshot the map with Playwright and upload it with upload_assets nodeIds. builder.js draws
single-glyph texts (arrows, +, -, the star) as icon instances, since Figma renders the star as a color emoji. A long SVG
(the satin between the Parents steps) can go in with upload_assets first and then be moved into its section.
"""
import json, sys
from playwright.sync_api import sync_playwright

js = open(__import__('os').path.join(__import__('os').path.dirname(__file__), 'extract.js'), encoding='utf-8').read()
page_path = sys.argv[1] if len(sys.argv) > 1 else 'about/'
sels = sys.argv[2].split(',') if len(sys.argv) > 2 else ['#about', '#the-sport', '#our-story', '#coaches', '#the-space', '#achievements', '.about-trial']
tag = sys.argv[3] if len(sys.argv) > 3 else 'about'
with sync_playwright() as p:
    b = p.chromium.launch()
    for w in (1440, 390):
        pg = b.new_page(viewport={'width': w, 'height': 900}, reduced_motion='reduce')
        pg.goto('http://127.0.0.1:4173/' + page_path)
        pg.wait_for_timeout(1500)
        data = {}
        for sel in sels:
            d = pg.evaluate(js, sel)
            data[sel] = d
            print(w, sel, d['w'], d['h'], d['bg'], (d['bgi'] or '')[:50], len(d['nodes']), 'chars', len(json.dumps(d, ensure_ascii=False)))
        json.dump(data, open(f'{tag}-{w}.json', 'w', encoding='utf-8'), ensure_ascii=False)
        pg.close()
    b.close()
