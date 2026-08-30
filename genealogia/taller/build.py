# -*- coding: utf-8 -*-
import json, re, unicodedata, pickle

D = json.load(open('assets/08fffc00-d395-438c-88b0-a0545e4c4793.bin', encoding='utf-8'))
blocks = D['blocks']; TOC = D['toc']
pages = json.load(open('mypages.json', encoding='utf-8'))

def blocktext(b):
    if b.get('parts') is not None:
        return ''.join((' ' if p.get('br') else (p.get('x') or '')) for p in b['parts'])
    if b.get('lines'):
        return ' '.join(' '.join(p.get('x') or '' for p in l) for l in b['lines'])
    if b.get('rows'):
        return ' '.join(''.join((' ' if p.get('br') else (p.get('x') or '')) for p in r.get('parts',[])) for r in b['rows'])
    if b.get('title'):
        return b['title'] + (' ' + b['sub'] if b.get('sub') else '')
    return ''

INVIS = {'anchor','cardEnd','pb','rule','orn'}
exp = []   # list of (blockindex, text)
for i,b in enumerate(blocks):
    t = b.get('t')
    if t in INVIS: continue
    if t == 'autotoc':
        for r in TOC:
            exp.append((i, r['label']))
        continue
    s = ''
    if t == 'field':
        s = (b.get('label') or '') + ' ' + blocktext(b)
    elif t == 'fnote':
        lab = b.get('label') or ''
        if lab and not re.search('Nota', lab): lab = lab + ' ·'
        s = lab + ' ' + blocktext(b)
    elif t == 'cardStart':
        s = re.sub(r'\.$','', b.get('label') or 'Ficha de catalogación')
    else:
        s = blocktext(b)
    if s.strip():
        exp.append((i, s))

pickle.dump(exp, open('exp.pkl','wb'))
print('bloques con texto:', len(exp))
print('chars exp:', sum(len(s) for _,s in exp))
