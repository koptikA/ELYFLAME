"""Builds paste-ready HTML for the Kirakito wiki (WordPress, page "ElyFlame RG") from the English docs.

    python -m pip install markdown   # once
    python tools/wiki.py

Writes outputs/wiki/<n>-<name>.html (gitignored). The first "# Title" line is dropped: it becomes the WordPress page
title. Paste each file into a Custom HTML block, or open it in a browser and copy the rendered text into the editor.
"""
import io
import os
import re

import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = [
    ('1-brief', 'outputs/brief.en.md'),
    ('2-competitive-research', 'outputs/research.en.md'),
    ('3-prd', 'outputs/prd.en.md'),
    ('4-questions', 'docs/client-questions.en.md'),
    ('5-how-the-site-works', 'docs/behavior-spec.en.md'),
    ('6-photos-and-video', 'docs/photos.en.md'),
    ('7-footer-team-layout', 'docs/footer-team.en.md'),
    ('8-decision-log', 'docs/decisions.en.md'),
]

out_dir = os.path.join(ROOT, 'outputs', 'wiki')
os.makedirs(out_dir, exist_ok=True)
for name, src in PAGES:
    text = io.open(os.path.join(ROOT, src), encoding='utf-8').read()
    text = re.sub(r'\A# .*\n+', '', text)
    # Nested lists in the docs are indented by 2 spaces; Python-Markdown wants 4.
    text = re.sub(r'(?m)^ {2}(?=(?:\d+\.|-) )', '    ', text)
    html = markdown.markdown(text, extensions=['tables', 'fenced_code', 'sane_lists'])
    io.open(os.path.join(out_dir, name + '.html'), 'w', encoding='utf-8', newline='\n').write(html + '\n')
    print(f'{name}.html  <-  {src}')
