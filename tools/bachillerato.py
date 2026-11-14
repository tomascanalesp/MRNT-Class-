#!/usr/bin/env python3
"""Listas de palabras para el juego «Bachillerato bíblico».

Genera dos archivos que la app carga al abrir el juego:

  bachillerato-dic.txt     Palabras del español (una por línea, sin tildes).
                           Fuente: diccionarios ortográficos libres de
                           LibreOffice es / es_CL (tools/diccionario/*.dic,
                           licencia GPL/LGPL/MPL, ver LICENSE.txt), cuyo
                           lemario sigue al diccionario de la RAE.
  bachillerato-biblia.txt  Vocabulario de la Biblia: cada palabra distinta que
                           aparece (sin tildes). Los nombres propios llevan
                           un «*» delante. Es solo una lista de palabras
                           sueltas y ordenadas, NO el texto bíblico.

Uso:  python3 tools/bachillerato.py
La Biblia se lee de BIBLIA_TXT o biblia/biblia.txt (igual que tools/biblia.py).
Si no está, solo se regenera el diccionario.
"""
import os
import re
import unicodedata
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIBLIA = os.environ.get('BIBLIA_TXT') or os.path.join(ROOT, 'biblia', 'biblia.txt')
DICS = [os.path.join(ROOT, 'tools', 'diccionario', f) for f in ('es.dic', 'es_CL.dic')]


def norm(s):
    """minúsculas, sin tildes (conserva la ñ) y solo letras."""
    s = s.lower().replace('ñ', '\0')
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-zñ]', '', s.replace('\0', 'ñ'))


def diccionario():
    words = set()
    for path in DICS:
        with open(path, encoding='utf-8') as f:
            for line in f:
                w = line.strip().split('/')[0]
                if not w or w[0].isdigit() or not w[0].islower() or not w.isalpha():
                    continue
                n = norm(w)
                if len(n) >= 2:
                    words.add(n)
    return words


def biblia(dic):
    with open(BIBLIA, encoding='utf-8') as f:
        text = f.read()
    lower, mid = Counter(), Counter()
    for m in re.finditer(r'[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+', text):
        w = m.group(0)
        n = norm(w)
        if len(n) < 2 or w.isupper():
            continue
        if w[0].islower():
            lower[n] += 1
        else:
            # Mayúscula en medio de la frase (tras una minúscula o una coma).
            prev = text[max(0, m.start() - 3):m.start()].rstrip(' ')
            if prev and (prev[-1].islower() or prev[-1] == ','):
                mid[n] += 1
    out = set()
    for n, c in lower.items():
        if c >= 2 or n in dic:
            out.add(n)
    for n, c in mid.items():
        # Nombre propio: nunca aparece en minúscula y va con mayúscula a mitad de frase.
        if n not in lower:
            out.add('*' + n)
    return out


def main():
    dic = diccionario()
    with open(os.path.join(ROOT, 'bachillerato-dic.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(sorted(dic)) + '\n')
    print('bachillerato-dic.txt:', len(dic), 'palabras')
    if os.path.exists(BIBLIA):
        bib = biblia(dic)
        with open(os.path.join(ROOT, 'bachillerato-biblia.txt'), 'w', encoding='utf-8') as f:
            f.write('\n'.join(sorted(bib, key=lambda w: w.lstrip('*'))) + '\n')
        print('bachillerato-biblia.txt:', len(bib), 'palabras,', sum(w[0] == '*' for w in bib), 'nombres propios')
    else:
        print('Sin', BIBLIA, '— no se regeneró bachillerato-biblia.txt')


if __name__ == '__main__':
    main()
