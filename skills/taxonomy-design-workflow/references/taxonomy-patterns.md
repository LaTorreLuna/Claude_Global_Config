# Common Taxonomy Patterns

## 1. Enumerative Taxonomy (Simple Hierarchy)

**Structure**: Single hierarchical tree with one path from root to each term

```
Root
├── Category A
│   ├── Subcategory A1
│   └── Subcategory A2
└── Category B
    ├── Subcategory B1
    └── Subcategory B2
```

**Best for**: Simple domains, clear hierarchical relationships, library classification
**Example**: Dewey Decimal System, organizational charts

## 2. Faceted Taxonomy (Multi-Dimensional)

**Structure**: Multiple independent hierarchies (facets) that can be combined

```
Facet 1: Document Type        Facet 2: Department        Facet 3: Status
├── Report                     ├── HR                     ├── Draft
├── Policy                     ├── Finance                ├── Final
└── Procedure                  └── IT                     └── Archived
```

**Best for**: Complex domains requiring multiple classification dimensions
**Example**: E-commerce (product type + brand + price range + color)

## 3. Polyhierarchical Taxonomy (Multiple Parents)

**Structure**: Terms can have multiple parent classifications

```
Root
├── Language Authorizations
│   └── BCLAD ←─┐
└── Subject Authorizations  │
    └── BCLAD ──────────────┘
```

**Best for**: Domains with natural overlaps, cross-cutting concepts
**Example**: Medical taxonomies, credential systems

## 4. Network Taxonomy (Rich Relationships)

**Structure**: Hierarchical structure enriched with associative (RT) relationships

```
Hiring Process (BT: HR Processes)
    NT: Job Posting
    NT: Candidate Screening
    NT: Interviews
    RT: Credential Verification
    RT: Onboarding Process
```

**Best for**: Knowledge graphs, complex domains with many interdependencies
**Example**: Enterprise taxonomies, semantic web applications

## Choosing the Right Pattern

| Pattern | Complexity | Flexibility | Maintenance | Best Use Case |
|---------|------------|-------------|-------------|---------------|
| Enumerative | Low | Low | Easy | Simple, stable domains |
| Faceted | Medium | High | Medium | E-commerce, multi-attribute search |
| Polyhierarchical | Medium-High | Medium | Medium | Cross-cutting concepts |
| Network | High | Very High | Complex | Knowledge management, semantic web |

## Implementation Guidance

**Start simple**: Begin with enumerative, add facets/polyhierarchy only when needed
**Validate with users**: Test classification patterns with actual usage scenarios
**Plan for evolution**: Choose patterns that support expected growth
