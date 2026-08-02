"""Builds the Round-1 Ascend Season 4 deck: cover + 3 content slides + appendix.
Run: python3 cases/2026-08-ascend-s4-cipla-cardiac/deck/build_deck.py
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
import copy

HERE = "cases/2026-08-ascend-s4-cipla-cardiac/deck"
ASSETS = f"{HERE}/assets"
OUT = f"{HERE}/Cipla_Ascend_S4_Round1_CardioCompass.pptx"

NAVY = RGBColor(0x0A, 0x1F, 0x3D)
CARD = RGBColor(0x12, 0x27, 0x4A)
CARD_LIGHT = RGBColor(0x1A, 0x33, 0x5C)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
TEXT_SECONDARY = RGBColor(0xC3, 0xCA, 0xD9)
TEXT_MUTED = RGBColor(0x8A, 0x93, 0xA8)
BLUE = RGBColor(0x4A, 0x90, 0xE2)
TEAL = RGBColor(0x22, 0xC3, 0x8F)
AMBER = RGBColor(0xFF, 0xB8, 0x4D)
GRAY = RGBColor(0x9A, 0xA0, 0xA6)
GRID = RGBColor(0x2C, 0x3E, 0x5C)
CIPLA_RED = RGBColor(0xE9, 0x4B, 0x3C)

FONT = "Arial"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
SW, SH = prs.slide_width, prs.slide_height


def add_slide():
    return prs.slides.add_slide(BLANK)


def bg(slide, color=NAVY):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color


def textbox(slide, l, t, w, h, text, size=14, color=WHITE, bold=False, italic=False,
            align=PP_ALIGN.LEFT, font=FONT, anchor=MSO_ANCHOR.TOP, line_spacing=1.0,
            space_after=0, wrap=True):
    box = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    lines = text.split("\n")
    for i, line in enumerate(lines):
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


def multirun_textbox(slide, l, t, w, h, runs_by_para, align=PP_ALIGN.LEFT,
                      anchor=MSO_ANCHOR.TOP, line_spacing=1.0, space_after=6):
    """runs_by_para: list of list-of-dict(text,size,color,bold,italic,font)"""
    box = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    for i, runs in enumerate(runs_by_para):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line_spacing
        p.space_after = Pt(space_after)
        for rd in runs:
            r = p.add_run()
            r.text = rd["text"]
            r.font.size = Pt(rd.get("size", 12))
            r.font.color.rgb = rd.get("color", WHITE)
            r.font.bold = rd.get("bold", False)
            r.font.italic = rd.get("italic", False)
            r.font.name = rd.get("font", FONT)
    return box


def rect(slide, l, t, w, h, fill=CARD, line_color=None, line_w=1.0, radius=None, shadow=False):
    shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if radius is not None else MSO_SHAPE.RECTANGLE
    sh = slide.shapes.add_shape(shape_type, Inches(l), Inches(t), Inches(w), Inches(h))
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


def kicker_bar(slide, color=CIPLA_RED, l=0.55, t=0.185, w=0.55, h=0.05):
    rect(slide, l, t, w, h, fill=color, radius=None)


def footer(slide, page_label, note=None):
    textbox(slide, 0.55, 7.16, 6.0, 0.3, "Cipla Ascend Season 4  |  CARDIO-COMPASS",
            size=8.5, color=TEXT_MUTED)
    textbox(slide, 10.5, 7.16, 2.3, 0.3, page_label, size=8.5, color=TEXT_MUTED,
            align=PP_ALIGN.RIGHT)
    if note:
        textbox(slide, 0.55, 6.9, 12.2, 0.25, note, size=7.8, color=TEXT_MUTED, italic=True)


def slide_header(slide, kicker, title, subtitle=None):
    kicker_bar(slide)
    textbox(slide, 0.55, 0.28, 11.5, 0.3, kicker, size=11, color=CIPLA_RED, bold=True)
    textbox(slide, 0.55, 0.55, 12.2, 0.7, title, size=23, color=WHITE, bold=True, line_spacing=1.05)
    y = 1.18
    if subtitle:
        textbox(slide, 0.55, y, 12.2, 0.4, subtitle, size=12.5, color=TEXT_SECONDARY)


def add_picture_fit(slide, path, l, t, w, h):
    return slide.shapes.add_picture(path, Inches(l), Inches(t), width=Inches(w), height=Inches(h))


def styled_table(slide, l, t, w, h, headers, rows, col_widths, header_bg=CARD_LIGHT,
                  row_colors=None, font_size=9.5, header_size=9.5, header_color=TEAL,
                  row_text_color=WHITE):
    n_rows = len(rows) + 1
    n_cols = len(headers)
    gshape = slide.shapes.add_table(n_rows, n_cols, Inches(l), Inches(t), Inches(w), Inches(h))
    table = gshape.table
    total = sum(col_widths)
    for i, cw in enumerate(col_widths):
        table.columns[i].width = Inches(w * cw / total)
    # remove default banding style visuals by setting each cell explicitly
    for ci, htext in enumerate(headers):
        cell = table.cell(0, ci)
        cell.fill.solid()
        cell.fill.fore_color.rgb = header_bg
        cell.margin_left = Inches(0.08)
        cell.margin_right = Inches(0.08)
        cell.margin_top = Inches(0.03)
        cell.margin_bottom = Inches(0.03)
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf = cell.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT if ci == 0 else PP_ALIGN.CENTER
        r = p.add_run()
        r.text = htext
        r.font.size = Pt(header_size)
        r.font.bold = True
        r.font.color.rgb = header_color
        r.font.name = FONT
    for ri, row in enumerate(rows):
        rc = row_colors[ri] if row_colors else CARD
        for ci, val in enumerate(row):
            cell = table.cell(ri + 1, ci)
            cell.fill.solid()
            cell.fill.fore_color.rgb = rc
            cell.margin_left = Inches(0.08)
            cell.margin_right = Inches(0.08)
            cell.margin_top = Inches(0.02)
            cell.margin_bottom = Inches(0.02)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if ci == 0 else PP_ALIGN.CENTER
            text = str(val)
            bold = ci == 0
            r = p.add_run()
            r.text = text
            r.font.size = Pt(font_size)
            r.font.bold = bold
            r.font.color.rgb = row_text_color
            r.font.name = FONT
    # strip table style banding (first-row/band coloring) so our explicit fills show
    tbl = gshape.table._tbl
    tblPr = tbl.find(qn('a:tblPr'))
    if tblPr is not None:
        tblPr.set('firstRow', '0')
        tblPr.set('bandRow', '0')
    return table


# =====================================================================
# COVER SLIDE
# =====================================================================
s = add_slide()
bg(s)
rect(s, 0, 0, 13.333, 7.5, fill=NAVY)
rect(s, 0, 0, 0.18, 7.5, fill=CIPLA_RED)
textbox(s, 1.0, 2.15, 10.5, 0.4, "CIPLA ASCEND — SEASON 4", size=15, color=CIPLA_RED, bold=True)
textbox(s, 1.0, 2.55, 11, 1.1, "CARDIO-COMPASS", size=54, color=WHITE, bold=True)
textbox(s, 1.02, 3.62, 11, 0.6,
        "A transparent, reproducible AI agent for prioritizing Cipla's Cardiac opportunity spaces",
        size=17, color=TEXT_SECONDARY)
textbox(s, 1.0, 4.35, 11, 0.4,
        "AI-Enabled Prioritization with Integrated Trend Analytics  |  Round 1 Submission",
        size=12.5, color=TEXT_MUTED, italic=True)

rect(s, 1.0, 6.35, 3.2, 0.02, fill=GRID)
textbox(s, 1.0, 6.5, 6, 0.3, "Ranjana Mainani", size=12, color=WHITE, bold=True)
textbox(s, 1.0, 6.8, 6, 0.3, "cases/2026-08-ascend-s4-cipla-cardiac", size=10, color=TEXT_MUTED)

# =====================================================================
# SLIDE 1 — THE AGENT
# =====================================================================
s = add_slide()
bg(s)
slide_header(
    s, "1 / 3  —  THE AGENT",
    "CARDIO-COMPASS is a transparent scoring pipeline, not a black box",
    "Every input, weight, and formula below is visible and re-runnable — the finale can test it live.",
)

add_picture_fit(s, f"{ASSETS}/agent_pipeline.png", 0.55, 1.65, 12.2, 2.15)

# Framework panel: objective + weighted formula
rect(s, 0.55, 4.05, 5.95, 2.75, fill=CARD, radius=0.04)
textbox(s, 0.80, 4.22, 5.5, 0.3, "OBJECTIVE & DATA INPUTS", size=11, color=BLUE, bold=True)
multirun_textbox(s, 0.80, 4.55, 5.45, 2.1, [
    [{"text": "Rank Cardiac opportunity spaces by likelihood of outperforming the ", "size": 10.5, "color": TEXT_SECONDARY},
     {"text": "broader market over 3-5 years", "size": 10.5, "color": WHITE, "bold": True},
     {"text": ", and by Cipla's ability to actually capture that growth.", "size": 10.5, "color": TEXT_SECONDARY}],
    [{"text": "Inputs: ", "size": 10.5, "color": BLUE, "bold": True},
     {"text": "7,452-row IQVIA-style MAT dataset (brand/company/molecule level, Feb'24-'26) "
               "+ a curated, source-cited external trend layer (epidemiology, dyslipidemia/"
               "hypertension guidelines, pipeline & launch signals).", "size": 10.5, "color": TEXT_SECONDARY}],
    [{"text": "Opportunity spaces are defined ", "size": 10.5, "color": TEXT_SECONDARY},
     {"text": "programmatically", "size": 10.5, "color": WHITE, "bold": True},
     {"text": " by molecule-pattern rules over MOLECULE_DESC — editable, auditable, not manual bucketing.",
      "size": 10.5, "color": TEXT_SECONDARY}],
], line_spacing=1.18, space_after=8)

rect(s, 6.75, 4.05, 6.03, 2.75, fill=CARD, radius=0.04)
textbox(s, 7.0, 4.22, 5.5, 0.3, "PRIORITIZATION FORMULA (WEIGHTS ARE VISIBLE)", size=11, color=BLUE, bold=True)

weight_rows = [
    ("Market attractiveness", "30%", "0.5×norm(market size) + 0.5×norm(2yr value CAGR)", BLUE),
    ("Future potential", "25%", "curated 0-100 signal score, cited to secondary research", AMBER),
    ("Competitive whitespace", "20%", "100 − norm(HHI) — inverse of concentration", TEAL),
    ("Cipla right-to-win", "25%", "0.4×share + 0.3×rank + 0.3×momentum (capped, low-base-safe)", TEAL),
]
y = 4.62
for label, wt, formula, color in weight_rows:
    rect(s, 7.0, y, 0.62, 0.32, fill=CARD_LIGHT, radius=0.25)
    textbox(s, 7.0, y + 0.045, 0.62, 0.28, wt, size=11, color=color, bold=True, align=PP_ALIGN.CENTER)
    textbox(s, 7.75, y - 0.02, 4.9, 0.25, label, size=10.5, color=WHITE, bold=True)
    textbox(s, 7.75, y + 0.235, 4.9, 0.3, formula, size=8.6, color=TEXT_MUTED)
    y += 0.53

footer(s, "Page 2",
       "Reproducible: `python analysis/agent_prioritization.py` regenerates this ranking straight from the raw dataset.")

# =====================================================================
# SLIDE 2 — RANKED OPPORTUNITIES
# =====================================================================
s = add_slide()
bg(s)
slide_header(
    s, "2 / 3  —  THE RANKING",
    "5 opportunity spaces ranked; 3 clear the bar to actively prioritize",
    "Trade-offs the agent resolves: ARB-CCB wins size AND growth together; Statin-Ezetimibe wins growth despite low competition; Fibrates win on Cipla's existing right-to-win over a bigger, slower field.",
)

add_picture_fit(s, f"{ASSETS}/priority_matrix.png", 0.4, 1.62, 7.5, 4.55)

headers = ["Opportunity space", "₹Cr,\nMAT'26", "2yr\nvalue CAGR", "HHI", "Cipla\nshare / rank", "Score", "Action"]
rows = [
    ["ARB-CCB combination AHT", "3,748", "+15.8%", "683", "1.6% / #18", "62.8", "BUILD"],
    ["Statin-Ezetimibe combo therapy", "333", "+60.8%", "1,380", "0.3% / #21", "57.9", "BUILD"],
    ["Fibrate-based lipid regulation", "1,002", "+14.8%", "1,319", "6.6% / #5", "52.5", "DOUBLE DOWN"],
    ["Next-gen non-statin lipid lowering", "118", "+110.1%", "1,948", "0.0% / n/a", "46.6", "SELECTIVE"],
    ["Legacy AHT monotherapy", "419", "+8.5%", "4,647", "1.3% / #6", "14.1", "AVOID"],
]
action_colors = {"BUILD": TEAL, "DOUBLE DOWN": TEAL, "SELECTIVE": AMBER, "AVOID": GRAY}
row_colors = [CARD if i % 2 == 0 else CARD_LIGHT for i in range(len(rows))]

tbl = styled_table(s, 8.05, 1.62, 4.85, 4.55, headers, rows,
                    col_widths=[2.1, 0.8, 0.95, 0.9, 1.0, 0.8, 1.55],
                    font_size=8.3, header_size=7.8, row_colors=row_colors)
# color the Action column text by status
for ri, row in enumerate(rows):
    cell = tbl.cell(ri + 1, len(headers) - 1)
    cell.text_frame.paragraphs[0].runs[0].font.color.rgb = action_colors[row[-1]]
    cell.text_frame.paragraphs[0].runs[0].font.bold = True

footer(s, "Page 3", "HHI = Herfindahl-Hirschman Index of company concentration within the space (lower = more fragmented / more whitespace).")

# =====================================================================
# SLIDE 3 — RIGHT TO WIN & STRATEGIC IMPLICATIONS
# =====================================================================
s = add_slide()
bg(s)
slide_header(
    s, "3 / 3  —  RIGHT-TO-WIN & THE PLAYBOOK",
    "Cipla trails the category leader everywhere except Fibrates — and the biggest",
    None,
)
textbox(s, 0.55, 1.15, 12.2, 0.35,
        "underpenetrated opportunity is patent-gated, not just uncontested.",
        size=15, color=WHITE, bold=True)

add_picture_fit(s, f"{ASSETS}/rtw_comparison.png", 0.45, 1.68, 7.1, 2.55)

# underpenetrated callout
rect(s, 7.85, 1.68, 4.95, 2.55, fill=CARD, radius=0.05, line_color=AMBER, line_w=1.25)
textbox(s, 8.08, 1.85, 4.5, 0.3, "UNDERPENETRATED, DESPITE STRONG POTENTIAL", size=10, color=AMBER, bold=True)
multirun_textbox(s, 8.08, 2.2, 4.55, 1.95, [
    [{"text": "Next-gen non-statin lipid lowering", "size": 10.3, "color": WHITE, "bold": True},
     {"text": " (+110% CAGR, highest in the dataset) splits in two:", "size": 10.3, "color": TEXT_SECONDARY}],
    [{"text": "• Inclisiran ", "size": 9.8, "color": WHITE, "bold": True},
     {"text": "— ₹60 Cr, 100% Novartis, patent-locked. Not accessible near-term.", "size": 9.8, "color": TEXT_SECONDARY}],
    [{"text": "• Bempedoic acid combos ", "size": 9.8, "color": WHITE, "bold": True},
     {"text": "— ₹57 Cr, already fragmenting across 7+ Indian generics majors post-Zydus's 2022 first-mover launch.", "size": 9.8, "color": TEXT_SECONDARY}],
    [{"text": "→ Selective fast-follower generic entry into bempedoic acid combinations; skip inclisiran.", "size": 9.8, "color": AMBER, "italic": True}],
], line_spacing=1.22, space_after=7)

# strategic action row (4 cards)
cards = [
    ("DOUBLE DOWN", "Fibrate-based lipid regulation", "Already rank #5, 6.6% share — defend and extend the FDC line.", TEAL),
    ("BUILD", "ARB-CCB combo + Statin-Ezetimibe combo", "Biggest prize + fastest grower; fragmented fields, real entry room.", BLUE),
    ("SELECTIVE", "Next-gen non-statin lipid lowering", "Fast-follow bempedoic acid generics only; inclisiran is off the table.", AMBER),
    ("AVOID", "Legacy AHT monotherapy", "Flat real volume (+0.07% CAGR), HHI 4,647 — fading, not investable.", GRAY),
]
card_w = 2.93
gap = 0.2
x = 0.55
y = 4.5
for tag, name, desc, color in cards:
    rect(s, x, y, card_w, 2.15, fill=CARD, radius=0.06, line_color=color, line_w=1.5)
    rect(s, x, y, card_w, 0.36, fill=color, radius=0.0)
    textbox(s, x, y + 0.045, card_w, 0.3, tag, size=11, color=NAVY, bold=True, align=PP_ALIGN.CENTER)
    textbox(s, x + 0.15, y + 0.52, card_w - 0.3, 0.75, name, size=10.3, color=WHITE, bold=True, line_spacing=1.1)
    textbox(s, x + 0.15, y + 1.28, card_w - 0.3, 0.8, desc, size=8.8, color=TEXT_SECONDARY, line_spacing=1.2)
    x += card_w + gap

footer(s, "Page 4")

# =====================================================================
# APPENDIX — SOURCES (not counted against the 3-slide limit)
# =====================================================================
s = add_slide()
bg(s)
slide_header(s, "APPENDIX", "Sources for external data & methodology notes", None)

textbox(s, 0.55, 1.55, 12.2, 0.3, "EXTERNAL SOURCES CITED (FUTURE-POTENTIAL SCORING)", size=11, color=BLUE, bold=True)
sources = [
    "Bempedoic Acid for Lipid Management in the Indian Population: An Expert Opinion — PMC (pmc.ncbi.nlm.nih.gov/articles/PMC10040092)",
    "Zydus launches Bemdac to treat LDL-Cholesterol — Indian Pharma Post (indianpharmapost.com)",
    "Bempedoic acid market in India will become crowded soon with more generic launches — GlobalData (globaldata.com)",
    "Unmet Need for Further LDL-C Lowering in India despite Statin Therapy: LAI Recommendations — PubMed (pubmed.ncbi.nlm.nih.gov/36082889)",
    "Guidelines for dyslipidemia management in India: current scenario and gaps — PMC (pmc.ncbi.nlm.nih.gov/articles/PMC9647649)",
    "CSI Clinical Practice Guidelines for Dyslipidemia Management — ScienceDirect (sciencedirect.com/science/article/pii/S0019483223004698)",
    "Epidemiological trends and age-period-cohort effects on CVD burden attributable to ambient air pollution across BRICS — Nature Sci Reports (nature.com/articles/s41598-024-62295-6)",
    "Does Ambient/Indoor Air Pollution Drive Hypertension in Women in India? — Air Qual Atmos Health, Springer (link.springer.com/article/10.1007/s11869-025-01770-z)",
    "The India Hypertension Control Initiative — early outcomes, 2018-2020 — J Human Hypertension, Nature (nature.com/articles/s41371-022-00742-5)",
    "Treatment Optimisation for BP with Single-Pill Combinations in India (TOPSPIN protocol) — PMC (ncbi.nlm.nih.gov/pmc/articles/PMC11565424)",
]
y = 1.92
for src in sources:
    textbox(s, 0.55, y, 12.3, 0.3, "•  " + src, size=9.3, color=TEXT_SECONDARY, line_spacing=1.1)
    y += 0.315

textbox(s, 0.55, 5.35, 12.2, 0.3, "METHODOLOGY NOTES", size=11, color=BLUE, bold=True)
notes = [
    "Primary dataset: Ascend Season 4 Cardiac market MAT dataset (IQVIA-style, 7,452 SKU-level rows, India, MAT Feb'24/'25/'26).",
    "\"Future potential\" pillar is analyst-curated from the sources above, not a live external feed — documented transparently given offline/sandboxed constraints.",
    "Cipla's own CAGR is capped at +100% before scoring to prevent low-base outliers (e.g. Statin-Ezetimibe, <₹1 Cr in FY24) from dominating the right-to-win pillar.",
]
y = 5.7
for n in notes:
    textbox(s, 0.55, y, 12.3, 0.4, "•  " + n, size=9.0, color=TEXT_SECONDARY, line_spacing=1.15)
    y += 0.4

footer(s, "Appendix")

prs.save(OUT)
print("Saved:", OUT)
