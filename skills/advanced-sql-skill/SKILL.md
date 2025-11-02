---
name: advanced-sql-skill
description: Advanced SQL query optimization, schema design, and performance tuning. Use when writing complex queries, optimizing slow queries, reviewing database schema, identifying anti-patterns, or working with HR/education database patterns. Specializes in window functions, CTEs, execution plan analysis, indexing strategies, and SQL best practices.
---

# Advanced SQL Skill

## Overview

This skill provides advanced SQL expertise for query optimization, schema design, performance troubleshooting, and best practices enforcement. It specializes in complex SQL techniques beyond basic SELECT/INSERT/UPDATE, with particular focus on educational HR databases.

**Core Capabilities:**
- Query optimization and execution plan analysis
- Advanced SQL techniques (window functions, CTEs, recursive queries)
- Schema design review and anti-pattern detection
- Performance troubleshooting and indexing strategies
- HR and education-specific SQL patterns

**When to Use This Skill:**
- Writing complex queries with JOINs, subqueries, or aggregations
- Optimizing slow-running queries
- Analyzing execution plans
- Designing or reviewing database schemas
- Identifying SQL anti-patterns and code smells
- Working with HR, payroll, credential, or student enrollment databases
- Implementing advanced SQL features (window functions, CTEs, pivots)

---

## Quick Start

### Common Trigger Phrases

**Query Optimization:**
- "This query is slow, can you optimize it?"
- "How can I improve the performance of this SQL?"
- "Analyze this execution plan"
- "Why is this query taking so long?"

**Advanced SQL Techniques:**
- "How do I calculate running totals in SQL?"
- "I need to implement a recursive hierarchy query"
- "Help me write a window function for ranking"
- "How do I pivot this data?"

**Schema Design:**
- "Review this table structure"
- "Is this database schema well-designed?"
- "How should I structure this many-to-many relationship?"
- "What indexes should I create?"

**Anti-Pattern Detection:**
- "Is this SQL query following best practices?"
- "What's wrong with this database design?"
- "Check this code for SQL injection"
- "Why am I getting duplicate rows?"

**HR/Education Specific:**
- "How do I track employee credentials in SQL?"
- "Query for expiring credentials"
- "Calculate employee leave balances"
- "Find substitute teacher availability"

---

## Task 1: Query Analysis and Optimization

### Step 1: Identify Performance Bottlenecks

When analyzing a slow query, follow this systematic approach:

**1. Capture Execution Plan**
```sql
SET STATISTICS IO ON;
SET STATISTICS TIME ON;

-- Your query here
SELECT ...
FROM ...;

SET STATISTICS IO OFF;
SET STATISTICS TIME OFF;
```

**2. Look for Key Indicators**
- **Table Scans** - Reading entire table instead of using index
- **Key Lookups** - Inefficient bookmark lookups
- **High Row Counts** - Operators processing millions of rows
- **Implicit Conversions** - Data type mismatches
- **Missing Indexes** - Execution plan suggestions

**3. Common Fixes**
```sql
-- BAD: Function on indexed column
WHERE YEAR(hire_date) = 2024

-- GOOD: Range comparison uses index
WHERE hire_date >= '2024-01-01' AND hire_date < '2025-01-01'

-- BAD: Leading wildcard
WHERE last_name LIKE '%son'

-- GOOD: Trailing wildcard or full-text search
WHERE last_name LIKE 'John%'
-- Or use CONTAINS() for full-text

-- BAD: Correlated subquery (N+1 problem)
SELECT e.employee_id,
       (SELECT COUNT(*) FROM credentials c WHERE c.employee_id = e.employee_id)
FROM employees e;

-- GOOD: JOIN with aggregation
WITH CredCounts AS (
    SELECT employee_id, COUNT(*) AS cred_count
    FROM credentials
    GROUP BY employee_id
)
SELECT e.employee_id, ISNULL(cc.cred_count, 0)
FROM employees e
LEFT JOIN CredCounts cc ON e.employee_id = cc.employee_id;
```

### Step 2: Apply Indexing Strategies

**Index Design Principles:**

1. **Index Foreign Keys** (used in JOINs)
```sql
CREATE NONCLUSTERED INDEX IX_employees_department_id
ON employees(department_id);
```

2. **Covering Indexes** (include all needed columns)
```sql
-- Query: SELECT first_name, last_name, email FROM employees WHERE status = 'Active'
CREATE NONCLUSTERED INDEX IX_employees_status_covering
ON employees(status)
INCLUDE (first_name, last_name, email);
```

3. **Filtered Indexes** (for subsets of data)
```sql
-- Only index active employees
CREATE NONCLUSTERED INDEX IX_employees_active_hire_date
ON employees(hire_date)
WHERE status = 'Active';
```

4. **Composite Indexes** (multiple columns)
```sql
-- Order matters! Most selective column first
CREATE NONCLUSTERED INDEX IX_employees_dept_status_hire
ON employees(department_id, status, hire_date);
```

**Reference:** See `references/query_optimization.md` for comprehensive execution plan analysis and indexing strategies.

---

## Task 2: Advanced SQL Techniques

### Window Functions

Use window functions for ranking, running totals, and moving averages without GROUP BY collapsing rows.

**Ranking Employees by Salary**
```sql
SELECT
    employee_id,
    first_name,
    last_name,
    department_id,
    salary,
    ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) AS salary_rank,
    RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS salary_rank_with_ties,
    DENSE_RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS dense_salary_rank
FROM employees
WHERE status = 'Active';
```

**Running Totals and Moving Averages**
```sql
SELECT
    hire_date,
    first_name,
    last_name,
    salary,
    -- Running total of salaries by hire date
    SUM(salary) OVER (ORDER BY hire_date ROWS UNBOUNDED PRECEDING) AS running_total,
    -- Moving average of last 3 hires
    AVG(salary) OVER (ORDER BY hire_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS moving_avg_3,
    -- Year-over-year comparison
    LAG(salary, 1) OVER (PARTITION BY employee_id ORDER BY hire_date) AS previous_salary,
    salary - LAG(salary, 1) OVER (PARTITION BY employee_id ORDER BY hire_date) AS salary_change
FROM employees;
```

### Common Table Expressions (CTEs)

**Simple CTE for Readability**
```sql
WITH ActiveEmployees AS (
    SELECT employee_id, first_name, last_name, department_id, salary
    FROM employees
    WHERE status = 'Active'
),
DepartmentStats AS (
    SELECT
        department_id,
        COUNT(*) AS employee_count,
        AVG(salary) AS avg_salary,
        MAX(salary) AS max_salary
    FROM ActiveEmployees
    GROUP BY department_id
)
SELECT
    ae.employee_id,
    ae.first_name,
    ae.last_name,
    ae.salary,
    ds.avg_salary AS dept_avg_salary,
    ae.salary - ds.avg_salary AS salary_vs_avg
FROM ActiveEmployees ae
INNER JOIN DepartmentStats ds ON ae.department_id = ds.department_id
WHERE ae.salary > ds.avg_salary * 1.2;  -- 20% above average
```

**Recursive CTE for Hierarchies**
```sql
WITH RECURSIVE EmployeeHierarchy AS (
    -- Anchor: Top-level managers
    SELECT
        employee_id,
        first_name,
        last_name,
        manager_id,
        1 AS level,
        CAST(first_name + ' ' + last_name AS NVARCHAR(1000)) AS hierarchy_path
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive: Subordinates
    SELECT
        e.employee_id,
        e.first_name,
        e.last_name,
        e.manager_id,
        eh.level + 1,
        CAST(eh.hierarchy_path + ' > ' + e.first_name + ' ' + e.last_name AS NVARCHAR(1000))
    FROM employees e
    INNER JOIN EmployeeHierarchy eh ON e.manager_id = eh.employee_id
    WHERE eh.level < 10  -- Prevent infinite loops
)
SELECT
    REPLICATE('  ', level - 1) + first_name + ' ' + last_name AS org_chart,
    level,
    hierarchy_path
FROM EmployeeHierarchy
ORDER BY hierarchy_path;
```

### PIVOT and UNPIVOT

**PIVOT: Rows to Columns**
```sql
-- Convert credential types from rows to columns
SELECT *
FROM (
    SELECT
        employee_id,
        credential_type,
        1 AS has_credential
    FROM employee_credentials
) AS source_data
PIVOT (
    MAX(has_credential)
    FOR credential_type IN ([Teaching], [Administrative], [Special Education], [ELL])
) AS pivot_table;
```

**UNPIVOT: Columns to Rows**
```sql
-- Convert quarterly sales from columns to rows
SELECT employee_id, quarter, sales_amount
FROM quarterly_sales
UNPIVOT (
    sales_amount FOR quarter IN ([Q1], [Q2], [Q3], [Q4])
) AS unpivot_table;
```

**Reference:** See `references/advanced_techniques.md` for 15 advanced SQL concepts with detailed examples.

---

## Task 3: Performance Troubleshooting

### Diagnostic Query: Identify Slow Queries

```sql
-- Top 10 slowest queries by average execution time
SELECT TOP 10
    qs.execution_count,
    qs.total_elapsed_time / 1000000.0 AS total_elapsed_time_sec,
    qs.total_elapsed_time / qs.execution_count / 1000000.0 AS avg_elapsed_time_sec,
    qs.total_worker_time / 1000000.0 AS total_cpu_time_sec,
    qs.total_logical_reads,
    qs.total_physical_reads,
    SUBSTRING(st.text, (qs.statement_start_offset/2)+1,
              ((CASE qs.statement_end_offset
                  WHEN -1 THEN DATALENGTH(st.text)
                  ELSE qs.statement_end_offset
                END - qs.statement_start_offset)/2) + 1) AS query_text
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) st
ORDER BY qs.total_elapsed_time / qs.execution_count DESC;
```

### Diagnostic Query: Missing Indexes

```sql
-- Identify missing indexes with high impact
SELECT
    CONVERT(DECIMAL(18,2), migs.user_seeks * migs.avg_total_user_cost * (migs.avg_user_impact * 0.01)) AS improvement_measure,
    'CREATE INDEX IX_' + OBJECT_NAME(mid.object_id, mid.database_id) + '_'
        + REPLACE(REPLACE(REPLACE(ISNULL(mid.equality_columns,''), ', ', '_'), '[', ''), ']', '')
        + CASE WHEN mid.inequality_columns IS NOT NULL THEN '_' + REPLACE(REPLACE(REPLACE(mid.inequality_columns, ', ', '_'), '[', ''), ']', '') ELSE '' END
        + ' ON ' + mid.statement
        + ' (' + ISNULL(mid.equality_columns, '')
        + CASE WHEN mid.equality_columns IS NOT NULL AND mid.inequality_columns IS NOT NULL THEN ',' ELSE '' END
        + ISNULL(mid.inequality_columns, '') + ')'
        + ISNULL(' INCLUDE (' + mid.included_columns + ')', '') AS create_index_statement,
    migs.user_seeks,
    migs.avg_total_user_cost,
    migs.avg_user_impact
FROM sys.dm_db_missing_index_group_stats migs
INNER JOIN sys.dm_db_missing_index_groups mig ON migs.group_handle = mig.index_group_handle
INNER JOIN sys.dm_db_missing_index_details mid ON mig.index_handle = mid.index_handle
WHERE migs.user_seeks > 100
  AND CONVERT(DECIMAL(18,2), migs.user_seeks * migs.avg_total_user_cost * (migs.avg_user_impact * 0.01)) > 100
ORDER BY improvement_measure DESC;
```

### Diagnostic Query: Index Fragmentation

```sql
-- Check index fragmentation and recommend action
SELECT
    OBJECT_NAME(ips.object_id) AS table_name,
    i.name AS index_name,
    ips.index_type_desc,
    ips.avg_fragmentation_in_percent,
    ips.page_count,
    CASE
        WHEN ips.avg_fragmentation_in_percent > 30 AND ips.page_count > 1000 THEN 'REBUILD'
        WHEN ips.avg_fragmentation_in_percent > 10 AND ips.page_count > 1000 THEN 'REORGANIZE'
        ELSE 'OK - No Action Needed'
    END AS recommended_action
FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'LIMITED') ips
INNER JOIN sys.indexes i ON ips.object_id = i.object_id AND ips.index_id = i.index_id
WHERE ips.avg_fragmentation_in_percent > 10
  AND ips.page_count > 1000
ORDER BY ips.avg_fragmentation_in_percent DESC;
```

### Common Performance Killers

**1. Parameter Sniffing**
```sql
-- Problem: Query plan optimized for first parameter value
CREATE PROCEDURE get_employees_by_department
    @department_id INT
AS
BEGIN
    -- BAD: Uses cached plan even if parameter changes drastically
    SELECT * FROM employees WHERE department_id = @department_id;
END;

-- Solution: Use OPTION (RECOMPILE) for varying parameters
CREATE PROCEDURE get_employees_by_department
    @department_id INT
AS
BEGIN
    SELECT employee_id, first_name, last_name
    FROM employees
    WHERE department_id = @department_id
    OPTION (RECOMPILE);
END;
```

**2. Implicit Conversions**
```sql
-- Problem: employee_id is INT, but comparing to VARCHAR
SELECT * FROM employees WHERE employee_id = '12345';  -- BAD!

-- Solution: Use correct data type
SELECT * FROM employees WHERE employee_id = 12345;  -- GOOD!
```

**3. Cursor Loops**
```sql
-- Problem: Row-by-row processing (10-100x slower)
DECLARE employee_cursor CURSOR FOR SELECT employee_id FROM employees;
-- ... cursor loop code ...

-- Solution: Set-based operation
UPDATE employees SET salary = salary * 1.03 WHERE status = 'Active';
```

**Reference:** See `references/query_optimization.md` for comprehensive performance troubleshooting guide.

---

## Task 4: HR and Education Patterns

This skill includes specialized SQL patterns for educational HR databases, covering:

### Employee Management
- Active employee roster with current assignments
- Employee change history tracking
- Substitute teacher availability
- Cross-department resource sharing

### Credential Tracking
- Expiring credentials alert system
- Credential subject area crosswalk (legacy → new system mapping)
- Credential compliance by department
- Prerequisite verification for advanced credentials

### Organization Structure
- Department budget allocation with hierarchical rollup
- Resource sharing across school sites
- FTE allocation tracking

### Student Enrollment
- Course enrollment with prerequisite checking
- Enrollment capacity management
- Section waitlist tracking

### Leave and Absence
- Leave balance calculation with accrual
- Substitute coverage gap detection
- FMLA tracking and compliance

### Payroll and Compensation
- Salary step and column progression (CBA schedules)
- Payroll period calculations
- Benefit eligibility tracking

**Example: Expiring Credentials Alert**
```sql
DECLARE @WarningDays INT = 90;

WITH ExpiringCredentials AS (
    SELECT
        e.employee_id,
        e.first_name + ' ' + e.last_name AS employee_name,
        e.email,
        c.credential_type,
        c.credential_number,
        c.expiration_date,
        DATEDIFF(DAY, GETDATE(), c.expiration_date) AS days_until_expiration,
        CASE
            WHEN DATEDIFF(DAY, GETDATE(), c.expiration_date) <= 30 THEN 'Critical'
            WHEN DATEDIFF(DAY, GETDATE(), c.expiration_date) <= 60 THEN 'High'
            ELSE 'Medium'
        END AS urgency_level
    FROM employees e
    INNER JOIN credentials c ON e.employee_id = c.employee_id
    WHERE e.status = 'Active'
      AND c.expiration_date BETWEEN GETDATE() AND DATEADD(DAY, @WarningDays, GETDATE())
)
SELECT *
FROM ExpiringCredentials
ORDER BY days_until_expiration ASC, urgency_level DESC;
```

**Reference:** See `references/hr_education_patterns.md` for 17 complete HR/education SQL patterns with examples.

---

## Task 5: Anti-Pattern Detection and Fixes

This skill helps identify and fix 24 common SQL anti-patterns across six categories:

### Query Design Anti-Patterns
1. **SELECT *** - Use explicit column lists
2. **Implicit column lists in INSERT** - Specify columns
3. **OR in JOIN conditions** - Use UNION or separate JOINs
4. **Correlated subqueries in SELECT** - Use JOINs or CTEs
5. **NOT IN with NULLs** - Use NOT EXISTS instead

### Performance Anti-Patterns
6. **Function calls on indexed columns** - Rewrite to be SARGable
7. **Leading wildcards in LIKE** - Use full-text search
8. **DISTINCT as band-aid** - Fix JOIN logic
9. **UNION instead of UNION ALL** - Use ALL when possible
10. **Cursor loops** - Use set-based operations (10-100x faster)
11. **Implicit data type conversion** - Match types exactly

### Data Integrity Anti-Patterns
12. **Flags instead of lookup tables** - Use proper foreign keys
13. **Delimited lists in columns** - Normalize to many-to-many
14. **No primary keys** - Always have PK
15. **EAV pattern** - Use proper schema or JSON

### Security Anti-Patterns
16. **SQL injection** - Use parameterized queries ALWAYS
17. **Plain text passwords** - Hash with bcrypt/PBKDF2
18. **Excessive permissions** - Principle of least privilege

### Schema Design Anti-Patterns
19. **FLOAT for money** - Use DECIMAL or MONEY
20. **VARCHAR(MAX) everywhere** - Use appropriate sizes
21. **GUID as clustered index** - Use INT IDENTITY or NEWSEQUENTIALID

### Maintenance Anti-Patterns
22. **No indexing strategy** - Query-driven index design
23. **No error handling** - Use TRY/CATCH blocks
24. **No documentation** - Comment complex logic

**Example: Fixing SQL Injection**
```sql
-- BAD: Vulnerable to SQL injection
CREATE PROCEDURE get_employee
    @last_name NVARCHAR(50)
AS
    DECLARE @sql NVARCHAR(1000);
    SET @sql = 'SELECT * FROM employees WHERE last_name = ''' + @last_name + '''';
    EXEC(@sql);  -- DANGER! Attack: @last_name = '''; DROP TABLE employees; --'

-- GOOD: Parameterized query (safe)
CREATE PROCEDURE get_employee
    @last_name NVARCHAR(50)
AS
    SELECT employee_id, first_name, last_name, email
    FROM employees
    WHERE last_name = @last_name;  -- Parameters prevent injection
```

**Reference:** See `references/sql_antipatterns.md` for all 24 anti-patterns with detailed explanations and fixes.

---

## Resources

This skill includes comprehensive reference material and utility scripts:

### references/ Directory

Four comprehensive SQL reference documents (~40,000 words total):

1. **advanced_techniques.md** (~10,000 words)
   - 15 advanced SQL concepts with code examples
   - Window functions (ROW_NUMBER, RANK, LAG, LEAD)
   - CTEs (simple, multiple, recursive)
   - PIVOT/UNPIVOT operations
   - User-defined functions (scalar, table-valued)
   - Temporary tables vs table variables

2. **query_optimization.md** (~8,000 words)
   - Execution plan analysis (reading plans, identifying bottlenecks)
   - Indexing strategies (clustered, non-clustered, covering, filtered, columnstore)
   - Query refactoring techniques (7 optimization patterns)
   - Performance monitoring (metrics, wait statistics, baselines)
   - Common issues (parameter sniffing, implicit conversions, N+1 problem)

3. **hr_education_patterns.md** (~12,000 words)
   - 17 common SQL patterns for HR/education databases
   - Employee management and assignment tracking
   - Credential verification and expiration monitoring
   - Department hierarchy and budget rollup
   - Student enrollment and prerequisite checking
   - Leave balance calculation and substitute coverage
   - Salary schedule progression (CBA steps and columns)

4. **sql_antipatterns.md** (~10,000 words)
   - 24 SQL anti-patterns with fixes
   - Query design mistakes (SELECT *, correlated subqueries)
   - Performance killers (function on indexed columns, cursors)
   - Data integrity issues (no primary keys, EAV pattern)
   - Security vulnerabilities (SQL injection, plain text passwords)
   - Schema design problems (FLOAT for money, VARCHAR(MAX) everywhere)

### scripts/ Directory

Three Python utility scripts for SQL analysis and documentation:

1. **query_optimizer.py**
   - Analyzes SQL queries and suggests improvements
   - Identifies non-SARGable predicates
   - Detects implicit conversions
   - Recommends index strategies

2. **execution_plan_analyzer.py**
   - Parses XML execution plans
   - Identifies expensive operators
   - Highlights missing indexes
   - Reports on table scans and key lookups

3. **schema_documenter.py**
   - Generates markdown documentation from database schemas
   - Creates entity-relationship diagrams
   - Documents foreign key relationships
   - Identifies missing indexes

**Note:** Python scripts require Python 3.8+ and dependencies listed in each script's header.

---

## Best Practices Summary

**Query Writing:**
- List columns explicitly (no SELECT *)
- Use JOINs instead of correlated subqueries
- Prefer EXISTS over IN for subqueries
- Use UNION ALL unless duplicates must be removed
- Apply functions to non-indexed side of comparisons

**Performance:**
- Index foreign keys
- Create covering indexes for frequent queries
- Use filtered indexes for subsets
- Avoid leading wildcards in LIKE
- Use set-based operations, not cursors

**Data Integrity:**
- Always define primary keys
- Use foreign keys for referential integrity
- Normalize data (avoid delimited lists)
- Use lookup tables instead of flag columns
- Choose appropriate data types (DECIMAL for money, not FLOAT)

**Security:**
- Use parameterized queries always
- Never concatenate user input into SQL
- Hash passwords with bcrypt or PBKDF2
- Grant minimum necessary permissions
- Implement error handling with TRY/CATCH

**Maintenance:**
- Comment complex logic
- Document business rules
- Monitor index usage
- Remove unused indexes
- Track slow queries with DMVs

---

## Example Workflows

### Workflow 1: Optimize a Slow Query

1. **Capture execution plan** with SET STATISTICS IO/TIME ON
2. **Identify bottleneck**: Table scan? Key lookup? High row count?
3. **Check for anti-patterns**: Function on indexed column? Leading wildcard? Cursor?
4. **Apply fix**: Rewrite to be SARGable, add covering index, convert to set-based
5. **Verify improvement**: Re-run with statistics and compare

### Workflow 2: Design New Schema

1. **Identify entities and relationships** (employees, departments, credentials)
2. **Choose primary keys** (INT IDENTITY recommended)
3. **Define foreign keys** for referential integrity
4. **Select data types** (DECIMAL for money, appropriate VARCHAR sizes)
5. **Add constraints** (NOT NULL, CHECK, UNIQUE)
6. **Plan indexes** based on expected query patterns
7. **Review against anti-patterns** (no EAV, no delimited lists)

### Workflow 3: Debug Production Issue

1. **Identify slow query** using DMV diagnostic queries
2. **Analyze execution plan** for expensive operators
3. **Check for missing indexes** using sys.dm_db_missing_index views
4. **Review anti-patterns** (implicit conversions, parameter sniffing)
5. **Apply fix** and test in non-production environment
6. **Monitor performance** after deployment

---

## Getting Started

When you engage this skill, specify your goal:

- **"Optimize this query"** → Execution plan analysis and refactoring
- **"Review this schema"** → Anti-pattern detection and recommendations
- **"How do I..."** → Advanced SQL technique examples
- **"Find employees with expiring credentials"** → HR/education pattern implementation
- **"Why is this slow?"** → Performance troubleshooting workflow

All reference material in `references/` will be loaded into context to inform analysis and provide detailed examples tailored to your specific SQL challenge.

This skill combines 40,000 words of comprehensive SQL documentation with practical, production-ready code examples specifically optimized for educational HR databases.
