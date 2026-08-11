"""HUL L.I.M.E. Season 18 — Stage 1 Kissan case. Builds the two required
submission slides on HUL's own templates (Consumer Job + Concept Card).

Run: python3 cases/2026-08-hul-lime-s18-kissan/deck/build_deck.py
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

HERE = "cases/2026-08-hul-lime-s18-kissan/deck"
ASSETS = f"{HERE}/assets"
OUT = f"{HERE}/LIME_S18_Kissan_Stage1_Slides.pptx"

WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BLACK = RGBColor(0x15, 0x15, 0x15)
KISSAN_RED = RGBColor(0xD5, 0x1A, 0x1A)
NAVY = RGBColor(0x0E, 0x3A, 0x54)      # matches HUL template's block blue
NAVY_LIGHT = RGBColor(0x14, 0x4E, 0x70)
CREAM = RGBColor(0xF5, 0xEE, 0xDD)
GREY = RGBColor(0x6B, 0x6B, 0x6B)

FONT = "Arial"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


def add_slide(bg=WHITE):
    s = prs.slides.add_slide(BLANK)
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = bg
    return s


def textbox(slide, l, t, w, h, text, size=14, color=BLACK, bold=False, italic=False,
            align=PP_ALIGN.LEFT, font=FONT, anchor=MSO_ANCHOR.TOP, line_spacing=1.0,
            space_after=0):
    box = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, line in enumerate(text.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line_spacing
        p.space_after = Pt(space_after)
        r = p.add_run()
        r.text = line
        r.font.size = Pt(size)
        r.font.color.rgb = color
        r.font.bold = bold
        r.font.italic = italic
        r.font.name = font
    return box


def rich(slide, l, t, w, h, paras, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
         line_spacing=1.15, space_after=6):
    box = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, runs in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line_spacing
        p.space_after = Pt(space_after)
        for rd in runs:
            r = p.add_run()
            r.text = rd["text"]
            r.font.size = Pt(rd.get("size", 12))
            r.font.color.rgb = rd.get("color", BLACK)
            r.font.bold = rd.get("bold", False)
            r.font.italic = rd.get("italic", False)
            r.font.name = rd.get("font", FONT)
    return box


def rect(slide, l, t, w, h, fill=NAVY, line_color=None, line_w=1.0, radius=None):
    st = MSO_SHAPE.ROUNDED_RECTANGLE if radius is not None else MSO_SHAPE.RECTANGLE
    sh = slide.shapes.add_shape(st, Inches(l), Inches(t), Inches(w), Inches(h))
    if radius is not None:
        try:
            sh.adjustments[0] = radius
        except Exception:
            pass
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    if line_color is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line_color
        sh.line.width = Pt(line_w)
    sh.shadow.inherit = False
    return sh


def block_label(slide, l, t, w, h, text, size=15, color=WHITE, bold=True, fill=NAVY):
    rect(slide, l, t, w, h, fill=fill)
    textbox(slide, l + 0.14, t, w - 0.28, h, text, size=size, color=color, bold=bold,
            align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.15)


def picture(slide, path, l, t, w, h):
    return slide.shapes.add_picture(path, Inches(l), Inches(t), width=Inches(w), height=Inches(h))


# ===========================================================================
# COVER (context only — not one of the two required slides, clearly marked)
# ===========================================================================
s = add_slide()
rect(s, 0, 0, 13.333, 7.5, fill=WHITE)
rect(s, 0, 0, 0.16, 7.5, fill=KISSAN_RED)
textbox(s, 0.9, 0.85, 10, 0.35, "L.I.M.E. SEASON 18 — STAGE 1", size=13, color=KISSAN_RED, bold=True)
textbox(s, 0.9, 1.3, 11, 1.6, "The Next Shelf:\nBuilding the Future of Kissan",
        size=38, color=BLACK, bold=True, line_spacing=1.05)
textbox(s, 0.9, 3.05, 10.5, 1.15,
        "Two required submission slides — Consumer Job and Concept Card — for the\n"
        "Kissan Chutney opportunity, built on a secondary-research hypothesis pending\n"
        "the team's own Task 1 interviews.", size=14, color=GREY, line_spacing=1.4)
rect(s, 0.92, 4.45, 3.2, 0.02, fill=GREY)
textbox(s, 0.9, 4.62, 8, 0.3, "cases/2026-08-hul-lime-s18-kissan", size=11, color=GREY)
rect(s, 0.9, 5.1, 11.5, 1.5, fill=CREAM, radius=0.06)
rich(s, 1.15, 5.32, 11.0, 1.1, [[
    {"text": "Not a real deliverable substitute: ", "size": 12, "bold": True, "color": KISSAN_RED},
    {"text": "the case grades a real 20-person consumer immersion (Task 1) hardest. This "
             "deck is a strong starting hypothesis and a ready-to-run interview guide — swap "
             "in real quotes before this goes anywhere near a jury.", "size": 12, "color": BLACK},
]], line_spacing=1.3)

# ===========================================================================
# SLIDE 1 — CONSUMER JOB (matches HUL's block-diagram template)
# ===========================================================================
s = add_slide()
textbox(s, 0.55, 0.4, 10, 0.4, "Slide 1: Consumer Job", size=22, color=BLACK, bold=True)
rect(s, 0.55, 0.85, 0.9, 0.05, fill=KISSAN_RED)

# Block A — persona
block_label(s, 0.55, 1.35, 3.35, 0.6, "DEFINE YOUR\nCONSUMER PERSONA", size=13, fill=NAVY)
rect(s, 0.55, 1.98, 3.35, 4.35, fill=CREAM)
rich(s, 0.75, 2.16, 2.98, 4.05, [
    [{"text": "“The Chatora”", "size": 17, "bold": True, "color": KISSAN_RED}],
    [{"text": "18–30, urban India (Tier 1 & 2 India). Grew up on Kissan ketchup. Discovers "
              "food on Instagram/YouTube reels before it shows up in a store.", "size": 11.5}],
    [{"text": "Already eats without asking permission: ketchup on dosa, chutney on pizza, "
              "double-dips, triple-dips — the exact behaviour in the case's own moodboard.",
      "size": 11.5}],
], line_spacing=1.3, space_after=10)

# Block B — opportunity
block_label(s, 4.05, 1.35, 3.35, 0.6, "IDENTIFY THE\nOPPORTUNITY", size=13, fill=NAVY)
rect(s, 4.05, 1.98, 3.35, 4.35, fill=CREAM)
rich(s, 4.25, 2.16, 2.98, 4.05, [
    [{"text": "Packaged chutney hasn't caught up to how this generation actually eats.",
      "size": 12, "bold": True}],
    [{"text": "It's still homemade, or stuck in jars/pouches nobody fully trusts or reaches "
              "for on the go.", "size": 11.5}],
    [{"text": "Ketchup already made the leap to “trust it, squeeze it, done.” "
              "Chutney hasn't — yet.", "size": 11.5}],
], line_spacing=1.3, space_after=10)

# Block C — JTBD, 3 stacked
x3, w3 = 7.55, 5.23
block_label(s, x3, 1.35, w3, 0.6, "THE JOB TO BE DONE", size=13, fill=KISSAN_RED)
jtbd = [
    ("WHEN I...", "am eating literally anything — pizza, noodles, dosa, momos, even Maggi"),
    ("I WANT TO...", "reach for a chutney that's as trusted and ready as ketchup already is"),
    ("SO THAT...", "I can dip and fuse whatever I want, without cooking it myself or gambling on a random jar"),
]
y = 1.98
row_h = 1.45
for tag, body in jtbd:
    rect(s, x3, y, w3, row_h, fill=NAVY_LIGHT)
    textbox(s, x3 + 0.22, y + 0.14, w3 - 0.44, 0.3, tag, size=13, color=RGBColor(0xFF, 0xC9, 0x3D), bold=True)
    textbox(s, x3 + 0.22, y + 0.46, w3 - 0.44, row_h - 0.55, body, size=13, color=WHITE, line_spacing=1.25)
    y += row_h + 0.13

textbox(s, 0.55, 6.85, 12.2, 0.4,
        "Hypothesis pending Task 1 interviews — see research/discovery-guide.md",
        size=10, color=GREY, italic=True)

# ===========================================================================
# SLIDE 2 — CONCEPT CARD (consumer-facing pitch, <=80 words, bold image)
# ===========================================================================
s = add_slide(bg=BLACK)
textbox(s, 0.55, 0.28, 10, 0.35, "Slide 2: Concept Card", size=16, color=GREY, bold=True)

picture(s, f"{ASSETS}/pack_illustration.png", 0.55, 0.75, 12.23, 5.55)

rect(s, 0.55, 6.42, 12.23, 0.02, fill=RGBColor(0x33, 0x33, 0x33))
rich(s, 0.55, 6.58, 12.23, 0.8, [[
    {"text": "Kissan Chutney — Mint, Imli & Schezwan, in the same trusted squeeze as your "
             "ketchup. No chopping. No random jars. Just a clean burst of real flavour on "
             "literally anything — dosa, pizza, noodles, Maggi. Because when you already "
             "dip everything in everything, your chutney deserves to keep up.",
     "size": 12.5, "color": CREAM}],
], line_spacing=1.3)

prs.save(OUT)
print("Saved:", OUT)

# word count check for the concept card copy (<=80 words, per the brief)
copy = ("Kissan Chutney — Mint, Imli & Schezwan, in the same trusted squeeze as your "
        "ketchup. No chopping. No random jars. Just a clean burst of real flavour on "
        "literally anything — dosa, pizza, noodles, Maggi. Because when you already "
        "dip everything in everything, your chutney deserves to keep up.")
wc = len(copy.split())
print(f"Concept card word count: {wc} (limit 80)")
assert wc <= 80
