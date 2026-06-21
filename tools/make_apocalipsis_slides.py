#!/usr/bin/env python3
"""Genera las slides (4:5, listas para publicar) de la Lección 13 — Apocalipsis 21-22.

Estilo MRNT Class / Maranata: fondo crema, tipografía Barlow Condensed,
colores del plan MRNT. Mismo lenguaje visual que make_hechos4_slides.py.
Salida: assets/apocalipsis21-22/*.png
"""
import os
from PIL import Image, ImageDraw, ImageFont

FONTS = "/tmp/fonts"
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "apocalipsis21-22")
os.makedirs(OUT, exist_ok=True)

W, H = 1080, 1350

# Paleta MRNT
CREAM   = (248, 245, 239)
NAVY    = (10, 14, 46)
INK     = (26, 30, 56)
MUTED   = (110, 114, 138)
BLUE    = (59, 130, 246)    # Misión
GOLD    = (161, 98, 7)      # Relación (oscuro p/legibilidad)
ORANGE  = (194, 65, 12)     # Nutrición
PURPLE  = (124, 58, 237)    # Templo
GOLDB   = (234, 179, 8)

def F(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)

BLACK   = "BarlowCondensed-Black.ttf"
BOLD    = "BarlowCondensed-Bold.ttf"
SEMI    = "BarlowCondensed-SemiBold.ttf"
MED     = "BarlowCondensed-Medium.ttf"
BODY    = "Barlow-Regular.ttf"
BODYM   = "Barlow-Medium.ttf"
BODYSB  = "Barlow-SemiBold.ttf"

def tracking_text(d, xy, text, font, fill, tracking=0, anchor_left=True):
    """Dibuja texto con tracking (espaciado entre letras). Devuelve ancho total."""
    x, y = xy
    total = 0
    widths = []
    for ch in text:
        w = d.textlength(ch, font=font)
        widths.append(w)
        total += w + tracking
    total -= tracking if text else 0
    if not anchor_left:
        x = x - total / 2
    cx = x
    for ch, w in zip(text, widths):
        d.text((cx, y), ch, font=font, fill=fill)
        cx += w + tracking
    return total

def wrap(d, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if d.textlength(test, font=font) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def rounded(d, box, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)

def base():
    img = Image.new("RGB", (W, H), CREAM)
    # halos radiales sutiles (elipses translúcidas)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse([-260, -300, 520, 480], fill=(59, 130, 246, 16))
    od.ellipse([W-420, H-520, W+320, H+260], fill=(124, 58, 237, 14))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    return img, ImageDraw.Draw(img)

def header(d, page):
    M = 84
    tag = "MRNT CLASS"
    d.text((M, 70), tag, font=F(BLACK, 30), fill=NAVY)
    w = d.textlength(tag, font=F(BLACK, 30))
    tracking_text(d, (M + w + 16, 78), "·  LECCIÓN 13 — HACIA LA ETERNIDAD",
                  F(SEMI, 24), MUTED, tracking=2)
    d.text((W - M, 70), f"{page}/4", font=F(BLACK, 30), fill=PURPLE, anchor="ra")
    d.line([(M, 120), (W - M, 120)], fill=(210, 205, 195), width=2)
    return M

def footer(d, M, right="“Yo hago nuevas todas las cosas.” 21:5"):
    tracking_text(d, (M, H - 64), "APOCALIPSIS 21–22 · RVR1960",
                  F(SEMI, 22), MUTED, tracking=3)
    d.text((W - M, H - 70), right, font=F(BODYM, 22), fill=MUTED, anchor="ra")

# ---------------------------------------------------------------- SLIDE 1
def slide1():
    img, d = base()
    M = header(d, 1)
    y = 166
    tracking_text(d, (M, y), "BOSQUEJO · LOS DOS ÚLTIMOS CAPÍTULOS", F(SEMI, 26), PURPLE, tracking=3)
    y += 42
    d.text((M, y), "APOCALIPSIS", font=F(BLACK, 88), fill=NAVY)
    y += 90
    d.text((M, y), "21–22", font=F(BLACK, 88), fill=PURPLE)
    y += 104
    for ln in wrap(d, "“He aquí, yo hago nuevas todas las cosas.” (21:5)",
                   F(BODYM, 29), W - 2*M):
        d.text((M, y), ln, font=F(BODYM, 29), fill=INK)
        y += 38
    y += 14

    secciones = [
        ("1", "TODO HECHO NUEVO", "21:1-8", BLUE,
         "“El tabernáculo de Dios con los hombres”; no más muerte, llanto ni dolor."),
        ("2", "LA NUEVA JERUSALÉN", "21:9-21", GOLD,
         "La esposa del Cordero: muro, 12 puertas, 12 cimientos, oro y piedras preciosas."),
        ("3", "SIN TEMPLO NI SOL", "21:22-27", ORANGE,
         "Dios y el Cordero son su templo y su luz; entran los del libro de la vida."),
        ("4", "RÍO Y ÁRBOL DE VIDA", "22:1-5", PURPLE,
         "Agua de vida, sanidad de las naciones; verán su rostro y reinarán por siempre."),
        ("5", "“VENGO PRONTO”", "22:6-15", BLUE,
         "Palabras fieles y verdaderas; “mi galardón conmigo”; guarda estas palabras."),
        ("6", "LA INVITACIÓN FINAL", "22:16-21", PURPLE,
         "“El Espíritu y la Esposa dicen: Ven”; “Sí, ven, Señor Jesús”."),
    ]
    desc_font = F(BODY, 25)
    x0, x1 = M, W - M
    tx = x0 + 116
    layout = []
    for num, title, ref, color, desc in secciones:
        lines = wrap(d, desc, desc_font, x1 - tx - 28)
        ch = 62 + len(lines) * 30 + 12
        layout.append((num, title, ref, color, lines, ch))
    total = sum(c[5] for c in layout)
    foot_top = H - 92
    gap = (foot_top - y - total) / len(layout)
    gap = max(8, min(gap, 18))
    for num, title, ref, color, lines, ch in layout:
        box = [x0, y, x1, y + ch]
        rounded(d, box, 24, fill=(255, 255, 255))
        rounded(d, [x0, y, x0 + 12, y + ch], 6, fill=color)
        cy = y + ch // 2
        d.ellipse([x0 + 30, cy - 30, x0 + 90, cy + 30], fill=color)
        d.text(((x0 + 60), cy), num, font=F(BLACK, 44), fill=(255, 255, 255), anchor="mm")
        d.text((tx, y + 16), title, font=F(BLACK, 38), fill=NAVY)
        tw = d.textlength(title, font=F(BLACK, 38))
        pill = [tx + tw + 16, y + 20, tx + tw + 16 + d.textlength(ref, font=F(BOLD, 24)) + 28, y + 54]
        rounded(d, pill, 16, fill=CREAM, outline=color, width=3)
        d.text(((pill[0] + pill[2]) / 2, (pill[1] + pill[3]) / 2), ref,
               font=F(BOLD, 24), fill=color, anchor="mm")
        ly = y + 64
        for ln in lines:
            d.text((tx, ly), ln, font=desc_font, fill=INK)
            ly += 30
        y += ch + gap
    footer(d, M)
    img.save(os.path.join(OUT, "apocalipsis-1-bosquejo.png"))

# ---------------------------------------------------------------- SLIDE 2
def slide2():
    img, d = base()
    M = header(d, 2)
    y = 172
    tracking_text(d, (M, y), "MAPA CONCEPTUAL · GRANDES TEMAS", F(SEMI, 26), BLUE, tracking=3)
    y += 44
    d.text((M, y), "SEIS HILOS", font=F(BLACK, 92), fill=NAVY)
    y += 112
    for ln in wrap(d, "Los hilos que atraviesan ambos capítulos y se entrelazan en la eternidad:",
                   F(BODYM, 29), W - 2*M):
        d.text((M, y), ln, font=F(BODYM, 29), fill=INK)
        y += 38
    y += 16

    temas = [
        ("Lo nuevo", "“He aquí, yo hago nuevas todas las cosas” (21:5).", BLUE),
        ("La presencia", "“El tabernáculo de Dios con los hombres”: Él morará con ellos (21:3).", GOLD),
        ("La ciudad-esposa", "La nueva Jerusalén, ataviada como esposa del Cordero (21:2, 9).", ORANGE),
        ("La luz", "Sin sol ni lámpara: “el Cordero es su lumbrera” (21:23; 22:5).", PURPLE),
        ("La vida", "Río y árbol de la vida; hojas para sanidad de las naciones (22:1-2).", BLUE),
        ("La invitación", "“El que tiene sed, venga… tome del agua de la vida” (22:17).", PURPLE),
    ]
    sub_font = F(BODY, 25)
    tx = M + 112
    layout = []
    for t, sub, color in temas:
        lines = wrap(d, sub, sub_font, W - M - tx - 20)
        ch = 58 + len(lines) * 30 + 16
        layout.append((t, lines, color, ch))
    total = sum(c[3] for c in layout)
    foot_top = H - 96
    gap = (foot_top - y - total) / len(layout)
    gap = max(8, min(gap, 22))
    for i, (t, lines, color, ch) in enumerate(layout, 1):
        box = [M, y, W - M, y + ch]
        rounded(d, box, 22, fill=(255, 255, 255))
        cy = y + ch // 2
        d.ellipse([M + 24, cy - 28, M + 80, cy + 28], fill=color)
        d.text((M + 52, cy), str(i), font=F(BLACK, 40), fill=(255, 255, 255), anchor="mm")
        d.text((tx, y + 14), t, font=F(BOLD, 36), fill=NAVY)
        ly = y + 58
        for ln in lines:
            d.text((tx, ly), ln, font=sub_font, fill=INK)
            ly += 30
        y += ch + gap
    footer(d, M)
    img.save(os.path.join(OUT, "apocalipsis-2-mapa.png"))

# ---------------------------------------------------------------- SLIDE 3
def slide3():
    img, d = base()
    M = header(d, 3)
    y = 172
    tracking_text(d, (M, y), "LECTURA BÍBLICA · RVR1960", F(SEMI, 26), PURPLE, tracking=4)
    y += 44
    d.text((M, y), "APOCALIPSIS 21:1-7", font=F(BLACK, 82), fill=NAVY)
    y += 110
    d.line([(M, y), (M + 120, y)], fill=PURPLE, width=6)
    y += 34

    versiculos = [
        ("1", "Vi un cielo nuevo y una tierra nueva; porque el primer cielo y la primera tierra pasaron, y el mar ya no existía más."),
        ("2", "Y yo Juan vi la santa ciudad, la nueva Jerusalén, descender del cielo, de Dios, dispuesta como una esposa ataviada para su marido."),
        ("3", "Y oí una gran voz del cielo que decía: He aquí el tabernáculo de Dios con los hombres, y él morará con ellos; y ellos serán su pueblo, y Dios mismo estará con ellos como su Dios."),
        ("4", "Enjugará Dios toda lágrima de los ojos de ellos; y ya no habrá muerte, ni habrá más llanto, ni clamor, ni dolor; porque las primeras cosas pasaron."),
        ("5", "Y el que estaba sentado en el trono dijo: He aquí, yo hago nuevas todas las cosas. Y me dijo: Escribe; porque estas palabras son fieles y verdaderas."),
        ("6", "Y me dijo: Hecho está. Yo soy el Alfa y la Omega, el principio y el fin. Al que tuviere sed, yo le daré gratuitamente de la fuente del agua de la vida."),
        ("7", "El que venciere heredará todas las cosas, y yo seré su Dios, y él será mi hijo."),
    ]
    fnt = F(BODY, 28)
    lh = 37
    for num, txt in versiculos:
        d.text((M, y - 4), num, font=F(BLACK, 34), fill=PURPLE)
        tx = M + 50
        for ln in wrap(d, txt, fnt, W - M - tx):
            d.text((tx, y), ln, font=fnt, fill=INK)
            y += lh
        y += 14
    footer(d, M, right="“…el tabernáculo de Dios con los hombres.” 21:3")
    img.save(os.path.join(OUT, "apocalipsis-3-texto.png"))

# ---------------------------------------------------------------- SLIDE 4
def slide4():
    img, d = base()
    M = header(d, 4)
    y = 162
    tracking_text(d, (M, y), "QUÉ NOS ENSEÑA LA ETERNIDAD", F(SEMI, 26), ORANGE, tracking=3)
    y += 42
    d.text((M, y), "CLAVES", font=F(BLACK, 92), fill=NAVY)
    y += 112
    for ln in wrap(d, "El desenlace de toda la historia de la salvación:",
                   F(BODYM, 29), W - 2*M):
        d.text((M, y), ln, font=F(BODYM, 29), fill=INK)
        y += 38
    y += 14

    puntos = [
        ("El destino es una Persona", "La dicha del cielo es habitar con Dios, cara a cara (21:3).", BLUE),
        ("Dios revierte el dolor", "Enjuga toda lágrima; no más muerte, llanto ni dolor (21:4).", GOLD),
        ("Todo es hecho nuevo", "No un parche, sino una creación renovada (21:5).", ORANGE),
        ("Cristo es el centro", "Alfa y Omega, lámpara de la ciudad, Cordero en el trono (21:23; 22:1).", PURPLE),
        ("La vida vuelve a abundar", "Río y árbol de la vida, con sanidad para las naciones (22:1-2).", BLUE),
        ("Veremos su rostro", "La promesa más íntima de toda la Escritura (22:4).", PURPLE),
        ("La invitación sigue abierta", "“El que tiene sed, venga… gratuitamente” (22:17, 20).", GOLD),
    ]
    sub_font = F(BODY, 25)
    tx = M + 112
    layout = []
    for t, sub, color in puntos:
        lines = wrap(d, sub, sub_font, W - M - tx - 20)
        ch = 58 + len(lines) * 30 + 16
        layout.append((t, lines, color, ch))
    total = sum(c[3] for c in layout)
    foot_top = H - 96
    gap = (foot_top - y - total) / len(layout)
    gap = max(8, min(gap, 20))
    for i, (t, lines, color, ch) in enumerate(layout, 1):
        box = [M, y, W - M, y + ch]
        rounded(d, box, 22, fill=(255, 255, 255))
        cy = y + ch // 2
        d.ellipse([M + 24, cy - 28, M + 80, cy + 28], fill=color)
        d.text((M + 52, cy), str(i), font=F(BLACK, 40), fill=(255, 255, 255), anchor="mm")
        d.text((tx, y + 14), t, font=F(BOLD, 36), fill=NAVY)
        ly = y + 58
        for ln in lines:
            d.text((tx, ly), ln, font=sub_font, fill=INK)
            ly += 30
        y += ch + gap
    footer(d, M, right="“Sí, ven, Señor Jesús.” 22:20")
    img.save(os.path.join(OUT, "apocalipsis-4-claves.png"))

if __name__ == "__main__":
    slide1()
    slide2()
    slide3()
    slide4()
    print("Slides generadas en", os.path.abspath(OUT))
