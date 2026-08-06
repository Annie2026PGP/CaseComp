"""Builds the Project NEXT pitch deck: cover + 5 content slides + appendix.
Run: python3 cases/2026-08-project-next-unilever-brand-lifecycle/deck/build_deck.py
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

HERE = "cases/2026-08-project-next-unilever-brand-lifecycle/deck"
ASSETS = f"{HERE}/assets"
OUT = f"{HERE}/Project_NEXT_PULSE.pptx"

BG = RGBColor(0x0A, 0x14, 0x40)
CARD = RGBColor(0x14, 0x28, 0x63)
CARD_LIGHT = RGBColor(0x1C, 0x34, 0x80)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
TEXT_SECONDARY = RGBColor(0xC2, 0xCB, 0xE8)
TEXT_MUTED = RGBColor(0x87, 0x91, 0xB8)
CYAN = RGBColor(0x3E, 0xC6, 0xFF)
CORAL = RGBColor(0xFF, 0x6B, 0x4A)
TEAL = RGBColor(0x22, 0xC3, 0x8F)
AMBER = RGBColor(0xFF, 0xB8, 0x4D)
GRAY = RGBColor(0x9A, 0xA0, 0xA6)
GRID = RGBColor(0x2C, 0x3F, 0x7C)

FONT = "Arial"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


def add_slide():
    return prs.slides.add_slide(BLANK)


def bg(slide, color=BG):
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


def rect(slide, l, t, w, h, fill=CARD, line_color=None, line_w=1.0, radius=None):
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


def kicker_bar(slide, color=CORAL, l=0.55, t=0.185, w=0.55, h=0.05):
    rect(slide, l, t, w, h, fill=color, radius=None)


def footer(slide, page_label, note=None):
    textbox(slide, 0.55, 7.16, 6.5, 0.3, "Project NEXT  |  PULSE — Unilever's Always-On Brand Nervous System",
            size=8.5, color=TEXT_MUTED)
    textbox(slide, 10.5, 7.16, 2.3, 0.3, page_label, size=8.5, color=TEXT_MUTED,
            align=PP_ALIGN.RIGHT)
    if note:
        textbox(slide, 0.55, 6.9, 12.2, 0.25, note, size=7.8, color=TEXT_MUTED, italic=True)


def slide_header(slide, kicker, title, subtitle=None):
    kicker_bar(slide)
    textbox(slide, 0.55, 0.28, 11.5, 0.3, kicker, size=11, color=CORAL, bold=True)
    textbox(slide, 0.55, 0.55, 12.2, 0.7, title, size=23, color=WHITE, bold=True, line_spacing=1.05)
    if subtitle:
        textbox(slide, 0.55, 1.18, 12.2, 0.4, subtitle, size=12.5, color=TEXT_SECONDARY)


def add_picture_fit(slide, path, l, t, w, h):
    return slide.shapes.add_picture(path, Inches(l), Inches(t), width=Inches(w), height=Inches(h))


def styled_table(slide, l, t, w, h, headers, rows, col_widths, header_bg=CARD_LIGHT,
                  row_colors=None, font_size=9.5, header_size=9.5, header_color=CYAN,
                  row_text_color=WHITE):
    n_rows = len(rows) + 1
    n_cols = len(headers)
    gshape = slide.shapes.add_table(n_rows, n_cols, Inches(l), Inches(t), Inches(w), Inches(h))
    table = gshape.table
    total = sum(col_widths)
    for i, cw in enumerate(col_widths):
        table.columns[i].width = Inches(w * cw / total)
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
            r = p.add_run()
            r.text = str(val)
            r.font.size = Pt(font_size)
            r.font.bold = ci == 0
            r.font.color.rgb = row_text_color
            r.font.name = FONT
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
rect(s, 0, 0, 0.18, 7.5, fill=CORAL)
textbox(s, 1.0, 1.85, 10.5, 0.4, "PROJECT NEXT  —  A PRODUCT PROPOSAL", size=15, color=CORAL, bold=True)
textbox(s, 1.0, 2.25, 11, 1.1, "PULSE", size=60, color=WHITE, bold=True)
textbox(s, 1.02, 3.42, 11, 0.5, "Unilever's Always-On Brand Nervous System", size=20, color=CYAN, bold=True)
textbox(s, 1.02, 3.95, 10.6, 0.7,
        "Turning a 3-second Rexona armband into the proof: brand teams don't need more AI "
        "features — they need the system that fires in minutes, not weeks.",
        size=13.5, color=TEXT_SECONDARY, line_spacing=1.25)
textbox(s, 1.0, 4.75, 11, 0.4,
        "How we'd architect the entire brand lifecycle if Unilever were founded today, AI-first",
        size=12, color=TEXT_MUTED, italic=True)

rect(s, 1.0, 6.35, 3.2, 0.02, fill=GRID)
textbox(s, 1.0, 6.5, 6, 0.3, "Ranjana Mainani — Product Manager, Project NEXT", size=12, color=WHITE, bold=True)
textbox(s, 1.0, 6.8, 6, 0.3, "cases/2026-08-project-next-unilever-brand-lifecycle", size=10, color=TEXT_MUTED)

# =====================================================================
# SLIDE 1 — THE PROBLEM
# =====================================================================
s = add_slide()
bg(s)
slide_header(
    s, "1 / 5  —  THE PROBLEM",
    "The viral window was minutes. Our pipeline is measured in weeks.",
    "The fourth official's board carried a Rexona logo for 3 seconds. Fans memed it before the final whistle. Our process couldn't have shipped a response before the tournament ended.",
)

add_picture_fit(s, f"{ASSETS}/timeline_comparison.png", 0.55, 1.75, 12.25, 3.15)

rect(s, 0.55, 5.15, 12.25, 1.55, fill=CARD, radius=0.04)
textbox(s, 0.8, 5.3, 11.7, 0.3, "THIS ISN'T A TOOLING GAP — IT'S A WIRING GAP", size=11, color=CORAL, bold=True)
multirun_textbox(s, 0.8, 5.62, 11.7, 1.0, [
    [{"text": "Social listening and web scraping already exist at Unilever ", "size": 10.3, "color": TEXT_SECONDARY},
     {"text": "— the brief says so directly.", "size": 10.3, "color": TEXT_SECONDARY, "italic": True},
     {"text": "  They just run independently, so a human has to manually notice, judge, brief, produce, clear, and "
              "publish — every single time. The fix isn't another dashboard. It's removing the human synthesis step from the critical path.",
      "size": 10.3, "color": TEXT_SECONDARY}],
], line_spacing=1.25)

footer(s, "Page 2")

# =====================================================================
# SLIDE 2 — THE SYSTEM
# =====================================================================
s = add_slide()
bg(s)
slide_header(
    s, "2 / 5  —  THE SYSTEM",
    "PULSE: one closed loop, not five more point solutions",
    "Perceive → Understand → Localize → Ship → Evaluate — built on top of what Unilever already has, wired for the first time.",
)

add_picture_fit(s, f"{ASSETS}/pulse_loop.png", 3.0, 1.55, 5.9, 5.9)

rect(s, 0.45, 1.75, 2.4, 5.5, fill=CARD, radius=0.06)
textbox(s, 0.62, 1.9, 2.1, 0.3, "BUILT ON, NOT INSTEAD OF", size=9.3, color=CYAN, bold=True)
multirun_textbox(s, 0.62, 2.22, 2.1, 5.0, [
    [{"text": "Brand DNAi", "size": 9.3, "color": WHITE, "bold": True},
     {"text": " — the safety & voice layer Understand/Localize score and generate against.", "size": 8.7, "color": TEXT_SECONDARY}],
    [{"text": "Digital-twin production", "size": 9.3, "color": WHITE, "bold": True},
     {"text": " — 2x faster, 50% cheaper product imagery, feeds Localize.", "size": 8.7, "color": TEXT_SECONDARY}],
    [{"text": "Desire at Scale", "size": 9.3, "color": WHITE, "bold": True},
     {"text": " — the multi-market activation engine PULSE's Ship stage drives.", "size": 8.7, "color": TEXT_SECONDARY}],
], line_spacing=1.25, space_after=12)

rect(s, 9.9, 1.75, 2.9, 5.5, fill=CARD, radius=0.06)
textbox(s, 10.07, 1.9, 2.6, 0.3, "WHAT'S ACTUALLY NEW", size=9.3, color=CORAL, bold=True)
multirun_textbox(s, 10.07, 2.22, 2.6, 5.0, [
    [{"text": "One Brand Signal Graph", "size": 9.3, "color": WHITE, "bold": True},
     {"text": " per brand — listening + scraping + broadcast unified, not siloed.", "size": 8.7, "color": TEXT_SECONDARY}],
    [{"text": "Tiered autonomy", "size": 9.3, "color": WHITE, "bold": True},
     {"text": " — auto-publish / fast-track / escalate, decided before the moment, not during it.", "size": 8.7, "color": TEXT_SECONDARY}],
    [{"text": "A closed Evaluate loop", "size": 9.3, "color": WHITE, "bold": True},
     {"text": " — every result re-trains the next playbook, so the system compounds.", "size": 8.7, "color": TEXT_SECONDARY}],
], line_spacing=1.25, space_after=12)

footer(s, "Page 3", "Brand DNAi, digital-twin production and Desire at Scale are real, existing Unilever capabilities — see appendix for sources.")

# =====================================================================
# SLIDE 3 — PULSE IN ACTION (REXONA WALKTHROUGH)
# =====================================================================
s = add_slide()
bg(s)
slide_header(
    s, "3 / 5  —  PULSE IN ACTION",
    "The Rexona armband, run through PULSE: under 4 hours, not 6 weeks",
    None,
)

headers = ["Stage", "What happens", "Elapsed"]
rows = [
    ["PERCEIVE", "Broadcast + social monitoring flags the logo appearance and rising meme velocity across markets.", "T+0 → T+10 min"],
    ["UNDERSTAND", "Signal scored against Rexona's codified strategy (composure under pressure); auto-classified Tier 1 — on-strategy, low-risk, high-velocity — triggers the pre-approved “cultural moment” playbook.", "T+10 → T+20 min"],
    ["LOCALIZE", "Generative layer (Brand DNAi + digital twin) drafts caption + product-shot variants in brand voice, localized for priority markets.", "T+20 min → T+1h20"],
    ["SHIP", "Brand manager — now a “signal editor” — reviews 3 AI-drafted options on one screen, edits, approves; publishes across markets simultaneously.", "T+1h20 → T+3h50"],
    ["EVALUATE", "Real-time engagement feeds the media-amplification decision and updates the playbook for next time.", "Continuous"],
]
row_colors = [CARD if i % 2 == 0 else CARD_LIGHT for i in range(len(rows))]
stage_colors = {"PERCEIVE": CYAN, "UNDERSTAND": CYAN, "LOCALIZE": CORAL, "SHIP": CORAL, "EVALUATE": TEAL}

tbl = styled_table(s, 0.55, 1.65, 12.25, 4.35, headers, rows,
                    col_widths=[1.4, 4.6, 1.3], font_size=10.3, header_size=10, row_colors=row_colors)
for ri, row in enumerate(rows):
    cell = tbl.cell(ri + 1, 0)
    cell.text_frame.paragraphs[0].runs[0].font.color.rgb = stage_colors[row[0]]

rect(s, 0.55, 6.15, 12.25, 0.65, fill=CARD_LIGHT, radius=0.1)
textbox(s, 0.85, 6.28, 11.7, 0.4,
        "The pre-built playbook is the point: the creative judgment happens calmly, in advance — the same composure the tagline promises, built into the process itself.",
        size=10.5, color=CYAN, italic=True, bold=True, anchor=MSO_ANCHOR.MIDDLE)

footer(s, "Page 4", "Illustrative timings for a system design proposal, not measured production data — see appendix.")

# =====================================================================
# SLIDE 4 — THREE CLOCK SPEEDS
# =====================================================================
s = add_slide()
bg(s)
slide_header(
    s, "4 / 5  —  THE WHOLE LIFECYCLE",
    "Not just reactive moments — the same nervous system runs three clock speeds",
    "One Brand Signal Graph, one Brand DNAi safety layer, three cadences of the same PULSE loop.",
)

add_picture_fit(s, f"{ASSETS}/three_clockspeeds.png", 4.35, 1.55, 4.7, 4.7)

for title, cadence, desc, color, x in [
    ("MOMENTS", "minutes – hours", "Unscripted cultural moments. PULSE runs end-to-end inside tiered guardrails.", CYAN, 0.55),
    ("CAMPAIGNS", "weeks", "Planned activations — same graph informs the brief; same engine cuts production time.", CORAL, 4.75),
    ("STRATEGY", "quarters – years", "Brand positioning — continuous signal replaces periodic research waves.", TEAL, 8.95),
]:
    rect(s, x, 6.35, 3.85, 0.85, fill=CARD, radius=0.08, line_color=color, line_w=1.3)
    textbox(s, x + 0.15, 6.42, 3.55, 0.25, f"{title}  ·  {cadence}", size=9.7, color=color, bold=True)
    textbox(s, x + 0.15, 6.68, 3.55, 0.5, desc, size=8.2, color=TEXT_SECONDARY, line_spacing=1.15)

footer(s, "Page 5")

# =====================================================================
# SLIDE 5 — THE MOAT & THE NEW ROLE
# =====================================================================
s = add_slide()
bg(s)
slide_header(
    s, "5 / 5  —  WHY THIS MAKES US INVINCIBLE",
    "Competitors can buy the same models. They can't buy our signal graph.",
    None,
)

cards = [
    ("COMPOUNDS OVER TIME", "The Brand Signal Graph and its playbooks accumulate with every loop — a rival starting today begins at zero, no matter which foundation model they license.", CYAN),
    ("GOVERNED BY DESIGN", "Tiered autonomy (auto / fast-track / escalate) means speed and brand safety were never a trade-off — Brand DNAi enforces voice and compliance at every tier.", TEAL),
    ("INSTITUTIONAL JUDGMENT, CODIFIED", "Playbooks capture what brand teams already know works — built calmly in advance, so the in-the-moment step is a lookup, not a live debate.", CORAL),
    ("A NEW ROLE, NOT A SMALLER ONE", "The Brand Manager becomes a “signal editor” — setting playbook strategy and approving output — spending time on judgment, not chasing agency deliverables.", AMBER),
]
card_w = 2.93
gap = 0.2
x = 0.55
y = 1.85
for tag, desc, color in cards:
    rect(s, x, y, card_w, 3.5, fill=CARD, radius=0.06, line_color=color, line_w=1.5)
    rect(s, x, y, card_w, 0.62, fill=color, radius=0.0)
    textbox(s, x + 0.12, y + 0.08, card_w - 0.24, 0.5, tag, size=10.3, color=BG, bold=True,
            align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.05)
    textbox(s, x + 0.18, y + 0.85, card_w - 0.36, 2.5, desc, size=9.7, color=TEXT_SECONDARY, line_spacing=1.3)
    x += card_w + gap

rect(s, 0.55, 5.65, 12.25, 1.05, fill=CARD_LIGHT, radius=0.06)
textbox(s, 0.85, 5.82, 11.7, 0.7,
        "“It won't EVER let you down” isn't just the Rexona tagline anymore — it's the design spec for the process behind it.",
        size=13, color=WHITE, bold=True, italic=True, anchor=MSO_ANCHOR.MIDDLE)

footer(s, "Page 6")

# =====================================================================
# APPENDIX
# =====================================================================
s = add_slide()
bg(s)
slide_header(s, "APPENDIX", "Sources, assumptions & governance notes", None)

textbox(s, 0.55, 1.55, 12.2, 0.3, "SOURCES", size=11, color=CYAN, bold=True)
sources = [
    "How Unilever is building an AI-first enterprise at scale — Unilever (unilever.com/news/news-search/2026)",
    "How AI is helping drive Desire at Scale across Unilever — Unilever (unilever.com/news/news-search/2025)",
    "Unilever reinvents product shoots with digital twins and AI — Unilever press release (unilever.com/news/press-and-media/2025)",
    "How AI is transforming Unilever's Personal Care business (names “Brand DNAi”) — Unilever (unilever.com/news/news-search/2025)",
    "Behind The Scenes Of Oreo's Real-Time Super Bowl Slam Dunk — Forbes, 2013 (forbes.com/sites/jenniferrooney)",
    "From ideation to execution: generative AI in modern digital marketing — ScienceDirect systematic review, 2025",
    "AI Marketing Case Studies 2026 — Pragmatic Digital (pragmatic.digital/blog)",
]
y = 1.92
for src in sources:
    textbox(s, 0.55, y, 12.3, 0.3, "•  " + src, size=9.5, color=TEXT_SECONDARY, line_spacing=1.1)
    y += 0.34

textbox(s, 0.55, 4.35, 12.2, 0.3, "ASSUMPTIONS & GOVERNANCE NOTES", size=11, color=CYAN, bold=True)
notes = [
    "This is a conceptual system-design case with no dataset or slide limit provided; scope and format (cover + 5 content slides + appendix) were self-set.",
    "Timings in the Rexona walkthrough (“under 4 hours”) are illustrative targets for a system proposal, not measured data — the honest reference point is the cited literature's 30-50% production-time reduction from generative AI adoption.",
    "Real-time computer-vision detection of an unscripted brand appearance (e.g. spotting a logo on a match official's armband) is a genuinely hard sensing problem beyond text/social listening and is flagged as a build risk, not assumed solved.",
    "Tiered auto-publish carries brand-safety and legal risk if scoring is miscalibrated — recommend a narrow Tier-1 (auto-publish) scope at launch, expanding only as the Signal Graph accumulates evidence.",
    "PULSE is proposed as an orchestration layer over Unilever's existing Brand DNAi, digital-twin production and Desire at Scale capabilities — not a replacement for them.",
]
y = 4.7
for n in notes:
    textbox(s, 0.55, y, 12.3, 0.55, "•  " + n, size=8.8, color=TEXT_SECONDARY, line_spacing=1.2)
    y += 0.5

footer(s, "Appendix")

prs.save(OUT)
print("Saved:", OUT)
