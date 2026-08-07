"""PwC Challenge 8.0 — StyleVerse Global. Builds the Round-1 submission deck.

Format rules enforced from the case brief:
  * Executive Summary = exactly 2 slides
  * Body = exactly 10 slides
  * Appendix <= 50 slides
  * No text below 10 pt anywhere
  * Slide headers in Georgia, all content in Arial
  * APA references and stated assumptions in the footer

Run: python3 cases/2026-08-pwc-challenge-8-styleverse/deck/build_deck.py
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

HERE = "cases/2026-08-pwc-challenge-8-styleverse/deck"
ASSETS = f"{HERE}/assets"
OUT = f"{HERE}/PwC_Challenge8_StyleVerse_RanjanaMainani.pptx"

# ---- PwC palette ----
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
PAPER     = RGBColor(0xFA, 0xF8, 0xF7)
CARD      = RGBColor(0xF4, 0xF1, 0xEF)
ORANGE    = RGBColor(0xD0, 0x4A, 0x02)
TANGERINE = RGBColor(0xEB, 0x8C, 0x00)
GOLD      = RGBColor(0xFF, 0xB6, 0x00)
ROSE      = RGBColor(0xE0, 0x30, 0x1E)
CHARCOAL  = RGBColor(0x2D, 0x2D, 0x2D)
GREY      = RGBColor(0x7D, 0x7D, 0x7D)
LIGHTGREY = RGBColor(0xDE, 0xDA, 0xD6)
RULE      = RGBColor(0xC9, 0xC3, 0xBE)

HEAD_FONT = "Georgia"   # mandated for slide headers
BODY_FONT = "Arial"     # mandated for content
MIN_PT = 10             # mandated floor

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


def add_slide(bg_color=WHITE):
    s = prs.slides.add_slide(BLANK)
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = bg_color
    return s


def _apply(run, text, size, color, bold, italic, font):
    assert size >= MIN_PT, f"font {size}pt below mandated {MIN_PT}pt floor: {text[:40]!r}"
    run.text = text
    run.font.size = Pt(size)
    run.font.color.rgb = color
    run.font.bold = bold
    run.font.italic = italic
    run.font.name = font


def textbox(slide, l, t, w, h, text, size=12, color=CHARCOAL, bold=False, italic=False,
            align=PP_ALIGN.LEFT, font=BODY_FONT, anchor=MSO_ANCHOR.TOP,
            line_spacing=1.0, space_after=0):
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
        _apply(p.add_run(), line, size, color, bold, italic, font)
    return box


def rich(slide, l, t, w, h, paras, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
         line_spacing=1.15, space_after=7):
    """paras: list of list of dicts {text,size,color,bold,italic,font}"""
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
            _apply(p.add_run(), rd["text"], rd.get("size", 11), rd.get("color", CHARCOAL),
                   rd.get("bold", False), rd.get("italic", False), rd.get("font", BODY_FONT))
    return box


def rect(slide, l, t, w, h, fill=CARD, line_color=None, line_w=1.0, radius=None,
         shape=MSO_SHAPE.RECTANGLE):
    st = MSO_SHAPE.ROUNDED_RECTANGLE if radius is not None else shape
    sh = slide.shapes.add_shape(st, Inches(l), Inches(t), Inches(w), Inches(h))
    if radius is not None:
        try:
            sh.adjustments[0] = radius
        except Exception:
            pass
    if fill is None:
        sh.fill.background()
    else:
        sh.fill.solid()
        sh.fill.fore_color.rgb = fill
    if line_color is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line_color
        sh.line.width = Pt(line_w)
    sh.shadow.inherit = False
    return sh


def picture(slide, path, l, t, w, h):
    return slide.shapes.add_picture(path, Inches(l), Inches(t), width=Inches(w), height=Inches(h))


def header(slide, eyebrow, title, kicker_color=ORANGE):
    rect(slide, 0.5, 0.34, 0.5, 0.055, fill=kicker_color)
    textbox(slide, 0.5, 0.46, 11.5, 0.26, eyebrow, size=10, color=kicker_color,
            bold=True, font=BODY_FONT)
    textbox(slide, 0.5, 0.74, 12.4, 0.62, title, size=20, color=CHARCOAL, bold=True,
            font=HEAD_FONT, line_spacing=1.05)


def footer(slide, page, note=None):
    rect(slide, 0.5, 6.93, 12.33, 0.012, fill=RULE)
    if note:
        textbox(slide, 0.5, 7.02, 10.9, 0.36, note, size=10, color=GREY, font=BODY_FONT,
                line_spacing=1.1)
    textbox(slide, 11.5, 7.02, 1.33, 0.24, page, size=10, color=GREY,
            align=PP_ALIGN.RIGHT, font=BODY_FONT)


def table(slide, l, t, w, h, headers, rows, col_widths, font_size=10.5, header_size=10.5,
          header_fill=CHARCOAL, header_color=WHITE, zebra=True, align_first_left=True):
    gs = slide.shapes.add_table(len(rows) + 1, len(headers), Inches(l), Inches(t),
                                Inches(w), Inches(h))
    tbl = gs.table
    total = sum(col_widths)
    for i, cw in enumerate(col_widths):
        tbl.columns[i].width = Inches(w * cw / total)

    def fill_cell(cell, text, size, color, bold, bg, alignment):
        cell.fill.solid()
        cell.fill.fore_color.rgb = bg
        cell.margin_left = cell.margin_right = Inches(0.07)
        cell.margin_top = cell.margin_bottom = Inches(0.035)
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf = cell.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.alignment = alignment
        p.line_spacing = 1.05
        _apply(p.add_run(), str(text), size, color, bold, False, BODY_FONT)

    for ci, htxt in enumerate(headers):
        fill_cell(tbl.cell(0, ci), htxt, header_size, header_color, True, header_fill,
                  PP_ALIGN.LEFT if (ci == 0 and align_first_left) else PP_ALIGN.CENTER)
    for ri, row in enumerate(rows):
        bg = (WHITE if ri % 2 == 0 else PAPER) if zebra else WHITE
        for ci, val in enumerate(row):
            fill_cell(tbl.cell(ri + 1, ci), val, font_size, CHARCOAL, ci == 0, bg,
                      PP_ALIGN.LEFT if (ci == 0 and align_first_left) else PP_ALIGN.CENTER)
    el = tbl._tbl.find(qn("a:tblPr"))
    if el is not None:
        el.set("firstRow", "0")
        el.set("bandRow", "0")
    return tbl


def stat(slide, l, t, w, value, label, color=ORANGE, vsize=26, lsize=10.5, h=1.02):
    textbox(slide, l, t, w, 0.42, value, size=vsize, color=color, bold=True,
            font=HEAD_FONT, line_spacing=1.0)
    textbox(slide, l, t + 0.44, w, h - 0.44, label, size=lsize, color=CHARCOAL,
            font=BODY_FONT, line_spacing=1.15)


# ===========================================================================
# COVER
# ===========================================================================
s = add_slide()
rect(s, 0, 0, 13.333, 7.5, fill=WHITE)
# PwC parallelogram motif
rect(s, 8.6, 4.25, 3.1, 0.62, fill=ORANGE, shape=MSO_SHAPE.PARALLELOGRAM)
rect(s, 10.05, 5.05, 2.3, 0.62, fill=TANGERINE, shape=MSO_SHAPE.PARALLELOGRAM)
rect(s, 9.5, 3.45, 1.55, 0.62, fill=GOLD, shape=MSO_SHAPE.PARALLELOGRAM)

textbox(s, 0.9, 1.05, 6, 0.3, "pwc", size=26, color=CHARCOAL, bold=True, font=HEAD_FONT)
textbox(s, 0.9, 2.15, 8.0, 0.34, "PwC CHALLENGE 8.0  |  ROUND 1 SUBMISSION",
        size=11.5, color=ORANGE, bold=True)
textbox(s, 0.9, 2.62, 8.3, 1.5, "Designing a Better\nOrganization",
        size=44, color=CHARCOAL, bold=True, font=HEAD_FONT, line_spacing=1.02)
rect(s, 0.92, 4.28, 1.6, 0.035, fill=ORANGE)
textbox(s, 0.9, 4.5, 8.2, 0.9,
        "An enterprise AI operating-model blueprint for StyleVerse Global —\n"
        "automating 40% of routine work while protecting all 28,000 roles.",
        size=13.5, color=CHARCOAL, line_spacing=1.3)
rich(s, 0.9, 5.55, 8.2, 0.6, [[
    {"text": "“Our next phase of growth depends on designing a better organization.”",
     "size": 11.5, "color": GREY, "italic": True},
    {"text": "   — CEO, StyleVerse Global", "size": 10.5, "color": GREY},
]])
rect(s, 0.92, 6.45, 12.0, 0.012, fill=RULE)
textbox(s, 0.9, 6.62, 7, 0.26, "Ranjana Mainani", size=12, color=CHARCOAL, bold=True)
textbox(s, 0.9, 6.9, 7, 0.26, "Strategic consultant team, StyleVerse AI transformation",
        size=10, color=GREY)

# ===========================================================================
# EXECUTIVE SUMMARY 1 / 2
# ===========================================================================
s = add_slide()
header(s, "EXECUTIVE SUMMARY  |  1 OF 2",
       "AI should touch 82% of StyleVerse's work — and replace none of its 28,000 people")

rect(s, 0.5, 1.44, 12.33, 0.9, fill=CARD)
rich(s, 0.72, 1.6, 11.9, 0.66, [[
    {"text": "StyleVerse does not have a growth problem — it has a conversion problem. ",
     "size": 12.5, "bold": True},
    {"text": "Insight becomes action too slowly because work, not talent, is mis-allocated. "
             "We re-architect every role into three tiers, automate 40% of routine work, and "
             "redeploy the released capacity into customer-facing work.",
     "size": 12.5},
]], line_spacing=1.22)

stats = [
    ("54%", "of all work is routine —\nnot the 48% Exhibit 4\naverages to (weighted\nby headcount)", ORANGE),
    ("6,056", "FTE-equivalents of\ncapacity released —\nconverted, not cut,\nunder Zero-Layoff", ORANGE),
    ("₹311 Cr", "annual run-rate value\nagainst a ₹200 Cr\none-time investment\n(payback < 12 months)", ORANGE),
    ("13.1%", "EBITDA margin by FY26,\nup from 9.5% today —\non 15% revenue\ngrowth", ORANGE),
]
x = 0.5
for val, lab, c in stats:
    rect(s, x, 2.46, 2.93, 1.62, fill=WHITE, line_color=RULE, line_w=1.0)
    rect(s, x, 2.46, 2.93, 0.045, fill=c)
    stat(s, x + 0.22, 2.62, 2.5, val, lab, color=c, vsize=25, lsize=10.5, h=1.35)
    x += 3.11

rect(s, 0.5, 4.28, 6.05, 2.5, fill=WHITE, line_color=RULE, line_w=1.0)
textbox(s, 0.72, 4.44, 5.6, 0.26, "WHAT WE FOUND", size=10.5, color=ORANGE, bold=True)
rich(s, 0.72, 4.76, 5.62, 1.95, [
    [{"text": "The operating model is the constraint. ", "size": 11, "bold": True},
     {"text": "Every function optimises locally; nobody owns the handoffs between them.", "size": 11}],
    [{"text": "Routine work is under-counted. ", "size": 11, "bold": True},
     {"text": "The two largest functions are the most routine-heavy, so the true load is 54%, not 48%.", "size": 11}],
    [{"text": "The biggest prize is the least ready. ", "size": 11, "bold": True},
     {"text": "Retail Operations ranks #2 on value but scores 1.35/5 on adoption readiness (fear 4.3/5).", "size": 11}],
], line_spacing=1.2, space_after=8)

rect(s, 6.78, 4.28, 6.05, 2.5, fill=WHITE, line_color=RULE, line_w=1.0)
textbox(s, 7.0, 4.44, 5.6, 0.26, "WHAT WE RECOMMEND", size=10.5, color=ORANGE, bold=True)
rich(s, 7.0, 4.76, 5.62, 1.95, [
    [{"text": "Phase 1: Marketing & CX, Merchandising, Retail Ops ", "size": 11, "bold": True},
     {"text": "— but Retail enters as a 20-store readiness pilot, not a 200-store rollout.", "size": 11}],
    [{"text": "Federated hub-and-spoke AI CoE ", "size": 11, "bold": True},
     {"text": "— a central platform and standards hub with embedded squads in each function.", "size": 11}],
    [{"text": "Brand-differentiated governance. ", "size": 11, "bold": True},
     {"text": "Maison Luxe stays human-led by design; SpeedStyle goes AI-forward. One policy would damage one of them.", "size": 11}],
], line_spacing=1.2, space_after=8)

footer(s, "1",
       "All figures derived from case Exhibits 1–5. Assumptions: markdown reduction at 35% pass-through; "
       "return cost = 25% of item value; ₹1.2 L replacement cost per exit. See Appendix A3.")

# ===========================================================================
# EXECUTIVE SUMMARY 2 / 2
# ===========================================================================
s = add_slide()
header(s, "EXECUTIVE SUMMARY  |  2 OF 2",
       "Four deliverables, one integrated answer — sequenced to build trust before scale")

table(s, 0.5, 1.5, 12.33, 2.72,
      ["Deliverable", "Our answer", "The number that proves it", "Slide"],
      [
          ["1. Task audit",
           "Three-gate test applied to every activity → 22% Automatable, 60% Augmentable, 18% Fundamentally Human",
           "6,056 FTE-equivalents released", "B2–B3"],
          ["2. Priority + operating model",
           "Phase 1 = Marketing & CX, Merchandising, Retail Ops (pilot-first); federated hub-and-spoke CoE",
           "Model reproduces leadership's own ranking", "B4–B7"],
          ["3. Workforce strategy",
           "Four learning journeys, 12 → 40 learning hours, six new role families as redeployment destinations",
           "Zero roles lost; 31% → 25% attrition", "B8"],
          ["4. Governance + change",
           "Brand-differentiated AI policy, four-tier decision rights, Zero-Layoff Charter in month 1",
           "100% of AI decisions tiered and logged", "B9–B10"],
      ],
      col_widths=[2.0, 5.6, 2.9, 0.85], font_size=10.5, header_size=10.5)

textbox(s, 0.5, 4.44, 12.33, 0.26, "THE ROADMAP — TRUST FIRST, THEN SCALE", size=10.5,
        color=ORANGE, bold=True)
picture(s, f"{ASSETS}/roadmap.png", 0.5, 4.72, 7.35, 2.05)

rect(s, 8.1, 4.72, 4.73, 2.05, fill=CARD)
textbox(s, 8.32, 4.88, 4.3, 0.26, "WHY THIS SEQUENCE", size=10.5, color=ORANGE, bold=True)
rich(s, 8.32, 5.2, 4.32, 1.45, [
    [{"text": "Highest-readiness functions go first so the first visible AI story inside "
              "StyleVerse is a ", "size": 10.5},
     {"text": "success, not a threat", "size": 10.5, "bold": True},
     {"text": ".", "size": 10.5}],
    [{"text": "Manufacturing is last despite the largest headcount — fear is 4.5/5 and "
              "digital skill 1.8/5. Sequencing it early would confirm employees' worst fear "
              "and stall the whole programme.", "size": 10.5}],
], line_spacing=1.18, space_after=7)

footer(s, "2", "Phase-1 selection scored on the five criteria named in the case: business impact, "
                "customer value, workforce size, automation potential and implementation feasibility.")

# ===========================================================================
# BODY 1 — DIAGNOSIS
# ===========================================================================
s = add_slide()
header(s, "BODY  |  B1  ·  DIAGNOSIS",
       "Growth is not the problem. The gap between insight and action is.")

cards = [
    ("SPEED", "14 weeks", "trend-to-store, against\n<4 weeks for digitally\nnative competitors"),
    ("ACCURACY", "62%", "forecast accuracy drives\n26% unsold inventory and\n₹380 Cr of markdowns"),
    ("SERVICE", "88,000", "customer queries a month;\n48 hrs to resolve; 58%\nfirst-time fit accuracy"),
    ("PEOPLE", "42%", "attrition in Retail Ops on\njust 12 hours of structured\nlearning a year"),
]
x = 0.5
for tag, big, desc in cards:
    rect(s, x, 1.5, 2.93, 1.72, fill=WHITE, line_color=RULE, line_w=1.0)
    textbox(s, x + 0.22, 1.66, 2.5, 0.24, tag, size=10, color=ORANGE, bold=True)
    textbox(s, x + 0.22, 1.94, 2.5, 0.46, big, size=27, color=CHARCOAL, bold=True, font=HEAD_FONT)
    textbox(s, x + 0.22, 2.46, 2.55, 0.72, desc, size=10.5, color=CHARCOAL, line_spacing=1.2)
    x += 3.11

rect(s, 0.5, 3.42, 12.33, 1.12, fill=CHARCOAL)
rich(s, 0.78, 3.62, 11.8, 0.8, [
    [{"text": "The common cause:  ", "size": 12.5, "color": GOLD, "bold": True},
     {"text": "each function has optimised its own systems and processes — so the handoffs "
              "between them are owned by nobody and bridged manually.",
      "size": 12.5, "color": WHITE}],
    [{"text": "AI applied function-by-function would automate the silos instead of dissolving them. "
              "The unit of redesign has to be the workflow, not the department.",
      "size": 11.5, "color": LIGHTGREY}],
], line_spacing=1.2, space_after=6)

rect(s, 0.5, 4.74, 6.05, 2.04, fill=CARD)
textbox(s, 0.72, 4.9, 5.6, 0.26, "AND THE PRIZE IS BIGGER THAN IT LOOKS", size=10.5,
        color=ORANGE, bold=True)
rich(s, 0.72, 5.22, 5.62, 1.4, [
    [{"text": "Exhibit 4 reports an organisation average of 48% routine work. That is an ",
      "size": 11},
     {"text": "unweighted", "size": 11, "bold": True},
     {"text": " mean of the six functions.", "size": 11}],
    [{"text": "Weighted by headcount it is 54.1%", "size": 11, "bold": True, "color": ORANGE},
     {"text": " — because the two largest functions (Manufacturing 11,000 at 60%; Retail 10,000 "
              "at 55%) are the most routine-heavy of all.", "size": 11}],
], line_spacing=1.2, space_after=7)

rect(s, 6.78, 4.74, 6.05, 2.04, fill=CARD)
textbox(s, 7.0, 4.9, 5.6, 0.26, "WHY THAT MATTERS", size=10.5, color=ORANGE, bold=True)
rich(s, 7.0, 5.22, 5.62, 1.4, [
    [{"text": "A 5.7-point understatement is roughly ", "size": 11},
     {"text": "1,600 FTE-equivalents", "size": 11, "bold": True},
     {"text": " of routine work missing from the plan — larger than the entire Corporate function.",
      "size": 11}],
    [{"text": "Sizing the programme off the headline average would under-scope the platform, "
              "the reskilling budget and the redeployment pipeline.", "size": 11}],
], line_spacing=1.2, space_after=7)

footer(s, "3", "Source: case Exhibits 3 and 4. Weighted routine load = Σ(headcount × routine %) ÷ 28,000 = 54.1%.")

# ===========================================================================
# BODY 2 — TASK AUDIT FRAMEWORK
# ===========================================================================
s = add_slide()
header(s, "BODY  |  B2  ·  DELIVERABLE 1",
       "Every activity passes the same three gates — so the classification is defensible, not arbitrary")

gates = [
    ("GATE 1", "Rule stability", "Is the activity governed by stable, codifiable rules,\nat high volume and low variance?", ORANGE),
    ("GATE 2", "Consequence of error", "Would a mistake cause irreversible customer,\nregulatory or brand harm?", TANGERINE),
    ("GATE 3", "Human premium", "Does the customer or the business specifically\nvalue that a human did it?", GOLD),
]
x = 0.5
for tag, name, q, c in gates:
    rect(s, x, 1.5, 4.03, 1.5, fill=WHITE, line_color=c, line_w=1.5)
    rect(s, x, 1.5, 4.03, 0.05, fill=c)
    textbox(s, x + 0.22, 1.68, 3.6, 0.24, tag, size=10, color=c, bold=True)
    textbox(s, x + 0.22, 1.94, 3.6, 0.3, name, size=14, color=CHARCOAL, bold=True, font=HEAD_FONT)
    textbox(s, x + 0.22, 2.32, 3.65, 0.6, q, size=10.5, color=CHARCOAL, line_spacing=1.2)
    x += 4.15

table(s, 0.5, 3.22, 12.33, 1.62,
      ["Classification", "Gate signature", "What the human does", "Design principle"],
      [
          ["Automatable", "G1 yes · G2 low · G3 no",
           "Sets the rules, handles exceptions, audits the output",
           "AI executes; human owns the standard"],
          ["Augmentable", "G1 partial, or G2 high",
           "Decides, using AI-prepared options and evidence",
           "AI proposes; human disposes"],
          ["Fundamentally Human", "G3 yes, or G2 critical",
           "Creates, judges, empathises, takes accountability",
           "AI supplies inputs; never the output"],
      ],
      col_widths=[2.3, 2.65, 3.9, 3.48], font_size=10.5, header_size=10.5)

rect(s, 0.5, 5.06, 12.33, 1.72, fill=CARD)
textbox(s, 0.72, 5.22, 11.9, 0.26, "WHERE WE CHALLENGE EXHIBIT 4 — as the case invites",
        size=10.5, color=ORANGE, bold=True)
rich(s, 0.72, 5.54, 5.7, 1.1, [
    [{"text": "Retail Operations — the human share is a design choice, not a constant. ",
      "size": 11, "bold": True},
     {"text": "Exhibit 4 shows 20% creative/strategic. Once AI removes stock look-ups and admin, "
              "we deliberately redesign the role upward to ~35% relationship work.", "size": 11}],
], line_spacing=1.2, space_after=6)
rich(s, 6.62, 5.54, 5.9, 1.1, [
    [{"text": "Manufacturing — routine ≠ automatable. ", "size": 11, "bold": True},
     {"text": "60% of its work is routine, but quality inspection carries safety and regulatory "
              "consequence (Gate 2). Most of it is Augmentable — AI-assisted vision with human "
              "sign-off — not Automatable.", "size": 11}],
], line_spacing=1.2, space_after=6)

footer(s, "4", "Classification applied to all six functions in case Exhibit 4; activity-level detail in Appendix A1.")

# ===========================================================================
# BODY 3 — TASK AUDIT RESULTS
# ===========================================================================
s = add_slide()
header(s, "BODY  |  B3  ·  DELIVERABLE 1",
       "AI touches 82% of the work and replaces 0% of the people")

picture(s, f"{ASSETS}/task_audit.png", 0.5, 1.46, 8.15, 3.08)

rect(s, 8.9, 1.46, 3.93, 3.08, fill=CARD)
textbox(s, 9.12, 1.62, 3.5, 0.26, "TARGET STATE, ORGANISATION-WIDE", size=10.5,
        color=ORANGE, bold=True)
splits = [("22%", "Automatable", ORANGE), ("60%", "Augmentable", GOLD),
          ("18%", "Fundamentally Human", CHARCOAL)]
yy = 1.98
for pct, lab, c in splits:
    rect(s, 9.12, yy + 0.05, 0.11, 0.34, fill=c)
    textbox(s, 9.36, yy, 1.1, 0.34, pct, size=19, color=c, bold=True, font=HEAD_FONT)
    textbox(s, 10.42, yy + 0.06, 2.3, 0.3, lab, size=11, color=CHARCOAL, bold=True)
    yy += 0.52
rect(s, 9.12, 3.62, 3.5, 0.012, fill=RULE)
rich(s, 9.12, 3.76, 3.55, 0.7, [
    [{"text": "Only the 22% is executed by AI alone. The 60% is where humans get faster and "
              "better — and it is the largest prize.", "size": 10.5}],
], line_spacing=1.2)

picture(s, f"{ASSETS}/capacity.png", 0.5, 4.72, 6.6, 2.06)

rect(s, 7.35, 4.72, 5.48, 2.06, fill=CHARCOAL)
textbox(s, 7.57, 4.88, 5.05, 0.26, "THE ZERO-LAYOFF ARITHMETIC", size=10.5, color=GOLD, bold=True)
rich(s, 7.57, 5.2, 5.06, 1.45, [
    [{"text": "15,140 ", "size": 12, "color": WHITE, "bold": True},
     {"text": "FTE-equivalents of routine work exist today. Automating 40% of it releases ",
      "size": 11, "color": LIGHTGREY},
     {"text": "6,056 FTE-equivalents", "size": 12, "color": GOLD, "bold": True},
     {"text": " — 21.6% of the workforce.", "size": 11, "color": LIGHTGREY}],
    [{"text": "Under Zero-Layoff this is capacity ", "size": 11, "color": LIGHTGREY},
     {"text": "converted, not cost cut", "size": 11, "color": WHITE, "bold": True},
     {"text": ". The ₹200 Cr does not buy a smaller payroll — it buys the same payroll doing "
              "higher-value work.", "size": 11, "color": LIGHTGREY}],
], line_spacing=1.2, space_after=7)

footer(s, "5", "Automatable = 40% of routine work per the case constraint. Augmentable = residual routine "
                "+ all judgment work. Fundamentally Human = all creative/strategic work.")

# ===========================================================================
# BODY 4 — PRIORITIZATION
# ===========================================================================
s = add_slide()
header(s, "BODY  |  B4  ·  DELIVERABLE 2",
       "The highest-value function is the least ready — so value alone cannot set the sequence")

picture(s, f"{ASSETS}/readiness_matrix.png", 0.42, 1.46, 6.6, 4.4)

table(s, 7.2, 1.46, 5.63, 2.5,
      ["Function", "Score", "Readiness", "Case priority"],
      [
          ["Marketing & CX", "4.05", "3.68", "Very High"],
          ["Retail Operations", "3.95", "1.35", "Very High"],
          ["Merchandising & Planning", "3.55", "2.73", "High"],
          ["Manufacturing & Quality", "3.10", "0.98", "Medium"],
          ["Design & Creative", "3.05", "3.83", "Medium"],
          ["Corporate", "2.80", "3.63", "Medium"],
      ],
      col_widths=[2.5, 0.95, 1.1, 1.4], font_size=10.5, header_size=10.5)

rect(s, 7.2, 4.14, 5.63, 1.14, fill=CARD)
rich(s, 7.42, 4.3, 5.2, 0.86, [
    [{"text": "Our model independently reproduces leadership's own ranking", "size": 11, "bold": True},
     {"text": " — the two “Very High” functions score #1 and #2, and “High” scores #3. "
              "The model does not overturn management judgment; it explains and sizes it.", "size": 11}],
], line_spacing=1.2)

rect(s, 7.2, 5.44, 5.63, 1.34, fill=WHITE, line_color=ROSE, line_w=1.5)
textbox(s, 7.42, 5.6, 5.2, 0.26, "THE READINESS PARADOX", size=10.5, color=ROSE, bold=True)
rich(s, 7.42, 5.92, 5.22, 0.78, [
    [{"text": "Retail Operations: ", "size": 11, "bold": True},
     {"text": "10,000 people, 200 stores, #2 on value — and 1.35/5 on readiness, with fear at "
              "4.3/5 and digital skill at 2.2/5. Deploying at scale here first would fail.", "size": 11}],
], line_spacing=1.2)

footer(s, "6", "Priority score = 0.25×business impact + 0.20×customer value + 0.15×workforce scale "
                "+ 0.20×automation potential + 0.20×feasibility. Readiness = mean(awareness, willingness, "
                "digital skill) − 0.5×(fear − 2.0). Scoring detail in Appendix A2.")

# ===========================================================================
# BODY 5 — PHASE 1
# ===========================================================================
s = add_slide()
header(s, "BODY  |  B5  ·  DELIVERABLE 2",
       "Phase 1: two functions scale, one function earns trust first")

phase1 = [
    ("MARKETING & CUSTOMER EXPERIENCE", "2,500 people  ·  readiness 3.68  ·  SCALE NOW", ORANGE,
     "AI service agent deflects delivery, returns and size/fit queries; unified customer profile "
     "across five brands; generative campaign variants.",
     "48 hrs → under 6 hrs resolution\n58% → 75% first-time fit accuracy"),
    ("MERCHANDISING & PLANNING", "1,200 people  ·  readiness 2.73  ·  SCALE NOW", ORANGE,
     "Demand sensing on external signals (social, weather, events); AI allocation and "
     "size-curve optimisation; exception-based planning replaces spreadsheets.",
     "62% → 78% forecast accuracy\n₹380 Cr → ₹247 Cr markdowns"),
    ("RETAIL OPERATIONS", "10,000 people  ·  readiness 1.35  ·  PILOT FIRST", TANGERINE,
     "20-store pilot: voice stock look-up, AI clienteling prompts, auto-rostering. Scale to 200 "
     "stores only after adoption and sentiment gates are met.",
     "42% → 32% attrition in pilot stores\nAssociate selling time +30%"),
]
y = 1.46
CARD_H, CARD_GAP = 1.42, 1.53
for name, meta, c, what, metric in phase1:
    rect(s, 0.5, y, 12.33, CARD_H, fill=WHITE, line_color=RULE, line_w=1.0)
    rect(s, 0.5, y, 0.06, CARD_H, fill=c)
    textbox(s, 0.78, y + 0.13, 6.3, 0.28, name, size=13, color=CHARCOAL, bold=True, font=HEAD_FONT)
    textbox(s, 0.78, y + 0.43, 6.3, 0.24, meta, size=10, color=c, bold=True)
    textbox(s, 0.78, y + 0.71, 6.35, 0.62, what, size=10.5, color=CHARCOAL, line_spacing=1.2)
    rect(s, 7.5, y + 0.16, 0.012, 1.10, fill=RULE)
    textbox(s, 7.78, y + 0.16, 4.9, 0.24, "TARGET MOVEMENT", size=10, color=GREY, bold=True)
    textbox(s, 7.78, y + 0.46, 4.9, 0.8, metric, size=12, color=CHARCOAL, bold=True,
            font=HEAD_FONT, line_spacing=1.35)
    y += CARD_GAP

rect(s, 0.5, 6.05, 12.33, 0.73, fill=CHARCOAL)
rich(s, 0.78, 6.2, 11.8, 0.5, [[
    {"text": "Deferred deliberately:  ", "size": 11.5, "color": GOLD, "bold": True},
    {"text": "Manufacturing & Quality (11,000 people) carries the largest routine load but the "
             "lowest readiness — it is Phase 3, paired with EPR traceability where AI creates new "
             "compliance roles rather than displacing existing ones.",
     "size": 11.5, "color": WHITE}],
], line_spacing=1.2)

footer(s, "7", "Pilot gate: adoption ≥70% of associates using the tool weekly and no decline in employee "
                "sentiment before scaling beyond 20 stores.")

# ===========================================================================
# BODY 6 — OPERATING MODEL
# ===========================================================================
s = add_slide()
header(s, "BODY  |  B6  ·  DELIVERABLE 2",
       "The workflow, not the org chart, is the unit of redesign")

textbox(s, 0.5, 1.44, 6.0, 0.26, "TODAY — SEQUENTIAL HANDOFFS", size=10.5, color=GREY, bold=True)
steps_now = ["Designer researches\ntrends manually", "Merchandising reviews\nhistorical sales",
             "Multiple approval\ncycles", "Retail executes\nwith no context"]
x = 0.5
for st in steps_now:
    rect(s, x, 1.74, 1.42, 0.86, fill=CARD, line_color=RULE, line_w=1.0)
    textbox(s, x + 0.09, 1.86, 1.24, 0.66, st, size=10, color=GREY, line_spacing=1.15,
            align=PP_ALIGN.CENTER)
    x += 1.53
textbox(s, 0.5, 2.68, 6.0, 0.26, "14 weeks  ·  62% forecast accuracy", size=11,
        color=ROSE, bold=True)

textbox(s, 6.9, 1.44, 6.0, 0.26, "FUTURE — ONE CONCURRENT WORKFLOW", size=10.5,
        color=ORANGE, bold=True)
rect(s, 6.9, 1.74, 5.93, 0.86, fill=WHITE, line_color=ORANGE, line_w=1.5)
textbox(s, 7.1, 1.86, 5.5, 0.3, "Shared signal & decision layer", size=12,
        color=CHARCOAL, bold=True, font=HEAD_FONT)
textbox(s, 7.1, 2.18, 5.5, 0.3, "Design · Merchandising · Retail work on the same live view",
        size=10.5, color=CHARCOAL)
textbox(s, 6.9, 2.68, 6.0, 0.26, "8 weeks  ·  78% forecast accuracy", size=11,
        color=ORANGE, bold=True)

table(s, 0.5, 3.16, 12.33, 2.28,
      ["Layer", "What changes", "Who owns it"],
      [
          ["Structure",
           "Cross-functional Product & Customer squads replace function-only teams for the 3 Phase-1 workflows",
           "Chief AI & Transformation Officer (new, reports to CEO)"],
          ["Roles",
           "Six new role families created as redeployment destinations; no role eliminated",
           "Function heads with CHRO"],
          ["Workflows",
           "Approval cycles replaced by exception-based review — humans intervene where AI flags uncertainty",
           "Squad leads, standards set by the AI CoE"],
          ["Decision rights",
           "Every AI-influenced decision assigned to one of four tiers with a named accountable human",
           "AI Governance Council"],
      ],
      col_widths=[1.6, 6.9, 3.83], font_size=10.5, header_size=10.5)

rect(s, 0.5, 5.6, 12.33, 1.18, fill=CARD)
textbox(s, 0.72, 5.76, 11.9, 0.26, "THE ONE STRUCTURAL RULE", size=10.5, color=ORANGE, bold=True)
rich(s, 0.72, 6.06, 11.9, 0.6, [[
    {"text": "No AI system is deployed into a workflow that still requires a manual handoff to "
             "complete. ", "size": 11.5, "bold": True},
    {"text": "Automating either side of a broken handoff makes the handoff the bottleneck and "
             "delivers none of the cycle-time gain — this is precisely how StyleVerse's current "
             "fragmentation was created.", "size": 11.5},
]], line_spacing=1.2)

footer(s, "8", "Cycle-time target of 8 weeks assumes concurrent design–merchandising review replaces "
                "three sequential approval cycles; benchmark competitors operate at under 4 weeks.")

# ===========================================================================
# BODY 7 — AI CoE
# ===========================================================================
s = add_slide()
header(s, "BODY  |  B7  ·  DELIVERABLE 2",
       "Recommendation: a federated hub-and-spoke CoE — centralised standards, embedded delivery")

blocks = [
    ("THE HUB", "AI Centre of Excellence", "~60 FTE", ORANGE,
     "Owns the data platform, MLOps, reusable components, model risk, standards and talent "
     "development. Reports to the Chief AI & Transformation Officer."),
    ("THE SPOKES", "Embedded AI squads", "8–10 FTE each", TANGERINE,
     "One squad per Phase-1 function, sitting inside the business. Owns use cases end to end. "
     "Dual reporting: outcomes to the function head, standards to the hub."),
    ("THE BRIDGE", "AI Translators", "~30, rotating", GOLD,
     "Business people trained to specify and test use cases — drawn from existing employees, "
     "making this the first and most visible redeployment destination."),
]
x = 0.5
for tag, name, size_lbl, c, desc in blocks:
    rect(s, x, 1.46, 4.03, 2.2, fill=WHITE, line_color=c, line_w=1.5)
    rect(s, x, 1.46, 4.03, 0.05, fill=c)
    textbox(s, x + 0.22, 1.64, 3.6, 0.24, tag, size=10, color=c, bold=True)
    textbox(s, x + 0.22, 1.9, 3.6, 0.3, name, size=14, color=CHARCOAL, bold=True, font=HEAD_FONT)
    textbox(s, x + 0.22, 2.24, 3.6, 0.24, size_lbl, size=10.5, color=GREY, bold=True)
    textbox(s, x + 0.22, 2.56, 3.65, 1.0, desc, size=10.5, color=CHARCOAL, line_spacing=1.2)
    x += 4.15

table(s, 0.5, 3.86, 12.33, 1.62,
      ["Model", "Strength", "Why it fails at StyleVerse"],
      [
          ["Fully centralised CoE", "Consistent standards, no duplicated spend",
           "Too far from five brands with genuinely different value propositions; becomes a queue"],
          ["Fully embedded in functions", "Fast, close to the business",
           "Recreates the exact fragmentation the case describes — duplicated tools, no shared model risk"],
          ["Federated hub-and-spoke  ✓", "Shared platform and governance, local ownership of outcomes",
           "Requires disciplined dual reporting — mitigated by a single standards charter"],
      ],
      col_widths=[2.85, 4.0, 5.48], font_size=10.5, header_size=10.5)

rect(s, 0.5, 5.68, 12.33, 1.1, fill=CHARCOAL)
rich(s, 0.78, 5.86, 11.8, 0.74, [[
    {"text": "The deciding argument:  ", "size": 11.5, "color": GOLD, "bold": True},
    {"text": "StyleVerse's current problem was caused by functions independently introducing "
             "“their own systems, processes and ways of working.” A fully embedded AI model "
             "would repeat that mistake with higher stakes — five brands each training their own "
             "models on their own data, with no shared governance and no shared learning.",
     "size": 11.5, "color": WHITE}],
], line_spacing=1.22)

footer(s, "9", "CoE sizing assumption: ~60 hub FTE and 3 squads of 8–10 in Phase 1, funded from the "
                "₹55 Cr use-case build and ₹60 Cr platform allocations. Roles filled substantially by internal redeployment.")

# ===========================================================================
# BODY 8 — WORKFORCE
# ===========================================================================
s = add_slide()
header(s, "BODY  |  B8  ·  DELIVERABLE 3",
       "6,056 FTE-equivalents of capacity need a destination — we name six")

table(s, 0.5, 1.46, 12.33, 2.28,
      ["From (routine work automated)", "To (new role family)", "What the role does", "Scale"],
      [
          ["Retail associates — stock look-ups, billing, admin",
           "Style Advisor", "Clienteling, styling, repeat-purchase building", "~2,200"],
          ["Planners — spreadsheet consolidation, sales pulls",
           "Demand Scientist", "Scenario planning, exceptions, model challenge", "~240"],
          ["Service reps — delivery, returns, size/fit queries",
           "Experience Specialist", "Complex, high-value, multi-brand resolution", "~400"],
          ["Manufacturing QC — repetitive inspection, reporting",
           "Traceability & Compliance Analyst", "EPR and circular-textiles traceability; supplier audit", "~2,640"],
          ["Corporate — report preparation, data gathering",
           "AI Translator / Process Owner", "Specifies, tests and owns AI use cases", "~396"],
          ["Designers — trend scanning, competitor collation",
           "Concept Lead", "More concepts per designer; EcoWeave expansion", "~180"],
      ],
      col_widths=[4.0, 2.7, 4.5, 1.13], font_size=10.5, header_size=10.5)

textbox(s, 0.5, 3.92, 6.6, 0.26, "FOUR LEARNING JOURNEYS  ·  12 → 40 HOURS PER EMPLOYEE",
        size=10.5, color=ORANGE, bold=True)
table(s, 0.5, 4.2, 6.35, 1.7,
      ["Journey", "Who", "Hours"],
      [
          ["AI Aware", "All 28,000", "16"],
          ["AI Assisted", "~18,000 operational roles", "40"],
          ["AI Enabled", "~8,000 judgment roles", "80"],
          ["AI Builders", "~800 squads & translators", "200"],
      ],
      col_widths=[1.75, 3.3, 1.3], font_size=10.5, header_size=10.5)

rect(s, 7.1, 4.2, 5.73, 1.7, fill=WHITE, line_color=ROSE, line_w=1.5)
textbox(s, 7.32, 4.34, 5.3, 0.26, "KNOWLEDGE CAPTURE IS A RACE AGAINST ATTRITION",
        size=10.5, color=ROSE, bold=True)
rich(s, 7.32, 4.64, 5.32, 1.2, [
    [{"text": "Retail tenure is 1.7 years at 42% attrition — institutional knowledge is already "
              "leaking faster than it is being recorded.", "size": 11}],
    [{"text": "We capture tacit know-how from the high-tenure functions (Corporate 5.1 yrs, "
              "Design 4.6 yrs) into structured knowledge bases ", "size": 11},
     {"text": "in Phase 0", "size": 11, "bold": True},
     {"text": " — before automation changes the roles that hold it.", "size": 11}],
], line_spacing=1.18, space_after=6)

rect(s, 0.5, 6.0, 12.33, 0.78, fill=CARD)
rich(s, 0.72, 6.16, 11.9, 0.52, [[
    {"text": "The Zero-Layoff mechanism:  ", "size": 11.5, "bold": True, "color": ORANGE},
    {"text": "a written redeployment guarantee, an internal talent marketplace matching released "
             "capacity to open roles on skills rather than titles, and a 90-day paid transition "
             "window with the learning journey completed before the role changes.", "size": 11.5},
]], line_spacing=1.2)

footer(s, "10", "Scale column = FTE-equivalents released per function (Appendix A1). Learning-hour targets "
                 "benchmarked against the case's stated 12 hours per employee per year.")

# ===========================================================================
# BODY 9 — GOVERNANCE
# ===========================================================================
s = add_slide()
header(s, "BODY  |  B9  ·  DELIVERABLE 4",
       "One AI policy across five brands would damage the most valuable one")

table(s, 0.5, 1.46, 12.33, 1.96,
      ["Brand", "NPS", "Brand promise", "AI posture", "Disclosure"],
      [
          ["Maison Luxe", "62", "Craftsmanship and human exclusivity",
           "Back-office only — no generative design, no AI-written client contact", "Human-crafted assurance"],
          ["EcoWeave", "55", "Environmental responsibility",
           "AI for traceability, EPR compliance and transparency reporting", "Publish AI use openly"],
          ["UrbanEdge", "48", "Seamless omnichannel",
           "AI personalisation and service across channels", "Disclosed at interaction"],
          ["SpeedStyle", "35", "Speed and trend",
           "AI-forward — trend sensing, generative concepts, service automation", "Disclosed at interaction"],
          ["ThreadBasics", "30", "Affordability and efficiency",
           "Maximum service and supply-chain automation", "Disclosed at interaction"],
      ],
      col_widths=[1.7, 0.7, 3.0, 4.6, 2.33], font_size=10.5, header_size=10.5)

textbox(s, 0.5, 3.6, 6.0, 0.26, "AI DECISION RIGHTS — FOUR TIERS", size=10.5, color=ORANGE, bold=True)
table(s, 0.5, 3.9, 6.35, 1.94,
      ["Tier", "Example", "Control"],
      [
          ["1 Auto", "Stock look-up, delivery status reply", "Logged, sampled"],
          ["2 Assisted", "Allocation, campaign targeting", "Human approves"],
          ["3 Sign-off", "Pricing, markdown, QC release", "Named accountable owner"],
          ["4 Prohibited", "Hiring, exit, credit decisions", "No AI involvement"],
      ],
      col_widths=[1.4, 3.3, 2.1], font_size=10.5, header_size=10.5)

rect(s, 7.1, 3.9, 5.73, 1.94, fill=CARD)
textbox(s, 7.32, 4.06, 5.3, 0.26, "TRUST, DATA, IP AND REGULATION", size=10.5,
        color=ORANGE, bold=True)
rich(s, 7.32, 4.38, 5.32, 1.4, [
    [{"text": "Data privacy: ", "size": 10.5, "bold": True},
     {"text": "DPDP Act 2023 for India, GDPR for European operations — consent, purpose "
              "limitation and residency enforced in the platform, not per project.", "size": 10.5}],
    [{"text": "IP: ", "size": 10.5, "bold": True},
     {"text": "training-data provenance recorded for every model; no competitor imagery scraped; "
              "designer attribution retained on AI-assisted concepts.", "size": 10.5}],
    [{"text": "Bias: ", "size": 10.5, "bold": True},
     {"text": "sizing and recommendation models tested across body types and demographics before "
              "release, and quarterly thereafter.", "size": 10.5}],
], line_spacing=1.15, space_after=5)

rect(s, 0.5, 6.0, 12.33, 0.78, fill=CHARCOAL)
rich(s, 0.72, 6.16, 11.9, 0.52, [[
    {"text": "Why brand-differentiated governance is the right call:  ", "size": 11.5,
     "color": GOLD, "bold": True},
    {"text": "Maison Luxe earns the highest NPS (62) and the lowest return rate (8%) precisely "
             "because customers believe a person made it. Applying SpeedStyle's AI posture there "
             "would automate away the thing being sold.", "size": 11.5, "color": WHITE},
]], line_spacing=1.2)

footer(s, "11", "References: European Parliament. (2024). Regulation (EU) 2024/1689 (AI Act). "
                 "Ministry of Electronics and IT. (2023). Digital Personal Data Protection Act, 2023. "
                 "NIST. (2023). AI Risk Management Framework 1.0.")

# ===========================================================================
# BODY 10 — CHANGE MANAGEMENT + INVESTMENT
# ===========================================================================
s = add_slide()
header(s, "BODY  |  B10  ·  DELIVERABLE 4",
       "Fear is measurable, so it is manageable — we treat it as the primary delivery risk")

table(s, 0.5, 1.46, 6.35, 2.02,
      ["Function", "Fear", "Intervention"],
      [
          ["Manufacturing", "4.5", "Phase 3 entry; EPR roles announced before tooling"],
          ["Retail Operations", "4.3", "20-store pilot; associates co-design the tool"],
          ["Merchandising", "3.0", "Planners become model challengers, not subjects"],
          ["Marketing / Design / Corp.", "≤2.5", "Champion source — seed advocates into the above"],
      ],
      col_widths=[2.4, 0.85, 4.6], font_size=10.5, header_size=10.5)

rect(s, 7.1, 1.46, 5.73, 2.02, fill=WHITE, line_color=ORANGE, line_w=1.5)
textbox(s, 7.32, 1.6, 5.3, 0.26, "FOUR MOVES, IN THIS ORDER", size=10.5, color=ORANGE, bold=True)
moves = [
    ("BELIEVE", "Zero-Layoff Charter, board-backed, published month 1"),
    ("BUILD", "Learning journeys start before tools arrive, not after"),
    ("BOND", "500 AI Champions (~2%) from high-willingness functions"),
    ("BEHAVE", "Adoption written into KPIs; redeployment celebrated"),
]
yy = 1.92
for tag, desc in moves:
    textbox(s, 7.32, yy, 1.15, 0.24, tag, size=10.5, color=ORANGE, bold=True)
    textbox(s, 8.5, yy, 4.2, 0.3, desc, size=10.5, color=CHARCOAL, line_spacing=1.1)
    yy += 0.37

textbox(s, 0.5, 3.66, 12.33, 0.26, "THE ₹200 CRORE, ALLOCATED", size=10.5, color=ORANGE, bold=True)
picture(s, f"{ASSETS}/investment.png", 0.5, 3.94, 7.5, 1.34)

rect(s, 8.25, 3.94, 4.58, 1.34, fill=CARD)
rich(s, 8.47, 4.08, 4.15, 1.05, [[
    {"text": "22% on people is deliberate. ", "size": 11, "bold": True},
    {"text": "Most transformations underfund reskilling and then discover the technology "
             "landed but the behaviour did not. Zero-Layoff is only credible if the "
             "redeployment budget is real.", "size": 11}],
], line_spacing=1.18)

textbox(s, 0.5, 5.42, 12.33, 0.26, "THE VALUE THIS UNLOCKS", size=10.5, color=ORANGE, bold=True)
picture(s, f"{ASSETS}/value_bridge.png", 0.5, 5.66, 7.7, 1.16)

rect(s, 8.45, 5.66, 4.38, 1.16, fill=CHARCOAL)
rich(s, 8.67, 5.78, 4.0, 0.98, [
    [{"text": "₹311 Cr", "size": 17, "color": GOLD, "bold": True, "font": HEAD_FONT},
     {"text": "  annual run-rate", "size": 11, "color": WHITE}],
    [{"text": "against ₹200 Cr one-time — payback under 12 months, and EBITDA margin from "
              "9.5% to 13.1%.", "size": 10.5, "color": LIGHTGREY}],
], line_spacing=1.18, space_after=4)

footer(s, "12", "Value bridge assumptions: markdown reduction at 35% pass-through of the ₹380 Cr pool; "
                 "return cost = 25% of item value; ₹1.2 L replacement cost per exit; 5pp of the 15% growth "
                 "target attributed to AI at 42% gross margin. Full workings in Appendix A3.")

# ===========================================================================
# APPENDIX
# ===========================================================================
s = add_slide()
header(s, "APPENDIX  |  A1", "Task audit — detail by function", kicker_color=GREY)
table(s, 0.5, 1.5, 12.33, 3.1,
      ["Function", "HC", "Routine", "Autom.", "Augm.", "Human", "FTE released", "Representative automatable activity"],
      [
          ["Design & Creative", "1,500", "30%", "12%", "43%", "45%", "180", "Trend report collation, competitor scanning"],
          ["Merchandising & Planning", "1,200", "50%", "20%", "60%", "20%", "240", "Sales data pulls, spreadsheet consolidation"],
          ["Manufacturing & Quality", "11,000", "60%", "24%", "66%", "10%", "2,640", "Routine inspection logging, shift reporting"],
          ["Retail Operations", "10,000", "55%", "22%", "58%", "20%", "2,200", "Stock look-ups, transfers, admin reporting"],
          ["Marketing & CX", "2,500", "40%", "16%", "49%", "35%", "400", "Delivery/returns queries, segment builds"],
          ["Corporate", "1,800", "55%", "22%", "63%", "15%", "396", "Report preparation, data gathering"],
          ["Total / weighted", "28,000", "54.1%", "21.6%", "59.9%", "18.4%", "6,056", "—"],
      ],
      col_widths=[2.3, 0.75, 0.85, 0.85, 0.8, 0.8, 1.15, 4.83], font_size=10, header_size=10)
rich(s, 0.5, 4.82, 12.33, 1.0, [
    [{"text": "Automatable = 40% × routine (case constraint). Augmentable = 60% × routine + all "
              "judgment work. Fundamentally Human = all creative/strategic work.", "size": 10.5}],
    [{"text": "Note the weighted total row: the routine load of 54.1% differs from Exhibit 4's "
              "stated 48% because Exhibit 4 reports an unweighted mean across the six functions.",
      "size": 10.5}],
], line_spacing=1.2, space_after=7)
footer(s, "A1", "Derived from case Exhibits 3 and 4 via analysis/task_audit_model.py.")

s = add_slide()
header(s, "APPENDIX  |  A2", "Prioritisation scoring — full workings", kicker_color=GREY)
table(s, 0.5, 1.5, 12.33, 2.6,
      ["Function", "Business impact (25%)", "Customer value (20%)", "Workforce scale (15%)",
       "Automation potential (20%)", "Feasibility (20%)", "Score", "Rank"],
      [
          ["Marketing & CX", "4", "5", "3", "3", "5", "4.05", "1"],
          ["Retail Operations", "4", "5", "5", "4", "2", "3.95", "2"],
          ["Merchandising & Planning", "5", "3", "2", "4", "3", "3.55", "3"],
          ["Manufacturing & Quality", "3", "2", "5", "5", "1", "3.10", "4"],
          ["Design & Creative", "3", "3", "2", "2", "5", "3.05", "5"],
          ["Corporate", "2", "1", "2", "4", "5", "2.80", "6"],
      ],
      col_widths=[2.4, 1.6, 1.5, 1.5, 1.7, 1.4, 0.9, 0.7], font_size=10, header_size=10)
rich(s, 0.5, 4.32, 12.33, 1.5, [
    [{"text": "Scoring basis (1–5). ", "size": 10.5, "bold": True},
     {"text": "Business impact — size of the addressable P&L pool. Customer value — effect on NPS, "
              "returns and resolution time. Workforce scale — headcount affected. Automation potential "
              "— automatable share × headcount. Feasibility — adoption readiness index from Exhibit 5.",
      "size": 10.5}],
    [{"text": "Readiness index = mean(awareness, willingness, digital skill) − 0.5 × (fear − 2.0). "
              "Fear is weighted at 0.5 so it moderates rather than dominates: Design 3.83, Marketing 3.68, "
              "Corporate 3.63, Merchandising 2.73, Retail 1.35, Manufacturing 0.98.", "size": 10.5}],
], line_spacing=1.2, space_after=8)
footer(s, "A2", "Weights sum to 100%. Sensitivity: Retail overtakes Marketing for rank 1 if feasibility "
                 "is weighted below 12%; the Phase-1 set of three is unchanged across all tested weightings.")

s = add_slide()
header(s, "APPENDIX  |  A3", "Value bridge — assumptions and calculations", kicker_color=GREY)
table(s, 0.5, 1.5, 12.33, 2.35,
      ["Lever", "Calculation", "Value (₹ Cr)"],
      [
          ["Markdown reduction",
           "₹380 Cr pool × 35% pass-through. Forecast accuracy 62% → 78% implies error 38% → 22%, "
           "a 42% relative reduction; 35% applied conservatively.", "133"],
          ["Return-rate reduction",
           "SpeedStyle 28% → 22%, UrbanEdge 15% → 13%, ThreadBasics 18% → 16% on brand revenue; "
           "cost of a return assumed at 25% of item value.", "40"],
          ["Attrition cost avoided",
           "Organisation attrition 31% → 25% on 28,000 employees × ₹1.2 L blended replacement cost.", "20"],
          ["AI-attributed revenue",
           "5pp of the 15% growth target attributed to AI-enabled speed and personalisation, "
           "valued at the 42% gross margin.", "118"],
          ["Total annual run-rate", "Against a ₹200 Cr one-time FY25 investment", "311"],
      ],
      col_widths=[2.5, 8.3, 1.53], font_size=10, header_size=10)
rich(s, 0.5, 4.07, 12.33, 1.7, [
    [{"text": "Resulting EBITDA. ", "size": 10.5, "bold": True},
     {"text": "FY24 EBITDA = ₹5,600 Cr × 9.5% = ₹532 Cr. Adding ₹311 Cr gives ₹843 Cr. On FY26 revenue "
              "of ₹6,440 Cr (15% growth) that is a 13.1% margin.", "size": 10.5}],
    [{"text": "Stated limitations. ", "size": 10.5, "bold": True},
     {"text": "These are directional planning estimates built only from the case exhibits, not audited "
              "figures. Under Zero-Layoff, no labour-cost saving is claimed anywhere in this bridge — the "
              "6,056 FTE-equivalents released are redeployed, and their value appears only through the "
              "business outcomes above.", "size": 10.5}],
], line_spacing=1.2, space_after=8)
footer(s, "A3", "All calculations reproducible via analysis/task_audit_model.py in the submission repository.")

s = add_slide()
header(s, "APPENDIX  |  A4", "Risk register and references", kicker_color=GREY)
table(s, 0.5, 1.5, 12.33, 2.4,
      ["Risk", "Likelihood", "Mitigation"],
      [
          ["Retail adoption stalls despite the pilot", "High",
           "Gate scaling on adoption ≥70% and stable sentiment; associates co-design; champions seeded first"],
          ["Data foundation slips, delaying every use case", "Medium",
           "Platform is Phase 0 and separately funded at ₹60 Cr; use cases contracted against data readiness milestones"],
          ["Brand dilution from generative content", "Medium",
           "Brand-differentiated posture; Maison Luxe excluded from generative customer-facing AI entirely"],
          ["Zero-Layoff commitment perceived as hollow", "High",
           "Written charter in month 1, redeployment guarantee, public reporting of redeployment counts"],
          ["Regulatory exposure (EU AI Act, DPDP, EPR)", "Medium",
           "Four-tier decision rights, model register, provenance logging, quarterly bias testing"],
      ],
      col_widths=[3.4, 1.4, 7.53], font_size=10, header_size=10)
textbox(s, 0.5, 4.12, 12.33, 0.26, "REFERENCES (APA)", size=10.5, color=ORANGE, bold=True)
refs = [
    "European Commission. (2022). EU strategy for sustainable and circular textiles. Publications Office of the European Union.",
    "European Parliament & Council of the European Union. (2024). Regulation (EU) 2024/1689 laying down harmonised rules on artificial intelligence (Artificial Intelligence Act).",
    "International Organization for Standardization. (2023). ISO/IEC 42001:2023 — Information technology, artificial intelligence, management system.",
    "Ministry of Electronics and Information Technology. (2023). Digital Personal Data Protection Act, 2023. Government of India.",
    "National Institute of Standards and Technology. (2023). Artificial intelligence risk management framework (AI RMF 1.0). U.S. Department of Commerce.",
]
yy = 4.44
for r in refs:
    textbox(s, 0.5, yy, 12.33, 0.4, "•  " + r, size=10, color=CHARCOAL, line_spacing=1.15)
    yy += 0.42
footer(s, "A4", "Industry statistics quoted in the deck (USD 1.7 tn market, 92 mn tonnes textile waste, "
                 "75 mn people employed) are taken from the case brief's industry overview.")

prs.save(OUT)
print("Saved:", OUT)
print(f"Slides: {len(prs.slides._sldIdLst)}  (1 cover + 2 exec summary + 10 body + 4 appendix)")
