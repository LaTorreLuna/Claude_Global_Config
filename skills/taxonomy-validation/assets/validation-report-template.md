# Taxonomy Validation Report

**Taxonomy Name**: [Name]
**Validation Date**: [Date]
**Validator**: [Name]
**Validation Type**: [Quick/Comprehensive]

---

## Executive Summary

**Overall Status**: [PASS/FAIL]

**Issue Summary**:
- Critical: [N]
- High: [N]
- Medium: [N]
- Low: [N]

**Top 5 Issues**:
1. [Issue description with severity]
2. [Issue description with severity]
3. [Issue description with severity]
4. [Issue description with severity]
5. [Issue description with severity]

---

## Structural Issues

### Orphaned Concepts
**Severity**: High
**Count**: [N]

**Examples**:
- [Concept URI] - [Concept Label]

**Remediation**: Connect to parent hierarchy or remove if obsolete.

---

### Circular References
**Severity**: Critical
**Count**: [N]

**Examples**:
- [Concept A] → [Concept B] → [Concept C] → [Concept A]

**Remediation**: Identify weakest link in chain and remove relationship.

---

### Depth Violations
**Severity**: Medium
**Count**: [N]

**Details**:
- Maximum depth: [N] levels
- Optimal depth: 5-6 levels
- Warning threshold: 7+ levels

**Branches exceeding 7 levels**:
- [Branch name]: [N] levels

**Remediation**: Flatten hierarchy or split into facets.

---

### Breadth Violations
**Severity**: Low
**Count**: [N]

**Details**:
- Optimal breadth: 5-9 children per node
- Nodes with <2 children: [N]
- Nodes with >15 children: [N]

**Examples**:
- [Concept URI] - [N] children (too many/few)

**Remediation**: Rebalance tree structure.

---

## Relationship Issues

### Non-Reciprocal BT/NT
**Severity**: High
**Count**: [N]

**Examples**:
- [Concept A] is BT of [Concept B], but [Concept B] not NT of [Concept A]

**Remediation**: Add missing reciprocal relationship.

---

### Asymmetric RT
**Severity**: High
**Count**: [N]

**Examples**:
- [Concept A] is RT of [Concept B], but [Concept B] not RT of [Concept A]

**Remediation**: Add missing symmetric relationship.

---

### Invalid BT/NT Relationships
**Severity**: Critical
**Count**: [N]

**Examples**:
- [Concept A] BT [Concept B] - Fails "is a kind of" test

**Remediation**: Review relationship type - may be part-of or related-to instead.

---

## Term Quality Issues

### Duplicate Preferred Labels
**Severity**: Critical
**Count**: [N]

**Examples**:
- "[Label]" used by:
  - [Concept URI 1]
  - [Concept URI 2]

**Remediation**: Disambiguate with qualifiers or merge concepts if truly identical.

---

### Missing Definitions
**Severity**: High
**Count**: [N]

**Concepts requiring definitions**:
- [Concept URI] - [Concept Label]

**Remediation**: Add scope notes or definitions, especially for top-level concepts.

---

### Inconsistent Terminology
**Severity**: Medium
**Count**: [N]

**Examples**:
- Singular/plural mixing: "Employee" vs "Employees"
- Capitalization: "human resources" vs "Human Resources"

**Remediation**: Establish and apply consistent terminology rules.

---

### Missing Alternative Labels
**Severity**: Low
**Count**: [N]

**Concepts missing altLabels for common synonyms**:
- [Concept URI] - [Concept Label]

**Remediation**: Add alternative labels for known synonyms.

---

## Coverage Analysis

### Domain Coverage Assessment

**Well-Covered Areas**:
- [Domain area 1]
- [Domain area 2]

**Under-Developed Areas**:
- [Domain area 1] - Missing key concepts: [list]
- [Domain area 2] - Insufficient granularity

**Missing Cross-References**:
- [Concept A] ↔ [Concept B] - RT relationship recommended

---

## Statistical Analysis

**Taxonomy Metrics**:
- Total concepts: [N]
- Top-level concepts: [N]
- Maximum depth: [N] levels
- Average breadth: [N] children per node
- Orphaned concepts: [N]
- Leaf concepts: [N]

**Relationship Metrics**:
- BT/NT pairs: [N]
- RT relationships: [N]
- Total relationships: [N]

**Term Quality Metrics**:
- Concepts with definitions: [N] ([%]%)
- Concepts with altLabels: [N] ([%]%)
- Average labels per concept: [N]

---

## Remediation Plan

### Priority 1 (Critical) - Fix before deployment
**Estimated effort**: [N] hours

1. [Issue description] - [Specific fix]
2. [Issue description] - [Specific fix]

---

### Priority 2 (High) - Fix before release
**Estimated effort**: [N] hours

1. [Issue description] - [Specific fix]
2. [Issue description] - [Specific fix]

---

### Priority 3 (Medium) - Address in next version
**Estimated effort**: [N] hours

1. [Issue description] - [Specific fix]
2. [Issue description] - [Specific fix]

---

### Priority 4 (Low) - Optional improvements
**Estimated effort**: [N] hours

1. [Issue description] - [Specific fix]
2. [Issue description] - [Specific fix]

---

## Validation Details

**Validation Tools Used**:
- [ ] validate_structure.py
- [ ] validate_relationships.py
- [ ] validate_terms.py
- [ ] Manual review

**Standards Compliance**:
- [ ] ANSI/NISO Z39.19 structural rules
- [ ] BT/NT reciprocity
- [ ] RT symmetry
- [ ] Term quality guidelines

---

## Recommendations

**Immediate Actions**:
1. [Recommendation 1]
2. [Recommendation 2]

**Long-Term Improvements**:
1. [Recommendation 1]
2. [Recommendation 2]

**Governance**:
- Establish regular validation schedule: [Frequency]
- Assign taxonomy owner: [Person/Team]
- Define change approval process

---

## Sign-Off

**Validator**: [Name]
**Date**: [Date]
**Next Review Date**: [Date]

**Status**: [Approved for Deployment / Requires Remediation]
