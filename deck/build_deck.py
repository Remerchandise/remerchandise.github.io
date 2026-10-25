"""Bouwt deck/accudetector_inworpzuil.pptx met python-pptx (Orchestrator).

Draai vanuit repo-root:
    python3 deck/charts.py && python3 deck/build_deck.py
Alle cijfers komen uit experiments/*, product/* en debate/R4_*.md.
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "deck", "charts")
OUTFILE = os.path.join(ROOT, "deck", "accudetector_inworpzuil.pptx")

HEAD, BODY = "Cambria", "Calibri"


def rgb(h):
    return RGBColor.from_string(h)


DARK, INK, MUTED = "1C2B2D", "1F2328", "5F646A"
EMBER, TEAL = "D9481C", "1F7A6D"
CARD, LINE, WHITE = "F2F4F5", "D5D9DD", "FFFFFF"
GOOD, WARN, CRIT = "2E8B57", "E39B00", "C8312F"

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]
N = [0]


# ---------- helpers ---------------------------------------------------------
def nb(t):
    """Houd getal en eenheid bij elkaar (geen regelafbreking voor % of na EUR)."""
    return t.replace(" %", "\u00a0%").replace("EUR ", "EUR\u00a0").replace(" ×", "\u00a0×")


def bg(slide, color):
    f = slide.background.fill
    f.solid(); f.fore_color.rgb = rgb(color)


def text(slide, x, y, w, h, runs, size=16, color=INK, bold=False, font=BODY, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, bullets=False, space=6, name=None):
    """runs: str | list[str | (str, dict)] -> één paragraaf per item."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    if name:
        tb.name = name
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.04)
    tf.margin_top = tf.margin_bottom = Inches(0.02)
    tf.vertical_anchor = anchor
    items = runs if isinstance(runs, list) else [runs]
    for i, it in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(space)
        segs = it if isinstance(it, tuple) and isinstance(it[0], list) else None
        parts = [it] if not isinstance(it, list) else it
        for part in parts:
            t, o = (part, {}) if isinstance(part, str) else part
            r = p.add_run()
            r.text = nb(("• " if bullets and part is parts[0] else "") + t)
            f = r.font
            f.name = o.get("font", font)
            f.size = Pt(o.get("size", size))
            f.bold = o.get("bold", bold)
            f.italic = o.get("italic", False)
            f.color.rgb = rgb(o.get("color", color))
    return tb


def box(slide, x, y, w, h, fill=CARD, line=None, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid(); s.fill.fore_color.rgb = rgb(fill)
    if line:
        s.line.color.rgb = rgb(line); s.line.width = Pt(1)
    else:
        s.line.fill.background()
    s.shadow.inherit = False
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = radius
    return s


def img(slide, path, x, y, w=None, h=None):
    kw = {}
    if w: kw["width"] = Inches(w)
    if h: kw["height"] = Inches(h)
    return slide.shapes.add_picture(path, Inches(x), Inches(y), **kw)


def chart(slide, name, x, y, w=None, h=None):
    return img(slide, os.path.join(CH, name), x, y, w, h)


def new(title, source=None, dark=False):
    s = prs.slides.add_slide(BLANK)
    N[0] += 1
    bg(s, DARK if dark else WHITE)
    text(s, 0.6, 0.38, 12.1, 1.05, title, size=26, bold=True, font=HEAD,
         color=WHITE if dark else INK, anchor=MSO_ANCHOR.TOP, name="Titel")
    if source:
        text(s, 0.6, 7.0, 11.0, 0.32, "Bron: " + source, size=10, color="AEB6BA" if dark else MUTED, name="Bron")
    text(s, 12.15, 7.0, 0.6, 0.32, str(N[0]), size=10, color="AEB6BA" if dark else MUTED, align=PP_ALIGN.RIGHT)
    return s


def table(slide, x, y, w, rows, colw=None, size=12, header_fill=DARK, rowh=0.34, first_bold=False, fills=None):
    nr, nc = len(rows), len(rows[0])
    gt = slide.shapes.add_table(nr, nc, Inches(x), Inches(y), Inches(w), Inches(rowh * nr)).table
    if colw:
        for j, cw in enumerate(colw):
            gt.columns[j].width = Inches(cw)
    for i, row in enumerate(rows):
        gt.rows[i].height = Inches(rowh)
        for j, val in enumerate(row):
            c = gt.cell(i, j)
            c.margin_left = c.margin_right = Inches(0.06)
            c.margin_top = c.margin_bottom = Inches(0.03)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = c.text_frame; tf.word_wrap = True
            p = tf.paragraphs[0]
            r = p.add_run(); r.text = nb(str(val))
            r.font.name = BODY; r.font.size = Pt(size)
            c.fill.solid()
            if i == 0:
                c.fill.fore_color.rgb = rgb(header_fill)
                r.font.bold = True; r.font.color.rgb = rgb(WHITE)
            else:
                f = (fills or {}).get((i, j))
                c.fill.fore_color.rgb = rgb(f if f else (CARD if i % 2 == 0 else WHITE))
                r.font.color.rgb = rgb(WHITE if f else INK)
                r.font.bold = bool(f) or (first_bold and j == 0)
    return gt


def pill(slide, x, y, w, label, color, size=12):
    b = box(slide, x, y, w, 0.34, fill=color, radius=0.5)
    tf = b.text_frame; tf.margin_left = tf.margin_right = Inches(0.05)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = label
    r.font.name = BODY; r.font.size = Pt(size); r.font.bold = True; r.font.color.rgb = rgb(WHITE)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    return b


def stat(slide, x, y, w, big, small, color=EMBER, h=1.55, bigsize=34):
    box(slide, x, y, w, h)
    text(slide, x + 0.18, y + 0.12, w - 0.3, 0.75, big, size=bigsize, bold=True, font=HEAD, color=color)
    off = 0.2 + bigsize * 0.018
    text(slide, x + 0.18, y + off, w - 0.3, h - off - 0.05, small, size=12.5, color=INK)


def card(slide, x, y, w, h, head, lines, headcolor=INK, size=13, fill=CARD):
    box(slide, x, y, w, h, fill=fill)
    text(slide, x + 0.18, y + 0.12, w - 0.34, 0.45, head, size=15, bold=True, color=headcolor)
    text(slide, x + 0.18, y + 0.58, w - 0.34, h - 0.65, lines, size=size, bullets=True, space=4)


# ---------- 1 Titel -----------------------------------------------------------
s = prs.slides.add_slide(BLANK); N[0] += 1; bg(s, DARK)
text(s, 0.8, 1.7, 11.5, 1.4, "Accudetectie bij de inworpzuil", size=46, bold=True, font=HEAD, color=WHITE)
text(s, 0.8, 3.0, 11.5, 1.0, "Productontwerp, tests en advies over een abonnement voor gemeenten",
     size=22, color="D8DEE0")
text(s, 0.8, 4.4, 11.5, 0.5, "Oktober 2026  ·  Multi-agent ontwerpteam: 8 specialisten + orchestrator  ·  4 sparringrondes",
     size=14, color="AEB6BA")
for i, (lab, col) in enumerate([("Risico", EMBER), ("Inductie", "4A5A5E"), ("Röntgen", "4A5A5E"),
                                ("Thermisch/gas", "4A5A5E"), ("Hardware", "4A5A5E"), ("Software", "4A5A5E"),
                                ("Business", "4A5A5E"), ("Red team", EMBER)]):
    pill(s, 0.8 + i * 1.47, 5.4, 1.37, lab, col, size=11)
text(s, 0.8, 6.7, 11.5, 0.4, "Prijspeil EUR 2026 excl. btw · energie in Wh · bandbreedtes laag / basis / hoog",
     size=11, color="AEB6BA")

# ---------- 2 Executive summary -----------------------------------------------
s = new("Advies: start geen abonnement op een accudetector in de zuil; investeer in de wagen en in preventie",
        "debate/R4_scorekaart.md, R4_redteam.md; experiments/r3_classificatie, r3_business")
tiles = [
    ("Aanbevolen", "Geen zuildetector als product", "Conditioneel: thermische camera boven de laadbak (inzamelaar) en accu-brievenbus aan de zuil (betaald door de producentenorganisatie)", TEAL),
    ("Detectie", "Inductie ziet staal, geen lithium", "Strandmetaaldetector: PPV 5 %. Röntgen ziet cellen (PPV 28 %), maar kost EUR 90 per maand per zuil", EMBER),
    ("Drempel", "Pakket ≥ 20 Wh-eq als rangorde", "95 % van de ledigingen bevat al lithium. Werkbaar is ≤ 20 meldingen per 1.000 ledigingen", INK),
    ("Prijs", "EUR 5,7–18,6 per container/mnd", "Zuilabonnement bij 10.000 containers, tegenover EUR 0,08–0,31 vermeden schade per maand", EMBER),
]
for i, (k, h, d, c) in enumerate(tiles):
    x = 0.6 + i * 3.08
    box(s, x, 1.65, 2.9, 3.1)
    text(s, x + 0.2, 1.8, 2.5, 0.35, k.upper(), size=11, bold=True, color=MUTED)
    text(s, x + 0.2, 2.15, 2.55, 1.0, h, size=19, bold=True, font=HEAD, color=c)
    text(s, x + 0.2, 3.25, 2.55, 1.9, d, size=13)
box(s, 0.6, 5.0, 12.13, 1.6, fill=DARK)
text(s, 0.85, 5.1, 11.7, 1.4, [
    [("MVP binnen 3–6 maanden: ", {"bold": True, "color": WHITE}),
     ("één meet-zuil (PI-lussen + IR/CO onder het deksel) als go/no-go, EUR 37k / 62k / 102k. ", {"color": WHITE}),
     ("Go alleen bij AUC ≥ 0,85 en PPV ≥ 30 % in een echte RVS-trommel; de modellen verwachten AUC 0,56–0,6.", {"color": "D8DEE0"})]],
     size=16, anchor=MSO_ANCHOR.MIDDLE)

# ---------- 3 Probleem ---------------------------------------------------------
s = new("Accubranden zijn reëel en nemen toe, maar ontstaan vooral bij het persen in de wagen",
        "NOS/NVRD 2023; Vereniging Afvalbedrijven; TK 2026D41104; Stichting OPEN 2026-04; raadsbesluit Oosterhout 2023")
stats = [("≥ 3 / mnd", "branden in vuilniswagens in NL (NVRD)"), ("~120 / jaar", "branden bij inzameling (Ver. Afvalbedrijven)"),
         ("38 %", "van branden bij verwerkers toegeschreven aan batterijen"), ("> 100 mln", "batterijen per jaar in het restafval (2025)"),
         ("EUR 250–475k", "nieuwe vuilniswagen, diesel tot elektrisch")]
for i, (b_, sm) in enumerate(stats):
    stat(s, 0.6 + i * 2.45, 1.55, 2.3, b_, sm, bigsize=21 if len(b_) > 10 else 30)
steps = [("Thuis", "laag", GOOD), ("Zuil / trommel", "laag", GOOD), ("Container\n(dagen)", "middel", WARN),
         ("Lediging", "laag–middel", WARN), ("Persen in\nwagen", "hoog", CRIT), ("Bunker /\noverslag", "hoog", CRIT),
         ("Shredder /\nAVI", "hoog", CRIT)]
text(s, 0.6, 3.45, 12, 0.4, "Route van inworp tot verwerking: waar ontstaat de brand?", size=15, bold=True)
for i, (lab, risk, col) in enumerate(steps):
    x = 0.6 + i * 1.75
    b = box(s, x, 4.0, 1.55, 1.15, fill=CARD)
    text(s, x + 0.05, 4.07, 1.45, 0.75, lab, size=13, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    pill(s, x + 0.12, 4.75, 1.31, risk, col, size=11)
    if i < len(steps) - 1:
        a = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x + 1.57), Inches(4.45), Inches(0.16), Inches(0.25))
        a.fill.solid(); a.fill.fore_color.rgb = rgb(LINE); a.line.fill.background()
text(s, 0.6, 5.45, 12.1, 1.3, [
    [("Gevolg voor het product: ", {"bold": True}),
     ("een cel ontsteekt meestal pas als de persplaat haar plet (TR binnen 0–30 s). Een detector in de zuil kan dus alleen waarschuwen; hij voorkomt de brand niet zelf.", {})]],
     size=15)

# ---------- 4 Het idee ---------------------------------------------------------
s = new("Het idee: de zak ligt 1–10 s stil in de trommel, dus daar kun je rustig en goedkoop meten",
        "Opdrachtgever; product/montage.png (A5); toetsing: debate/R4_scorekaart.md")
img(s, os.path.join(ROOT, "product", "montage.png"), 0.6, 1.45, h=5.4)
text(s, 5.8, 1.5, 7, 0.4, "Vijf uitgangspunten van de opdrachtgever, getoetst", size=16, bold=True)
up = [("1  Stilstand maakt goedkope sensoren mogelijk", "DEELS", WARN, "Helpt röntgen (0,2–14 s), maar inductie wint niets boven 0,3 s"),
      ("2  Een risicodrempel volstaat", "KLOPT", GOOD, "Maar per container moeilijk: 95 % van de ledigingen bevat al lithium"),
      ("3  Een strandmetaaldetector is het eenvoudigst", "VERWORPEN", CRIT, "Ziet staal; 18650 ≈ AA-alkaline; PPV 5 %"),
      ("4  Melding aan de ophaaldienst", "DEELS", WARN, "Alleen waardevol als er wordt ingegrepen; melden kost EUR 10–150"),
      ("5  Abonnement per gemeente of container", "VERWORPEN", CRIT, "Prijs 70–130× hoger dan de vermeden schade")]
for i, (h, v, c, d) in enumerate(up):
    y = 2.05 + i * 0.96
    box(s, 5.8, y, 6.93, 0.86)
    text(s, 5.98, y + 0.07, 4.9, 0.38, h, size=14, bold=True)
    text(s, 5.98, y + 0.43, 5.2, 0.4, d, size=12, color=MUTED)
    pill(s, 11.25, y + 0.25, 1.35, v, c, size=11)

# ---------- 5 Risicobenchmark ---------------------------------------------------
s = new("Grote packs maken een container gevaarlijk: 5 % van de Li-items draagt 58 % van het risico",
        "experiments/r3_risico (A1): Pareto, brandkansmodel P = 1 − exp(−k·Wh-eq), k gekalibreerd op NL-branddata")
chart(s, "c01_pareto.png", 0.5, 1.45, w=6.4)
text(s, 7.2, 1.45, 5.5, 0.4, "Risicoscore R = Σ Wh × w_chemie × w_toestand (Wh-eq)", size=14, bold=True)
table(s, 7.2, 1.95, 5.5, [
    ["", "Per inworp", "Per container", "Actie"],
    ["Groen", "< 50", "< 75", "niets"],
    ["Oranje", "≥ 50", "≥ 75", "laatste in de route"],
    ["Rood", "≥ 75–100", "≥ 150 of brandsignaal", "apart legen, niet persen"]],
    colw=[0.9, 1.1, 1.75, 1.75], size=12, fills={(1, 0): GOOD, (2, 0): WARN, (3, 0): CRIT})
for i, (b_, sm) in enumerate([("95 %", "van de ledigingen bevat al ≥ 1 Li-item: 'accu aanwezig' zegt dus niets"),
                              ("1,4", "brand per 1.000 containers per jaar (basis; band 0,3–11)"),
                              ("σ ≤ 0,5", "maximale Wh-schattingsfout; anders 2–5× zoveel alarmen")]):
    stat(s, 7.2 + i * 1.86, 3.65, 1.74, b_, sm, h=2.05, bigsize=26)
text(s, 7.2, 5.85, 5.5, 0.9, "Drempels na Ronde 3 verhoogd: met de oorspronkelijke drempels (10/50 Wh-eq) zou bijna elke container oranje kleuren.",
     size=12, color=MUTED)

# ---------- 6 Wat meetbaar is -----------------------------------------------------
s = new("Een accu zendt niets uit: meetbaar zijn alleen staal, folie, dichtheid, warmte en gas",
        "research/A2–A4; experiments/r3_inductie, r3_rontgen, r3_thermisch")
rows = [["Principe", "Wat het meet", "Li vs blik/folie", "Li vs alkaline", "Aantal / Wh", "Oordeel"],
        ["Inductie (VLF, PI)", "stalen huls, Cu/Al-folie", "zwak (AUC 0,56–0,59)", "nee: 18650 ≈ AA", "nee (σ 0,7; positie 171×)", "zwak"],
        ["Röntgen ≤ 30 kV", "dichtheid × Z, vorm", "ja: blik/folie transparant", "nee (R 1,19 vs 1,20)", "ja, via vorm/aantal", "werkt, duur"],
        ["Thermisch (IR)", "warmte aan oppervlak", "alleen bij TR", "n.v.t.", "nee", "alleen brand"],
        ["Gas (CO, H₂, VOC)", "uitgassing, venting", "rotting stoort", "n.v.t.", "nee", "alleen brand"],
        ["Gewicht / vulgraad", "massa per inworp", "nee", "nee", "nee", "ondersteunend"],
        ["Radar / capacitief", "diëlektrisch, metaal", "nee", "nee", "nee", "ongeschikt"]]
fills = {(1, 5): WARN, (2, 5): TEAL, (3, 5): MUTED, (4, 5): MUTED, (5, 5): MUTED, (6, 5): CRIT}
table(s, 0.6, 1.55, 12.13, rows, colw=[2.0, 2.3, 2.3, 2.0, 2.2, 1.33], size=13, rowh=0.55, first_bold=True, fills=fills)
text(s, 0.6, 5.65, 12.1, 1.1, [[("Kern: ", {"bold": True}),
     ("geen goedkoop principe onderscheidt lithium van alkaline. Wat wel kan: grote metalen pakketten herkennen (röntgen goed, inductie zwak) en een brand detecteren zodra die begint (warmte, gas).", {})]],
     size=15)

# ---------- 7 Sparren -------------------------------------------------------------
s = new("Van 43 ideeën naar 5 testconcepten en 2 benchmarks, na ~80 aanvallen",
        "debate/R1_*, R2_*_aanvallen, R2b_*_verdediging, R2_shortlist.md")
funnel = [("43", "concepten in Ronde 1", "8 agents, elk ≥ 1 radicaal eenvoudig en ≥ 1 onconventioneel concept"),
          ("~80", "aanvallen in Ronde 2", "op fysica, kosten, energie, regelgeving en praktijk; elke agent op ≥ 2 anderen"),
          ("14 / 23", "ingetrokken / verbeterd", "o.a. PI-klikker, röntgen per zuil, smeltdraad, shared savings"),
          ("5 + 2", "getest in Ronde 3", "K1–K5 plus de benchmarks camera op de wagen (B1) en geen sensor (B0)")]
for i, (b_, h, d) in enumerate(funnel):
    w = 5.6 - i * 0.55
    x = 0.6 + i * 0.275
    y = 1.5 + i * 1.3
    box(s, x, y, w, 1.15, fill=DARK if i == 3 else CARD)
    text(s, x + 0.2, y + 0.12, 1.5, 0.9, b_, size=26, bold=True, font=HEAD, color=EMBER if i < 3 else WHITE, anchor=MSO_ANCHOR.MIDDLE)
    text(s, x + 1.75, y + 0.1, w - 1.9, 0.4, h, size=14, bold=True, color=WHITE if i == 3 else INK)
    text(s, x + 1.75, y + 0.48, w - 1.9, 0.65, d, size=11.5, color="D8DEE0" if i == 3 else MUTED)
short = [("K1", "Strandmetaaldetector (VLF) in trommel", "opdrachtgever"), ("K2", "Pakketwachter: PI-lussen, OEM op pas-zuil", "A2 + A1 + A5"),
         ("K3", "Röntgen ≤ 30 kV: vast (a) / ijkpaal (b)", "A3"), ("K4", "Deksel-eventmodule: IR + CO", "A4"),
         ("K5", "Hybride K2 + K4 + actieprotocol", "A1 + A6"), ("B1", "Benchmark: thermische camera laadbak", "A5, A7, A8"),
         ("B0", "Benchmark: geen sensor, accu-brievenbus", "A6, A8")]
text(s, 6.75, 1.5, 6, 0.4, "Shortlist voor de tests", size=15, bold=True)
for i, (k, n, o) in enumerate(short):
    y = 1.95 + i * 0.68
    pill(s, 6.75, y + 0.1, 0.65, k, EMBER if k.startswith("K") else TEAL, size=12)
    text(s, 7.55, y + 0.04, 3.9, 0.5, n, size=13.5, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 11.35, y + 0.04, 1.4, 0.5, o, size=11, color=MUTED, anchor=MSO_ANCHOR.MIDDLE)

# ---------- 8 Strandmetaaldetector -------------------------------------------------
s = new("De strandmetaaldetector ziet staal, geen lithium: hij meldt 13 % van de 18650's, bij 2 % vals alarm",
        "experiments/r3_inductie (A2): dipool-/eddy-currentmodel, 6 frequenties + PI-verval, zakken met gem. 5,9 metaalobjecten")
chart(s, "c03_inductie.png", 0.5, 1.45, w=6.9)
facts = [("0,56–0,59", "AUC cel/telefoon/vape vs gewone zak: nauwelijks beter dan toeval"),
         ("171×", "spreiding van het signaal door de positie in de trommel: Wh is niet te schatten"),
         ("> 0,3 s", "langer meten helpt niet; ander metaal in de zak is de grens, niet ruis")]
for i, (b_, d) in enumerate(facts):
    stat(s, 7.75, 1.5 + i * 1.5, 4.98, b_, d, h=1.35, bigsize=26)
box(s, 7.75, 6.05, 4.98, 0.75, fill=DARK)
text(s, 7.95, 6.1, 4.6, 0.65, [[("Uitgangspunt 3 verworpen. ", {"bold": True, "color": WHITE}),
     ("Alleen e-bike-packs vallen op; vapes zijn onzichtbaar.", {"color": "D8DEE0"})]], size=13, anchor=MSO_ANCHOR.MIDDLE)

# ---------- 9 Röntgen ---------------------------------------------------------------
s = new("Röntgen ziet cellen wél, maar stilstand maakt het niet goedkoop: EUR 90 per container per maand",
        "experiments/r3_rontgen (A3): NIST XCOM, Beer-Lambert, fotonbudget, dosis; Bbs art. 3.18 (te bevestigen door stralingsdeskundige)")
chart(s, "c04_rontgen_transmissie.png", 0.5, 1.45, w=6.1)
chart(s, "c05_rontgen_tijd.png", 6.8, 1.45, w=5.9)
for i, (h, d, c) in enumerate([("Vergunningsvrij mogelijk", "≤ 30 kV en ≤ 1 µSv/h op 0,1 m; 3 mm stalen zuilwand schermt ruim af", TEAL),
                               ("Geen chemie", "Li-ion vs alkaline niet te scheiden: dual-energy R 1,19 vs 1,20", EMBER),
                               ("Niet off-grid", "1,2–5,5 Wh per dag; HW EUR 1.785 per zuil", EMBER)]):
    x = 0.6 + i * 4.08
    box(s, x, 5.55, 3.9, 1.25)
    text(s, x + 0.18, 5.62, 3.6, 0.4, h, size=14, bold=True, color=c)
    text(s, x + 0.18, 6.0, 3.6, 0.8, d, size=12)

# ---------- 10 Thermisch / gas ------------------------------------------------------
s = new("Continue monitoring ziet brand, geen accu: vóór thermal runaway waarschuwt hij in 0–5 % van de gevallen",
        "experiments/r3_thermisch (A4): 1D-warmte/gas-diffusie, vals-alarm-MC; Li-ion Tamer (DNV-GL); Seek Thermal/Goodyear 2025")
chart(s, "c06_tijdlijn.png", 0.5, 1.5, w=7.0)
rows = [["Deksel-eventmodule (K4)", "laag / basis / hoog"],
        ["Brand gezien binnen 60 min", "48 / 100 / 100 %"],
        ["Vals alarm alleen CO > 50 ppm", "2 / 10 / 36 per jaar"],
        ["Met regel IR + CO + stijgsnelheid", "≈ 0 (veld bevestigen)"],
        ["Hete as, peuken, vuurwerk", "0,5 / 1,9 / 4,2 per jaar"],
        ["IR ziet tot diepte", "0,13 m vape – 0,35 m pack"],
        ["Camera laadbak (B1): wagenbrand", "19 / 49 / 76 % in ~1 s"]]
table(s, 7.8, 1.55, 4.93, rows, colw=[2.9, 2.03], size=12, rowh=0.46)
text(s, 0.6, 4.95, 7.0, 1.4, [[("Waarom: ", {"bold": True}),
     ("afval isoleert sterk (0,5 m ≈ 19 dagen warmtetransport) en bij het persen is er geen venster. Een continue sensor is dus een brandmelder voor de container, geen accudetector.", {})]],
     size=14)

# ---------- 11 Testresultaten -------------------------------------------------------
s = new("Bij een werkbare meldingslast vangt zelfs een perfecte zuilsensor maar 15 % van het risico",
        "experiments/r3_classificatie (A6): Monte Carlo met zakinhoud (params.py), sensormodellen A2/A3, brandkans A1, 3 scenario's")
chart(s, "c07_recall_meldingen.png", 0.5, 1.45, w=6.6)
chart(s, "c08_inworp.png", 7.3, 1.45, w=5.4)
text(s, 7.3, 5.25, 5.4, 0.3, "Per inworp: aandeel Li-zakken gemeld (recall) en juiste meldingen (PPV)", size=11, color=MUTED)
text(s, 0.6, 5.95, 12.1, 0.9, [[("Lezen: ", {"bold": True}),
     ("bij 20 meldingen per 1.000 ledigingen vangt K1 3,6 % van de risico-energie, K2 4,4 %, geen sensor (B0) 4,4 %, röntgen 9,3 % en perfect 15 %. Inductie doet het dus niet beter dan helemaal geen sensor.", {})]],
     size=14)


# ---------- 12–15 per concept --------------------------------------------------------
def concept_slide(title, source, blocks):
    s = new(title, source)
    n = len(blocks)
    w = (12.13 - 0.25 * (n - 1)) / n
    for i, b in enumerate(blocks):
        x = 0.6 + i * (w + 0.25)
        box(s, x, 1.5, w, 5.3)
        text(s, x + 0.2, 1.62, w - 0.4, 0.45, b["id"] + "  " + b["naam"], size=16, bold=True, font=HEAD)
        text(s, x + 0.2, 2.1, w - 0.4, 0.8, b["ontwerp"], size=12, color=MUTED)
        table(s, x + 0.2, 2.95, w - 0.4, [["Kosten", "Basis"]] + b["kosten"], colw=[(w - 0.4) * 0.62, (w - 0.4) * 0.38],
              size=11.5, rowh=0.3)
        y = 2.95 + 0.3 * (len(b["kosten"]) + 1) + 0.15
        text(s, x + 0.2, y, w - 0.4, 0.35, f"Score {b['score']}  ·  betrouwbaarheid {b['betr']}", size=12, bold=True)
        text(s, x + 0.2, y + 0.38, w - 0.4, 6.2 - y - 0.38, b["arg"], size=12, bullets=True, space=3)
        pill(s, x + 0.2, 6.3, w - 0.4, b["oordeel"], b["kleur"], size=12)
    return s


concept_slide("K1 en K2: inductie is het goedkoopst, maar meldt vooral blikken en alkaline",
              "product/BOM_K1.csv, BOM_K2.csv (A5); experiments/r3_business (A7); r3_inductie (A2); debate/R4_scorekaart.md",
              [dict(id="K1", naam="Strandmetaaldetector", ontwerp="VLF op 2–3 frequenties, meedraaiende DD-spoel in PE-liner, D-cel Li-SOCl₂ (13 mWh/dag), LTE-M",
                    kosten=[["Hardware per zuil", "EUR 137"], ["Installatie", "EUR 60"], ["TCO per container/mnd", "EUR 2,64"],
                            ["Abonnement @1.000 / @10.000", "EUR 14,6 / 9,3"], ["Vermeden schade/mnd", "EUR 0,07"]],
                    score="2,55", betr="hoog", oordeel="NIET AANBEVOLEN (knock-out)", kleur=CRIT,
                    arg=["Ziet staal: 18650 ≈ AA, PPV 5 %", "Recall Li-zak 5 %; vapes onzichtbaar", "Wel goedkoop en 6–14 jaar op een D-cel"]),
               dict(id="K2", naam="Pakketwachter", ontwerp="2 PI-lussen + ferro-kanaal in liner; klassen geen / cel / pakket ≥ 20 Wh-eq; meelift op accu en modem van de pas-zuil",
                    kosten=[["Hardware per zuil", "EUR 91"], ["Installatie", "EUR 45"], ["TCO per container/mnd", "EUR 1,50"],
                            ["Abonnement @1.000 / @10.000", "EUR 10,7 / 5,7"], ["Vermeden schade/mnd", "EUR 0,08"]],
                    score="2,52", betr="middel", oordeel="NIET AANBEVOLEN (knock-out)", kleur=CRIT,
                    arg=["Pakketrecall 8–12 %, PPV 4 %", "Op containerniveau gelijk aan geen sensor (B0)", "Laagste kostprijs; NRE OEM-adapter EUR 50–150k"])])

concept_slide("K3: röntgen werkt fysiek, maar is als product per zuil 300× te duur",
              "product/BOM_K3a.csv, BOM_K3b.csv (A5); experiments/r3_rontgen (A3), r3_business (A7)",
              [dict(id="K3a", naam="Röntgen vast per zuil", ontwerp="30 kV-buis 4 W + GOS-scherm + camera achter PE-venster in trommel; interlock op klep; zonnepaneel 20–50 Wp of net",
                    kosten=[["Hardware per zuil", "EUR 1.785"], ["Installatie", "EUR 650"], ["TCO per container/mnd", "EUR 40,6"],
                            ["Abonnement @1.000 / @10.000", "EUR 90 / 78"], ["Vermeden schade/mnd", "EUR 0,18"]],
                    score="2,00", betr="middel", oordeel="NIET AANBEVOLEN (knock-out)", kleur=CRIT,
                    arg=["Pakketrecall 82 %, PPV pakket 34 %", "Li en alkaline niet te scheiden", "1,2–5,5 Wh per dag: niet off-grid haalbaar"]),
               dict(id="K3b", naam="Röntgen-ijkpaal", ontwerp="Zelfde hardware, rouleert langs 20–50 containers; levert grondwaarheid om goedkope sensoren te ijken en voor risicokaarten",
                    kosten=[["Hardware per unit", "EUR 1.785"], ["Containers per unit", "35"], ["TCO per container/mnd", "EUR 9,7"],
                            ["Abonnement @1.000 / @10.000", "EUR 26,7 / 20,6"], ["Als campagne per gemeente", "EUR 5–15k"]],
                    score="2,50", betr="middel", oordeel="ALLEEN ALS MEETINSTRUMENT", kleur=MUTED,
                    arg=["Geen schadebesparing als abonnement", "Waardevol als ijkdata in pilot", "Kandidaat als EPR-lekmeting verplicht wordt"])])

concept_slide("K4 en K5: een brandmelder in de container is goedkoop, maar geen accudetector",
              "product/BOM_K4.csv, BOM_K5.csv (A5); experiments/r3_thermisch (A4), r3_business (A7)",
              [dict(id="K4", naam="Deksel-eventmodule", ontwerp="8×8 IR-thermopile + passieve CO-cel + NTC onder containerkop; regel stijgsnelheid + 2-van-3; 12 mWh/dag, ~10 jaar op D-cel",
                    kosten=[["Hardware", "EUR 103"], ["Installatie", "EUR 30"], ["Los abonnement @1.000", "EUR 13,9"],
                            ["Als add-on @1.000 / @10.000", "EUR 3,6 / 2,2"], ["Vermeden schade/mnd", "EUR 0,31"]],
                    score="3,30 los · 3,65 add-on", betr="laag–middel", oordeel="CONDITIONEEL: add-on, hotspots", kleur=TEAL,
                    arg=["Ziet brand binnen 60 min; accu vooraf vrijwel nooit", "Break-even ≥ 15 branden/1.000 containerjaar", "Alleen meeliften op bestaande vulgraadsensor"]),
               dict(id="K5", naam="Hybride K2 + K4", ontwerp="Pakketwachter in de zuil + K4-lite onder deksel via BLE; twee kanalen: rangorde en brand-event; actieprotocol oranje/rood",
                    kosten=[["Hardware", "EUR 188"], ["Installatie", "EUR 75"], ["TCO per container/mnd", "EUR 3,14"],
                            ["Abonnement @1.000 / @10.000", "EUR 18,6 / 10,4"], ["Vermeden schade/mnd", "EUR 0,08"]],
                    score="2,23", betr="middel", oordeel="NIET AANBEVOLEN (knock-out)", kleur=CRIT,
                    arg=["Erft vals alarm van K2", "Duurste inductieconcept", "Behouden idee: twee gescheiden meldkanalen"])])

concept_slide("De benchmarks winnen: camera op de wagen en preventie aan de zuil",
              "product/BOM_B1.csv, BOM_B0.csv (A5); experiments/r3_thermisch/b1, r3_business (A7); r3_redteam (A8)",
              [dict(id="B1", naam="Thermische camera laadbak", ontwerp="Radiometrische camera boven de laadbak, 24 V boordnet; alarm bij ΔT/dt; chauffeur dumpt de lading (bestaand draaiboek)",
                    kosten=[["Hardware per wagen", "EUR 2.050"], ["Containers per wagen", "~300"], ["Fabrieksoptie @1.000 / @10.000", "EUR 2,3 / 0,97"],
                            ["Als los abonnement @1.000", "EUR 8,4"], ["Vermeden schade/mnd", "EUR 1,35"]],
                    score="4,00 (OEM)", betr="middel", oordeel="CONDITIONEEL: ≥ 10 wagens, OEM", kleur=TEAL,
                    arg=["Meet waar het risico ontstaat; 19–76 % in ~1 s", "Rendabel vanaf ~3.000 containers", "Koper is de inzamelaar (67 % van de baat)"]),
               dict(id="B0", naam="Accu-brievenbus aan zuil", ontwerp="Brandwerende RVS-sleuf aan de zuil voor losse batterijen en vapes; lediging via Stibat; geen beloning, geen pas",
                    kosten=[["Hardware", "EUR 40"], ["Installatie", "EUR 40"], ["Met sortering @1.000", "EUR 23,1"],
                            ["Zonder sortering", "lager [A]"], ["Vermeden schade/mnd", "EUR 0,44"]],
                    score="3,40", betr="laag", oordeel="CONDITIONEEL: PRO betaalt", kleur=TEAL,
                    arg=["Verlaagt prevalentie, geen vals alarm", "Effect niet gemeten: 2 × 1 t sorteren nodig", "Betaler: Stichting OPEN (inzameldoel 63 %)"])])

# ---------- 16 Vergelijking ---------------------------------------------------------
s = new("Geen zuilconcept haalt 3,5 zonder knock-out; de camera op de wagen scoort het hoogst",
        "experiments/r4_scorekaart/scorekaart.py; debate/R4_scorekaart.md")
chart(s, "c09_scores.png", 0.5, 1.45, w=7.4)
table(s, 8.2, 1.55, 4.53, [["Criterium", "Gewicht"], ["Detectie vs benchmark", "25 %"], ["Kostprijs en abonnement", "20 %"],
                            ["Eenvoud en bouwbaarheid", "15 %"], ["Inpasbaarheid en energie", "15 %"], ["Juridisch: straling, AVG, CE", "10 %"],
                            ["Waarde voor gemeente", "15 %"]], colw=[3.3, 1.23], size=12.5, rowh=0.4)
text(s, 8.2, 4.55, 4.53, 2.2, [[("Knock-outs: ", {"bold": True}), ("discriminatie (K1), vals alarm (K2, K5), prijs en energie (K3a), geen accudetector (K4 los). ", {})],
                              [("Regel: ", {"bold": True}), ("AANBEVOLEN vereist ≥ 3,5 én geen knock-out. Ook de camera op de wagen is als los abonnement bij 1.000 containers te duur.", {})]],
     size=13)

# ---------- 17 Product visueel -------------------------------------------------------
s = new("Wat we wél bouwen: één meet-zuil die in 3–6 maanden beslist of inductie een kans heeft",
        "product/ontwerp.md, montage.png, blokschema.png (A5); experiments/r3_signaal (A6); debate/R4_scorekaart.md")
img(s, os.path.join(ROOT, "product", "montage.png"), 0.6, 1.45, h=5.35)
parts = [("1", "PE-liner met 2 PI-lussen", "in de RVS-trommel, draait mee; logt ruwe vervalcurves"),
         ("2", "Module in zuilkop", "STM32 + PI-front-end; voeding van de pas-zuil-accu; fail-open"),
         ("3", "K4-lite onder deksel", "8×8 IR + CO + NTC; BLE naar de zuilmodule"),
         ("4", "Data naar dashboard", "13-byte LoRaWAN/LTE-M-bericht; TTN-decoder en mock aanwezig"),
         ("5", "Grondwaarheid", "62 gespikete zakken per klasse + 300 echte zakken sorteren")]
for i, (n_, h, d) in enumerate(parts):
    y = 1.5 + i * 0.86
    b = box(s, 5.75, y + 0.08, 0.5, 0.5, fill=EMBER, shape=MSO_SHAPE.OVAL)
    text(s, 5.75, y + 0.12, 0.5, 0.42, n_, size=15, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 6.45, y, 6.3, 0.4, h, size=14.5, bold=True)
    text(s, 6.45, y + 0.38, 6.3, 0.45, d, size=12.5, color=MUTED)
box(s, 5.75, 5.95, 6.98, 0.85, fill=DARK)
text(s, 5.95, 6.0, 6.6, 0.75, [[("Kosten EUR 37k / 62k / 102k. ", {"bold": True, "color": WHITE}),
     ("Go bij AUC ≥ 0,85 en PPV ≥ 30 % (pakket ≥ 20 Wh-eq, ≤ 2 % zakken gemeld).", {"color": "D8DEE0"})]],
     size=13.5, anchor=MSO_ANCHOR.MIDDLE)

# ---------- 18 Detectie naar actie --------------------------------------------------
s = new("Een melding helpt alleen als iemand ingrijpt, en elke ingreep kost EUR 10–150",
        "research/A6_software.md; experiments/r3_signaal (A6); r3_business alarm_cost (A7); debate/R4_redteam.md")
flow = [("Meting", "inworp of continu"), ("Score", "per container, reset bij lediging"), ("Bericht", "13 B LoRaWAN / LTE-M"),
        ("Dashboard", "kaart + lijst per route"), ("Boordcomputer", "via vulgraad-API (bijv. HVC)")]
for i, (h, d) in enumerate(flow):
    x = 0.6 + i * 2.47
    box(s, x, 1.55, 2.2, 1.1, fill=DARK)
    text(s, x + 0.1, 1.62, 2.0, 0.45, h, size=15, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    text(s, x + 0.1, 2.05, 2.0, 0.55, d, size=11.5, color="D8DEE0", align=PP_ALIGN.CENTER)
    if i < 4:
        a = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x + 2.22), Inches(1.98), Inches(0.22), Inches(0.26))
        a.fill.solid(); a.fill.fore_color.rgb = rgb(LINE); a.line.fill.background()
table(s, 0.6, 3.0, 7.4, [["Niveau", "Wat de ophaaldienst doet", "Kosten per keer"],
                         ["Groen", "niets, alleen statistiek", "EUR 0"],
                         ["Oranje", "container als laatste legen, niet extra persen", "EUR 10–30 [A]"],
                         ["Rood", "apart legen zonder persen of bovenkant controleren", "EUR 50–150 [A]"],
                         ["Brand (B1/K4)", "lading dumpen of niet legen; brandweerprotocol", "bestaand draaiboek"]],
      colw=[1.4, 4.3, 1.7], size=12.5, rowh=0.5, fills={(1, 0): GOOD, (2, 0): WARN, (3, 0): CRIT, (4, 0): INK})
for i, (b_, d) in enumerate([("EUR 0", "vermeden schade bij alleen melden, zonder ingreep"),
                             ("EUR 42", "per container per jaar aan vervolgacties (20 meldingen per 1.000 ledigingen)")]):
    stat(s, 8.3, 3.0 + i * 1.35, 4.43, b_, d, h=1.25, bigsize=26)
text(s, 0.6, 5.8, 12.1, 1.0, [[("AVG: ", {"bold": True}),
     ("een alarm per container bevat geen persoonsgegevens. Koppeling aan de pashouder vraagt een DPIA en is bij 93–95 % valse meldingen niet proportioneel (AP 2017). Dus geen pas-koppeling.", {})]],
     size=14)

# ---------- 19 Abonnementsmodel -------------------------------------------------------
s = new("Een zuilabonnement kost bij 10.000 containers nog EUR 5,7–18,6 per maand: 70× de vermeden schade",
        "experiments/r3_business (A7): 6 jaar levensduur, 40 % brutomarge, NRE, support, CAC; BOM A5")
chart(s, "c11_schaal.png", 0.5, 1.45, w=6.6)
table(s, 7.4, 1.55, 5.33, [["K2 bij 1.000 containers", "EUR/c/mnd"], ["Hardware", "1,01"], ["Installatie", "0,53"],
                            ["Connectiviteit", "0,20"], ["Onderhoud", "0,17"], ["Support", "2,10"], ["NRE (OEM-adapter)", "1,39"],
                            ["Klantwerving", "1,04"], ["Kostprijs", "6,44"], ["Prijs incl. 40 % marge", "10,73"]],
      colw=[3.6, 1.73], size=12.5, rowh=0.36, fills={(9, 0): EMBER, (9, 1): EMBER})
text(s, 7.4, 5.35, 5.33, 1.4, [[("De elektronica is niet de kostendrijver: ", {"bold": True}),
     ("support, NRE en klantwerving zijn samen 70 %. Een per-container-abonnement schaalt dus slecht onder ~10.000 units.", {})]],
     size=13)

# ---------- 20 Business case -----------------------------------------------------------
s = new("Voor een gemeente met 1.000 containers komt alleen de camera op de wagen in de buurt; de baat ligt bij de inzamelaar",
        "experiments/r3_business (A7): 1,27 wagenbranden per 1.000 containerjaar (A6/A1), schade EUR 10k/25k/50k per wagenbrand [A]")
chart(s, "c10_prijs_vs_schade.png", 0.5, 1.5, w=7.0)
chart(s, "c13_baat.png", 7.7, 1.5, w=5.0)
for i, (b_, d) in enumerate([("0,58", "baat/kosten camera op wagen (OEM) bij 1.000 containers; 1,33 bij 10.000"),
                             ("0–18 %", "van de vermeden schade valt bij de gemeente (0 % bij de camera)")]):
    stat(s, 7.7, 4.15 + i * 1.38, 5.03, b_, d, h=1.28, bigsize=26)

# ---------- 21 Red team -----------------------------------------------------------------
s = new("Red team: de conclusie houdt stand; de grootste risico's zitten in vals alarm en het ontbreken van een koper",
        "debate/R4_redteam.md (A8); break-even uit experiments/r3_business")
rows = [["#", "Risico", "Kans", "Impact", "Mitigatie"],
        ["1", "Camera op de wagen: te veel vals alarm, chauffeur negeert het", "middel", "hoog", "Pilot 2–4 wagens × 6 mnd; ≤ 1 vals alarm per wagen per maand"],
        ["2", "Geen koper: de baat is statistisch niet aan te tonen (≥ 41k containerjaren)", "hoog", "hoog", "Verkopen op chauffeursveiligheid en premie; fabrieksoptie in voertuigbestek"],
        ["3", "Concurrent eerst: Seek, Oshkosh, wagenbouwers", "hoog", "middel", "Geen eigen hardware; rol als integrator, draaiboek en datalaag"],
        ["4", "Accu-brievenbus wordt zelf brand- of vandalismebron", "middel", "middel", "Brandwerend RVS, labtest met 1 cel, sluiten rond jaarwisseling"],
        ["5", "Meet-zuil geeft een vals 'go'", "laag–middel", "hoog", "Geblindeerd, echte metaalmix en trommel, criterium vooraf vast"]]
fills = {(1, 3): CRIT, (2, 2): CRIT, (2, 3): CRIT, (3, 2): CRIT, (5, 3): CRIT, (1, 2): WARN, (3, 3): WARN, (4, 2): WARN, (4, 3): WARN, (5, 2): WARN}
table(s, 0.6, 1.55, 12.13, rows, colw=[0.45, 4.6, 1.1, 1.0, 4.98], size=12.5, rowh=0.62, fills=fills)
text(s, 0.6, 5.5, 12.1, 1.3, [[("Wat zou het advies omdraaien? ", {"bold": True}),
     ("Voor K2 is 170× de basisbrandkans nodig (220 per 1.000 containerjaar); 10× meer branden of 10× meer schade is niet genoeg. Alleen een verplichte EPR-lekmeting zou een meetdienst (K3b) rechtvaardigen.", {})]],
     size=14)

# ---------- 22 Roadmap -------------------------------------------------------------------
s = new("Roadmap: eerst falsificeren en de wagen testen, pas opschalen bij bewezen effect",
        "debate/R4_scorekaart.md, R4_redteam.md; experiments/r3_redteam/labtests.md")
cols = [("0–6 maanden", "Prototype en bewijs", ["Meet-zuil in 1 zuil: go/no-go inductie (EUR 37–102k)",
                                                 "Pilot camera op 2 wagens bij één inzamelaar",
                                                 "Labtest brandwerende accu-brievenbus",
                                                 "Vooroverleg met Stichting OPEN; stralingsdeskundige over K3"]),
        ("6–18 maanden", "Pilot in één gemeente", ["Camera op ≥ 10 wagens; vals alarm en dumpacties meten",
                                                   "Accu-brievenbus in 1 cluster + sorteeranalyse 2 × 1 t",
                                                   "K4 als add-on op 20 hotspot-containers",
                                                   "Alleen bij 'go': K2-lite op 10 zuilen met OEM"]),
        ("18–36 maanden", "Opschalen", ["Camera als fabrieksoptie in voertuigbestekken",
                                        "Brievenbus landelijk via de producentenorganisatie",
                                        "Risicokaart en datalaag als dienst aan inzamelaars",
                                        "Zuilproduct alleen bij bewezen PPV ≥ 50 %"])]
for i, (t, sub, items) in enumerate(cols):
    x = 0.6 + i * 4.08
    box(s, x, 1.55, 3.9, 0.95, fill=EMBER if i == 0 else DARK)
    text(s, x + 0.2, 1.6, 3.5, 0.45, t, size=18, bold=True, font=HEAD, color=WHITE)
    text(s, x + 0.2, 2.03, 3.5, 0.4, sub, size=13, color=WHITE)
    box(s, x, 2.65, 3.9, 3.6)
    text(s, x + 0.2, 2.8, 3.55, 3.4, items, size=13.5, bullets=True, space=10)
text(s, 0.6, 6.4, 12.1, 0.45, "Beslismoment na elke fase: door alleen bij gemeten effect; anders stoppen of bijsturen.",
     size=13, color=MUTED)

# ---------- 23 Partners, labtests, open vragen ------------------------------------------
s = new("Nodig: één inzamelaar, één zuilleverancier en zeven labtests om de open vragen te beslissen",
        "experiments/r3_redteam/labtests.md (L1–L7), r3_*/RESULTATEN.md; research/A5, A7")
card(s, 0.6, 1.5, 3.9, 5.3, "Partners", ["Inzamelaar met eigen AVI (zoals HVC): wagens en data",
                                          "Leverancier toegangscontrole (Bammens e.a.): OEM-interface",
                                          "Stichting OPEN: brievenbus, financiering",
                                          "Stralingsdeskundige en ANVS (K3)",
                                          "Wagenbouwer of camerapartner (B1)"])
card(s, 4.72, 1.5, 3.9, 5.3, "Labtests (prototype)", ["L1 Inductie in echte RVS-trommel: ≥ 300 zakken",
                                                      "L2 Gespikete zakken: 62 per klasse, geblindeerd",
                                                      "L3 Röntgendosimetrie bij open klep",
                                                      "L4 IR + CO in container, 20 × 3 mnd",
                                                      "L5 Camera op wagen: vals alarm 6 mnd",
                                                      "L6 Brievenbus: thermal runaway van 1 cel",
                                                      "L7 BLE door valschacht en platform"])
card(s, 8.84, 1.5, 3.89, 5.3, "Open vragen", ["Echte brandfrequentie per containerjaar (nu 0,3–11 per 1.000)",
                                              "Aandeel Li-ion in NL-restafval (aanname 3/6/12 per ton)",
                                              "Schade per wagenbrand (niet gevonden)",
                                              "Aantal ondergrondse containers NL (~45k [A])",
                                              "Bbs-vrijstelling bevestigen",
                                              "Effect van een brievenbus op gedrag"])

# ---------- 24 Bronnen en aannames -------------------------------------------------------
s = new("Bijlage: bronnen en belangrijkste aannames",
        "Volledige lijsten met datum: research/A1–A8 (§ Bronnen); alle code: experiments/; prijspeil EUR 2026 excl. btw")
text(s, 0.6, 1.45, 6.0, 0.4, "Bronnen (selectie, met datum)", size=15, bold=True)
text(s, 0.6, 1.9, 6.0, 4.9, [
    "Stichting OPEN/Eureco, Batterijen in huishoudelijk restafval 2025 (2026-04)",
    "Tweede Kamer, 2026D41104 – Kamervragen batterijbranden (2026)",
    "NOS / NVRD, branden in vuilniswagens (2023)",
    "Nigl e.a., SOC van afgedankte Li-ion, Waste Management (2021)",
    "Gausden & Cerik, vapes als ontstekingsbron, Batteries (2024-07)",
    "Eunomia/ESA, Li-ion fires in the waste industry (2021-01); US EPA 530-R-21-002 (2021-07)",
    "Chen e.a., Li-ion-branden in stortplaats, PSEP (2025)",
    "NIST XCOM attenuatiedata; Besluit basisveiligheidsnormen stralingsbescherming art. 3.18 (2018)",
    "Li-ion Tamer / DNV-GL testrapport (z.d.); Seek Thermal – Goodyear, SWANA (2025)",
    "Rijkswaterstaat sorteeranalyse restafval (2022); CBS gemeenten (2026-01)",
    "TenderNed-bestekken ondergrondse containers (2019–2026); Europese drempels 2026–2027"],
    size=11.5, bullets=True, space=3)
text(s, 6.95, 1.45, 5.8, 0.4, "Belangrijkste aannames [A]", size=15, bold=True)
table(s, 6.95, 1.9, 5.78, [["Parameter", "Laag / basis / hoog"],
                           ["Li-items per ton restafval", "3 / 6 / 15"],
                           ["Zakken per lediging", "80 / 100 / 120"],
                           ["Wagenbranden per 1.000 containerjaar", "0,07 / 1,27 / 48"],
                           ["Schade per wagenbrand", "EUR 10k / 25k / 50k"],
                           ["Effect ingreep oranje / rood", "30 % / 80 %"],
                           ["Kosten per melding", "EUR 10–150"],
                           ["Levensduur, marge", "6 jaar, 40 %"],
                           ["Ondergrondse restafvalcontainers NL", "30k / 45k / 65k"]],
      colw=[3.6, 2.18], size=11.5, rowh=0.36)
text(s, 6.95, 5.35, 5.8, 1.4, [[("Niet gevonden of niet getest: ", {"bold": True}),
     ("schade per wagenbrand, aandeel Li-ion naar aantal, gemeten vervalcurves van cellen, KPN/Vodafone IoT-tarieven, datasheets zuilleveranciers. Niets is fysiek gemeten: alle prestaties komen uit modellen.", {})]],
     size=11.5)

prs.save(OUTFILE)
print("geschreven:", OUTFILE, "slides:", len(prs.slides))
