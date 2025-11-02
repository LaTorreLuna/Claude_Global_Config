# Taxonomy Validation Report

**Taxonomy**: [Taxonomy Name]
**Version**: [Version Number]
**Date**: [Validation Date]
**Validator**: [Name]
**Status**: [PASS / FAIL / PASS WITH WARNINGS]

---

## Executive Summary

[1-2 paragraph summary of validation results]

**Overall Assessment**: [PASS/FAIL]

**Critical Issues**: [Number]
**High Priority Issues**: [Number]
**Medium Priority Issues**: [Number]
**Low Priority Issues**: [Number]

---

## Taxonomy Statistics

- **Total Concepts**: [N]
- **Top-Level Concepts**: [N]
- **Maximum Depth**: [N] levels
- **Average Depth**: [N] levels
- **Total Broader/Narrower Relationships**: [N]
- **Total Related Relationships**: [N]
- **Polyhierarchical Concepts** (multiple parents): [N] ([%]%)

---

## ANSI/NISO Z39.19 Compliance

### Structural Rules

| Rule | Status | Details |
|------|--------|---------|
| Single root or 3-7 top-level concepts | ✓ PASS / ✗ FAIL | [Details] |
| Depth within recommended range (5-6 optimal) | ✓ PASS / ⚠ WARNING / ✗ FAIL | Max depth: [N] levels |
| Balanced tree structure | ✓ PASS / ✗ FAIL | [Details] |
| Consistent granularity at each level | ✓ PASS / ✗ FAIL | [Details] |
| No orphaned concepts | ✓ PASS / ✗ FAIL | [N] orphans found |
| No circular references | ✓ PASS / ✗ FAIL | [N] cycles found |

### Relationship Rules

| Rule | Status | Details |
|------|--------|---------|
| BT/NT relationships are reciprocal | ✓ PASS / ✗ FAIL | [N] violations |
| "Is a kind of" test passes for BT/NT | ✓ PASS / ✗ FAIL | [N] violations |
| RT relationships are symmetric | ✓ PASS / ✗ FAIL | [N] violations |
| No mixing of relationship types | ✓ PASS / ✗ FAIL | [Details] |

### Term Quality

| Rule | Status | Details |
|------|--------|---------|
| Preferred labels are unique | ✓ PASS / ✗ FAIL | [N] duplicates |
| Alternative labels captured for synonyms | ✓ PASS / ⚠ WARNING | [Details] |
| Scope notes where needed | ✓ PASS / ⚠ WARNING | [Details] |
| Consistent terminology | ✓ PASS / ✗ FAIL | [Details] |
| No undefined jargon | ✓ PASS / ✗ FAIL | [N] terms flagged |

---

## Issues Identified

### Critical Issues (Must Fix Before Deployment)

#### 1. [Issue Title]
- **Severity**: Critical
- **Location**: [Concept ID or path]
- **Description**: [What is wrong]
- **Impact**: [Why this is critical]
- **Recommendation**: [How to fix]

### High Priority Issues (Fix Before Final Release)

#### 1. [Issue Title]
- **Severity**: High
- **Location**: [Concept ID or path]
- **Description**: [What is wrong]
- **Impact**: [Why this matters]
- **Recommendation**: [How to fix]

### Medium Priority Issues (Address in Next Version)

#### 1. [Issue Title]
- **Severity**: Medium
- **Location**: [Concept ID or path]
- **Description**: [What could be improved]
- **Recommendation**: [How to improve]

### Low Priority Issues (Optional Improvements)

#### 1. [Issue Title]
- **Severity**: Low
- **Location**: [Concept ID or path]
- **Description**: [Minor improvement opportunity]
- **Recommendation**: [How to improve]

---

## Detailed Findings

### Orphaned Concepts

[List of concepts with no parent or children (except root and leaves)]

| Concept ID | Preferred Label | Issue |
|------------|-----------------|-------|
| [ID] | [Label] | No parent relationship |
| [ID] | [Label] | No children (not a leaf) |

### Circular References

[List of circular dependency chains]

| Chain | Description |
|-------|-------------|
| A → B → C → A | [Explanation] |

### Duplicate Preferred Labels

[List of non-unique preferred labels]

| Preferred Label | Concept IDs | Issue |
|-----------------|-------------|-------|
| [Label] | [ID1, ID2] | Ambiguous term |

### Depth Violations

[Branches exceeding recommended depth]

| Branch | Depth | Path |
|--------|-------|------|
| [Root → ... → Leaf] | [N] levels | [Full path] |

---

## Recommendations

### Immediate Actions (Before Deployment)
1. [Action 1]
2. [Action 2]
3. [Action 3]

### Short-Term Improvements (Within 1 Month)
1. [Action 1]
2. [Action 2]

### Long-Term Enhancements (Future Versions)
1. [Action 1]
2. [Action 2]

---

## Validation Methodology

**Tools Used**: [List of validation tools]
**Manual Review**: [Scope of manual review]
**Test Cases**: [Number of test scenarios]

---

## Sign-Off

**Validator Signature**: ___________________
**Date**: ___________________

**Taxonomy Owner Review**: ___________________
**Date**: ___________________

**Approval Status**: [ ] Approved [ ] Approved with Conditions [ ] Rejected

**Conditions** (if applicable):
[List any conditions for approval]

---

## Appendix: Validation Checklist

- [ ] No orphaned concepts (except root and leaves)
- [ ] No circular references
- [ ] All BT/NT relationships are reciprocal
- [ ] All RT relationships are symmetric
- [ ] Depth within recommended range (5-6 levels)
- [ ] Breadth per node within recommended range (5-9 children)
- [ ] Top-level concepts are mutually exclusive
- [ ] Preferred labels are unique
- [ ] "Is a kind of" test passes for all BT/NT pairs
- [ ] Consistent terminology throughout
- [ ] Scope notes provided where needed
- [ ] Alternative labels captured for common synonyms
