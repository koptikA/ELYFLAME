import json, re, sys
d = json.load(open(sys.argv[1], encoding='utf-8'))
for s in d:
    for n in s['nodes']:
        if n[0] == 'S':
            n[6] = re.sub(r' (opacity|fill-rule|stroke-linecap|stroke-linejoin)="[^"]*"', '', n[6])
            n[6] = n[6].replace(' fill="none" stroke="rgb(203, 119, 77)" stroke-width="1.4px"/>', '/>')
        if n[0] == 'A':
            n[5] = re.sub(r' (opacity)="1"', '', n[5])
open(sys.argv[2], 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, separators=(',', ':')))
