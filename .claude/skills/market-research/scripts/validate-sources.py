#!/usr/bin/env python3

"""
Source Validation Script
Automates CRAAP testing for research sources

Usage: python scripts/validate-sources.py <bibliography-file>
Example: python scripts/validate-sources.py projects/acme-corp/analysis/source-bibliography.md

This script analyzes sources documented in source-bibliography.md and provides:
1. Automated CRAAP scoring (where possible)
2. Quality assessment summary
3. Triangulation validation
4. Recommendations for improvement

Note: Full CRAAP testing requires human judgment. This script provides
automated checks for objective criteria (Currency, some Authority checks).
"""

import sys
import re
from datetime import datetime
from typing import List, Dict, Optional
import os

class Source:
    """Represents a research source with CRAAP assessment"""

    def __init__(self, citation: str, tier: int):
        self.citation = citation
        self.tier = tier
        self.currency_score = 0
        self.relevance_score = 0
        self.authority_score = 0
        self.accuracy_score = 0
        self.purpose_score = 0
        self.total_score = 0
        self.publication_year = None
        self.source_type = None

    def calculate_currency_score(self) -> int:
        """
        Automated currency scoring based on publication date
        5 = Within 12 months
        4 = 1-2 years
        3 = 2-3 years
        2 = 3-5 years
        1 = >5 years
        """
        if not self.publication_year:
            return 0

        current_year = datetime.now().year
        age = current_year - self.publication_year

        if age <= 1:
            return 5
        elif age <= 2:
            return 4
        elif age <= 3:
            return 3
        elif age <= 5:
            return 2
        else:
            return 1

    def calculate_authority_score(self) -> int:
        """
        Automated authority scoring based on source type and tier
        Tier 1 = 5 points base
        Tier 2 = 4 points base
        Tier 3 = 3 points base
        """
        tier_scores = {1: 5, 2: 4, 3: 3}
        return tier_scores.get(self.tier, 0)


def parse_bibliography(file_path: str) -> List[Source]:
    """Parse source-bibliography.md file and extract sources"""

    if not os.path.exists(file_path):
        print(f"ERROR: File not found: {file_path}")
        sys.exit(1)

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    sources = []
    current_tier = None

    # Extract tier sections
    tier_patterns = {
        1: r'## TIER 1 SOURCES.*?(?=## TIER 2 SOURCES|## TIER 3 SOURCES|$)',
        2: r'## TIER 2 SOURCES.*?(?=## TIER 3 SOURCES|## REJECTED SOURCES|$)',
        3: r'## TIER 3 SOURCES.*?(?=## REJECTED SOURCES|## SOURCE TRIANGULATION|$)'
    }

    for tier, pattern in tier_patterns.items():
        tier_section = re.search(pattern, content, re.DOTALL)
        if tier_section:
            # Extract individual sources
            source_blocks = re.findall(
                r'\*\*Citation:\*\*\s*\n([^\n]+)\n',
                tier_section.group(),
                re.MULTILINE
            )

            for citation in source_blocks:
                source = Source(citation, tier)

                # Extract publication year
                year_match = re.search(r'\((\d{4})\)', citation)
                if year_match:
                    source.publication_year = int(year_match.group(1))

                # Determine source type
                if 'census' in citation.lower() or 'gov' in citation.lower():
                    source.source_type = 'Government'
                elif 'journal' in citation.lower() or 'doi' in citation.lower():
                    source.source_type = 'Academic'
                elif 'sec.gov' in citation.lower():
                    source.source_type = 'SEC Filing'
                else:
                    source.source_type = 'Other'

                sources.append(source)

    return sources


def calculate_automated_scores(sources: List[Source]) -> None:
    """Calculate automated CRAAP scores for all sources"""

    for source in sources:
        source.currency_score = source.calculate_currency_score()
        source.authority_score = source.calculate_authority_score()
        # Note: Relevance, Accuracy, and Purpose require manual assessment
        source.total_score = source.currency_score + source.authority_score


def print_summary(sources: List[Source]) -> None:
    """Print validation summary"""

    print("=" * 60)
    print("SOURCE VALIDATION SUMMARY")
    print("=" * 60)
    print(f"Total sources analyzed: {len(sources)}")
    print()

    # Breakdown by tier
    tier_counts = {1: 0, 2: 0, 3: 0}
    for source in sources:
        tier_counts[source.tier] += 1

    print("Sources by tier:")
    print(f"  Tier 1 (Highest credibility): {tier_counts[1]}")
    print(f"  Tier 2 (High credibility):    {tier_counts[2]}")
    print(f"  Tier 3 (Requires verification): {tier_counts[3]}")
    print()

    # Currency analysis
    current_year = datetime.now().year
    recent_sources = sum(1 for s in sources if s.publication_year and current_year - s.publication_year <= 3)
    print(f"Recent sources (≤3 years old): {recent_sources} ({recent_sources/len(sources)*100:.1f}%)")
    print()

    # Average scores (automated portion only)
    avg_currency = sum(s.currency_score for s in sources) / len(sources) if sources else 0
    avg_authority = sum(s.authority_score for s in sources) / len(sources) if sources else 0

    print("Automated CRAAP Scores (out of 5):")
    print(f"  Average Currency:  {avg_currency:.2f}")
    print(f"  Average Authority: {avg_authority:.2f}")
    print()
    print("NOTE: Relevance, Accuracy, and Purpose require manual assessment")
    print()


def print_detailed_analysis(sources: List[Source]) -> None:
    """Print detailed source-by-source analysis"""

    print("=" * 60)
    print("DETAILED SOURCE ANALYSIS")
    print("=" * 60)
    print()

    for idx, source in enumerate(sources, 1):
        print(f"Source #{idx} [Tier {source.tier}]")
        print(f"  Citation: {source.citation[:80]}...")
        print(f"  Type: {source.source_type}")
        if source.publication_year:
            print(f"  Year: {source.publication_year}")
        print(f"  Currency Score: {source.currency_score}/5")
        print(f"  Authority Score: {source.authority_score}/5")
        print()


def print_recommendations(sources: List[Source]) -> None:
    """Print recommendations for improving source quality"""

    print("=" * 60)
    print("RECOMMENDATIONS")
    print("=" * 60)
    print()

    # Check for outdated sources
    current_year = datetime.now().year
    outdated = [s for s in sources if s.publication_year and current_year - s.publication_year > 5]

    if outdated:
        print(f"⚠ WARNING: {len(outdated)} sources are >5 years old:")
        for source in outdated[:3]:  # Show first 3
            print(f"  - {source.citation[:60]}...")
        print(f"  Recommendation: Seek more recent data or justify use of historical sources")
        print()

    # Check tier distribution
    tier_1_ratio = sum(1 for s in sources if s.tier == 1) / len(sources) if sources else 0

    if tier_1_ratio < 0.4:
        print(f"⚠ WARNING: Only {tier_1_ratio*100:.1f}% of sources are Tier 1")
        print(f"  Recommendation: Increase use of government and peer-reviewed sources")
        print()

    # Check for sufficient triangulation
    if len(sources) < 15:
        print(f"⚠ INFO: Only {len(sources)} sources documented")
        print(f"  Recommendation: Typical MBB projects use 20-40+ sources")
        print()

    # Check source diversity
    source_types = set(s.source_type for s in sources)
    if len(source_types) < 3:
        print(f"⚠ WARNING: Limited source diversity (only {len(source_types)} types)")
        print(f"  Recommendation: Include mix of government, academic, and industry sources")
        print()

    # Positive feedback
    recent_tier1 = sum(1 for s in sources
                       if s.tier == 1 and s.publication_year and current_year - s.publication_year <= 3)
    if recent_tier1 >= 5:
        print(f"✓ EXCELLENT: {recent_tier1} recent Tier 1 sources provide strong foundation")
        print()


def main():
    """Main validation workflow"""

    if len(sys.argv) < 2:
        print("Usage: python validate-sources.py <bibliography-file>")
        print("Example: python validate-sources.py projects/acme-corp/analysis/source-bibliography.md")
        sys.exit(1)

    bibliography_file = sys.argv[1]

    print("=" * 60)
    print("MARKET RESEARCH SOURCE VALIDATOR")
    print("=" * 60)
    print(f"Analyzing: {bibliography_file}")
    print()

    # Parse sources
    sources = parse_bibliography(bibliography_file)

    if not sources:
        print("WARNING: No sources found in bibliography file")
        print("Ensure file follows source-bibliography.md template format")
        sys.exit(1)

    # Calculate automated scores
    calculate_automated_scores(sources)

    # Print results
    print_summary(sources)
    print_detailed_analysis(sources)
    print_recommendations(sources)

    # Final message
    print("=" * 60)
    print("VALIDATION COMPLETE")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Complete manual CRAAP assessment for Relevance, Accuracy, Purpose")
    print("2. Address any warnings in recommendations section")
    print("3. Ensure critical findings triangulated with 2-3 sources")
    print("4. Update source-bibliography.md with complete CRAAP scores")
    print()


if __name__ == "__main__":
    main()
