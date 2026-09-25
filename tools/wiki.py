"""Builds paste-ready HTML for the Kirakito wiki (WordPress, page "ElyFlame RG") from the English docs.

    python -m pip install markdown   # once
    python tools/wiki.py                 # full pages
    python tools/wiki.py --since b5fa189 # add-on pages: only what is new or changed since that commit

Writes outputs/wiki/<n>-<name>.html (gitignored). The first "# Title" line is dropped: it becomes the WordPress page
title. Paste each file into a Custom HTML block, or open it in a browser and copy the rendered text into the editor.

A page nobody has read yet is simply replaced with a fresh full build. Once the team has read it, it stays as it is (it is the
record of what was sent), so later changes go on add-on pages.
--since compares each doc with the given commit, block by block (a numbered or bulleted item, a table row, a paragraph),
and keeps the new or changed blocks under their section headings; table rows keep the table header. Docs with no
changes get no page.
"""
import io
import os
import re
import subprocess
import sys

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


def blocks(text):
    """Split markdown into (section heading, block) pairs; a block is a list item with its continuation lines,
    a table row, or a paragraph."""
    out, heading, cur = [], '', []

    def flush():
        if cur:
            out.append((heading, '\n'.join(cur).strip()))
            cur.clear()
    for line in text.split('\n'):
        if re.match(r'#{1,6} ', line):
            flush(); heading = line; continue
        if not line.strip():
            flush(); continue
        if re.match(r'(\d+\.|-|\*) ', line) or line.startswith('|'):
            flush()
        cur.append(line)
    flush()
    return out


def changes(old, new):
    """Markdown with only the blocks of `new` that are not in `old`, under their headings."""
    seen = {b for _, b in blocks(old)}
    parts, last, table_head = [], None, {}
    for heading, b in blocks(new):
        if b.startswith('|') and re.match(r'\|[\s:-]+\|', b):
            continue
        if b.startswith('|') and heading not in table_head:
            table_head[heading] = b  # the first row of a section's table is its header
            continue
        if b in seen:
            continue
        if heading != last:
            parts.append(heading)
            last = heading
            if b.startswith('|') and heading in table_head:
                cols = table_head[heading].count('|') - 1
                parts.append(table_head[heading] + '\n|' + ' --- |' * cols)
        parts.append(b)
    md, prev = '', ''
    for p in parts:  # table rows must stay on consecutive lines
        if md:
            md += '\n' if p.startswith('|') and prev.startswith('|') else '\n\n'
        md += p
        prev = p.split('\n')[-1]
    return md


def render(text):
    text = re.sub(r'\A# .*\n+', '', text)
    # Nested lists in the docs are indented by 2 spaces; Python-Markdown wants 4.
    text = re.sub(r'(?m)^ {2}(?=(?:\d+\.|-) )', '    ', text)
    return markdown.markdown(text, extensions=['tables', 'fenced_code', 'sane_lists'])


since = sys.argv[sys.argv.index('--since') + 1] if '--since' in sys.argv else None
out_dir = os.path.join(ROOT, 'outputs', 'wiki')
os.makedirs(out_dir, exist_ok=True)
for name, src in PAGES:
    text = io.open(os.path.join(ROOT, src), encoding='utf-8').read()
    if since:
        old = subprocess.run(['git', 'show', f'{since}:{src}'], cwd=ROOT, capture_output=True, encoding='utf-8').stdout
        text = changes(old, re.sub(r'\A# .*\n+', '', text))
        if not text.strip():
            continue
        text = f'Changes since the published version (commit {since}): new and changed items only.\n\n' + text
        name = f'{name}-update-since-{since}'
    io.open(os.path.join(out_dir, name + '.html'), 'w', encoding='utf-8', newline='\n').write(render(text) + '\n')
    print(f'{name}.html  <-  {src}')
