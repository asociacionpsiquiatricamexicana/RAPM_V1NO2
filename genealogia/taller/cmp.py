# -*- coding: utf-8 -*-
import json, re, pickle, unicodedata, difflib, os

pages = json.load(open('mypages.json', encoding='utf-8'))
idx   = json.load(open('indice_final.json', encoding='utf-8'))['pages']
exp   = pickle.load(open('exp.pkl','rb'))

def clean_page(i):
    # U+FFFE marca el punto de guionizacion suave que produjo un salto de
    # linea visible (silabas() en bookstyle_extraido.js); para comparar
    # contra el texto esperado (sin guionizar) se reune la palabra quitando
    # la marca, en vez de dejar un guion literal que rompe el token en dos.
    t = pages[i].replace('￾', '')
    L = [l for l in t.replace('\r\n','\n').split('\n') if l.strip()]
    meta = idx[i]
    if not meta['bleed']:
        if L: L = L[1:]                       # cornisa
        if L and meta.get('impreso'):
            # folio al pie
            if L and re.fullmatch(r'[ivxlcdm]+|\d+', L[-1].strip(), re.I):
                L = L[:-1]
    return L

act_tok = []   # (page, token)
for i in range(len(pages)):
    for l in clean_page(i):
        for w in l.split():
            act_tok.append((i, w))

exp_tok = []
for bi, s in exp:
    for w in s.split():
        exp_tok.append((bi, w))

def norm(w):
    w = unicodedata.normalize('NFC', w)
    w = w.replace('’',"'").replace('–','-').replace('—','-')
    return w

A = [norm(w) for _,w in exp_tok]
B = [norm(w) for _,w in act_tok]
print('exp tokens', len(A), 'act tokens', len(B))

sm = difflib.SequenceMatcher(a=A, b=B, autojunk=False)
ops = sm.get_opcodes()
pickle.dump((exp_tok, act_tok, A, B, ops), open('align.pkl','wb'))
tot=0
for tag,i1,i2,j1,j2 in ops:
    if tag=='equal': continue
    tot+=1
print('opcodes no iguales:', tot)

# La cifra anclada. La norma del proyecto dice que este numero es la senal
# —si sube tras un cambio que debia ser solo visual, algo se movio que no
# debia—, pero hasta ahora no habia contra que compararlo: habia que recordar
# la cifra de la tanda anterior. Aqui queda escrita, y la comparacion se hace
# sola. Al cerrar una tanda que la mueva legitimamente, se actualiza el
# archivo y se dice en el registro por que se movio.
REF = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cmp_referencia.txt')
esperado = None
if os.path.exists(REF):
    for linea in open(REF, encoding='utf-8'):
        linea = linea.split('#')[0].strip()
        if linea.isdigit():
            esperado = int(linea); break

if esperado is None:
    print(f'  (sin cifra anclada: escribe {tot} en cmp_referencia.txt para anclarla)')
elif tot == esperado:
    print(f'  cuadra con la cifra anclada ({esperado})')
elif tot < esperado:
    print(f'  BAJA: {esperado} -> {tot}. Se cerraron {esperado - tot} diferencias;')
    print('  si era lo buscado, actualiza cmp_referencia.txt al cerrar la tanda.')
else:
    print(f'  SUBE: {esperado} -> {tot}. Aparecieron {tot - esperado} diferencias nuevas.')
    print('  Si el cambio debia ser solo visual, algo se movio que no debia.')
    print('  Las diferencias van listadas abajo; busca las que no reconozcas.')
for tag,i1,i2,j1,j2 in ops:
    if tag=='equal': continue
    print('---', tag, 'bloq', exp_tok[i1][0] if i1<len(exp_tok) else '?', 'pag', act_tok[j1][0] if j1<len(act_tok) else '?')
    print('  EXP:', ' '.join(A[max(0,i1-6):i1]), '<<<', ' '.join(A[i1:i2])[:300], '>>>', ' '.join(A[i2:i2+6]))
    print('  ACT:', ' '.join(B[max(0,j1-6):j1]), '<<<', ' '.join(B[j1:j2])[:300], '>>>', ' '.join(B[j2:j2+6]))
