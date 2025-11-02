# SQL Query Optimization - Performance Tuning Guide

This guide covers advanced query optimization techniques, execution plan analysis, and indexing strategies to improve SQL query performance by up to 70%.

---

## Table of Contents

1. [Understanding Query Execution](#understanding-query-execution)
2. [Execution Plan Analysis](#execution-plan-analysis)
3. [Indexing Strategies](#indexing-strategies)
4. [Query Refactoring Techniques](#query-refactoring-techniques)
5. [Performance Monitoring](#performance-monitoring)
6. [Common Performance Issues](#common-performance-issues)

---

## Understanding Query Execution

### SQL Query Processing Pipeline

```
SQL Query → Parsing → Optimization → Execution Plan → Execution → Results
```

**Key Phases**:

1. **Parsing**: Syntax validation, object resolution
2. **Optimization**: Cost-based query plan generation
3. **Compilation**: Plan caching for reuse
4. **Execution**: Data retrieval and processing

### Cost-Based Optimization

The query optimizer evaluates multiple execution strategies and selects the plan with the lowest estimated cost based on:

- **Statistics**: Row counts, data distribution, cardinality estimates
- **Indexes**: Available indexes and their selectivity
- **Join algorithms**: Nested loops, hash joins, merge joins
- **Resource availability**: Memory, CPU, I/O capacity

---

## Execution Plan Analysis

### Reading Execution Plans

**SQL Server**:
```sql
-- Enable actual execution plan
SET STATISTICS TIME ON;
SET STATISTICS IO ON;
SET SHOWPLAN_ALL ON;

-- Your query
SELECT * FROM employees e
JOIN departments d ON e.department_id = d.department_id
WHERE e.salary > 50000;

SET SHOWPLAN_ALL OFF;
SET STATISTICS IO OFF;
SET STATISTICS TIME OFF;
```

**PostgreSQL**:
```sql
EXPLAIN ANALYZE
SELECT * FROM employees e
JOIN departments d ON e.department_id = d.department_id
WHERE e.salary > 50000;
```

**MySQL**:
```sql
EXPLAIN FORMAT=JSON
SELECT * FROM employees e
JOIN departments d ON e.department_id = d.department_id
WHERE e.salary > 50000;
```

### Key Execution Plan Operators

#### 1. **Table Scan vs Index Seek**

**Table Scan** (Slow - reads entire table):
```
Table Scan
  Object: [dbo].[employees]
  Estimated Rows: 10,000
  Actual Rows: 10,000
  Cost: 5.2 (HIGH)
```

**Index Seek** (Fast - uses index to find specific rows):
```
Index Seek
  Object: [dbo].[employees].[IX_Salary]
  Seek Predicates: [salary] > 50000
  Estimated Rows: 2,500
  Actual Rows: 2,480
  Cost: 0.3 (LOW)
```

**Action**: Create indexes on columns in WHERE, JOIN, ORDER BY clauses.

#### 2. **Join Types**

**Nested Loops Join** (Best for small datasets):
- Inner table is scanned for each outer table row
- Efficient when: Outer table is small, inner table has index
- Cost: O(n * m)

**Hash Join** (Best for large datasets without indexes):
- Builds hash table from smaller table
- Probes hash table for matches
- Cost: O(n + m)

**Merge Join** (Best for sorted data):
- Both inputs sorted on join key
- Single pass through each input
- Cost: O(n + m)

Example:
```sql
-- Force hash join for large table comparison
SELECT /*+ USE_HASH(e, d) */ *
FROM employees e
JOIN departments d ON e.department_id = d.department_id;
```

#### 3. **Sort Operations**

Sorts are expensive operations indicated by:
```
Sort
  Order By: [employees].[last_name], [employees].[first_name]
  Estimated Rows: 10,000
  Estimated I/O Cost: 2.5
  Estimated CPU Cost: 0.8
```

**Optimization**:
- Create covering index with sort order
- Use EXISTS instead of DISTINCT when possible
- Limit result set before sorting

### Identifying Performance Bottlenecks

**High-Cost Indicators**:
- **Table Scans**: >5% of query cost
- **Sort Operations**: >10% of query cost
- **Hash Matches**: >20% of query cost (large datasets)
- **Key Lookups**: Multiple lookups indicate missing covering index

**Example Analysis**:
```sql
-- Find expensive queries
SELECT TOP 10
    qs.execution_count,
    qs.total_elapsed_time / 1000000 AS total_elapsed_time_sec,
    qs.total_worker_time / 1000000 AS total_worker_time_sec,
    qs.total_logical_reads,
    qs.total_physical_reads,
    SUBSTRING(qt.text, (qs.statement_start_offset/2)+1,
        ((CASE qs.statement_end_offset
            WHEN -1 THEN DATALENGTH(qt.text)
            ELSE qs.statement_end_offset
        END - qs.statement_start_offset)/2) + 1) AS query_text
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) qt
ORDER BY qs.total_elapsed_time DESC;
```

---

## Indexing Strategies

### Index Types

#### 1. **Clustered Index**
- Determines physical row order
- One per table
- Leaf nodes contain actual data

```sql
-- Create clustered index on primary key
CREATE CLUSTERED INDEX IX_Employees_EmployeeID
ON employees (employee_id);
```

#### 2. **Non-Clustered Index**
- Separate structure with pointers to data
- Multiple per table
- Leaf nodes contain key values + row locators

```sql
-- Create non-clustered index on frequently filtered columns
CREATE NONCLUSTERED INDEX IX_Employees_DepartmentSalary
ON employees (department_id, salary)
INCLUDE (first_name, last_name, hire_date);
```

#### 3. **Covering Index**
- Includes all columns needed by query
- Eliminates key lookups
- Significant performance improvement

```sql
-- Covering index for specific query pattern
CREATE NONCLUSTERED INDEX IX_Employees_Covering
ON employees (department_id, status)
INCLUDE (employee_id, first_name, last_name, salary, hire_date);

-- Query uses covering index (no lookups)
SELECT employee_id, first_name, last_name, salary, hire_date
FROM employees
WHERE department_id = 5 AND status = 'Active';
```

#### 4. **Filtered Index**
- Index subset of rows
- Smaller, more efficient
- Ideal for common WHERE conditions

```sql
-- Index only active employees (reduces index size by 80%)
CREATE NONCLUSTERED INDEX IX_Employees_Active
ON employees (hire_date, department_id)
WHERE status = 'Active';
```

#### 5. **Columnstore Index**
- Columnar storage for analytics
- Massive compression (10x-20x)
- Ideal for large fact tables

```sql
-- Create columnstore index for analytical queries
CREATE NONCLUSTERED COLUMNSTORE INDEX IX_EmployeeHistory_Columnstore
ON employee_history (employee_id, transaction_date, transaction_type, amount);
```

### Index Design Best Practices

#### Column Order Matters

**Principle**: Most selective column first (in WHERE clause)

```sql
-- GOOD: Selective column first
CREATE INDEX IX_Employees_StatusDepartment
ON employees (status, department_id);

-- Query benefits from selectivity
SELECT * FROM employees
WHERE status = 'Active'  -- Filters 90% of rows
  AND department_id = 5;  -- Filters remaining 10%

-- POOR: Less selective column first
CREATE INDEX IX_Employees_DepartmentStatus
ON employees (department_id, status);
-- Less efficient because department filters only 5% initially
```

#### INCLUDE Columns for Covering

```sql
-- Query pattern
SELECT employee_id, first_name, last_name, salary
FROM employees
WHERE department_id = 5 AND status = 'Active';

-- Optimal index
CREATE INDEX IX_Employees_DeptStatus_Cover
ON employees (department_id, status)
INCLUDE (first_name, last_name, salary);
-- employee_id included automatically (clustered key)
```

#### Index Maintenance

```sql
-- Find fragmented indexes (>30% fragmentation)
SELECT
    OBJECT_NAME(ips.object_id) AS table_name,
    i.name AS index_name,
    ips.avg_fragmentation_in_percent,
    ips.page_count
FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'LIMITED') ips
JOIN sys.indexes i ON ips.object_id = i.object_id AND ips.index_id = i.index_id
WHERE ips.avg_fragmentation_in_percent > 30
  AND ips.page_count > 1000
ORDER BY ips.avg_fragmentation_in_percent DESC;

-- Rebuild heavily fragmented indexes
ALTER INDEX IX_Employees_DepartmentSalary
ON employees
REBUILD WITH (ONLINE = ON, SORT_IN_TEMPDB = ON);

-- Reorganize moderately fragmented indexes
ALTER INDEX IX_Employees_HireDate
ON employees
REORGANIZE;
```

### Finding Missing Indexes

```sql
-- SQL Server: Missing index recommendations
SELECT
    migs.avg_user_impact AS avg_improvement_pct,
    migs.avg_total_user_cost * (migs.user_seeks + migs.user_scans) AS total_cost,
    migs.user_seeks + migs.user_scans AS total_reads,
    OBJECT_NAME(mid.object_id) AS table_name,
    mid.equality_columns,
    mid.inequality_columns,
    mid.included_columns,
    'CREATE NONCLUSTERED INDEX IX_' + OBJECT_NAME(mid.object_id) + '_Missing'
        + ' ON ' + mid.statement
        + ' (' + ISNULL(mid.equality_columns, '') + ISNULL(mid.inequality_columns, '') + ')'
        + CASE WHEN mid.included_columns IS NOT NULL
            THEN ' INCLUDE (' + mid.included_columns + ')'
            ELSE ''
        END AS create_statement
FROM sys.dm_db_missing_index_group_stats migs
JOIN sys.dm_db_missing_index_groups mig ON migs.group_handle = mig.index_group_handle
JOIN sys.dm_db_missing_index_details mid ON mig.index_handle = mid.index_handle
WHERE migs.avg_user_impact > 50  -- Focus on high-impact indexes
  AND migs.user_seeks + migs.user_scans > 100  -- Frequently used
ORDER BY total_cost DESC;
```

### Index Anti-Patterns

#### 1. **Over-Indexing**

**Problem**: Too many indexes slow down INSERT/UPDATE/DELETE

```sql
-- BAD: Redundant indexes
CREATE INDEX IX_Emp_Dept ON employees (department_id);
CREATE INDEX IX_Emp_DeptStatus ON employees (department_id, status);
CREATE INDEX IX_Emp_DeptStatusSalary ON employees (department_id, status, salary);
-- First two are redundant! Third index covers all scenarios.

-- GOOD: Single optimal index
CREATE INDEX IX_Emp_DeptStatusSalary ON employees (department_id, status, salary);
```

#### 2. **Wrong Column Order**

```sql
-- BAD: Non-selective column first
CREATE INDEX IX_Emp_StatusDept ON employees (status, department_id);
-- If status has 2 values (Active/Inactive), not selective

-- GOOD: Selective column first
CREATE INDEX IX_Emp_DeptStatus ON employees (department_id, status);
-- department_id has 50 values, much more selective
```

#### 3. **Missing INCLUDE Columns**

```sql
-- BAD: Forces key lookup
CREATE INDEX IX_Emp_Dept ON employees (department_id);

SELECT employee_id, first_name, last_name, salary
FROM employees
WHERE department_id = 5;
-- Requires key lookup for first_name, last_name, salary

-- GOOD: Covering index
CREATE INDEX IX_Emp_Dept ON employees (department_id)
INCLUDE (first_name, last_name, salary);
-- All columns in index, no lookup needed
```

---

## Query Refactoring Techniques

### 1. Eliminate Unnecessary DISTINCT

```sql
-- BEFORE: Expensive DISTINCT operation
SELECT DISTINCT e.employee_id, e.first_name, e.last_name
FROM employees e
JOIN departments d ON e.department_id = d.department_id;
-- DISTINCT forces sort if duplicate rows possible

-- AFTER: Use EXISTS to prevent duplicates
SELECT e.employee_id, e.first_name, e.last_name
FROM employees e
WHERE EXISTS (
    SELECT 1 FROM departments d WHERE d.department_id = e.department_id
);
-- No sort needed, faster execution
```

### 2. Replace Cursors with Set-Based Operations

```sql
-- BEFORE: Cursor-based update (SLOW)
DECLARE @EmployeeID INT;
DECLARE emp_cursor CURSOR FOR
    SELECT employee_id FROM employees WHERE status = 'Active';

OPEN emp_cursor;
FETCH NEXT FROM emp_cursor INTO @EmployeeID;

WHILE @@FETCH_STATUS = 0
BEGIN
    UPDATE employee_metrics
    SET last_login_date = (
        SELECT MAX(login_date)
        FROM user_activity
        WHERE employee_id = @EmployeeID
    )
    WHERE employee_id = @EmployeeID;

    FETCH NEXT FROM emp_cursor INTO @EmployeeID;
END;

CLOSE emp_cursor;
DEALLOCATE emp_cursor;

-- AFTER: Set-based update (FAST - 100x faster)
UPDATE em
SET em.last_login_date = ua.max_login_date
FROM employee_metrics em
JOIN (
    SELECT employee_id, MAX(login_date) AS max_login_date
    FROM user_activity
    GROUP BY employee_id
) ua ON em.employee_id = ua.employee_id
WHERE em.employee_id IN (
    SELECT employee_id FROM employees WHERE status = 'Active'
);
```

### 3. Optimize Subqueries

```sql
-- BEFORE: Correlated subquery (executes per row)
SELECT
    e.employee_id,
    e.first_name,
    e.last_name,
    (SELECT COUNT(*) FROM credentials WHERE employee_id = e.employee_id) AS credential_count,
    (SELECT MAX(expiration_date) FROM credentials WHERE employee_id = e.employee_id) AS latest_expiration
FROM employees e;
-- Credentials table scanned once per employee!

-- AFTER: Single join with aggregation (executes once)
SELECT
    e.employee_id,
    e.first_name,
    e.last_name,
    COUNT(c.credential_id) AS credential_count,
    MAX(c.expiration_date) AS latest_expiration
FROM employees e
LEFT JOIN credentials c ON e.employee_id = c.employee_id
GROUP BY e.employee_id, e.first_name, e.last_name;
-- Credentials table scanned once total!
```

### 4. Use EXISTS Instead of IN

```sql
-- BEFORE: IN with subquery (slower for large result sets)
SELECT *
FROM employees e
WHERE e.employee_id IN (
    SELECT employee_id
    FROM credentials
    WHERE expiration_date < GETDATE()
);
-- Subquery fully materialized

-- AFTER: EXISTS (short-circuits after first match)
SELECT *
FROM employees e
WHERE EXISTS (
    SELECT 1
    FROM credentials c
    WHERE c.employee_id = e.employee_id
      AND c.expiration_date < GETDATE()
);
-- Stops searching after first match found
```

### 5. Partition Large Queries

```sql
-- BEFORE: Single massive query
SELECT *
FROM employee_history
WHERE transaction_date BETWEEN '2020-01-01' AND '2024-12-31';
-- Scans 5 years of data (billions of rows)

-- AFTER: Partition by year using UNION ALL
SELECT * FROM employee_history_2024 WHERE transaction_date >= '2024-01-01'
UNION ALL
SELECT * FROM employee_history_2023
UNION ALL
SELECT * FROM employee_history_2022
UNION ALL
SELECT * FROM employee_history_2021
WHERE transaction_date < '2022-01-01';
-- Each partition smaller, faster, potentially parallel execution
```

### 6. Avoid Functions on Indexed Columns

```sql
-- BEFORE: Function prevents index usage
SELECT *
FROM employees
WHERE YEAR(hire_date) = 2024;
-- hire_date index NOT used (function applied to column)

-- AFTER: Compare to date range
SELECT *
FROM employees
WHERE hire_date >= '2024-01-01'
  AND hire_date < '2025-01-01';
-- hire_date index USED efficiently
```

### 7. Use UNION ALL Instead of UNION

```sql
-- BEFORE: UNION removes duplicates (requires sort)
SELECT employee_id, first_name FROM employees WHERE department_id = 1
UNION
SELECT employee_id, first_name FROM employees WHERE department_id = 2;
-- Implicitly adds DISTINCT (expensive sort operation)

-- AFTER: UNION ALL keeps duplicates (no sort)
SELECT employee_id, first_name FROM employees WHERE department_id = 1
UNION ALL
SELECT employee_id, first_name FROM employees WHERE department_id = 2;
-- No sort needed, 2-3x faster
```

---

## Performance Monitoring

### Key Metrics to Track

#### 1. **Query Execution Time**

```sql
-- Enable timing statistics
SET STATISTICS TIME ON;

SELECT * FROM large_table WHERE condition;

-- Output:
-- SQL Server Execution Times:
--    CPU time = 1250 ms,  elapsed time = 3420 ms.

SET STATISTICS TIME OFF;
```

#### 2. **Logical and Physical Reads**

```sql
SET STATISTICS IO ON;

SELECT * FROM employees WHERE department_id = 5;

-- Output:
-- Table 'employees'. Scan count 1, logical reads 250, physical reads 0

SET STATISTICS IO OFF;
```

**Interpretation**:
- **Logical reads**: Pages read from buffer cache (memory)
- **Physical reads**: Pages read from disk (slow!)
- **Goal**: Minimize physical reads through proper indexing

#### 3. **Wait Statistics**

```sql
-- Identify wait types causing delays
SELECT
    wait_type,
    waiting_tasks_count,
    wait_time_ms,
    max_wait_time_ms,
    signal_wait_time_ms
FROM sys.dm_os_wait_stats
WHERE wait_type NOT IN (
    'CLR_SEMAPHORE', 'LAZYWRITER_SLEEP', 'RESOURCE_QUEUE',
    'SLEEP_TASK', 'SLEEP_SYSTEMTASK', 'SQLTRACE_BUFFER_FLUSH', 'WAITFOR'
)
ORDER BY wait_time_ms DESC;
```

**Common Wait Types**:
- **LCK_M_X**: Lock waits (blocking/deadlocks)
- **PAGEIOLATCH_SH**: Disk I/O waits (missing indexes, insufficient memory)
- **CXPACKET**: Parallelism coordination (consider MAXDOP tuning)
- **SOS_SCHEDULER_YIELD**: CPU pressure (query optimization needed)

### Query Performance Baseline

```sql
-- Create performance baseline
CREATE TABLE query_performance_baseline (
    query_id INT IDENTITY(1,1) PRIMARY KEY,
    query_text NVARCHAR(MAX),
    avg_execution_time_ms INT,
    avg_logical_reads INT,
    execution_count INT,
    baseline_date DATETIME DEFAULT GETDATE()
);

-- Capture baseline from query stats
INSERT INTO query_performance_baseline (query_text, avg_execution_time_ms, avg_logical_reads, execution_count)
SELECT TOP 100
    SUBSTRING(qt.text, 1, 500) AS query_text,
    qs.total_elapsed_time / qs.execution_count / 1000 AS avg_execution_time_ms,
    qs.total_logical_reads / qs.execution_count AS avg_logical_reads,
    qs.execution_count
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) qt
WHERE qs.execution_count > 10
ORDER BY qs.total_elapsed_time / qs.execution_count DESC;
```

---

## Common Performance Issues

### Issue 1: Parameter Sniffing

**Problem**: Cached plan optimized for first parameter value performs poorly for others.

```sql
-- Stored procedure with parameter sniffing issue
CREATE PROCEDURE GetEmployeesByDepartment
    @DepartmentID INT
AS
BEGIN
    SELECT * FROM employees WHERE department_id = @DepartmentID;
END;
GO

-- First call: dept 1 has 5 employees (index seek plan cached)
EXEC GetEmployeesByDepartment @DepartmentID = 1;  -- Fast (0.1s)

-- Second call: dept 5 has 5000 employees (same index seek plan, slow!)
EXEC GetEmployeesByDepartment @DepartmentID = 5;  -- Slow (5s)
```

**Solutions**:

**Option 1**: OPTIMIZE FOR UNKNOWN hint
```sql
ALTER PROCEDURE GetEmployeesByDepartment
    @DepartmentID INT
AS
BEGIN
    SELECT * FROM employees WHERE department_id = @DepartmentID
    OPTION (OPTIMIZE FOR UNKNOWN);
END;
```

**Option 2**: RECOMPILE hint
```sql
ALTER PROCEDURE GetEmployeesByDepartment
    @DepartmentID INT
AS
BEGIN
    SELECT * FROM employees WHERE department_id = @DepartmentID
    OPTION (RECOMPILE);
END;
```

### Issue 2: Implicit Conversions

**Problem**: Data type mismatch prevents index usage.

```sql
-- employees.employee_id is INT, but parameter is VARCHAR
DECLARE @EmpID VARCHAR(10) = '12345';

SELECT * FROM employees WHERE employee_id = @EmpID;
-- Implicit conversion: CAST(employee_id AS VARCHAR) = @EmpID
-- Index on employee_id NOT used!
```

**Solution**: Match data types
```sql
DECLARE @EmpID INT = 12345;

SELECT * FROM employees WHERE employee_id = @EmpID;
-- No conversion needed, index used efficiently
```

### Issue 3: SELECT * Anti-Pattern

**Problem**: Retrieves unnecessary columns, prevents covering indexes.

```sql
-- BAD: Retrieves all columns
SELECT * FROM employees WHERE department_id = 5;
-- Cannot use covering index, requires key lookups

-- GOOD: Only needed columns
SELECT employee_id, first_name, last_name, hire_date
FROM employees WHERE department_id = 5;
-- Can use covering index: (department_id) INCLUDE (employee_id, first_name, last_name, hire_date)
```

### Issue 4: N+1 Query Problem

**Problem**: Multiple round-trips to database instead of batch operation.

```sql
-- BAD: N+1 queries (application code pattern)
-- Query 1: Get departments
SELECT department_id FROM departments;

-- Query 2-N: Get employees for each department (N separate queries)
FOR EACH department_id:
    SELECT * FROM employees WHERE department_id = ?;
```

**Solution**: Single batch query
```sql
-- GOOD: Single query with JOIN
SELECT
    d.department_id,
    d.department_name,
    e.employee_id,
    e.first_name,
    e.last_name
FROM departments d
LEFT JOIN employees e ON d.department_id = e.department_id
ORDER BY d.department_id, e.employee_id;
```

---

## Performance Tuning Checklist

### Before Optimization
- [ ] Capture baseline metrics (execution time, reads, CPU)
- [ ] Enable execution plans and statistics
- [ ] Identify high-cost operations (>10% of total cost)

### Index Optimization
- [ ] Create indexes on WHERE clause columns
- [ ] Create indexes on JOIN columns
- [ ] Add INCLUDE columns for covering indexes
- [ ] Use filtered indexes for common WHERE conditions
- [ ] Remove redundant/unused indexes

### Query Refactoring
- [ ] Replace cursors with set-based operations
- [ ] Optimize correlated subqueries
- [ ] Use EXISTS instead of IN for large result sets
- [ ] Avoid functions on indexed columns
- [ ] Use UNION ALL instead of UNION when possible
- [ ] Replace DISTINCT with EXISTS when appropriate

### Code Review
- [ ] Match parameter data types to column data types
- [ ] Select only needed columns (avoid SELECT *)
- [ ] Implement proper error handling
- [ ] Add NOLOCK hints only when appropriate (read uncommitted)

### Testing & Validation
- [ ] Test with production-size datasets
- [ ] Compare before/after execution plans
- [ ] Validate result accuracy
- [ ] Monitor for regression after deployment

---

## Tools & Resources

### SQL Server
- **SQL Server Management Studio (SSMS)**: Execution plan analysis
- **Database Engine Tuning Advisor**: Index recommendations
- **SQL Server Profiler**: Query tracing and analysis
- **Extended Events**: Lightweight monitoring
- **DMVs**: sys.dm_exec_query_stats, sys.dm_db_missing_index_*

### PostgreSQL
- **EXPLAIN ANALYZE**: Execution plan with actual costs
- **pg_stat_statements**: Query performance statistics
- **pgBadger**: Log analyzer for slow queries
- **auto_explain**: Automatic explain plan logging

### MySQL
- **EXPLAIN FORMAT=JSON**: Detailed execution plans
- **MySQL Workbench**: Visual explain and profiling
- **Performance Schema**: Query instrumentation
- **Slow Query Log**: Identify problematic queries

---

## Summary

**Key Principles**:
1. **Measure before optimizing**: Baseline metrics are essential
2. **Focus on high-impact queries**: 80/20 rule applies
3. **Index strategically**: Right columns in right order
4. **Think set-based**: Avoid row-by-row processing
5. **Test with production data**: Small datasets hide problems

**Expected Improvements**:
- Proper indexing: **50-70% faster queries**
- Query refactoring: **2-10x performance gain**
- Eliminating cursors: **10-100x improvement**
- Set-based operations: **Predictable, scalable performance**

For practical SQL patterns, see `hr_education_patterns.md`.
For mistakes to avoid, see `sql_antipatterns.md`.
For advanced techniques, see `advanced_techniques.md`.
