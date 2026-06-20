#!/usr/bin/env python3
"""Genera las slides (4:5, listas para publicar) de la Lección 12 — Hechos 4.

Estilo MRNT Class: fondo crema, tipografía Barlow Condensed, colores del plan MRNT.
Salida: assets/hechos4/*.png
"""
import os
from PIL import Image, ImageDraw, ImageFont

FONTS = "/tmp/fonts"
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "hechos4")
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

def base(draw_grain=True):
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    # halos radiales sutiles (rectángulos translúcidos)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse([-260, -300, 520, 480], fill=(59, 130, 246, 16))
    od.ellipse([W-420, H-520, W+320, H+260], fill=(124, 58, 237, 14))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    return img, ImageDraw.Draw(img)

def header(d, kicker, page):
    M = 84
    # tag superior
    tag = "MRNT CLASS"
    d.text((M, 70), tag, font=F(BLACK, 30), fill=NAVY)
    w = d.textlength(tag, font=F(BLACK, 30))
    tracking_text(d, (M + w + 16, 78), "·  LECCIÓN 12 — COMPÁRTELO",
                  F(SEMI, 24), MUTED, tracking=2)
    # número de slide
    d.text((W - M, 70), f"{page}/3", font=F(BLACK, 30), fill=BLUE, anchor="ra")
    # línea
    d.line([(M, 120), (W - M, 120)], fill=(210, 205, 195), width=2)
    return M

def footer(d, M):
    tracking_text(d, (M, H - 64), "HECHOS 4 · RVR1960",
                  F(SEMI, 22), MUTED, tracking=3)
    d.text((W - M, H - 70), "“…habían estado con Jesús.” v.13",
           font=F(BODYM, 22), fill=MUTED, anchor="ra")

# ---------------------------------------------------------------- SLIDE 1
def slide1():
    img, d = base()
    M = header(d, "BOSQUEJO", 1)
    y = 168
    tracking_text(d, (M, y), "BOSQUEJO DEL CAPÍTULO", F(SEMI, 26), BLUE, tracking=4)
    y += 44
    d.text((M, y), "HECHOS 4", font=F(BLACK, 138), fill=NAVY)
    y += 150
    for ln in wrap(d, "“No podemos dejar de decir lo que hemos visto y oído.” (v. 20)",
                   F(BODYM, 30), W - 2*M):
        d.text((M, y), ln, font=F(BODYM, 30), fill=INK)
        y += 40
    y += 22

    secciones = [
        ("1", "EL ARRESTO", "vv. 1-4", BLUE,
         "Predican a Jesús resucitado; los encarcelan, pero la Palabra crece (≈5.000)."),
        ("2", "LA DEFENSA", "vv. 5-12", GOLD,
         "Ante el Sanedrín, Pedro lleno del Espíritu: “En ningún otro hay salvación.”"),
        ("3", "LA AMENAZA", "vv. 13-22", ORANGE,
         "“Habían estado con Jesús.” Les prohíben hablar: obedecer a Dios, no a los hombres."),
        ("4", "LA ORACIÓN", "vv. 23-31", PURPLE,
         "La iglesia ora unida y pide denuedo —no comodidad—; son llenos del Espíritu."),
        ("5", "LA COMUNIÓN", "vv. 32-37", BLUE,
         "“Un corazón y un alma”: testimonio de la resurrección con gran poder y gracia."),
    ]
    card_h = 152
    gap = 18
    for num, title, ref, color, desc in secciones:
        x0, x1 = M, W - M
        box = [x0, y, x1, y + card_h]
        rounded(d, box, 26, fill=(255, 255, 255))
        # barra de color a la izquierda
        rounded(d, [x0, y, x0 + 12, y + card_h], 6, fill=color)
        # chip número
        cy = y + card_h // 2
        d.ellipse([x0 + 34, cy - 34, x0 + 102, cy + 34], fill=color)
        d.text(((x0 + 68), cy), num, font=F(BLACK, 50), fill=(255, 255, 255), anchor="mm")
        tx = x0 + 130
        d.text((tx, y + 24), title, font=F(BLACK, 44), fill=NAVY)
        tw = d.textlength(title, font=F(BLACK, 44))
        # ref pill
        pill = [tx + tw + 18, y + 30, tx + tw + 18 + d.textlength(ref, font=F(BOLD, 26)) + 32, y + 68]
        rounded(d, pill, 18, fill=CREAM, outline=color, width=3)
        d.text(((pill[0] + pill[2]) / 2, (pill[1] + pill[3]) / 2), ref,
               font=F(BOLD, 26), fill=color, anchor="mm")
        ly = y + 84
        for ln in wrap(d, desc, F(BODY, 27), x1 - tx - 28):
            d.text((tx, ly), ln, font=F(BODY, 27), fill=INK)
            ly += 33
        y += card_h + gap
    footer(d, M)
    img.save(os.path.join(OUT, "hechos4-1-bosquejo.png"))

# ---------------------------------------------------------------- SLIDE 2
def slide2():
    img, d = base()
    M = header(d, "TEXTO", 2)
    y = 172
    tracking_text(d, (M, y), "LECTURA BÍBLICA · RVR1960", F(SEMI, 26), PURPLE, tracking=4)
    y += 44
    d.text((M, y), "HECHOS 4:13-17", font=F(BLACK, 92), fill=NAVY)
    y += 122
    d.line([(M, y), (M + 120, y)], fill=PURPLE, width=6)
    y += 36

    versiculos = [
        ("13", "Entonces viendo el denuedo de Pedro y de Juan, y sabiendo que eran hombres sin letras y del vulgo, se maravillaban; y les reconocían que habían estado con Jesús."),
        ("14", "Y viendo al hombre que había sido sanado, que estaba en pie con ellos, no podían decir nada en contra."),
        ("15", "Entonces les ordenaron que saliesen del concilio; y conferenciaban entre sí,"),
        ("16", "diciendo: ¿Qué haremos con estos hombres? Porque de cierto, señal manifiesta ha sido hecha por ellos, notoria a todos los que moran en Jerusalén, y no lo podemos negar."),
        ("17", "Sin embargo, para que no se divulgue más entre el pueblo, amenacémoslos para que no hablen de aquí en adelante a hombre alguno en este nombre."),
    ]
    fnt = F(BODY, 31)
    lh = 40
    for num, txt in versiculos:
        d.text((M, y - 4), num, font=F(BLACK, 38), fill=PURPLE)
        tx = M + 56
        for i, ln in enumerate(wrap(d, txt, fnt, W - M - tx)):
            d.text((tx, y), ln, font=fnt, fill=INK)
            y += lh
        y += 18
    footer(d, M)
    img.save(os.path.join(OUT, "hechos4-2-texto.png"))

# ---------------------------------------------------------------- SLIDE 3
def slide3():
    img, d = base()
    M = header(d, "APLICACIÓN", 3)
    y = 162
    tracking_text(d, (M, y), "CÓMO SER UN TESTIGO DE CRISTO", F(SEMI, 26), ORANGE, tracking=3)
    y += 42
    d.text((M, y), "DIRECTRICES", font=F(BLACK, 92), fill=NAVY)
    y += 112
    for ln in wrap(d, "Lo que esta historia nos enseña sobre dar testimonio:",
                   F(BODYM, 29), W - 2*M):
        d.text((M, y), ln, font=F(BODYM, 29), fill=INK)
        y += 38
    y += 14

    puntos = [
        ("Habla en el poder del Espíritu", "No en fuerza propia: “Pedro, lleno del Espíritu Santo” (v. 8).", BLUE),
        ("Permanece con Jesús", "El secreto del denuedo: “habían estado con Jesús” (v. 13).", GOLD),
        ("Céntrate en Cristo", "Solo en Él hay salvación; “no hay otro nombre” (v. 12).", ORANGE),
        ("Deja que tu vida hable", "El sanado, de pie, fue evidencia innegable (v. 14).", PURPLE),
        ("Obedece a Dios antes que a los hombres", "Aun bajo amenaza; no puedes callar lo visto y oído (vv. 19-20).", BLUE),
        ("Ora pidiendo valentía", "La iglesia pidió denuedo, no comodidad (v. 29).", PURPLE),
        ("Testifica en comunidad", "“Un corazón y un alma”, con gracia y generosidad (vv. 32-35).", GOLD),
    ]
    sub_font = F(BODY, 25)
    tx = M + 112
    # alturas adaptativas según líneas de descripción
    layout = []
    for t, sub, color in puntos:
        lines = wrap(d, sub, sub_font, W - M - tx - 20)
        ch = 60 + len(lines) * 30 + 18
        layout.append((t, lines, color, ch))
    total = sum(c[3] for c in layout)
    foot_top = H - 96
    gap = (foot_top - y - total) / (len(layout))
    gap = max(8, min(gap, 20))
    for i, (t, lines, color, ch) in enumerate(layout, 1):
        box = [M, y, W - M, y + ch]
        rounded(d, box, 22, fill=(255, 255, 255))
        cy = y + ch // 2
        d.ellipse([M + 24, cy - 28, M + 80, cy + 28], fill=color)
        d.text((M + 52, cy), str(i), font=F(BLACK, 40), fill=(255, 255, 255), anchor="mm")
        d.text((tx, y + 16), t, font=F(BOLD, 36), fill=NAVY)
        ly = y + 60
        for ln in lines:
            d.text((tx, ly), ln, font=sub_font, fill=INK)
            ly += 30
        y += ch + gap
    footer(d, M)
    img.save(os.path.join(OUT, "hechos4-3-directrices.png"))

if __name__ == "__main__":
    slide1()
    slide2()
    slide3()
    print("Slides generadas en", os.path.abspath(OUT))
