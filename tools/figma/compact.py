import json, sys

tag, width, sels = sys.argv[1], sys.argv[2], sys.argv[3].split(',')
data = json.load(open(f'{tag}-{width}.json', encoding='utf-8'))
r = lambda v: round(v) if abs(v - round(v)) < .05 else round(v, 1)


def color(c):
    if not c:
        return None
    if c['token']:
        return c['token'] if c['a'] == 1 else [c['token'], c['a']]
    return [c['hex'], c['a']]


out = []
for sel in sels:
    d = data[sel]
    nodes = []
    for n in d['nodes']:
        box = [r(n['x']), r(n['y']), r(n['w']), r(n['h'])]
        if n['t'] == 'text':
            nodes.append(['T', *box, n['text'], n['fam'], r(n['size']), n['weight'], r(n['lh'] or n['size'] * 1.2), r(n['ls']), color(n['color']),
                          n['align'][0] if n['align'] in ('center', 'right', 'end') else 0, 1 if 'underline' in n['deco'] else 0])
        elif n['t'] == 'rect':
            nodes.append(['R', *box, r(n['rot']), color(n['bg']), color(n['bc']), n['bw'], 1 if n['shadow'] else 0, r(n['radius']), 1 if n['mono'] else 0])
        elif n['t'] == 'svg':
            nodes.append(['S', *box, r(n['rot']), n['svg']])
        elif n['t'] == 'kid':
            nodes.append(['K', n['k'], *box])
            if n.get('satinSvg'):
                s = n['satin']
                nodes.append(['A', r(s['x']), r(s['y']), r(s['w']), r(s['h']), n['satinSvg']])
        elif n['t'] == 'img':
            nodes.append(['I', *box, r(n['rot']), n['src']])
    out.append({'n': sel.lstrip('#.'), 'w': r(d['w']), 'h': r(d['h']), 'bg': color(d['bg']), 'nodes': nodes})
s = json.dumps(out, ensure_ascii=False, separators=(',', ':'))
open(sys.argv[4] if len(sys.argv) > 4 else f'c-{tag}-{width}.json', 'w', encoding='utf-8').write(s)
print(len(s))
