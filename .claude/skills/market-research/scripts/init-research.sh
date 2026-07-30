#!/bin/bash

# Market Research Project Initialization Script
# Creates project structure and populates templates for new research project
#
# Usage: bash scripts/init-research.sh <client-name> <industry>
# Example: bash scripts/init-research.sh "acme-corp" "healthcare"

set -e  # Exit on error

# Check arguments
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <client-name> <industry>"
    echo "Example: $0 acme-corp healthcare"
    exit 1
fi

CLIENT_NAME="$1"
INDUSTRY="$2"
PROJECT_DIR="projects/${CLIENT_NAME}"
TIMESTAMP=$(date +"%Y-%m-%d")

echo "=================================================="
echo "Initializing Market Research Project"
echo "=================================================="
echo "Client: ${CLIENT_NAME}"
echo "Industry: ${INDUSTRY}"
echo "Date: ${TIMESTAMP}"
echo ""

# Create project directory structure
echo "[1/5] Creating project directory structure..."
mkdir -p "${PROJECT_DIR}"
mkdir -p "${PROJECT_DIR}/data"
mkdir -p "${PROJECT_DIR}/analysis"
mkdir -p "${PROJECT_DIR}/deliverables"

# Copy templates
echo "[2/5] Copying research templates..."
cp templates/research-brief.md "${PROJECT_DIR}/research-brief.md"
cp templates/pyramid-analysis.md "${PROJECT_DIR}/analysis/pyramid-analysis.md"
cp templates/source-bibliography.md "${PROJECT_DIR}/analysis/source-bibliography.md"
cp templates/slide-deck.html "${PROJECT_DIR}/deliverables/slide-deck.html"

# Populate templates with project info
echo "[3/5] Personalizing templates..."

# Update research-brief.md
sed -i.bak "s/\[Insert project name\]/${CLIENT_NAME} Market Research/g" "${PROJECT_DIR}/research-brief.md"
sed -i.bak "s/\[Client organization\]/${CLIENT_NAME}/g" "${PROJECT_DIR}/research-brief.md"
sed -i.bak "s/\[Target industry\/sector\]/${INDUSTRY}/g" "${PROJECT_DIR}/research-brief.md"
sed -i.bak "s/\[Creation date\]/${TIMESTAMP}/g" "${PROJECT_DIR}/research-brief.md"

# Update pyramid-analysis.md
sed -i.bak "s/\[Project name\]/${CLIENT_NAME} Market Research/g" "${PROJECT_DIR}/analysis/pyramid-analysis.md"
sed -i.bak "s/\[Client name\]/${CLIENT_NAME}/g" "${PROJECT_DIR}/analysis/pyramid-analysis.md"
sed -i.bak "s/\[Industry\/sector\]/${INDUSTRY}/g" "${PROJECT_DIR}/analysis/pyramid-analysis.md"
sed -i.bak "s/\[Date\]/${TIMESTAMP}/g" "${PROJECT_DIR}/analysis/pyramid-analysis.md"

# Update source-bibliography.md
sed -i.bak "s/\[Project name\]/${CLIENT_NAME} Market Research/g" "${PROJECT_DIR}/analysis/source-bibliography.md"
sed -i.bak "s/\[Date\]/${TIMESTAMP}/g" "${PROJECT_DIR}/analysis/source-bibliography.md"

# Update slide-deck.html
sed -i.bak "s/\[PROJECT NAME\]/${CLIENT_NAME} Market Research/g" "${PROJECT_DIR}/deliverables/slide-deck.html"
sed -i.bak "s/\[Client Name\]/${CLIENT_NAME}/g" "${PROJECT_DIR}/deliverables/slide-deck.html"
sed -i.bak "s/\[Industry\/Sector\]/${INDUSTRY}/g" "${PROJECT_DIR}/deliverables/slide-deck.html"
sed -i.bak "s/\[Presentation Date\]/${TIMESTAMP}/g" "${PROJECT_DIR}/deliverables/slide-deck.html"

# Remove backup files
rm -f "${PROJECT_DIR}"/*.bak
rm -f "${PROJECT_DIR}"/analysis/*.bak
rm -f "${PROJECT_DIR}"/deliverables/*.bak

# Create project README
echo "[4/5] Creating project README..."
cat > "${PROJECT_DIR}/README.md" << EOF
# ${CLIENT_NAME} Market Research Project

**Industry:** ${INDUSTRY}
**Created:** ${TIMESTAMP}

## Project Structure

\`\`\`
${CLIENT_NAME}/
├── research-brief.md           # Phase 1: Hypothesis-driven research plan
├── data/                        # Raw data and sources
├── analysis/
│   ├── pyramid-analysis.md     # Phase 2: Four-level pyramid analysis
│   └── source-bibliography.md  # Source tracking and CRAAP validation
└── deliverables/
    ├── slide-deck.html         # Phase 3: HTML for PPTX conversion
    └── ${CLIENT_NAME}-report.pptx  # Final presentation (generated)
\`\`\`

## Workflow

### Phase 1: Research Philosophy (30 min)
1. Complete \`research-brief.md\`
2. Define hypothesis tree using MECE principle
3. Identify source strategy

### Phase 2: Pyramídová Analýza (1-2 days)
1. Collect data for Level 4 (Market & Segment)
2. Collect data for Level 3 (Customer Insights)
3. Collect data for Level 2 (Competitive Landscape)
4. Analyze Level 1 (Your Company Position)
5. Document all sources in \`source-bibliography.md\`
6. Complete \`pyramid-analysis.md\`

### Phase 3: PPTX Generation (1-2 hours)
1. Update \`slide-deck.html\` with findings
2. Run \`node ../scripts/generate-slides.js deliverables/slide-deck.html\`
3. Review and refine \`${CLIENT_NAME}-report.pptx\`

## Quality Checklist

- [ ] Research brief completed with SMART objectives
- [ ] Hypothesis tree validated with MECE principle
- [ ] All four pyramid levels analyzed
- [ ] Critical findings triangulated (2-3 sources)
- [ ] All sources CRAAP tested (score ≥18 for primary evidence)
- [ ] Source bibliography complete
- [ ] Pyramid analysis document complete
- [ ] PPTX slides generated and reviewed
- [ ] Professional design standards met (no AI slop)

## References

- **Methodologies:** ../references/MBB_METHODOLOGY.md
- **Free Sources:** ../references/FREE_SOURCES_GUIDE.md
- **Validation:** ../references/VALIDATION_FRAMEWORKS.md
EOF

# Project initialization complete
echo "[5/5] Project initialization complete!"
echo ""
echo "=================================================="
echo "Next Steps:"
echo "=================================================="
echo "1. cd ${PROJECT_DIR}"
echo "2. Open research-brief.md and complete Phase 1"
echo "3. Begin data collection for pyramid analysis"
echo "4. Document sources in analysis/source-bibliography.md"
echo ""
echo "Reference materials available in ../references/"
echo "=================================================="
