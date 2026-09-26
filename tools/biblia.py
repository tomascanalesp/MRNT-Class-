#!/usr/bin/env python3
"""Versículos de la Biblia para las presentaciones del repaso.

El texto bíblico NO está en el repositorio (el repo es público y la NVI
tiene derechos de autor). Este script lee la Biblia completa desde un
archivo local y copia en `index.html` solo los pasajes que usan las
presentaciones (constante BIBLE_VERSES), para que se abran sin internet.

Archivo de la Biblia (texto plano exportado del PDF NVI):
  - variable de entorno BIBLIA_TXT, o
  - biblia/biblia.txt  (ignorado por git)

Uso:
  python3 tools/biblia.py actualizar        # regenera BIBLE_VERSES en index.html
  python3 tools/biblia.py "Juan 3:16"       # muestra un pasaje
  python3 tools/biblia.py "Juan 14:1, 11; 15:10-14"

Referencias aceptadas: "Libro c:v", "c:v-w", "c:v, w", "c:v; c2:w",
"c:v-c2:w" (varios capítulos, se numeran "c:v") y "Libro c" (capítulo
completo). Las claves de BIBLE_VERSES son la referencia EXACTA escrita
en el array `verses` de cada slide.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, 'index.html')
BIBLIA = os.environ.get('BIBLIA_TXT') or os.path.join(ROOT, 'biblia', 'biblia.txt')

# Referencias de capítulo/rango amplio que no abren el modal a propósito.
SKIP = {'Mateo 5–7', 'Mateo 7'}

_BOOKS = None


def _load():
    """Divide el texto en {LIBRO: {capítulo: [líneas]}}."""
    global _BOOKS
    if _BOOKS is not None:
        return _BOOKS
    if not os.path.exists(BIBLIA):
        sys.exit(f'No encuentro la Biblia en {BIBLIA}. Copia el .txt ahí o define BIBLIA_TXT.')
    lines = open(BIBLIA, encoding='utf-8').read().replace('\r', '').split('\n')
    hdr = re.compile(r'^((?:[123] )?[A-ZÁÉÍÓÚÑ ]+?) (\d+)(?:\[\d+\])?$')
    books, cur, buf, notes = {}, None, [], False
    for line in lines:
        s = line.strip()
        m = hdr.match(s)
        if m and m.group(1) != 'A':
            if cur:
                books.setdefault(cur[0], {})[cur[1]] = buf
            cur, buf, notes = (m.group(1), int(m.group(2))), [], False
            continue
        if cur is None or not s or s.startswith('Made with Xodo'):
            continue
        # Al final de cada libro vienen las notas al pie: se ignoran.
        if re.search(r'\| \| (Antiguo|Nuevo) Testamento', s) or s.startswith('[VOLVER'):
            notes = True
        if not notes:
            buf.append(s)
    if cur:
        books.setdefault(cur[0], {})[cur[1]] = buf
    _BOOKS = books
    return books


def verses_of(book, ch):
    """{número: texto} de un capítulo, sin títulos, notas ni asteriscos."""
    ls = [re.sub(r'\[\d+\]', '', x).replace('*', '').strip() for x in _load()[book][ch]]
    xref = lambda x: re.match(r'^\d+:\d+.*—', x)  # "5:25–26 — Lc 12:58–59"
    # Fuera las líneas de pasajes paralelos y el título que las precede.
    ls = [x for j, x in enumerate(ls) if x and not xref(x)
          and not (j + 1 < len(ls) and xref(ls[j + 1]) and not re.match(r'^\d', x))]
    # Algunos capítulos traen "1 Texto" (con espacio) en el primer versículo.
    if not any(re.match(r'^1[^\d\s]', y) for y in ls):
        ls = [re.sub(r'^1 (?=\S)', '1', x) for x in ls]
    # Títulos de sección: sin número, sin puntuación final y seguidos de un versículo.
    keep = [s for j, s in enumerate(ls)
            if not (not re.match(r'^\d', s)
                    and j + 1 < len(ls) and re.match(r'^\d', ls[j + 1])
                    and not re.search(r'[.,;:!?»”’)—\-]$', s))]
    txt = ''
    for s in keep:
        txt = txt[:-1] + s if txt.endswith('-') and not txt.endswith(' -') else (f'{txt} {s}' if txt else s)
    # Corta por números de versículo en orden (admite versículos omitidos, p. ej. Mt 23:14).
    first = re.search(r'(?<!\d)1(?=[^\d\s.,:;–-])', txt)
    if not first:
        return {}
    vs, cur, start = {}, 1, first.end()
    while True:
        found = None
        for cand in (cur + 1, cur + 2):
            m = re.compile(r'(?<!\d)(?<!\d[.:,])%d(?= ?[^\d\s.,:;–\-])' % cand).search(txt, start)
            if m and (found is None or m.start() < found[1].start()):
                found = (cand, m)
        if not found:
            vs[cur] = txt[start:]
            break
        vs[cur] = txt[start:found[1].start()]
        cur, start = found[0], found[1].end()
    return {n: re.sub(r'\s+', ' ', t).strip() for n, t in vs.items()}


def _book_key(name):
    return 'SALMO' if name in ('Salmo', 'Salmos') else name.upper()


def passage(ref):
    """Lista [{n, t}] para una referencia como las de las slides."""
    m = re.match(r'^((?:[123] )?[^\d]+?) (.+)$', ref)
    book, rest = _book_key(m.group(1)), m.group(2)
    out, ch = [], None
    for seg in re.split(r';\s*', rest):
        for part in re.split(r',\s*', seg):
            part = part.replace('–', '-')
            if ':' in part:
                c, v = part.split(':', 1)
                ch = int(c)
            elif ch is None:  # capítulo completo
                ch = int(part)
                out += [(ch, n) for n in sorted(verses_of(book, ch))]
                continue
            else:
                v = part
            if '-' in v:
                a, b = v.split('-')
                if ':' in b:  # c:v-c2:w
                    c2, b2 = map(int, b.split(':'))
                    for c in range(ch, c2 + 1):
                        vs = verses_of(book, c)
                        lo = int(a) if c == ch else 1
                        hi = b2 if c == c2 else max(vs)
                        out += [(c, n) for n in range(lo, hi + 1) if n in vs]
                    ch = c2
                    continue
                out += [(ch, n) for n in range(int(a), int(b) + 1)]
            else:
                out.append((ch, int(v)))
    multi = len({c for c, _ in out}) > 1
    res = []
    for c, n in out:
        vs = verses_of(book, c)
        if n in vs:  # los versículos omitidos por la NVI se saltan
            res.append({'n': f'{c}:{n}' if multi else n, 't': vs[n]})
    if not res:
        raise ValueError(f'sin texto para {ref}')
    return res


def _js(s):
    return "'" + s.replace('\\', '\\\\').replace("'", "\\'") + "'"


def actualizar():
    html = open(INDEX, encoding='utf-8').read()
    a = html.index('const PRESENTATIONS')
    b = html.index('const findPresentation')
    refs = set()
    for arr in re.findall(r'verses: \[(.*?)\]', html[a:b], re.S):
        refs.update(re.findall(r"'((?:[^'\\]|\\.)*)'", arr))
    out, fail = {}, []
    for r in sorted(refs - SKIP):
        try:
            out[r] = passage(r)
        except Exception as e:  # noqa: BLE001
            fail.append(f'{r} ({e})')
    lines = ['const BIBLE_VERSES = {']
    for k, vs in out.items():
        lines.append(f'  {_js(k)}: [')
        lines += [f"    {{ n: {v['n'] if isinstance(v['n'], int) else _js(v['n'])}, t: {_js(v['t'])} }}," for v in vs]
        lines.append('  ],')
    lines.append('};')
    s = html.index('const BIBLE_VERSES = {')
    e = html.index('\n};', s) + 3
    html = html[:s] + '\n'.join(lines) + html[e:]
    open(INDEX, 'w', encoding='utf-8').write(html)
    print(f'BIBLE_VERSES: {len(out)} pasajes.')
    for f in fail:
        print('  sin texto:', f)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    if sys.argv[1] == 'actualizar':
        actualizar()
    else:
        for v in passage(' '.join(sys.argv[1:])):
            print(v['n'], v['t'])
