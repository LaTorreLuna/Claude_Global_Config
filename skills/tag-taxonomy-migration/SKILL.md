---
name: tag-taxonomy-migration
description: Migrate flat tag structures to hierarchical taxonomies in Obsidian vaults or markdown systems. Use when converting unstructured tags (like #credentials, #GHR, #hiring) into formal SKOS-compliant hierarchies with broader/narrower/related relationships while preserving existing content links.
---

# Tag Taxonomy Migration

## Overview

This skill provides a systematic workflow for migrating flat, unstructured tag systems to hierarchical, standards-compliant taxonomies. The process analyzes existing tags, identifies natural groupings, designs hierarchical relationships, generates migration scripts, and validates the migration before deployment.

## When to Use This Skill

Deploy this skill when:
- Obsidian vault has grown organically with inconsistent flat tags
- Tags have become too numerous and unmanageable
- Need to establish hierarchy and relationships between tags
- Migrating to formal taxonomy for better knowledge organization
- Converting legacy classification to modern taxonomy standards

## Workflow Decision Tree

```
Start: User wants to migrate tags
    ↓
Are there existing tags to analyze?
    │
    ├─ YES → Follow full workflow (Steps 1-6)
    │
    └─ NO → Creating taxonomy from scratch?
           └─ Use taxonomy-design-workflow skill instead
```

## Step 1: Tag Analysis & Inventory

Analyze current tag usage to understand migration scope.

### 1.1 Extract All Tags

Use `scripts/analyze_tags.py` to extract current tags:

```bash
python scripts/analyze_tags.py <vault-path> --output tag_inventory.csv
```

Output includes:
- Tag name
- Usage count (how many files use this tag)
- Co-occurrence patterns (which tags appear together)
- File examples

### 1.2 Review Tag Inventory

Review with user:
- **High-value tags**: Frequently used, represent important concepts
- **Redundant tags**: Duplicates, synonyms (e.g., #credential vs #credentials)
- **Deprecated tags**: No longer relevant or used
- **Ambiguous tags**: Multiple meanings depending on context

### 1.3 Identify Tag Relationships

Look for natural patterns:
- **Parent-child**: #credentials contains #preliminary-credential, #clear-credential
- **Synonyms**: #GHR-system, #GHR, #go-live (all refer to same system)
- **Related**: #hiring and #onboarding (different processes, but related)
- **Cross-cutting**: Tags that span multiple hierarchies

**Output**: Tag inventory with relationship candidates

---

## Step 2: Design Target Taxonomy Structure

Define the hierarchical structure tags will migrate to.

### 2.1 Propose Hierarchy

Create proposed taxonomy structure:

```
HR_Processes
├── Hiring
│   ├── Job_Posting
│   ├── Candidate_Screening
│   └── Interviewing
├── Onboarding
└── Retention

Credentials
├── Preliminary_Credentials
├── Clear_Credentials
│   ├── Single_Subject
│   └── Multiple_Subject
└── Specialist_Credentials

Systems
├── Lawson_HRIS
├── GHR_System
└── SmartFind
```

### 2.2 Map Old Tags to New Taxonomy

Create mapping table:

| Old Tag | New Taxonomy Term | Relationship | Notes |
|---------|-------------------|--------------|-------|
| #credentials | Credentials | Exact match | Top-level concept |
| #credential | Credentials | Synonym | Merge with #credentials |
| #prelim | Preliminary_Credentials | Child of Credentials | Abbreviation expanded |
| #clear-credential | Clear_Credentials | Child of Credentials | Standardize naming |
| #GHR | GHR_System | Exact match | |
| #ghr-conversion | GHR_System | Synonym | Context-specific tag |

### 2.3 Validate with User

Present proposed taxonomy and mapping:
- Does the hierarchy make sense?
- Are any important tags missing from the migration?
- Should any tags be split (one tag → multiple taxonomy terms)?
- Should any tags be merged?

**Output**: Approved taxonomy hierarchy and tag mapping table

---

## Step 3: Generate Migration Plan

Create detailed migration strategy.

### 3.1 Categorize Migration Complexity

**Automatic (1:1 mapping)**:
- Tags that map directly to new taxonomy terms
- No content changes needed
- Script can handle automatically

**Semi-Automatic (requires validation)**:
- Synonym merges (multiple old tags → one new term)
- Tag splits (one old tag → multiple new terms based on context)
- Ambiguous tags needing human review

**Manual (human judgment)**:
- Context-dependent tags
- Tags with multiple meanings
- Edge cases requiring subject matter expertise

### 3.2 Generate Migration Scripts

Use `scripts/generate_migration_plan.py`:

```bash
python scripts/generate_migration_plan.py tag_mapping.csv --output migration_scripts/
```

Creates:
- `1_automatic_migrations.sh` - Safe automatic replacements
- `2_semiautomatic_candidates.csv` - Requires review
- `3_manual_review_needed.csv` - Human judgment required

### 3.3 Create Rollback Plan

Document how to revert if migration fails:
- Git commit before migration (checkpoint)
- Backup of vault before changes
- Script to reverse all changes if needed

**Output**: Complete migration plan with automated scripts

---

## Step 4: Pilot Migration

Test migration on subset before full deployment.

### 4.1 Select Pilot Files

Choose 10-20 representative files:
- Files with many tags (test complexity)
- Files with few tags (test simplicity)
- Files with ambiguous tags (test edge cases)
- High-value files (test critical content)

### 4.2 Run Pilot Migration

Execute migration on pilot files:

```bash
# Create pilot branch
git checkout -b tag-migration-pilot

# Run automatic migrations on pilot files
bash migration_scripts/1_automatic_migrations.sh --files pilot_files.txt

# Review results
git diff
```

### 4.3 Validate Pilot Results

Check:
- ✓ All tags migrated correctly?
- ✓ No broken links or references?
- ✓ YAML frontmatter valid?
- ✓ File content unchanged (except tags)?
- ✓ Backlinks still work?

**Output**: Validated pilot migration with lessons learned

---

## Step 5: Full Migration Execution

Deploy migration across entire vault.

### 5.1 Create Backup

```bash
# Git commit current state
git add .
git commit -m "Pre-migration checkpoint: Taxonomy migration v1.0"

# Tag this commit for easy rollback
git tag pre-taxonomy-migration
```

### 5.2 Execute Automatic Migrations

```bash
# Run automated migration script
bash migration_scripts/1_automatic_migrations.sh

# Check status
git status
git diff --stat
```

### 5.3 Handle Semi-Automatic Cases

Review and process semi-automatic migrations:
- Load `2_semiautomatic_candidates.csv`
- For each case, make decision (merge/split/keep)
- Run batch operations for validated cases

### 5.4 Process Manual Cases

For `3_manual_review_needed.csv`:
- Review each file individually
- Apply context-appropriate taxonomy terms
- Document decisions for future reference

**Output**: Fully migrated vault with new taxonomy

---

## Step 6: Post-Migration Validation

Verify migration success and quality.

### 6.1 Run Validation Script

```bash
python scripts/validate_migration.py <vault-path> --report validation_report.md
```

Checks:
- All old tags migrated or deprecated
- No orphaned tag references
- YAML frontmatter valid across all files
- New taxonomy structure is consistent
- No circular references in hierarchy

### 6.2 Statistical Comparison

**Before Migration**:
- Total unique tags: [N]
- Average tags per file: [N]
- Tag usage distribution: [Chart]

**After Migration**:
- Total taxonomy terms: [N]
- Average terms per file: [N]
- Hierarchy depth: [N] levels
- Orphaned concepts: [N]

### 6.3 User Acceptance Testing

Test key workflows:
- Search by taxonomy term works?
- Tag-based queries return expected results?
- Graph view shows taxonomy hierarchy?
- Dataview queries still function?

### 6.4 Create Migration Documentation

Document using `assets/migration-report-template.md`:
- What was migrated
- Mapping decisions and rationale
- Known limitations or edge cases
- Post-migration maintenance guidelines

**Output**: Validation report and migration documentation

---

## Resources

### scripts/

**`analyze_tags.py`** - Extract and analyze current tag usage:
- Tag inventory with counts
- Co-occurrence analysis
- Synonym detection

**`generate_migration_plan.py`** - Create migration scripts from mapping table:
- Automatic migration script
- Semi-automatic candidate list
- Manual review list

**`validate_migration.py`** - Validate post-migration quality:
- Orphan detection
- Consistency checks
- Statistical reports

### references/

**`migration-strategies.md`** - Best practices for different migration scenarios:
- Simple hierarchy migration
- Faceted taxonomy migration
- Polyhierarchical migration
- Large-scale migrations (1000+ tags)

### assets/

**`migration-checklist.md`** - Step-by-step checklist for execution
**`migration-report-template.md`** - Template for documenting migration results

---

## Migration Best Practices

1. **Commit early, commit often** - Git checkpoint before each major step
2. **Start with pilot** - Never run full migration without testing on subset
3. **Preserve history** - Keep old tags as altLabels in taxonomy
4. **Communicate changes** - Inform users of new taxonomy structure
5. **Provide training** - Create quick guide for using new taxonomy
6. **Plan for iteration** - First migration won't be perfect; plan for refinement

---

## Common Pitfalls to Avoid

❌ **Migrating without backup** - Always create git checkpoint and tag
❌ **Skipping pilot phase** - Test on subset before full deployment
❌ **Over-automating** - Some cases require human judgment
❌ **Losing information** - Preserve old tags as alternative labels
❌ **Breaking existing workflows** - Test dataview queries, graph view, etc.
❌ **No rollback plan** - Know how to revert if migration fails

---

**Migration Complete**: Tags successfully migrated to hierarchical taxonomy with validation and documentation.
