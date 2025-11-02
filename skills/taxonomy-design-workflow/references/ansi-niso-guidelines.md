# ANSI/NISO Z39.19 Key Guidelines

## Structural Requirements

### Hierarchy Depth
- **Optimal**: 5-6 levels
- **Warning**: 7+ levels (review for necessity)
- **Maximum**: 10 levels (rarely justified)

### Breadth per Node
- **Optimal**: 5-9 children per parent (Miller's Law - human working memory)
- **Minimum**: 2 children (otherwise, not a true parent)
- **Maximum**: 15 children (review for sub-grouping opportunities)

### Top-Level Concepts
- **Recommended**: 3-7 top-level categories
- **Avoid**: Single top-level concept (except "Root")
- **Avoid**: More than 12 top-level concepts (too fragmented)

### Tree Balance
- Branches should be relatively balanced in depth
- No single branch significantly deeper than others
- Consistent granularity at each level

## Relationship Rules

### Broader Term / Narrower Term (BT/NT)
- **"Is a kind of" test**: X is BT of Y if "Y is a kind of X"
- **Reciprocal**: If X is BT of Y, then Y must be NT of X
- **Transitive**: If A is BT of B, and B is BT of C, then A is BT of C
- **No mixing**: Don't use BT/NT for part-whole relationships

### Related Term (RT)
- **Symmetric**: If X is RT of Y, then Y is RT of X
- **Cross-facet**: Connect terms from different hierarchical branches
- **Associative**: Terms that are connected but not hierarchical

### Polyhierarchy
- **Allowed**: A term can have multiple broader terms
- **Use sparingly**: Only when genuinely needed
- **Validate**: Ensure all parent paths make logical sense

## Term Quality Standards

### Preferred Labels (prefLabel)
- **Uniqueness**: Unique within taxonomy scope
- **Clarity**: Unambiguous and clearly understood
- **Consistency**: Use consistent form (singular vs plural, capitalization)
- **Natural language**: Use terminology familiar to users

### Alternative Labels (altLabel)
- **Synonyms**: Capture all common variants
- **Acronyms**: Include both expanded and acronym forms
- **Historical terms**: Deprecated terms with references to current

### Scope Notes
- **When needed**: Ambiguous terms, jargon, specialized usage
- **Content**: Definition, usage context, examples
- **Concise**: 1-2 sentences typically sufficient

## Validation Checklist

- [ ] No orphaned concepts (except root and leaves)
- [ ] No circular references (A cannot be ancestor and descendant of B)
- [ ] All BT/NT relationships are reciprocal
- [ ] All RT relationships are symmetric
- [ ] Depth within recommended range (5-6 levels)
- [ ] Breadth per node within recommended range (5-9 children)
- [ ] Top-level concepts are mutually exclusive
- [ ] Preferred labels are unique
- [ ] "Is a kind of" test passes for all BT/NT pairs
- [ ] Consistent terminology throughout
