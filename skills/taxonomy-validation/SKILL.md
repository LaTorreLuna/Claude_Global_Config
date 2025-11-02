---
name: taxonomy-validation
description: Validate taxonomies against ANSI/NISO Z39.19 standards by detecting structural issues, relationship inconsistencies, and term quality problems. Use when checking taxonomy health, auditing compliance, or preparing taxonomies for deployment. Generates comprehensive validation reports with severity-rated issues and remediation recommendations.
---

# Taxonomy Validation

## Overview

This skill provides systematic validation of taxonomies against ANSI/NISO Z39.19 standards, detecting structural problems (circular references, orphans, depth violations), relationship inconsistencies (non-reciprocal BT/NT, asymmetric RT), and term quality issues (duplicate labels, missing definitions, inconsistent terminology).

## When to Use This Skill

Deploy this skill when:
- Validating newly created taxonomy before deployment
- Auditing existing taxonomy for compliance
- Troubleshooting taxonomy issues reported by users
- Periodic quality checks (quarterly/annual reviews)
- Post-migration validation to ensure integrity
- Preparing taxonomy for formal release or publication

## Validation Categories

### 1. Structural Validation
Check hierarchy integrity and depth compliance.

**Automated Checks**:
```python
python scripts/validate_structure.py <taxonomy-file> --report structure_report.md
```

Detects:
- ✓ Orphaned concepts (no parent/children except root/leaves)
- ✓ Circular references (A → B → C → A)
- ✓ Depth violations (>7 levels)
- ✓ Unbalanced tree (one branch significantly deeper)
- ✓ Breadth violations (<2 or >15 children per node)
- ✓ Disconnected subgraphs

**Standards**:
- Optimal depth: 5-6 levels
- Warning at: 7+ levels
- Maximum recommended: 10 levels
- Optimal breadth: 5-9 children per node

---

### 2. Relationship Validation
Verify BT/NT/RT relationship consistency.

**Automated Checks**:
```python
python scripts/validate_relationships.py <taxonomy-file> --report relationship_report.md
```

Detects:
- ✓ Non-reciprocal BT/NT (A is BT of B, but B is not NT of A)
- ✓ Asymmetric RT (A is RT of B, but B is not RT of A)
- ✓ Invalid BT/NT relationships (fails "is a kind of" test)
- ✓ Mixed relationship types (part-of disguised as is-a)
- ✓ Redundant relationships (transitive duplicates)

**Validation Rules**:
- BT/NT must be reciprocal
- RT must be symmetric
- "Is a kind of" test must pass for all BT/NT pairs
- No mixing of relationship types

---

### 3. Term Quality Validation
Check label uniqueness, definitions, and consistency.

**Automated Checks**:
```python
python scripts/validate_terms.py <taxonomy-file> --report term_quality_report.md
```

Detects:
- ✓ Duplicate preferred labels (prefLabel)
- ✓ Missing definitions for top-level concepts
- ✓ Undefined jargon or acronyms
- ✓ Inconsistent terminology (singular/plural mixing)
- ✓ Missing alternative labels for common synonyms
- ✓ Inconsistent capitalization

**Quality Standards**:
- Preferred labels must be unique
- Top-level concepts must have definitions
- Acronyms must be expanded
- Consistent form (singular vs plural)
- Scope notes for ambiguous terms

---

### 4. Coverage Validation
Ensure taxonomy covers intended domain.

**Manual Checks**:
- Review sample content for classification gaps
- Validate all use cases can be addressed
- Check for missing cross-references (RT relationships)
- Identify under-developed branches

**Checklist**:
- [ ] All major domain areas covered
- [ ] No significant classification gaps
- [ ] Important cross-facet relationships captured
- [ ] Granularity appropriate for use cases

---

## Validation Workflow

### Quick Validation (10 minutes)
For routine checks:

```bash
# Run all automated validations
python scripts/validate_all.py <taxonomy-file> --quick --output quick_report.md
```

Provides:
- Issue count by severity (Critical/High/Medium/Low)
- Top 5 issues
- Overall PASS/FAIL status

---

### Comprehensive Validation (30-60 minutes)
For pre-deployment or formal audits:

```bash
# Run full validation suite
python scripts/validate_all.py <taxonomy-file> --comprehensive --output comprehensive_report.md
```

Includes:
- All automated checks
- Statistical analysis
- Comparison against best practices
- Detailed remediation recommendations
- Sample issues with examples

---

## Validation Report Format

Reports generated use `references/validation-rules.md` for standards compliance.

**Report Sections**:
1. **Executive Summary** - Overall status, issue counts
2. **Structural Issues** - Orphans, cycles, depth
3. **Relationship Issues** - Non-reciprocal, asymmetric
4. **Term Quality Issues** - Duplicates, missing definitions
5. **Coverage Analysis** - Gaps and recommendations
6. **Remediation Plan** - Prioritized fixes with effort estimates

**Severity Levels**:
- **Critical**: Must fix before deployment (circular references, duplicate labels)
- **High**: Should fix before release (orphans, depth violations)
- **Medium**: Address in next version (missing alt labels, minor inconsistencies)
- **Low**: Optional improvements (documentation, examples)

---

## Common Issues and Fixes

### Circular References
**Issue**: A → B → C → A
**Impact**: Critical - breaks hierarchy integrity
**Fix**: Identify weakest link in chain, remove relationship

### Orphaned Concepts
**Issue**: Concept with no parent or children (not root/leaf)
**Impact**: High - unreachable concepts
**Fix**: Connect to appropriate parent or remove if obsolete

### Non-Reciprocal BT/NT
**Issue**: A is BT of B, but B not defined as NT of A
**Impact**: High - relationship inconsistency
**Fix**: Add missing reciprocal relationship

### Duplicate Preferred Labels
**Issue**: Two concepts share same prefLabel
**Impact**: Critical - ambiguity
**Fix**: Disambiguate with qualifiers or merge concepts

### Depth Violation
**Issue**: Hierarchy exceeds 7 levels
**Impact**: Medium - usability concern
**Fix**: Flatten hierarchy or split into facets

---

## Resources

### scripts/

**`validate_structure.py`** - Check hierarchy integrity:
- Orphan detection
- Circular reference detection
- Depth analysis
- Balance assessment

**`validate_relationships.py`** - Verify relationship consistency:
- BT/NT reciprocity
- RT symmetry
- "Is a kind of" test

**`validate_terms.py`** - Check term quality:
- Label uniqueness
- Definition completeness
- Terminology consistency

**`validate_all.py`** - Run complete validation suite:
- Quick or comprehensive modes
- Generates unified report

### references/

**`validation-rules.md`** - Complete ANSI/NISO Z39.19 validation checklist
**`common-issues.md`** - Issue patterns and remediation strategies

### assets/

**`validation-report-template.md`** - Standard report format

---

## Validation Best Practices

1. **Validate early and often** - Catch issues during development
2. **Automate what you can** - Use scripts for objective checks
3. **Manual review is essential** - Some issues require human judgment
4. **Fix critical issues first** - Prioritize by severity and impact
5. **Document rationale** - Explain validation decisions
6. **Re-validate after fixes** - Ensure remediation didn't introduce new issues
7. **Schedule periodic audits** - Quarterly or when significant changes occur

---

## Integration with Other Skills

**After taxonomy-design-workflow**: Validate newly created taxonomy
**After tag-taxonomy-migration**: Validate migrated taxonomy structure
**Before deployment**: Final validation checkpoint

---

**Validation Complete**: Taxonomy health assessed with prioritized remediation plan.
