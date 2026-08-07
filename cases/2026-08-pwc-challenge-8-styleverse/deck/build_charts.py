import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle
import numpy as np

plt.rcParams["font.family"] = "DejaVu Sans"

# ---- PwC palette (light) ----
BG        = "#FFFFFF"
PAPER     = "#FAF8F7"
ORANGE    = "#D04A02"   # PwC orange  - Automatable
GOLD      = "#FFB600"   # PwC yellow  - Augmentable
CHARCOAL  = "#2D2D2D"   # ink         - Fundamentally Human
TANGERINE = "#EB8C00"
ROSE      = "#E0301E"
GREY      = "#7D7D7D"
LIGHTGREY = "#DEDAD6"
RULE      = "#C9C3BE"

OUT = "/home/user/CaseComp/cases/2026-08-pwc-challenge-8-styleverse/deck/assets"

FUNCS = ["Design &\nCreative", "Merchandising\n& Planning", "Manufacturing\n& Quality",
         "Retail\nOperations", "Marketing\n& CX", "Corporate"]
HC        = [1500, 1200, 11000, 10000, 2500, 1800]
AUTO      = [12, 20, 24, 22, 16, 22]
AUGM      = [43, 60, 66, 58, 49, 63]
HUMAN     = [45, 20, 10, 20, 35, 15]
READINESS = [3.83, 2.73, 0.98, 1.35, 3.68, 3.63]
PRIORITY  = [3.05, 3.55, 3.10, 3.95, 4.05, 2.80]

def style_axes(ax, grid_axis=None):
    ax.set_facecolor(BG)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(RULE)
        ax.spines[side].set_linewidth(0.9)
    ax.tick_params(colors=GREY, labelsize=8.5, length=3, width=0.8)
    if grid_axis:
        ax.grid(axis=grid_axis, color=LIGHTGREY, linewidth=0.7, zorder=0)
        ax.set_axisbelow(True)

# ===========================================================================
# 1. TASK AUDIT — stacked horizontal bars
# ===========================================================================
fig, ax = plt.subplots(figsize=(10.6, 4.0), dpi=300)
fig.patch.set_facecolor(BG)
style_axes(ax)

y = np.arange(len(FUNCS))[::-1]
h = 0.58
ax.barh(y, AUTO, height=h, color=ORANGE, zorder=3, label="Automatable")
ax.barh(y, AUGM, left=AUTO, height=h, color=GOLD, zorder=3, label="Augmentable")
ax.barh(y, HUMAN, left=np.array(AUTO) + np.array(AUGM), height=h, color=CHARCOAL,
        zorder=3, label="Fundamentally Human")

for yi, a, g, hm in zip(y, AUTO, AUGM, HUMAN):
    ax.text(a / 2, yi, f"{a}%", ha="center", va="center", fontsize=8.6,
            color="white", fontweight="bold", zorder=4)
    ax.text(a + g / 2, yi, f"{g}%", ha="center", va="center", fontsize=8.6,
            color=CHARCOAL, fontweight="bold", zorder=4)
    ax.text(a + g + hm / 2, yi, f"{hm}%", ha="center", va="center", fontsize=8.6,
            color="white", fontweight="bold", zorder=4)

ax.set_yticks(y)
ax.set_yticklabels(FUNCS, fontsize=9, color=CHARCOAL, linespacing=1.25)
ax.set_xlim(0, 100)
ax.set_xticks([0, 25, 50, 75, 100])
ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"])
ax.set_xlabel("Share of function's task time", fontsize=9, color=GREY, labelpad=7)
leg = ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.16), ncol=3, frameon=False,
                fontsize=9.2, handlelength=1.2, handleheight=1.0, columnspacing=2.2)
for t in leg.get_texts():
    t.set_color(CHARCOAL)
plt.tight_layout()
plt.savefig(f"{OUT}/task_audit.png", facecolor=BG, bbox_inches="tight", pad_inches=0.12)
plt.close()
print("saved task_audit.png")

# ===========================================================================
# 2. READINESS vs PRIORITY — the paradox matrix
# ===========================================================================
fig, ax = plt.subplots(figsize=(8.4, 5.6), dpi=300)
fig.patch.set_facecolor(BG)
style_axes(ax)

ax.axvline(3.4, color=RULE, lw=1.0, ls=(0, (4, 3)), zorder=1)
ax.axhline(2.6, color=RULE, lw=1.0, ls=(0, (4, 3)), zorder=1)

# quadrant wash for the "act now" zone
ax.add_patch(Rectangle((3.4, 2.6), 1.2, 2.4, facecolor=ORANGE, alpha=0.05, zorder=0))

labels = ["Design & Creative", "Merchandising\n& Planning", "Manufacturing\n& Quality",
          "Retail Operations", "Marketing & CX", "Corporate"]
colors = [GREY, ORANGE, GREY, ORANGE, ORANGE, GREY]

# label sits above each bubble, offset by that bubble's own radius so text
# never lands on the marker regardless of headcount
for x, yv, hc, lab, c in zip(PRIORITY, READINESS, HC, labels, colors):
    s = hc / 8.0
    ax.scatter(x, yv, s=s, color=c, alpha=0.85, edgecolors="white",
               linewidths=1.6, zorder=3)
    r_pt = np.sqrt(s / np.pi)
    ax.annotate(lab, (x, yv), xytext=(0, r_pt + 9), textcoords="offset points",
                ha="center", va="bottom", fontsize=9,
                color=CHARCOAL, fontweight="bold", linespacing=1.2, zorder=4)

ax.set_xlim(2.5, 4.45)
ax.set_ylim(0.0, 5.2)
ax.set_xlabel("Phase-1 priority score  (business impact, customer value, scale, automation potential)  →",
              fontsize=8.6, color=GREY, labelpad=8)
ax.set_ylabel("Adoption readiness  (awareness, willingness, skill − fear)  →",
              fontsize=8.6, color=GREY, labelpad=8)

ax.text(4.40, 5.12, "READY & VALUABLE", ha="right", va="top", fontsize=8.4,
        color=ORANGE, fontweight="bold", style="italic")
ax.text(4.40, 0.10, "VALUABLE BUT NOT READY", ha="right", va="bottom", fontsize=8.4,
        color=ROSE, fontweight="bold", style="italic")
ax.text(2.54, 0.10, "LOW PRIORITY, LOW READINESS", ha="left", va="bottom", fontsize=8.4,
        color=GREY, fontweight="bold", style="italic")
ax.text(2.54, 5.12, "READY, LOWER VALUE", ha="left", va="top", fontsize=8.4,
        color=GREY, fontweight="bold", style="italic")
ax.text(0.99, -0.135, "Bubble size = headcount", ha="right", va="top",
        fontsize=8, color=GREY, style="italic", transform=ax.transAxes)

plt.tight_layout()
plt.savefig(f"{OUT}/readiness_matrix.png", facecolor=BG, bbox_inches="tight", pad_inches=0.15)
plt.close()
print("saved readiness_matrix.png")

# ===========================================================================
# 3. VALUE BRIDGE — EBITDA waterfall
# ===========================================================================
fig, ax = plt.subplots(figsize=(10.2, 4.2), dpi=300)
fig.patch.set_facecolor(BG)
style_axes(ax, grid_axis="y")

cats = ["FY24\nEBITDA", "Markdown\nreduction", "Return-rate\nreduction",
        "Attrition\navoided", "AI-attributed\nrevenue", "FY26\nEBITDA"]
vals = [532, 133, 40, 20, 118, 843]
bar_colors = [CHARCOAL, ORANGE, ORANGE, ORANGE, ORANGE, CHARCOAL]

running = 532
bottoms, heights = [0], [532]
for v in vals[1:-1]:
    bottoms.append(running)
    heights.append(v)
    running += v
bottoms.append(0)
heights.append(843)

x = np.arange(len(cats))
ax.bar(x, heights, bottom=bottoms, color=bar_colors, width=0.6, zorder=3)

for xi, (b, hgt, v, c) in enumerate(zip(bottoms, heights, vals, bar_colors)):
    label = f"{v:,.0f}" if c == CHARCOAL else f"+{v:,.0f}"
    ax.text(xi, b + hgt + 22, label, ha="center", va="bottom", fontsize=9.4,
            color=CHARCOAL, fontweight="bold", zorder=4)

# connectors
for i in range(len(cats) - 1):
    y_conn = bottoms[i] + heights[i]
    ax.plot([x[i] + 0.30, x[i + 1] - 0.30], [y_conn, y_conn],
            color=RULE, lw=0.9, ls=(0, (3, 2)), zorder=2)

ax.set_xticks(x)
ax.set_xticklabels(cats, fontsize=8.8, color=CHARCOAL, linespacing=1.3)
ax.set_ylabel("EBITDA (₹ Cr)", fontsize=9, color=GREY, labelpad=8)
ax.set_ylim(0, 1010)
ax.text(0, 505 - 120, "9.5%\nmargin", ha="center", va="top", fontsize=8.4,
        color="white", fontweight="bold", linespacing=1.25, zorder=5)
ax.text(5, 843 - 120, "13.1%\nmargin", ha="center", va="top", fontsize=8.4,
        color="white", fontweight="bold", linespacing=1.25, zorder=5)
plt.tight_layout()
plt.savefig(f"{OUT}/value_bridge.png", facecolor=BG, bbox_inches="tight", pad_inches=0.12)
plt.close()
print("saved value_bridge.png")

# ===========================================================================
# 4. ROADMAP — phased gantt
# ===========================================================================
fig, ax = plt.subplots(figsize=(10.6, 3.5), dpi=300)
fig.patch.set_facecolor(BG)
style_axes(ax)

rows = [
    ("Foundation — data layer, CoE, Zero-Layoff Charter", 0, 3, CHARCOAL),
    ("Marketing & CX — service AI, personalization", 3, 9, ORANGE),
    ("Merchandising — demand & allocation AI", 3, 9, ORANGE),
    ("Retail Ops — 20-store pilot → 200-store scale", 4, 20, TANGERINE),
    ("Design & Creative — trend & concept AI", 12, 12, GOLD),
    ("Corporate — process automation", 12, 12, GOLD),
    ("Manufacturing & Quality — vision QC, EPR traceability", 24, 12, GREY),
]
y = np.arange(len(rows))[::-1]
for yi, (label, start, dur, c) in zip(y, rows):
    ax.barh(yi, dur, left=start, height=0.55, color=c, zorder=3)
    ax.text(start + dur + 0.7, yi, label, va="center", ha="left", fontsize=8.6,
            color=CHARCOAL)

ax.set_xlim(0, 78)
ax.set_ylim(-0.7, len(rows) - 0.3)
ax.set_yticks([])
ax.set_xticks([0, 3, 12, 24, 36])
ax.set_xticklabels(["M0", "M3", "M12", "M24", "M36"], fontsize=8.6)
for xv in (3, 12, 24):
    ax.axvline(xv, color=LIGHTGREY, lw=0.9, ls=":", zorder=1)
ax.spines["left"].set_visible(False)

phase_labels = [(1.5, "PHASE 0"), (7.5, "PHASE 1"), (18, "PHASE 2"), (30, "PHASE 3")]
for xv, lab in phase_labels:
    ax.text(xv, len(rows) - 0.35, lab, ha="center", va="bottom", fontsize=8.2,
            color=GREY, fontweight="bold")

plt.tight_layout()
plt.savefig(f"{OUT}/roadmap.png", facecolor=BG, bbox_inches="tight", pad_inches=0.12)
plt.close()
print("saved roadmap.png")

# ===========================================================================
# 5. INVESTMENT ALLOCATION — single stacked bar
# ===========================================================================
fig, ax = plt.subplots(figsize=(10.6, 1.95), dpi=300)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.axis("off")

buckets = [
    ("Data & AI platform\nfoundation", 60, ORANGE),
    ("Phase-1 use-case\nbuild", 55, TANGERINE),
    ("Workforce reskilling\n& AI Academy", 45, GOLD),
    ("Governance & risk", 20, GREY),
    ("Change mgmt\n& adoption", 20, CHARCOAL),
]
# the two 10% buckets are too narrow to caption side-by-side, so the last one
# drops to a second line with a leader tick
left = 0.0
for i, (label, val, c) in enumerate(buckets):
    ax.barh(0, val, left=left, height=0.42, color=c, zorder=3)
    mid = left + val / 2
    txt_color = "white" if c in (ORANGE, CHARCOAL, GREY, TANGERINE) else CHARCOAL
    ax.text(mid, 0, f"₹{val} Cr", ha="center", va="center", fontsize=9.6,
            color=txt_color, fontweight="bold", zorder=4)
    label_y = -0.78 if i == len(buckets) - 1 else -0.34
    if i == len(buckets) - 1:
        ax.plot([mid, mid], [-0.24, -0.70], color=RULE, lw=0.8, zorder=2)
    ax.text(mid, label_y, label, ha="center", va="top", fontsize=8.2,
            color=CHARCOAL, linespacing=1.25)
    ax.text(mid, 0.30, f"{val/200:.0%}", ha="center", va="bottom", fontsize=8,
            color=GREY)
    left += val

ax.set_xlim(0, 200)
ax.set_ylim(-1.5, 0.62)
plt.tight_layout()
plt.savefig(f"{OUT}/investment.png", facecolor=BG, bbox_inches="tight", pad_inches=0.1)
plt.close()
print("saved investment.png")

# ===========================================================================
# 6. CAPACITY REDEPLOYMENT — where the 6,056 FTE go
# ===========================================================================
fig, ax = plt.subplots(figsize=(9.2, 3.3), dpi=300)
fig.patch.set_facecolor(BG)
style_axes(ax, grid_axis="x")

fn = ["Manufacturing\n& Quality", "Retail\nOperations", "Marketing\n& CX",
      "Corporate", "Merchandising\n& Planning", "Design &\nCreative"]
released = [2640, 2200, 400, 396, 240, 180]
cols = [GREY, ORANGE, ORANGE, GREY, ORANGE, GREY]

y = np.arange(len(fn))[::-1]
ax.barh(y, released, height=0.6, color=cols, zorder=3)
for yi, v in zip(y, released):
    ax.text(v + 55, yi, f"{v:,}", va="center", ha="left", fontsize=9,
            color=CHARCOAL, fontweight="bold")

ax.set_yticks(y)
ax.set_yticklabels(fn, fontsize=8.8, color=CHARCOAL, linespacing=1.25)
ax.set_xlim(0, 3100)
ax.set_xlabel("FTE-equivalent capacity released and redeployed (not removed)",
              fontsize=8.8, color=GREY, labelpad=7)
plt.tight_layout()
plt.savefig(f"{OUT}/capacity.png", facecolor=BG, bbox_inches="tight", pad_inches=0.12)
plt.close()
print("saved capacity.png")
