#!/usr/bin/env node

/**
 * PPTX Generation Script
 * Converts HTML slides to PPTX using document-skills/pptx html2pptx workflow
 *
 * Usage: node scripts/generate-slides.js <html-file>
 * Example: node scripts/generate-slides.js projects/acme-corp/deliverables/slide-deck.html
 *
 * Prerequisites:
 * - document-skills/pptx skill must be available
 * - HTML file must follow html2pptx format requirements:
 *   - Dimensions: 720pt × 405pt (16:9)
 *   - All text in <p>, <h1>-<h6>, <ul>, <ol> tags
 *   - No text directly in <div> or <span>
 *
 * This script serves as a wrapper to invoke the pptx skill.
 * It could be extended to:
 * 1. Validate HTML format before conversion
 * 2. Extract pyramid-analysis.md data to populate slides
 * 3. Integrate color scheme from assets/color-scheme.json
 * 4. Add automated quality checks
 */

const fs = require('fs');
const path = require('path');

// Parse command line arguments
const args = process.argv.slice(2);
if (args.length < 1) {
    console.error('Usage: node generate-slides.js <html-file>');
    console.error('Example: node generate-slides.js projects/acme-corp/deliverables/slide-deck.html');
    process.exit(1);
}

const htmlFile = args[0];
const outputFile = htmlFile.replace('.html', '.pptx');

console.log('================================================');
console.log('Market Research PPTX Generator');
console.log('================================================');
console.log(`Input:  ${htmlFile}`);
console.log(`Output: ${outputFile}`);
console.log('');

// Validate HTML file exists
if (!fs.existsSync(htmlFile)) {
    console.error(`ERROR: HTML file not found: ${htmlFile}`);
    process.exit(1);
}

// Read HTML content
console.log('[1/5] Reading HTML file...');
const htmlContent = fs.readFileSync(htmlFile, 'utf-8');

// Validate HTML format
console.log('[2/5] Validating HTML format...');
validateHtmlFormat(htmlContent);

// Check for document-skills/pptx availability
console.log('[3/5] Checking document-skills/pptx availability...');
const pptxSkillPath = path.join(__dirname, '../../document-skills/pptx');
const hasPptxSkill = fs.existsSync(pptxSkillPath);

if (!hasPptxSkill) {
    console.warn('WARNING: document-skills/pptx not found locally.');
    console.warn('Assuming pptx skill is available in Claude environment.');
    console.warn('To install locally: git submodule add https://github.com/anthropics/skills document-skills');
    console.log('');
}

// Generate PPTX
console.log('[4/5] Generating PPTX...');
console.log('');
console.log('INSTRUCTION: This script requires the pptx skill to complete conversion.');
console.log('Please invoke the pptx skill with the following HTML file:');
console.log(`  ${path.resolve(htmlFile)}`);
console.log('');
console.log('The pptx skill will:');
console.log('1. Parse HTML slides using html2pptx workflow');
console.log('2. Convert to PPTX format with proper dimensions (16:9)');
console.log('3. Save to: ' + outputFile);
console.log('');

// Quality checks
console.log('[5/5] Pre-generation quality checks...');
runQualityChecks(htmlContent);

console.log('');
console.log('================================================');
console.log('Next Steps:');
console.log('================================================');
console.log('1. Invoke the pptx skill in Claude Code');
console.log('2. Provide the HTML file path above');
console.log('3. Review generated PPTX for:');
console.log('   - Professional design (no AI slop patterns)');
console.log('   - All text visible (check no text in plain <div>)');
console.log('   - Source citations present');
console.log('   - Slide narrative flows logically');
console.log('4. Make refinements as needed');
console.log('================================================');

/**
 * Validate HTML follows html2pptx requirements
 */
function validateHtmlFormat(html) {
    const issues = [];

    // Check for required dimensions
    if (!html.includes('720pt') || !html.includes('405pt')) {
        issues.push('Missing required slide dimensions (720pt × 405pt)');
    }

    // Check for text directly in div/span (common error)
    const divTextPattern = /<div[^>]*>[^<]*[a-zA-Z]+[^<]*<\/div>/;
    const spanTextPattern = /<span[^>]*>[^<]*[a-zA-Z]+[^<]*<\/span>/;

    if (divTextPattern.test(html)) {
        issues.push('WARNING: Found text directly in <div> tags (may be invisible in PPTX)');
    }
    if (spanTextPattern.test(html)) {
        issues.push('WARNING: Found text directly in <span> tags (may be invisible in PPTX)');
    }

    // Check for # prefix in colors (causes corruption in PptxGenJS)
    const colorPattern = /color:\s*#[0-9A-Fa-f]{6}/;
    if (colorPattern.test(html)) {
        console.log('   INFO: Found # prefix in colors (acceptable in HTML/CSS)');
        console.log('   REMINDER: Remove # when using colors in PptxGenJS calls');
    }

    if (issues.length > 0) {
        console.warn('   Format issues found:');
        issues.forEach(issue => console.warn(`   - ${issue}`));
    } else {
        console.log('   ✓ HTML format looks good');
    }
}

/**
 * Run quality checks on content
 */
function runQualityChecks(html) {
    const checks = [];

    // Check for AI slop patterns
    if (html.includes('#6366F1') || html.includes('#8B5CF6') || html.includes('#A855F7')) {
        checks.push('✗ AI slop detected: Found Tailwind default purple colors');
    } else {
        checks.push('✓ No AI slop purple gradients detected');
    }

    // Check for professional structure
    if (html.includes('class="slide"')) {
        checks.push('✓ Slide structure present');
    }

    // Check for semantic HTML
    const hasSemanticTags = html.includes('<h1') || html.includes('<h2') || html.includes('<p>') || html.includes('<ul>');
    if (hasSemanticTags) {
        checks.push('✓ Semantic HTML tags present');
    } else {
        checks.push('✗ Missing semantic HTML tags');
    }

    // Check for required slides
    const requiredSlides = [
        'Executive Summary',
        'Market',
        'Customer',
        'Competitive',
        'Company',
        'Recommendations'
    ];

    requiredSlides.forEach(slide => {
        if (html.includes(slide)) {
            checks.push(`✓ "${slide}" slide found`);
        } else {
            checks.push(`⚠ "${slide}" slide may be missing`);
        }
    });

    checks.forEach(check => console.log(`   ${check}`));
}
