"""Builds the Techtonic S8 / Project NEXT submission deck: cover + 3 required
content slides (synopsis & analysis / portfolio / product in depth) + appendix.
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
OUT = f"{HERE}/Techtonic_S8_Project_NEXT_PULSE.pptx"

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
textbox(s, 1.0, 1.6, 10.5, 0.4, "TECHTONIC SEASON 8  ·  PROJECT NEXT", size=15, color=CORAL, bold=True)
textbox(s, 1.0, 2.0, 11, 1.1, "PULSE", size=58, color=WHITE, bold=True)
textbox(s, 1.02, 3.12, 11, 0.5, "Unilever's Always-On Brand Nervous System", size=19, color=CYAN, bold=True)
textbox(s, 1.02, 3.62, 10.7, 0.7,
        "A portfolio of AI products on one shared backbone — proven end-to-end on the Rexona "
        "armband moment, with a working prototype of the flagship product, Moment Studio.",
        size=13, color=TEXT_SECONDARY, line_spacing=1.25)
textbox(s, 1.0, 4.35, 11, 0.35,
        "#AIAtUnilever   #TechDoneRight",
        size=11.5, color=TEXT_MUTED, italic=True)

rect(s, 1.0, 6.05, 3.2, 0.02, fill=GRID)
textbox(s, 1.0, 6.2, 8, 0.3, "Ranjana Mainani — Product Manager, Project NEXT", size=12, color=WHITE, bold=True)
textbox(s, 1.0, 6.5, 8, 0.3, "cases/2026-08-project-next-unilever-brand-lifecycle", size=10, color=TEXT_MUTED)
textbox(s, 1.0, 6.8, 10, 0.3, "Prototype: claude.ai/code/artifact/07a83b55-6cab-4866-937b-f4f79e9b7701", size=10, color=CYAN)

# =====================================================================
# SLIDE 1 / 3 — SYNOPSIS & ANALYSIS
# =====================================================================
s = add_slide()
bg(s)
slide_header(
    s, "1 / 3  —  SYNOPSIS & ANALYSIS",
    "The gap isn't tooling. It's synthesis — and it costs us the whole moment.",
    "Unilever already has social listening, web scraping and isolated AI pilots. They run independently, so a human manually stitches signal to publish — every time, across every stage of the lifecycle.",
)

add_picture_fit(s, f"{ASSETS}/timeline_comparison.png", 0.5, 1.62, 6.35, 2.35)
textbox(s, 0.55, 4.05, 6.25, 0.28, "WHAT'S ACTUALLY BROKEN", size=10.3, color=CORAL, bold=True)
multirun_textbox(s, 0.55, 4.35, 6.25, 2.5, [
    [{"text": "43-day agency pipeline", "size": 9.8, "color": WHITE, "bold": True},
     {"text": " vs. a viral window measured in minutes — by the time content ships, the moment is dead.", "size": 9.6, "color": TEXT_SECONDARY}],
    [{"text": "Point capabilities, zero wiring", "size": 9.8, "color": WHITE, "bold": True},
     {"text": " — listening, scraping and AI pilots exist but don't talk to each other; a human is the integration layer.", "size": 9.6, "color": TEXT_SECONDARY}],
    [{"text": "Every asset is bespoke", "size": 9.8, "color": WHITE, "bold": True},
     {"text": " — nothing from one campaign compounds into the next; each cycle restarts from zero.", "size": 9.6, "color": TEXT_SECONDARY}],
], line_spacing=1.2, space_after=10)

add_picture_fit(s, f"{ASSETS}/three_clockspeeds.png", 7.15, 1.55, 3.55, 3.55)
textbox(s, 10.85, 1.7, 1.9, 0.6, "REDEFINING THE LIFECYCLE — WHERE AI CREATES VALUE", size=9.6, color=CYAN, bold=True, line_spacing=1.2)
multirun_textbox(s, 10.85, 2.55, 1.95, 4.2, [
    [{"text": "Moments", "size": 9.4, "color": CYAN, "bold": True},
     {"text": " (min–hrs): sense & react before virality decays.", "size": 8.6, "color": TEXT_SECONDARY}],
    [{"text": "Campaigns", "size": 9.4, "color": CORAL, "bold": True},
     {"text": " (weeks): brief + production cut from weeks to days.", "size": 8.6, "color": TEXT_SECONDARY}],
    [{"text": "Strategy", "size": 9.4, "color": TEAL, "bold": True},
     {"text": " (qtrs–yrs): continuous signal replaces periodic research.", "size": 8.6, "color": TEXT_SECONDARY}],
], line_spacing=1.2, space_after=10)

rect(s, 0.55, 6.55, 12.25, 0.6, fill=CARD_LIGHT, radius=0.12)
textbox(s, 0.85, 6.66, 11.7, 0.4,
        "This isn't a tooling gap — it's a wiring gap. The fix is removing manual synthesis from the critical path, at every clock speed.",
        size=10.3, color=CYAN, italic=True, bold=True, anchor=MSO_ANCHOR.MIDDLE)

footer(s, "Page 2")

# =====================================================================
# SLIDE 2 / 3 — THE PORTFOLIO
# =====================================================================
s = add_slide()
bg(s)
slide_header(
    s, "2 / 3  —  THE PORTFOLIO",
    "Six products, one backbone — prioritized by dependency and time-to-value",
    "Every product below is built on PULSE: one Brand Signal Graph + Brand DNAi orchestration layer, not six separate AI builds.",
)

headers = ["Product", "Lifecycle stage", "Area of solution", "Core tech", "Phase"]
rows = [
    ["Signal Radar", "Perceive", "Unified real-time sensing", "Multi-source ingestion, brand/logo recognition", "1"],
    ["Playbook Studio", "Understand", "Governance & knowledge codification", "Rules+ML brand-fit/risk scoring", "1"],
    ["Moment Studio", "Localize + Ship (reactive)", "Real-time creative production & approval", "Multi-agent generation + human console", "1"],
    ["Campaign Composer", "Localize + Ship (planned)", "Planned content production", "Same generation agents, brief-driven", "2"],
    ["Brand Pulse Dashboard", "Evaluate", "Measurement & feedback", "Real-time analytics, closed-loop scoring", "2"],
    ["Strategy Compass", "Strategy", "Long-cycle positioning", "Longitudinal signal analysis", "3"],
]
row_colors = [CARD if i % 2 == 0 else CARD_LIGHT for i in range(len(rows))]
phase_colors = {"1": CORAL, "2": TEAL, "3": AMBER}

tbl = styled_table(s, 0.55, 1.72, 7.55, 3.15, headers, rows,
                    col_widths=[1.7, 1.5, 1.9, 1.9, 0.6], font_size=8.5, header_size=8.3, row_colors=row_colors)
for ri, row in enumerate(rows):
    cell = tbl.cell(ri + 1, 4)
    cell.text_frame.paragraphs[0].runs[0].font.color.rgb = phase_colors[row[-1]]
    cell.text_frame.paragraphs[0].runs[0].font.bold = True

add_picture_fit(s, f"{ASSETS}/portfolio_roadmap.png", 8.3, 1.72, 4.5, 2.15)

rect(s, 0.55, 5.1, 12.25, 1.95, fill=CARD, radius=0.04)
textbox(s, 0.8, 5.25, 11.7, 0.3, "PRIORITIZATION RATIONALE", size=10.5, color=CORAL, bold=True)
multirun_textbox(s, 0.8, 5.58, 11.7, 1.4, [
    [{"text": "Phase 1 — foundation + first win: ", "size": 9.7, "color": CORAL, "bold": True},
     {"text": "Signal Radar + Playbook Studio are prerequisites nothing else works without; Moment Studio ships alongside them as the fastest, highest-visibility proof of value.", "size": 9.5, "color": TEXT_SECONDARY}],
    [{"text": "Phase 2 — scale production: ", "size": 9.7, "color": TEAL, "bold": True},
     {"text": "Campaign Composer reuses Moment Studio's generation agents at near-zero incremental cost; Brand Pulse Dashboard closes the loop to justify further investment.", "size": 9.5, "color": TEXT_SECONDARY}],
    [{"text": "Phase 3 — compounding advantage: ", "size": 9.7, "color": AMBER, "bold": True},
     {"text": "Strategy Compass ships last, deliberately — it needs the longest accumulated signal history to be trustworthy.", "size": 9.5, "color": TEXT_SECONDARY}],
], line_spacing=1.2, space_after=6)

footer(s, "Page 3")

# =====================================================================
# SLIDE 3 / 3 — PRODUCT IN DEPTH: MOMENT STUDIO
# =====================================================================
s = add_slide()
bg(s)
slide_header(
    s, "3 / 3  —  PRODUCT IN DEPTH",
    "Moment Studio: user journey, agents, governance, cost & roadmap",
    None,
)

add_picture_fit(s, f"{ASSETS}/moment_studio_pipeline.png", 0.45, 1.42, 12.4, 2.28)

# Bottom row: 3 columns
col_w = 3.97
gap = 0.17
x0 = 0.55
y0 = 3.85
h = 2.95

# Column 1 — Capabilities + governance tiers
rect(s, x0, y0, col_w, h, fill=CARD, radius=0.05)
textbox(s, x0 + 0.16, y0 + 0.12, col_w - 0.32, 0.22, "CAPABILITIES", size=9, color=CYAN, bold=True)
caps = [
    "Real-time signal-to-playbook matching",
    "Multi-variant generative drafting (copy + visual)",
    "Side-by-side human review, inline editing",
    "One-click multi-market publish",
    "Full audit trail + kill-switch recall",
]
yy = y0 + 0.36
for c in caps:
    textbox(s, x0 + 0.16, yy, col_w - 0.32, 0.2, "•  " + c, size=7.8, color=TEXT_SECONDARY, line_spacing=1.05)
    yy += 0.195

textbox(s, x0 + 0.16, yy + 0.05, col_w - 0.32, 0.22, "HUMAN OVERSIGHT BY TIER", size=9, color=CYAN, bold=True)
tiers = [
    ("Tier 1", "Pre-cleared archetype", "Single-tap approve, ≤15 min SLA", TEAL),
    ("Tier 2", "Novel but on-strategy", "Full review + edit required", AMBER),
    ("Tier 3", "Off-playbook / sensitive", "Escalate to brand & legal, no AI draft", GRAY),
]
yy += 0.3
for t, trig, over, c in tiers:
    textbox(s, x0 + 0.16, yy, 0.55, 0.36, t, size=8, color=c, bold=True)
    textbox(s, x0 + 0.72, yy, col_w - 0.9, 0.36, trig + " — " + over, size=7.3, color=TEXT_SECONDARY, line_spacing=1.05)
    yy += 0.32

# Column 2 — Cost & roadmap
x2 = x0 + col_w + gap
rect(s, x2, y0, col_w, h, fill=CARD, radius=0.05)
textbox(s, x2 + 0.18, y0 + 0.14, col_w - 0.36, 0.25, "COST & IMPLEMENTATION ROADMAP", size=9.3, color=CYAN, bold=True)
c_headers = ["Phase", "Duration", "Squad", "Illustrative cost"]
c_rows = [
    ["MVP", "Mo. 0-3", "~6 (PM, 2-3 AI/ML eng, 1-2 full-stack, design)", "$250-400K"],
    ["Pilot expand", "Mo. 4-6", "Same squad + brand/legal governance lead", "$150-250K"],
    ["Phase 2 rollout", "Mo. 7-12", "+2 eng for Campaign Composer, Dashboard", "$400-600K"],
]
tbl2 = styled_table(s, x2 + 0.15, y0 + 0.44, col_w - 0.3, 1.7, c_headers, c_rows,
                     col_widths=[1.1, 0.9, 2.6, 1.15], font_size=7.3, header_size=7.2)
textbox(s, x2 + 0.18, y0 + 2.22, col_w - 0.36, 0.6,
        "Illustrative planning estimates only — not sourced Unilever cost data. Assumes reuse of existing Brand DNAi / digital-twin infrastructure.",
        size=7.4, color=TEXT_MUTED, italic=True, line_spacing=1.15)

# Column 3 — Prototype
x3 = x2 + col_w + gap
rect(s, x3, y0, col_w, h, fill=CARD, radius=0.05, line_color=CORAL, line_w=1.3)
textbox(s, x3 + 0.18, y0 + 0.14, col_w - 0.36, 0.25, "PROTOTYPE — TRY IT LIVE", size=9.3, color=CORAL, bold=True)
add_picture_fit(s, f"{ASSETS}/prototype_screenshot.png", x3 + 0.16, y0 + 0.42, col_w - 0.32, 1.72)
textbox(s, x3 + 0.18, y0 + 2.2, col_w - 0.36, 0.6,
        "Functional console: signal detected → AI-tiered → variants drafted → human approve → publish → performance feedback loop.",
        size=7.6, color=TEXT_SECONDARY, line_spacing=1.15)
textbox(s, x3 + 0.18, y0 + 2.62, col_w - 0.36, 0.25,
        "claude.ai/code/artifact/07a83b55…", size=7.8, color=CYAN, bold=True)

footer(s, "Page 4", "Full architecture, agent detail and cost assumptions in the appendix and analysis.md.")

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
    "Official brief (Techtonic Season 8, source PDF) requires 3 submission slides + a mandatory prototype; cover and this appendix sit outside that count.",
    "Timings in the Moment Studio walkthrough are illustrative targets for a system proposal, not measured data — the honest reference point is the cited literature's 30-50% production-time reduction from generative AI adoption.",
    "Cost estimates on slide 3 are illustrative planning placeholders, not sourced Unilever figures — flagged explicitly rather than presented as researched.",
    "Real-time computer-vision detection of an unscripted brand appearance (e.g. a logo on a match official's armband) is a genuinely hard sensing problem beyond text/social listening, flagged as build risk, not assumed solved.",
    "Human-tap approval, even fast-tracked (Tier 1, ≤15 min SLA), is a deliberate choice over fully autonomous publish — speed traded for governance rigor.",
    "The prototype (linked on cover and slide 3) is a UI/flow mock-up demonstrating the intended experience and decision logic — not wired to real Unilever data, Brand DNAi, or distribution systems.",
]
y = 4.7
for n in notes:
    textbox(s, 0.55, y, 12.3, 0.55, "•  " + n, size=8.5, color=TEXT_SECONDARY, line_spacing=1.15)
    y += 0.44

footer(s, "Appendix")

prs.save(OUT)
print("Saved:", OUT)
