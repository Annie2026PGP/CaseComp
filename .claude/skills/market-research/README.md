# Market Research Skill

Professional market research and competitive analysis using McKinsey/BCG/Bain methodologies. Generates hypothesis-driven research with PPTX presentation deliverables.

## Overview

This Claude skill implements proven consulting methodologies for market research, structured as a four-level pyramid analysis:

```
                   YOUR COMPANY (Level 1)
                 Strategic Fit & Positioning
                            ▲
             COMPETITIVE LANDSCAPE (Level 2)
           Positioning & Differentiation Analysis
                            ▲
          CUSTOMER INSIGHTS (Level 3)
       Needs, Motivations, Barriers, Behaviors
                            ▲
     MARKET & SEGMENT ANALYSIS (Level 4)
    Size, Growth, Trends, Development Opportunities
```

## Features

✅ **Hypothesis-driven methodology** - MECE principle, Issue Trees, 7-step consulting process
✅ **Four-level pyramid analysis** - Systematic bottom-up market research
✅ **CRAAP source validation** - Professional-grade source quality assessment
✅ **Multi-source triangulation** - Validate critical findings with 2-3 independent sources
✅ **Free sources optimization** - Designed for government, academic, and free industry data
✅ **PPTX generation** - Professional presentations via document-skills/pptx integration
✅ **Quick scan timing** - Optimized for 1-2 day research projects

## Quick Start

### 1. Installation

```bash
# Clone or copy this skill to your Claude skills directory
cp -r market-research ~/.claude/skills/

# OR for project-specific installation
cp -r market-research .claude/skills/
```

### 2. Initialize New Research Project

```bash
cd .claude/skills/market-research
bash scripts/init-research.sh "acme-corp" "healthcare"
```

This creates:
- Project structure with templates
- Pre-populated research brief
- Pyramid analysis framework
- Source bibliography tracker

### 3. Execute Three-Phase Workflow

**Phase 1: Research Philosophy (30 min)**
- Complete `research-brief.md`
- Define hypothesis tree using MECE
- Identify source strategy

**Phase 2: Pyramid Analysis (1-2 days)**
- Level 4: Market & segment data collection
- Level 3: Customer insights research
- Level 2: Competitive landscape analysis
- Level 1: Company positioning assessment
- Document in `pyramid-analysis.md`

**Phase 3: PPTX Generation (1-2 hours)**
- Update `slide-deck.html` with findings
- Run: `node scripts/generate-slides.js deliverables/slide-deck.html`
- Invoke `pptx` skill for final conversion

## Directory Structure

```
market-research/
├── SKILL.md                    # Main skill definition
├── LICENSE.txt                 # MIT License
├── README.md                   # This file
├── references/                 # Methodology documentation
│   ├── MBB_METHODOLOGY.md      # 7-step, MECE, Pyramid Principle
│   ├── FREE_SOURCES_GUIDE.md   # Tier 1-3 data sources
│   └── VALIDATION_FRAMEWORKS.md # CRAAP test, triangulation
├── templates/                  # Project templates
│   ├── research-brief.md       # Phase 1 hypothesis setup
│   ├── pyramid-analysis.md     # Phase 2 data collection
│   ├── source-bibliography.md  # Source tracking
│   └── slide-deck.html         # Phase 3 PPTX template
├── scripts/                    # Helper automation
│   ├── init-research.sh        # Project initialization
│   ├── generate-slides.js      # PPTX generation wrapper
│   └── validate-sources.py     # Automated CRAAP scoring
└── assets/                     # Visual resources
    ├── color-scheme.json       # Professional color palette
    └── pyramid-diagram.svg     # Pyramid visualization
```

## Methodology Details

### MBB 7-Step Process

1. **Define Problem** - SMART criteria, success metrics
2. **Structure Problem** - MECE decomposition, hypothesis trees
3. **Prioritize** - Impact vs. ease, 80/20 rule
4. **Work Plan** - Timeline, sources, responsibilities
5. **Execute Analysis** - Systematic testing, triangulation
6. **Synthesize Findings** - Pyramid Principle, "Day 1 drafts"
7. **Develop Recommendations** - Actionable with ownership

### Source Quality Hierarchy

**Tier 1 (Highest Credibility):**
- Government agencies (Census, BLS, Eurostat)
- Peer-reviewed academic journals
- Public company SEC filings
- Established market research firms

**Tier 2 (High Credibility):**
- Industry associations
- Premium databases (IBISWorld, Euromonitor)
- Think tanks and research centers
- Consulting firm public research

**Tier 3 (Requires Verification):**
- Company white papers
- Industry blogs and media
- Third-party databases
- Must be cross-validated with Tier 1-2

### CRAAP Test Framework

Every source evaluated on 5 dimensions (1-5 scale):

- **Currency** - Publication date and timeliness
- **Relevance** - Fit to research question
- **Authority** - Author credentials and reputation
- **Accuracy** - Methodology and verification
- **Purpose** - Intent and potential bias

**Quality thresholds:**
- 22-25: Excellent (use as primary)
- 18-21: Good (use confidently)
- 14-17: Acceptable (use with caution)
- <14: Questionable or reject

## Dependencies

### Required

- **Claude Code** - This skill runs within Claude environment
- **Bash** - For init-research.sh script (Unix/Linux/Mac)
- **Python 3.6+** - For validate-sources.py script
- **Node.js 14+** - For generate-slides.js script

### Optional (for PPTX generation)

- **document-skills/pptx** - From Anthropic skills repository

```bash
# Install as git submodule
cd .claude/skills
git submodule add https://github.com/anthropics/skills document-skills
```

**Note:** PPTX generation can also be done by invoking the `pptx` skill directly in Claude Code without local installation.

## Usage Examples

### Example 1: Quick Market Sizing

```markdown
User: "Research the US plant-based protein market size and growth"

Claude (with market-research skill):
Phase 1: Creating hypothesis tree for market sizing
- TAM estimation (top-down from food industry)
- SAM focus on plant-based segment
- Growth drivers identification

Phase 2: Data collection
- Level 4: Census food manufacturing data, USDA reports
- Level 4: Academic papers on plant-based trends
- Level 4: Industry association (GFI) reports

Phase 3: Synthesis
- Market size: $7.4B (2024)
- CAGR: 11.4% (2020-2024)
- Key trends: Health consciousness, sustainability
- Sources: USDA, Good Food Institute, Euromonitor

Deliverable: PPTX with market sizing analysis
```

### Example 2: Competitive Analysis

```markdown
User: "Analyze top 5 competitors in enterprise SaaS project management"

Claude (with market-research skill):
Phase 1: Hypothesis - Market dominated by established players
Phase 2: Analysis
- Level 4: $6.5B market, 12% CAGR
- Level 3: Customer need for integration (78% priority)
- Level 2: Top 5 identified (Monday, Asana, Jira, Clickup, Smartsheet)
- Level 2: Positioning map created
- Level 1: Gap analysis vs. client capabilities

Phase 3: PPTX with competitive landscape and positioning recommendations
```

### Example 3: Customer Insights

```markdown
User: "Research B2B SaaS buyer decision criteria"

Claude (with market-research skill):
Phase 1: Hypothesis tree on decision factors
Phase 2: Research
- Level 3: Academic papers on B2B buying behavior
- Level 3: Industry surveys (Gartner, Forrester previews)
- Level 3: Case studies and analyst reports

Findings:
1. ROI justification (87% cite as critical)
2. Integration capabilities (76%)
3. Support/training (68%)
4. Security/compliance (65%)

Deliverable: Customer insights deck with decision journey map
```

## Best Practices

### 1. Start with Hypothesis

❌ **Wrong:** "Let me collect all available data on healthcare market"
✅ **Right:** "Hypothesis: Telehealth market will grow 15%+ due to aging population and tech adoption"

### 2. Apply MECE Ruthlessly

❌ **Wrong:** Overlapping segments (SMB, Mid-market, Enterprise, B2B)
✅ **Right:** Mutually exclusive (B2B SMB, B2B Enterprise, B2C)

### 3. Triangulate Critical Findings

❌ **Wrong:** Single source for market size: "$4B market"
✅ **Right:** Three sources converge: $4.0B, $4.2B, $4.1B → High confidence: $4.1B

### 4. Document Everything

❌ **Wrong:** "Market growing fast" (no source)
✅ **Right:** "Market growing 12% CAGR (Source: IBISWorld 2024, CRAAP: 23/25)"

### 5. Continuous Synthesis

❌ **Wrong:** Collect all data first, then analyze at end
✅ **Right:** "Day 1 draft" immediately, refine continuously

## Common Pitfalls

### Pitfall 1: Accepting Sources at Face Value
**Solution:** CRAAP test every source, score ≥18 for primary evidence

### Pitfall 2: Cherry-picking Data
**Solution:** Document comprehensive search, explain exclusions

### Pitfall 3: Ignoring Original Context
**Solution:** Understand data collection purpose and methodology

### Pitfall 4: Outdated Information
**Solution:** Check publication dates, apply growth rates to update

### Pitfall 5: Unclear Methodology
**Solution:** Reject sources without transparent methodology

## Integration with document-skills/pptx

### HTML → PPTX Requirements

The slide-deck.html template follows html2pptx format:

✅ **Correct dimensions:** 720pt × 405pt (16:9)
✅ **Semantic HTML:** All text in `<p>`, `<h1>-<h6>`, `<ul>`, `<ol>`
✅ **Professional colors:** No purple gradients (#6366F1, #8B5CF6)
✅ **Proper structure:** No text directly in `<div>` or `<span>`

### PPTX Generation Workflow

1. Complete pyramid-analysis.md with findings
2. Update slide-deck.html with data from analysis
3. Run validation: `node scripts/generate-slides.js deliverables/slide-deck.html`
4. Invoke pptx skill with HTML file
5. Review generated PPTX for quality

## Quality Checklist

Before delivering research to client:

- [ ] Research brief demonstrates clear hypothesis-driven approach
- [ ] All four pyramid levels analyzed with CRAAP-validated sources
- [ ] Critical findings triangulated with 2-3 independent sources
- [ ] Every quantitative claim backed by cited source
- [ ] Source bibliography complete with validation scores
- [ ] Pyramid analysis document complete
- [ ] PPTX slides generated and reviewed
- [ ] Professional design standards met (no AI slop)
- [ ] Slide narrative flows logically from market to company
- [ ] Recommendations are specific, actionable, and prioritized
- [ ] Final deliverable matches McKinsey/BCG/Bain quality standards

## Troubleshooting

### Issue: Scripts don't run
**Solution:**
```bash
# Make scripts executable
chmod +x scripts/*.sh
chmod +x scripts/*.py

# Ensure dependencies installed
python3 --version  # Should be 3.6+
node --version     # Should be 14+
```

### Issue: PPTX generation fails
**Solution:**
- Verify HTML has correct dimensions (720pt × 405pt)
- Check all text is in semantic tags (`<p>`, `<h1>`, etc.)
- Ensure document-skills/pptx is available
- Remove # prefix from colors when using PptxGenJS

### Issue: Sources score low on CRAAP
**Solution:**
- Prioritize Tier 1 sources (government, academic)
- Verify publication dates within 3 years
- Check methodology transparency
- Cross-validate with additional sources

### Issue: Can't find data for market sizing
**Solution:**
- Try bottom-up estimation (components → total)
- Use proxy markets and apply ratios
- Leverage Census data and industry associations
- See FREE_SOURCES_GUIDE.md for discovery strategies

## Contributing

To improve this skill:

1. Fork and make changes
2. Test with real research projects
3. Submit pull request with:
   - Description of improvement
   - Example usage
   - Documentation updates

## Support

- **Documentation:** See `references/` for detailed methodology guides
- **Issues:** Report bugs or feature requests on GitHub
- **Questions:** Consult MBB_METHODOLOGY.md for process questions

## License

MIT License - See LICENSE.txt for details

This skill implements publicly documented methodologies from top consulting firms. No proprietary client work or confidential information is included.

## Acknowledgments

Based on methodologies from:
- McKinsey & Company (MECE, Pyramid Principle, 7-step process)
- Boston Consulting Group (Growth-Share Matrix, frameworks)
- Bain & Company (Results-oriented approaches)

Inspired by:
- "The McKinsey Way" by Ethan Rasiel
- "The Pyramid Principle" by Barbara Minto
- "Research Methods for Business Students" by Saunders, Lewis & Thornhill
- ESOMAR Guidelines on Secondary Data (2021)
- MRS Code of Conduct (2023)

Integration with:
- Anthropic document-skills/pptx for presentation generation

---

**Version:** 1.0
**Last Updated:** 2025
**Status:** Production Ready

For latest updates: Check repository for new versions and enhancements.
