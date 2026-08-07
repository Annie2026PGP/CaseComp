"""
STYLEVERSE AI TRANSFORMATION — reproducible analysis model.

Every number quoted in the deck is produced here from the case exhibits, so a
reviewer can re-run it and see exactly how each figure was derived.

    python3 cases/2026-08-pwc-challenge-8-styleverse/analysis/task_audit_model.py

Outputs: task_audit.csv, prioritization.csv, value_bridge.csv (same folder).
"""
import pandas as pd

OUT = "cases/2026-08-pwc-challenge-8-styleverse/analysis"
pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 40)

# ---------------------------------------------------------------------------
# SOURCE DATA — verbatim from case Exhibits 3, 4, 5
# ---------------------------------------------------------------------------
FUNCTIONS = ["Design & Creative", "Merchandising & Planning", "Manufacturing & Quality",
             "Retail Operations", "Marketing & CX", "Corporate"]

ex3 = pd.DataFrame({  # Exhibit 3 — workforce profile
    "headcount":  [1500, 1200, 11000, 10000, 2500, 1800],
    "attrition":  [0.18, 0.22, 0.36, 0.42, 0.24, 0.14],
    "tenure_yrs": [4.6, 3.9, 2.3, 1.7, 3.3, 5.1],
    "case_priority": ["Medium", "High", "Medium", "Very High", "Very High", "Medium"],
}, index=FUNCTIONS)

ex4 = pd.DataFrame({  # Exhibit 4 — task distribution (% of time)
    "routine":  [0.30, 0.50, 0.60, 0.55, 0.40, 0.55],
    "judgment": [0.25, 0.30, 0.30, 0.25, 0.25, 0.30],
    "creative": [0.45, 0.20, 0.10, 0.20, 0.35, 0.15],
}, index=FUNCTIONS)

ex5 = pd.DataFrame({  # Exhibit 5 — AI adoption readiness (1-5)
    "awareness":    [3.8, 3.2, 2.1, 2.3, 3.9, 3.5],
    "willingness":  [4.1, 3.5, 2.8, 3.0, 4.2, 3.8],
    "fear":         [2.2, 3.0, 4.5, 4.3, 2.5, 2.0],
    "digital_skill":[3.9, 3.0, 1.8, 2.2, 3.7, 3.6],
}, index=FUNCTIONS)

df = ex3.join(ex4).join(ex5)
TOTAL_HC = df["headcount"].sum()
assert TOTAL_HC == 28000, TOTAL_HC

# ---------------------------------------------------------------------------
# INSIGHT 1 — the exhibit's "Organization Average" is an UNWEIGHTED mean.
# Weighted by headcount the routine load is materially higher, because the two
# largest functions (Manufacturing 11k @60%, Retail 10k @55%) are the most
# routine-heavy. This changes the size of the prize.
# ---------------------------------------------------------------------------
unweighted_routine = ex4["routine"].mean()                       # 0.483 -> case says 48%
weighted_routine = (df["routine"] * df["headcount"]).sum() / TOTAL_HC

# ---------------------------------------------------------------------------
# DELIVERABLE 1 — task audit.
# Classification rule (the "3-gate test", applied consistently):
#   Gate 1 Rule stability   : codifiable rules, high volume, low variance?
#   Gate 2 Consequence      : does error cause irreversible customer / regulatory
#                             / brand harm?
#   Gate 3 Human premium    : does the customer or business specifically value
#                             that a HUMAN did it (creativity, empathy,
#                             craftsmanship, accountability)?
# Automatable        = Gate1 yes, Gate2 low,  Gate3 no   -> capped at 40% of routine
# Augmentable        = residual routine (AI drafts, human checks) + all judgment work
# Fundamentally Human= all creative/strategic work (Gate3 yes)
# ---------------------------------------------------------------------------
AUTOMATION_CAP = 0.40   # case constraint: "AI automates up to 40% of routine work"

df["automatable"] = df["routine"] * AUTOMATION_CAP
df["augmentable"] = df["routine"] * (1 - AUTOMATION_CAP) + df["judgment"]
df["human"] = df["creative"]
assert ((df[["automatable", "augmentable", "human"]].sum(axis=1) - 1).abs() < 1e-9).all()

# FTE-equivalent capacity released (NOT headcount removed - Zero-Layoff)
df["routine_fte"] = df["routine"] * df["headcount"]
df["fte_released"] = df["automatable"] * df["headcount"]

org_auto = (df["automatable"] * df["headcount"]).sum() / TOTAL_HC
org_augm = (df["augmentable"] * df["headcount"]).sum() / TOTAL_HC
org_human = (df["human"] * df["headcount"]).sum() / TOTAL_HC

# ---------------------------------------------------------------------------
# INSIGHT 2 — adoption readiness index.
# Readiness = mean(awareness, willingness, digital skill), penalised by fear
# above a 2.0 neutral baseline. Fear is weighted at 0.5 so it moderates rather
# than dominates the score.
# ---------------------------------------------------------------------------
df["readiness_raw"] = df[["awareness", "willingness", "digital_skill"]].mean(axis=1)
df["readiness"] = df["readiness_raw"] - 0.5 * (df["fear"] - 2.0)

# ---------------------------------------------------------------------------
# DELIVERABLE 2 — phase-1 prioritization model.
# Criteria are exactly those the case names: business impact, customer value,
# workforce size, automation potential, implementation feasibility.
# Scores 1-5, scored against the evidence noted in `score_notes`.
# ---------------------------------------------------------------------------
WEIGHTS = {"business_impact": 0.25, "customer_value": 0.20, "workforce_scale": 0.15,
           "automation_potential": 0.20, "feasibility": 0.20}

scores = pd.DataFrame({
    #                          Design Merch  Mfg  Retail Mktg  Corp
    "business_impact":        [3,     5,     3,   4,     4,    2],
    "customer_value":         [3,     3,     2,   5,     5,    1],
    "workforce_scale":        [2,     2,     5,   5,     3,    2],
    "automation_potential":   [2,     4,     5,   4,     3,    4],
    "feasibility":            [5,     3,     1,   2,     5,    5],
}, index=FUNCTIONS)

score_notes = {
    "Design & Creative": "14-wk cycle vs 4-wk competitors; small HC; highest readiness (3.83)",
    "Merchandising & Planning": "owns the Rs380 Cr markdown pool + 62% forecast accuracy",
    "Manufacturing & Quality": "largest HC & routine load, but readiness 0.98 and safety/regulatory exposure",
    "Retail Operations": "200 stores, primary touchpoint, 42% attrition - but readiness only 1.35",
    "Marketing & CX": "88k queries/mo, NPS 35 on largest brand, rising CAC; readiness 3.68",
    "Corporate": "high readiness but low direct customer value",
}

df["priority_score"] = sum(scores[k] * w for k, w in WEIGHTS.items())
df["rank"] = df["priority_score"].rank(ascending=False).astype(int)
df["score_note"] = [score_notes[f] for f in df.index]

# ---------------------------------------------------------------------------
# DELIVERABLE 2 (value) — P&L bridge. Assumptions stated inline and in the deck
# footer; all are directional planning estimates, not audited figures.
# ---------------------------------------------------------------------------
REVENUE = 5600.0          # Rs Cr, FY24
GROSS_MARGIN = 0.42
EBITDA_MARGIN = 0.095
MARKDOWN_LOSS = 380.0     # Rs Cr
BRAND_MIX = {"SpeedStyle": 0.35, "UrbanEdge": 0.30, "Maison Luxe": 0.15,
             "EcoWeave": 0.12, "ThreadBasics": 0.08}
RETURN_RATE = {"SpeedStyle": 0.28, "UrbanEdge": 0.15, "Maison Luxe": 0.08,
               "EcoWeave": 0.12, "ThreadBasics": 0.18}
RETURN_TARGET = {"SpeedStyle": 0.22, "UrbanEdge": 0.13, "ThreadBasics": 0.16}
COST_PER_RETURN = 0.25    # assumption: reverse logistics + refurb + markdown = 25% of item value

# 1. Markdown reduction. Forecast accuracy 62% -> 78% target => error 38% -> 22%,
#    a 42% relative reduction. Applied at a conservative 35% pass-through.
markdown_gain = MARKDOWN_LOSS * 0.35

# 2. Return-rate reduction from AI fit guidance (first-time fit 58% -> 75%).
returns_gain = sum(
    REVENUE * BRAND_MIX[b] * (RETURN_RATE[b] - RETURN_TARGET[b]) * COST_PER_RETURN
    for b in RETURN_TARGET
)

# 3. Attrition. Org 31% -> 25%; blended replacement cost Rs1.2 L per exit.
BLENDED_ATTRITION_NOW, BLENDED_ATTRITION_TGT = 0.31, 0.25
REPLACEMENT_COST_LAKH = 1.2
attrition_gain = (TOTAL_HC * (BLENDED_ATTRITION_NOW - BLENDED_ATTRITION_TGT)
                  * REPLACEMENT_COST_LAKH / 100)   # Rs L -> Rs Cr

# 4. Revenue uplift. Of the 15% growth target, 5pp attributed to AI-enabled
#    speed-to-market and personalization; valued at gross margin.
AI_ATTRIBUTED_GROWTH = 0.05
revenue_gain = REVENUE * AI_ATTRIBUTED_GROWTH * GROSS_MARGIN

value_bridge = pd.DataFrame({
    "lever": ["Markdown reduction", "Return-rate reduction", "Attrition cost avoided",
              "AI-attributed revenue uplift"],
    "rs_cr": [markdown_gain, returns_gain, attrition_gain, revenue_gain],
    "basis": [
        "Rs380 Cr pool; forecast accuracy 62%->78%; 35% conservative pass-through",
        "First-time fit 58%->75%; return cost = 25% of item value",
        "Org attrition 31%->25%; Rs1.2 L replacement cost per exit",
        "5pp of the 15% growth target attributed to AI; valued at 42% GM",
    ],
})
total_value = value_bridge["rs_cr"].sum()
ebitda_now = REVENUE * EBITDA_MARGIN
revenue_next = REVENUE * 1.15
ebitda_next = ebitda_now + total_value
ebitda_margin_next = ebitda_next / revenue_next

# ---------------------------------------------------------------------------
# Rs200 Cr FY25 investment allocation
# ---------------------------------------------------------------------------
INVESTMENT = pd.DataFrame({
    "bucket": ["Data & AI platform foundation", "Phase-1 use-case build",
               "Workforce reskilling & AI Academy", "Governance, risk & responsible AI",
               "Change management & adoption"],
    "rs_cr": [60, 55, 45, 20, 20],
})
assert INVESTMENT["rs_cr"].sum() == 200

# ---------------------------------------------------------------------------
# REPORT
# ---------------------------------------------------------------------------
print("=" * 100)
print("INSIGHT 1 — routine work is bigger than the exhibit suggests")
print(f"  Exhibit 4 'Organization Average' (unweighted mean) : {unweighted_routine:.1%}")
print(f"  Headcount-weighted routine load                    : {weighted_routine:.1%}")
print(f"  -> understated by {weighted_routine - unweighted_routine:.1%} because the two largest")
print("     functions (Mfg 11k @60%, Retail 10k @55%) are the most routine-heavy.")

print("\n" + "=" * 100)
print("DELIVERABLE 1 — TASK AUDIT (share of each function's task time)")
print(df[["headcount", "routine", "judgment", "creative",
          "automatable", "augmentable", "human", "fte_released"]].round(3).to_string())
print(f"\n  Organization target state: {org_auto:.1%} Automatable | "
      f"{org_augm:.1%} Augmentable | {org_human:.1%} Fundamentally Human")
print(f"  Total routine FTE-equivalent : {df['routine_fte'].sum():,.0f}")
print(f"  Capacity released at 40% cap : {df['fte_released'].sum():,.0f} FTE-equivalents "
      f"({df['fte_released'].sum() / TOTAL_HC:.1%} of workforce)")
print("  NOTE: Zero-Layoff -> this is capacity CONVERTED, not headcount removed.")

print("\n" + "=" * 100)
print("INSIGHT 2 + DELIVERABLE 2 — READINESS vs PRIORITY")
print(df[["headcount", "readiness_raw", "fear", "readiness", "priority_score",
          "rank", "case_priority"]].round(2).to_string())
print("\n  Model rank vs the case's own 'Transformation Priority' column:")
for f in df.sort_values("priority_score", ascending=False).index:
    print(f"    {df.loc[f, 'rank']}. {f:<28} score {df.loc[f, 'priority_score']:.2f} "
          f"| case says: {df.loc[f, 'case_priority']:<10} | {df.loc[f, 'score_note']}")

print("\n  PARADOX: Retail Operations ranks #2 on value but LAST-but-one on readiness")
print("  (1.35/5, fear 4.3) -> phase 1 for Retail must be a readiness-building pilot,")
print("  not a full 200-store rollout.")

print("\n" + "=" * 100)
print("VALUE BRIDGE (annual run-rate, Rs Cr)")
print(value_bridge.to_string(index=False))
print(f"\n  Total annual impact      : Rs{total_value:,.0f} Cr")
print(f"  One-time FY25 investment : Rs200 Cr  -> payback < 12 months at run-rate")
print(f"  EBITDA {ebitda_now:,.0f} Cr ({EBITDA_MARGIN:.1%}) -> {ebitda_next:,.0f} Cr "
      f"({ebitda_margin_next:.1%}) on Rs{revenue_next:,.0f} Cr revenue")

print("\n" + "=" * 100)
print("Rs200 Cr FY25 ALLOCATION")
for _, r in INVESTMENT.iterrows():
    print(f"  {r['bucket']:<38} Rs{r['rs_cr']:>3} Cr  ({r['rs_cr']/200:.0%})")

df.to_csv(f"{OUT}/task_audit.csv")
df[["priority_score", "rank", "readiness", "case_priority", "score_note"]].to_csv(f"{OUT}/prioritization.csv")
value_bridge.to_csv(f"{OUT}/value_bridge.csv", index=False)
print(f"\nWrote task_audit.csv, prioritization.csv, value_bridge.csv to {OUT}")
