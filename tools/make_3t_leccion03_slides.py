#!/usr/bin/env python3
"""Genera las slides (4:5, listas para publicar) de la Lección 03 — 3T 2026.

"Las escenas finales" — Juan 14. Ministerio Joven Unión Chilena.
Estilo MRNT Class: fondo crema, tipografía Barlow Condensed, colores del plan MRNT.
Salida: assets/3t/leccion03-escenas-finales/*.png
"""
import os
from PIL import Image, ImageDraw, ImageFont

FONTS = "/tmp/fonts"
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "3t", "leccion03-escenas-finales")
os.makedirs(OUT, exist_ok=True)

W, H = 1080, 1350
TOTAL_PAGES = 10

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
WHITE   = (255, 255, 255)

def F(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)

BLACK   = "BarlowCondensed-Black.ttf"
BOLD    = "BarlowCondensed-Bold.ttf"
SEMI    = "BarlowCondensed-SemiBold.ttf"
MED     = "BarlowCondensed-Medium.ttf"
REG     = "BarlowCondensed-Regular.ttf"
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

def base(halo_a=BLUE, halo_b=PURPLE, bg=CREAM):
    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse([-260, -300, 520, 480], fill=halo_a + (16,))
    od.ellipse([W-420, H-520, W+320, H+260], fill=halo_b + (14,))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    return img, ImageDraw.Draw(img)

def logo(d, x, y, color=NAVY, scale=1.0):
    """Dibuja el badge 'MRNT CLASS' (libro + wordmark) en (x, y) = esquina sup. izq."""
    s = scale
    bx0, by0 = x, y
    bw, bh = int(46 * s), int(34 * s)
    rounded(d, [bx0, by0, bx0 + bw, by0 + bh], int(6 * s), outline=color, width=max(2, int(2 * s)))
    d.line([(bx0 + bw / 2, by0 + 4 * s), (bx0 + bw / 2, by0 + bh - 4 * s)], fill=color, width=max(2, int(2 * s)))
    tx = bx0 + bw + int(10 * s)
    fnt = F(BLACK, int(28 * s))
    d.text((tx, by0 - int(3 * s)), "MRNT", font=fnt, fill=color)
    tw = d.textlength("MRNT", font=fnt)
    fnt2 = F(SEMI, int(16 * s))
    d.text((tx + tw + int(4 * s), by0 + int(9 * s)), "CLASS", font=fnt2, fill=color)

def header(d, kicker, page, accent=BLUE):
    M = 84
    tag = "MRNT CLASS"
    d.text((M, 70), tag, font=F(BLACK, 30), fill=NAVY)
    w = d.textlength(tag, font=F(BLACK, 30))
    tracking_text(d, (M + w + 16, 78), "·  " + kicker, F(SEMI, 22), MUTED, tracking=2)
    d.text((W - M, 70), f"{page}/{TOTAL_PAGES}", font=F(BLACK, 30), fill=accent, anchor="ra")
    d.line([(M, 120), (W - M, 120)], fill=(210, 205, 195), width=2)
    return M

def footer(d, M, left, right):
    tracking_text(d, (M, H - 64), left, F(SEMI, 22), MUTED, tracking=3)
    d.text((W - M, H - 70), right, font=F(BODYM, 22), fill=MUTED, anchor="ra")

def bullet_cards(d, M, y, items, accent, max_bottom, card_gap=16):
    """items: lista de strings. Devuelve y final. Autoajusta alto según líneas."""
    x0, x1 = M, W - M
    body_font = F(BODY, 28)
    pad = 26
    layout = []
    for text in items:
        lines = wrap(d, text, body_font, x1 - x0 - 2 * pad)
        ch = pad * 2 + len(lines) * 36
        layout.append((lines, ch))
    total = sum(c[1] for c in layout) + card_gap * (len(layout) - 1)
    avail = max_bottom - y
    if total > avail and len(layout) > 0:
        # reduce line-height/gap proportionally
        shrink = avail / total
        card_gap = max(8, int(card_gap * shrink))
    for lines, ch in layout:
        box = [x0, y, x1, y + ch]
        rounded(d, box, 22, fill=WHITE)
        rounded(d, [x0, y, x0 + 10, y + ch], 5, fill=accent)
        ty = y + pad
        for ln in lines:
            d.text((x0 + pad + 16, ty), ln, font=body_font, fill=INK)
            ty += 36
        y += ch + card_gap
    return y

def ref_chip(d, x, y, refs, accent, title="REF. BÍBLICA"):
    w = 210
    lines_h = 26 * len(refs) + 46
    box = [x, y, x + w, y + lines_h]
    rounded(d, box, 16, fill=(255, 255, 255, 255))
    d.rectangle(box, fill=(255, 250, 235))
    rounded(d, box, 16, outline=accent, width=2)
    d.text((x + 18, y + 14), title, font=F(BOLD, 19), fill=accent)
    ty = y + 42
    for r in refs:
        d.text((x + 22, ty), "•  " + r, font=F(BODYM, 18), fill=INK)
        ty += 26
    return box

# ------------------------------------------------------------------ DATA
DAYS = [
    dict(num=1, name="SÁBADO", label="INICIA", color=BLUE,
         title="PONER LAS COSAS EN ORDEN",
         bullets=[
             "Antes de su muerte, Jesús preparó a sus discípulos para enfrentar su ausencia con esperanza y confianza.",
             "Les habló del arrepentimiento, del perdón y de las dificultades que vendrían, pero también les aseguró que volvería por ellos.",
             "Prometió enviar al Espíritu Santo para guiarlos y consolarlos.",
             "Además, les recordó el amor, la paz y la presencia permanente del Padre en sus vidas.",
         ],
         refs=["Juan 13", "Juan 14:1-3", "Juan 14:16-18", "Juan 14:26-27"]),
    dict(num=3, name="LUNES", label="ASIMILA", color=ORANGE,
         title="PROMESAS PARA LO QUE VIENE",
         bullets=[
             "Jesús preparó a sus discípulos para su partida con la promesa de que volvería por ellos y les prepararía un lugar en el cielo.",
             "Reveló que conocerlo a él es conocer al Padre, mostrando que ambos comparten el mismo amor y carácter.",
             "Aseguró que el Padre escucha y responde las oraciones de quienes acuden a él con fe.",
             "También afirmó que, aun conociendo las debilidades de sus discípulos, tanto él como el Padre desean permanecer para siempre con quienes lo aman.",
         ],
         refs=["Juan 14:1-3", "Juan 14:7-9", "Juan 14:13-14", "Juan 14:23"]),
    dict(num=4, name="MARTES", label="INTERPRETA", color=PURPLE,
         title="LA AYUDA ESTÁ EN CAMINO",
         bullets=[
             "El amor a Jesús se manifiesta naturalmente en la obediencia, la cual es fruto de una relación con él y no una imposición.",
             "Jesús prometió que el Padre enviaría al Espíritu Santo para fortalecer, guiar y capacitar a sus seguidores.",
             "El Padre, el Hijo y el Espíritu Santo trabajan unidos en la obra de la salvación y en la transformación del creyente.",
             "El Espíritu Santo también enseña, recuerda las palabras de Cristo y sostiene a los creyentes en los momentos de prueba.",
         ],
         refs=["Juan 14:15", "Juan 14:16-17", "Juan 14:25-26", "Juan 14:26"]),
    dict(num=6, name="JUEVES", label="ENFOCA", color=GOLD,
         title="PREPARAR UN LUGAR",
         bullets=[
             "La promesa de la segunda venida dio esperanza a los discípulos y sigue fortaleciendo a los creyentes en medio de las dificultades.",
             "Jesús anhela llevar a su pueblo a vivir con él para siempre y soportó la cruz con ese propósito.",
             "La Biblia presenta la segunda venida como una boda, símbolo del amor y del reencuentro definitivo entre Cristo y su pueblo.",
             "Quienes esperan a Jesús viven preparándose con alegría, compartiendo y anhelando su pronto regreso.",
         ],
         refs=["Juan 14:2-3", "Mateo 9:15; 22:2; 25:1", "Apocalipsis 19:7-9",
               "Isaías 25:8-9", "Apocalipsis 6:15-17"]),
]

QUOTE_DOMINGO = ("Jesús no reveló cualidades ni ejerció facultades que los hombres "
                  "no puedan tener a través de la fe en él.")

INVESTIGA_TOPICS = [
    ("La promesa de la presencia de Dios",
     ["Deuteronomio 31:6, 8", "Josué 1:5", "Isaías 43:2", "Hebreos 13:5"], BLUE),
    ("La promesa del Espíritu",
     ["Ezequiel 36:24-27", "Lucas 11:13", "Hechos 5:32", "1 Juan 3:24"], PURPLE),
]

REFLEXIONA_QUOTE = (
    "«Hasta entonces los discípulos no conocían los recursos y el poder ilimitado "
    "del Salvador. Él les dijo: “Hasta ahora nada habéis pedido en mi nombre” (Juan 16:24). "
    "Explicó que el secreto de su éxito residiría en pedir fuerza y gracia en su nombre. "
    "Estaría delante del Padre para pedir por ellos. La oración del suplicante humilde "
    "es presentada por él como su propio deseo en favor de esa alma. Cada oración sincera "
    "es oída en el cielo. Tal vez no sea expresada con fluidez; pero si se pone el corazón "
    "en ella, ascenderá al santuario donde Jesús ministra y él la presentará al Padre "
    "hermosa y fragante con el incienso de su propia perfección, y sin una palabra "
    "inapropiada o balbuceante».")
REFLEXIONA_CITA = "Elena de White, El Deseado de todas las gentes (ACES, 2008), pp. 619-620."

DIALOGA_COLS = [
    ("LA PROMESA DE SU REGRESO", BLUE, [
        "¿Qué esperanza les dio Jesús a sus discípulos, que estaban confundidos por su partida? (Juan 14:1-6).",
        "¿Por qué la Biblia suele describir la segunda venida de Cristo con la imagen de una boda? (ver Mat. 22:2; 25:1; Apoc. 19:7-9).",
        "¿De qué manera la enseñanza del segundo advenimiento basada en el miedo puede afectar la forma en que se recibe el mensaje?",
        "¿Alguna vez pensaste que se le da menos importancia al «por qué» de la segunda venida que al «cómo»? Si es así, ¿cómo podemos cambiar eso?",
    ]),
    ("LA AYUDA DIVINA CONCEDIDA", GOLD, [
        "¿Alguna vez te has sentido tentado a creer, como muchos, que Dios el Padre es severo y distante? ¿Cómo corrigió Jesús estas creencias erróneas? (Juan 14:7-14).",
        "¿Cómo siguieron experimentando los discípulos la presencia de Dios tras la partida de Cristo? (Juan 14:15-24).",
        "Al leer Juan 14, ¿logras percibir cómo el Padre, el Hijo y el Espíritu Santo trabajan juntos para nuestra salvación?",
    ]),
    ("PAZ Y FE", PURPLE, [
        "A pesar de los tiempos difíciles que se avecinaban, Cristo prometió su paz a los discípulos en Juan 14:27. ¿Cómo se manifiesta esa paz en nuestra vida?",
        "Jesús les habló a los discípulos de muchas cosas futuras y, en Juan 14:29, dijo que cuando estas cosas sucedieran, serían razones para creer en él. ¿Qué nos dice esto sobre la importancia de las profecías para fortalecer nuestra fe?",
        "¿Qué preocupaciones o temores te causan más inquietud? ¿En qué se diferencia la paz que ofrece Jesús de la que tú buscarías de forma natural?",
    ]),
]

AGENDA_TEXT = ("Realiza la #SemanaJoven en tu iglesia o en el lugar donde estén llevando "
               "a cabo la Misión Caleb. Aprovecha para invitar a los amigos que ya están "
               "estudiando la Biblia con el estudio Maranata.")

NEXT_LESSON = dict(
    title="PERMANEZCAN EN MÍ", ref="JUAN 15",
    body=("Charles Spurgeon fue el gran comunicador cristiano del siglo XIX, publicando "
          "sus sermones con la misma rapidez y alcance que un livestream de hoy. Él "
          "entendía que para impactar a otros hay que involucrarse y \"llevar sus "
          "cargas\", una poderosa lección de empatía que extrajo simplemente observando "
          "la vida cotidiana.\n\n"
          "Esa misma capacidad de transformar lo ordinario en algo eterno fue la "
          "especialidad de Jesús; de hecho, de camino a la noche más asfixiante de su "
          "vida en Getsemaní, no dio un discurso teológico complicado, sino que usó un "
          "viñedo en el camino para regalarnos la increíble metáfora de la vid y los "
          "pámpanos (Juan 15). Prepárate para sumergirte en este capítulo y descubrir "
          "cómo el mayor Maestro de la historia nos enseña a mantenernos radicalmente "
          "conectados a Él, dándonos el equilibrio perfecto entre aliento puro y la "
          "cruda realidad que necesitamos para enfrentar cualquier desafío."),
)

# ---------------------------------------------------------------- SLIDE 0 — PORTADA
def slide_portada():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse([-300, -320, 560, 460], fill=BLUE + (30,))
    od.ellipse([W-460, H-560, W+360, H+280], fill=PURPLE + (26,))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    d = ImageDraw.Draw(img)
    M = 84

    logo(d, M, 66, color=(232, 229, 220), scale=1.15)

    y = 220
    tracking_text(d, (M, y), "MATERIAL PARA EL REPASO DE LA LECCIÓN 3T 2026", F(SEMI, 22), (215, 212, 205), tracking=2)
    y += 32
    tracking_text(d, (M, y), "MINISTERIO JOVEN UNIÓN CHILENA", F(SEMI, 22), (215, 212, 205), tracking=2)
    y += 90

    d.text((M, y), "03", font=F(BLACK, 150), fill=(255, 255, 255, 40))
    tracking_text(d, (M, y + 6), "LECCIÓN", F(BOLD, 30), BLUE, tracking=6)
    y += 158

    for ln in ["LAS ESCENAS", "FINALES"]:
        d.text((M, y), ln, font=F(BLACK, 108), fill=CREAM)
        y += 118
    y += 30
    rounded(d, [M, y, M + 120, y + 6], 3, fill=BLUE)
    y += 40
    tracking_text(d, (M, y), "JULIO – SEPTIEMBRE 2026 · GUÍA DE ESTUDIO DE LA BIBLIA PARA JÓVENES",
                  F(SEMI, 21), (200, 197, 190), tracking=1)

    # franja inferior "comienza la clase"
    band_y = H - 210
    d.rectangle([0, band_y, W, H], fill=(20, 25, 58))
    d.text((M, band_y + 40), "03", font=F(BLACK, 90), fill=BLUE)
    tracking_text(d, (M + 150, band_y + 46), "COMIENZA LA CLASE", F(BLACK, 34), CREAM, tracking=2)
    tracking_text(d, (M + 150, band_y + 96), "JUAN 14", F(SEMI, 26), (190, 187, 180), tracking=3)

    img.save(os.path.join(OUT, "3t-00-portada.png"))

# ---------------------------------------------------------------- SLIDES DÍAS (regulares)
def slide_dia(idx, dday):
    img, d = base(halo_a=dday["color"], halo_b=PURPLE if dday["color"] != PURPLE else BLUE)
    M = header(d, f"LECCIÓN 03 · {dday['name']} — {dday['label']}", idx, accent=dday["color"])
    y = 168
    tracking_text(d, (M, y), f"{dday['name']} · {dday['label']}", F(SEMI, 26), dday["color"], tracking=4)
    y += 46
    title_font = F(BLACK, 66)
    for ln in wrap(d, dday["title"], title_font, W - 2 * M):
        d.text((M, y), ln, font=title_font, fill=NAVY)
        y += 72
    y += 20

    refs = dday.get("refs")
    max_bottom = H - 96
    if refs:
        chip_h = 26 * len(refs) + 46
        chip_y = max_bottom - chip_h
        ref_chip(d, W - M - 210, chip_y, refs, dday["color"])
        bullet_right_margin = 0
    y = bullet_cards(d, M, y, dday["bullets"], dday["color"], max_bottom)

    footer(d, M, "JUAN 14 · RVR1960", "MRNT CLASS · 3T 2026")
    ascii_name = dday["name"].lower().replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
    img.save(os.path.join(OUT, f"3t-{idx:02d}-{ascii_name}-{dday['label'].lower()}.png"))

# ---------------------------------------------------------------- SLIDE 2 — DOMINGO (cita)
def slide_domingo():
    img, d = base(halo_a=GOLDB, halo_b=BLUE)
    M = header(d, "LECCIÓN 03 · DOMINGO — ESCRIBE", 2, accent=GOLD)
    y = 168
    tracking_text(d, (M, y), "DOMINGO · ESCRIBE", F(SEMI, 26), GOLD, tracking=4)
    y += 46
    title_font = F(BLACK, 60)
    d.text((M, y), "UNA FRASE PARA COMPARTIR", font=title_font, fill=NAVY)
    y += 90

    card_box = [M, y, W - M, H - 220]
    rounded(d, card_box, 30, fill=WHITE)
    rounded(d, card_box, 30, outline=GOLDB, width=4)

    # cabecera tipo "post"
    cx, cy = M + 44, y + 44
    d.ellipse([cx, cy, cx + 56, cy + 56], fill=GOLDB)
    d.text((cx + 28, cy + 28), "MJ", font=F(BOLD, 24), fill=NAVY, anchor="mm")
    d.text((cx + 70, cy + 2), "Ministerio Joven", font=F(BOLD, 26), fill=NAVY)
    d.text((cx + 70, cy + 30), "@ministeriojoven", font=F(BODYM, 20), fill=MUTED)

    qy = cy + 100
    quote_font = F(SEMI, 40)
    for ln in wrap(d, QUOTE_DOMINGO, quote_font, card_box[2] - card_box[0] - 88):
        d.text((cx, qy), ln, font=quote_font, fill=INK)
        qy += 52

    d.line([(cx, card_box[3] - 70), (card_box[2] - 44, card_box[3] - 70)], fill=(225, 220, 208), width=2)
    tracking_text(d, (cx, card_box[3] - 50), "COMENTAR   ·   COMPARTIR   ·   GUARDAR", F(SEMI, 18), MUTED, tracking=1)

    footer(d, M, "JUAN 14 · RVR1960", "MRNT CLASS · 3T 2026")
    img.save(os.path.join(OUT, "3t-02-domingo-escribe.png"))

# ---------------------------------------------------------------- SLIDE 5 — MIÉRCOLES (investiga)
def slide_investiga():
    img, d = base(halo_a=BLUE, halo_b=PURPLE)
    M = header(d, "LECCIÓN 03 · MIÉRCOLES — INVESTIGA", 5, accent=BLUE)
    y = 168
    tracking_text(d, (M, y), "MIÉRCOLES · INVESTIGA", F(SEMI, 26), BLUE, tracking=4)
    y += 46
    title_font = F(BLACK, 62)
    d.text((M, y), "BUSCA EN TU BIBLIA", font=title_font, fill=NAVY)
    y += 96

    for title, refs, color in INVESTIGA_TOPICS:
        card_h = 220
        box = [M, y, W - M, y + card_h]
        rounded(d, box, 26, fill=WHITE)
        rounded(d, [M, y, M + 10, y + card_h], 5, fill=color)
        cx, cyc = M + 56, y + 58
        d.ellipse([cx - 34, cyc - 34, cx + 34, cyc + 34], outline=color, width=4)
        d.ellipse([cx - 10, cyc - 10, cx + 10, cyc + 10], fill=color)
        tx = M + 116
        title_f = F(BOLD, 34)
        d.text((tx, y + 34), title, font=title_f, fill=NAVY)
        ty = y + 92
        for r in refs:
            d.ellipse([tx, ty + 8, tx + 8, ty + 16], fill=color)
            d.text((tx + 22, ty), r, font=F(BODYM, 27), fill=INK)
            ty += 38
        y += card_h + 34

    footer(d, M, "JUAN 14 · RVR1960", "MRNT CLASS · 3T 2026")
    img.save(os.path.join(OUT, "3t-05-miercoles-investiga.png"))

# ---------------------------------------------------------------- SLIDE 7 — VIERNES (reflexiona / EGW)
def slide_reflexiona():
    img, d = base(halo_a=ORANGE, halo_b=PURPLE)
    M = header(d, "LECCIÓN 03 · VIERNES — REFLEXIONA", 7, accent=ORANGE)
    y = 168
    tracking_text(d, (M, y), "VIERNES · REFLEXIONA", F(SEMI, 26), ORANGE, tracking=4)
    y += 46
    title_font = F(BLACK, 62)
    d.text((M, y), "OBRAS AÚN MÁS GRANDES", font=title_font, fill=NAVY)
    y += 92

    body_font = F(BODYM, 26)
    lines = wrap(d, REFLEXIONA_QUOTE, body_font, W - 2 * M - 80)
    card_h = 60 + len(lines) * 34 + 30
    box = [M, y, W - M, y + card_h]
    rounded(d, box, 26, fill=WHITE)
    rounded(d, [M, y, M + 10, y + card_h], 5, fill=ORANGE)
    ty = y + 34
    for ln in lines:
        d.text((M + 40, ty), ln, font=body_font, fill=INK)
        ty += 34
    y += card_h + 26

    for ln in wrap(d, REFLEXIONA_CITA, F(BODYM, 22), W - 2 * M):
        d.text((M, y), ln, font=F(BODYM, 22), fill=MUTED)
        y += 30

    footer(d, M, "JUAN 14 · RVR1960", "MRNT CLASS · 3T 2026")
    img.save(os.path.join(OUT, "3t-07-viernes-reflexiona.png"))

# ---------------------------------------------------------------- SLIDE 8 — DIALOGA
def slide_dialoga():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    band_h = 210
    d.rectangle([0, 0, W, band_h], fill=NAVY)
    M = 84
    logo(d, M, 40, color=(215, 212, 205), scale=0.9)
    tracking_text(d, (M, band_h - 90), "DIALOGA", F(BLACK, 64), CREAM, tracking=2)
    tracking_text(d, (M, band_h - 30), "PREGUNTAS PARA CONVERSAR EN GRUPO", F(SEMI, 20), (190, 187, 180), tracking=3)
    d.text((W - M, 40), "8/10", font=F(BLACK, 30), fill=BLUE, anchor="ra")

    col_w = (W - 2 * M - 2 * 26) / 3
    y0 = band_h + 40
    q_font = F(BODY, 21)
    for i, (title, color, questions) in enumerate(DIALOGA_COLS):
        x0 = M + i * (col_w + 26)
        x1 = x0 + col_w
        rounded(d, [x0, y0, x0 + 34, y0 + 6], 3, fill=color)
        ty = y0 + 20
        tfont = F(BOLD, 24)
        for ln in wrap(d, title, tfont, col_w):
            d.text((x0, ty), ln, font=tfont, fill=NAVY)
            ty += 28
        ty += 14
        for n, q in enumerate(questions, 1):
            d.text((x0, ty), str(n), font=F(BLACK, 22), fill=color)
            qx = x0 + 26
            qlines = wrap(d, q, q_font, col_w - 26)
            for ln in qlines:
                d.text((qx, ty), ln, font=q_font, fill=INK)
                ty += 27
            ty += 16

    # agenda joven box (alto calculado según líneas reales)
    ag_font = F(BODYM, 22)
    ag_lines = wrap(d, AGENDA_TEXT, ag_font, W - 2 * M - 60)
    ag_h = 66 + len(ag_lines) * 30 + 24
    ag_y = H - 100 - ag_h
    ag_box = [M, ag_y, W - M, ag_y + ag_h]
    rounded(d, ag_box, 24, fill=(20, 25, 58))
    tracking_text(d, (M + 30, ag_y + 24), "AGENDA JOVEN", F(BLACK, 28), CREAM, tracking=2)
    ay = ag_y + 66
    for ln in ag_lines:
        d.text((M + 30, ay), ln, font=ag_font, fill=(215, 212, 205))
        ay += 30

    tracking_text(d, (M, H - 46), "JUAN 14 · RVR1960", F(SEMI, 20), MUTED, tracking=3)
    d.text((W - M, H - 50), "MRNT CLASS · 3T 2026", font=F(BODYM, 20), fill=MUTED, anchor="ra")
    img.save(os.path.join(OUT, "3t-08-dialoga.png"))

# ---------------------------------------------------------------- SLIDE 9 — PRÓXIMA LECCIÓN
def slide_proxima():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    panel_w = int(W * 0.42)
    d.rectangle([0, 0, panel_w, H], fill=PURPLE)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse([-160, H - 520, 420, H - 60], fill=(255, 255, 255, 18))
    od.ellipse([-120, -160, 320, 260], fill=(255, 255, 255, 14))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    d = ImageDraw.Draw(img)

    cx = panel_w // 2
    d.ellipse([cx - 150, 430, cx + 150, 730], outline=(255, 255, 255), width=6)
    d.line([(cx, 470), (cx, 690)], fill=(255, 255, 255), width=6)
    d.line([(cx - 90, 500), (cx + 90, 660)], fill=(255, 255, 255), width=4)
    d.line([(cx + 90, 500), (cx - 90, 660)], fill=(255, 255, 255), width=4)
    tracking_text(d, (60, 60), "PRÓXIMA LECCIÓN", F(BOLD, 24), (232, 227, 250), tracking=3)
    logo(d, 60, H - 110, color=(232, 227, 250), scale=1.0)

    M2 = panel_w + 70
    y = 110
    d.text((W - 84, 40), "9/10", font=F(BLACK, 30), fill=PURPLE, anchor="ra")
    title_font = F(BLACK, 76)
    for ln in wrap(d, NEXT_LESSON["title"], title_font, W - M2 - 70):
        d.text((M2, y), ln, font=title_font, fill=NAVY)
        y += 82
    y += 6
    tracking_text(d, (M2, y), NEXT_LESSON["ref"], F(SEMI, 30), PURPLE, tracking=4)
    y += 60

    body_font = F(BODYM, 24)
    for para in NEXT_LESSON["body"].split("\n\n"):
        for ln in wrap(d, para, body_font, W - M2 - 70):
            d.text((M2, y), ln, font=body_font, fill=INK)
            y += 33
        y += 20

    footer_y = H - 60
    d.line([(M2, footer_y - 24), (W - 70, footer_y - 24)], fill=(210, 205, 195), width=2)
    tracking_text(d, (M2, footer_y - 4), "JUAN 15 · MRNT CLASS · 3T 2026", F(SEMI, 20), MUTED, tracking=2)

    img.save(os.path.join(OUT, "3t-09-proxima-leccion.png"))

# ---------------------------------------------------------------------- MAIN
if __name__ == "__main__":
    slide_portada()
    slide_dia(1, DAYS[0])          # sábado
    slide_domingo()                # domingo
    slide_dia(3, DAYS[1])          # lunes
    slide_dia(4, DAYS[2])          # martes
    slide_investiga()              # miércoles
    slide_dia(6, DAYS[3])          # jueves
    slide_reflexiona()             # viernes
    slide_dialoga()                # dialoga
    slide_proxima()                # próxima lección
    print("Slides generadas en", os.path.abspath(OUT))
