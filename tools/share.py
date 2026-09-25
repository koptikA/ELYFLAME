"""Copy only the public site into outputs/share/ for Netlify Drop (drag the folder to app.netlify.com/drop).

Never tunnel tools/serve.py to the client: it serves the whole repo, including docs/ (the SOW) and .git/.
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'outputs' / 'share'
FILES = ['index.html', 'site.css', 'site.js', 'hero-reveal.js']
DIRS = ['lib', 'assets', 'about', 'stretching', 'contact', 'parents', 'ru', 'uk']
# Source sheets and originals stay private; the pages only load the traced SVGs and processed files.
SKIP = shutil.ignore_patterns('originals', 'source', 'sheet-2.jpg', 'team-sheet.jpg', 'split.jpg')

shutil.rmtree(OUT, ignore_errors=True)
OUT.mkdir(parents=True)
for name in FILES:
    shutil.copy2(ROOT / name, OUT / name)
for name in DIRS:
    shutil.copytree(ROOT / name, OUT / name, ignore=SKIP)
size = sum(p.stat().st_size for p in OUT.rglob('*') if p.is_file())
print(f'{OUT} ready: {size / 1e6:.1f} MB')
