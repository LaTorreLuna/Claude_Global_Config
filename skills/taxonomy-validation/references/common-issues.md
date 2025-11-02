# Common Taxonomy Issues and Remediation

## Circular References
**Pattern**: A → B → C → A
**Remediation**: Remove weakest relationship link

## Orphaned Concepts
**Pattern**: Concept with no relationships
**Remediation**: Connect to parent or remove if obsolete

## Non-Reciprocal Relationships
**Pattern**: A is BT of B, but B not NT of A
**Remediation**: Add missing reciprocal relationship

## Duplicate Labels
**Pattern**: Two concepts with same prefLabel
**Remediation**: Disambiguate or merge concepts

## Depth Violations
**Pattern**: >7 hierarchy levels
**Remediation**: Flatten or split into facets
