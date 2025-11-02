# SQL Anti-Patterns and Common Mistakes

This reference documents common SQL anti-patterns, mistakes, and bad practices to avoid, with explanations of why they're problematic and how to fix them. Each anti-pattern includes a "bad" example showing the problem and a "good" example showing the correct approach.

## Table of Contents

1. [Query Design Anti-Patterns](#query-design-anti-patterns)
2. [Performance Anti-Patterns](#performance-anti-patterns)
3. [Data Integrity Anti-Patterns](#data-integrity-anti-patterns)
4. [Security Anti-Patterns](#security-anti-patterns)
5. [Schema Design Anti-Patterns](#schema-design-anti-patterns)
6. [Maintenance Anti-Patterns](#maintenance-anti-patterns)

---

## Query Design Anti-Patterns

### Anti-Pattern 1: SELECT * (SELECT Star)

**Problem**: Using `SELECT *` returns all columns, even those not needed, wasting network bandwidth and memory. It also breaks when columns are added/removed from tables.

**Bad Example**:
```sql
-- Returns all columns, even if only need a few
SELECT *
FROM employees e
INNER JOIN departments d ON e.department_id = d.department_id
WHERE e.status = 'Active';
```

**Good Example**:
```sql
-- Explicitly list only needed columns
SELECT
    e.employee_id,
    e.first_name,
    e.last_name,
    e.email,
    d.department_name
FROM employees e
INNER JOIN departments d ON e.department_id = d.department_id
WHERE e.status = 'Active';
```

**Why It Matters**:
- Performance: Transferring unnecessary data wastes bandwidth (10-100x more data)
- Maintenance: Code breaks when table structure changes
- Covering indexes: Can't use covering indexes effectively
- Memory: Larger result sets consume more memory

**Exceptions**:
- Quick ad-hoc queries for exploration
- INSERT INTO...SELECT * for table copies (same structure)

---

### Anti-Pattern 2: Implicit Column Lists in INSERT

**Problem**: INSERT statements without column lists break when table structure changes.

**Bad Example**:
```sql
-- Implicit column order - breaks if columns are added/reordered
INSERT INTO employees
VALUES (12345, 'John', 'Doe', 'john.doe@example.com', '555-1234', '2025-01-15', 'Active', 50000);
```

**Good Example**:
```sql
-- Explicit column list - resilient to schema changes
INSERT INTO employees (
    employee_id,
    first_name,
    last_name,
    email,
    phone,
    hire_date,
    status,
    salary
)
VALUES (
    12345,
    'John',
    'Doe',
    'john.doe@example.com',
    '555-1234',
    '2025-01-15',
    'Active',
    50000
);
```

**Why It Matters**:
- Schema changes break implicit inserts
- Clarity: Column names document what each value represents
- Defaults: Can omit columns with defaults or NULL
- Reordering: Column order in table definition can change

---

### Anti-Pattern 3: OR in JOIN Conditions

**Problem**: Using OR in JOIN conditions often indicates flawed logic and kills performance.

**Bad Example**:
```sql
-- Confusing logic, terrible performance
SELECT
    e.employee_id,
    e.first_name,
    e.last_name,
    c.credential_type
FROM employees e
LEFT JOIN credentials c ON e.employee_id = c.employee_id
                        OR e.email = c.email_used  -- WRONG!
WHERE e.status = 'Active';
```

**Good Example**:
```sql
-- Separate JOINs or UNION for multiple join paths
SELECT
    e.employee_id,
    e.first_name,
    e.last_name,
    c.credential_type,
    'By ID' AS match_method
FROM employees e
LEFT JOIN credentials c ON e.employee_id = c.employee_id
WHERE e.status = 'Active'

UNION ALL

SELECT
    e.employee_id,
    e.first_name,
    e.last_name,
    c.credential_type,
    'By Email' AS match_method
FROM employees e
LEFT JOIN credentials c ON e.email = c.email_used
                        AND NOT EXISTS (
                            SELECT 1
                            FROM credentials c2
                            WHERE c2.employee_id = e.employee_id
                        )
WHERE e.status = 'Active';
```

**Why It Matters**:
- Performance: OR in JOIN prevents index usage (10-100x slower)
- Semantics: Usually indicates confused logic
- Duplicates: Can create unexpected duplicate rows
- Indexing: Optimizer can't use indexes efficiently

---

### Anti-Pattern 4: Correlated Subqueries in SELECT

**Problem**: Correlated subqueries in SELECT list execute once per row, causing N+1 query problem.

**Bad Example**:
```sql
-- Subquery executes for EVERY row (N+1 problem)
SELECT
    e.employee_id,
    e.first_name,
    e.last_name,
    (SELECT COUNT(*)
     FROM credentials c
     WHERE c.employee_id = e.employee_id) AS credential_count,
    (SELECT MAX(c.expiration_date)
     FROM credentials c
     WHERE c.employee_id = e.employee_id) AS next_expiration
FROM employees e
WHERE e.status = 'Active';
```

**Good Example**:
```sql
-- Use JOINs or window functions instead
WITH CredentialStats AS (
    SELECT
        employee_id,
        COUNT(*) AS credential_count,
        MAX(expiration_date) AS next_expiration
    FROM credentials
    GROUP BY employee_id
)
SELECT
    e.employee_id,
    e.first_name,
    e.last_name,
    ISNULL(cs.credential_count, 0) AS credential_count,
    cs.next_expiration
FROM employees e
LEFT JOIN CredentialStats cs ON e.employee_id = cs.employee_id
WHERE e.status = 'Active';
```

**Why It Matters**:
- Performance: 10-1000x slower with correlated subqueries
- Scalability: Query time grows linearly with row count
- Resource usage: High CPU and I/O consumption
- Execution plans: Harder to optimize

**Measured Impact**: 1,000 rows = 1,000 subquery executions vs 1 JOIN

---

### Anti-Pattern 5: NOT IN with NULLs

**Problem**: `NOT IN` returns no results if the subquery contains any NULL values.

**Bad Example**:
```sql
-- Returns NO rows if any manager_id is NULL (unexpected!)
SELECT employee_id, first_name, last_name
FROM employees
WHERE employee_id NOT IN (
    SELECT manager_id
    FROM employees
);
```

**Good Example**:
```sql
-- Use NOT EXISTS instead (NULL-safe)
SELECT employee_id, first_name, last_name
FROM employees e
WHERE NOT EXISTS (
    SELECT 1
    FROM employees e2
    WHERE e2.manager_id = e.employee_id
);

-- Or use LEFT JOIN with NULL check
SELECT e.employee_id, e.first_name, e.last_name
FROM employees e
LEFT JOIN employees managed ON managed.manager_id = e.employee_id
WHERE managed.manager_id IS NULL;
```

**Why It Matters**:
- Logic error: Produces incorrect results silently
- NULL handling: NOT IN (NULL) evaluates to unknown, filtering all rows
- Debugging: Hard to spot why query returns no results
- Best practice: Use NOT EXISTS for negation

**Rule of Thumb**: Never use `NOT IN` with subqueries; always use `NOT EXISTS`

---

## Performance Anti-Patterns

### Anti-Pattern 6: Function Calls on Indexed Columns

**Problem**: Applying functions to indexed columns in WHERE prevents index usage.

**Bad Example**:
```sql
-- Index on hire_date cannot be used!
SELECT employee_id, first_name, last_name, hire_date
FROM employees
WHERE YEAR(hire_date) = 2024;

-- Index on email cannot be used!
SELECT employee_id, email
FROM employees
WHERE UPPER(email) = 'JOHN.DOE@EXAMPLE.COM';
```

**Good Example**:
```sql
-- Range comparison uses index effectively
SELECT employee_id, first_name, last_name, hire_date
FROM employees
WHERE hire_date >= '2024-01-01'
  AND hire_date < '2025-01-01';

-- Store uppercase version or use case-insensitive collation
-- Option 1: Computed column with index
ALTER TABLE employees
ADD email_upper AS UPPER(email) PERSISTED;

CREATE INDEX IX_employees_email_upper ON employees(email_upper);

SELECT employee_id, email
FROM employees
WHERE email_upper = 'JOHN.DOE@EXAMPLE.COM';

-- Option 2: Use case-insensitive comparison
SELECT employee_id, email
FROM employees
WHERE email = 'john.doe@example.com' COLLATE SQL_Latin1_General_CP1_CI_AS;
```

**Why It Matters**:
- Performance: Index scans instead of seeks (10-100x slower)
- SARGability: Non-SARGable queries can't use indexes
- Scalability: Performance degrades with table growth
- CPU usage: Function calls add computational overhead

**Common Function Offenders**: YEAR(), MONTH(), UPPER(), LOWER(), SUBSTRING(), DATEPART(), CONVERT()

---

### Anti-Pattern 7: Leading Wildcards in LIKE

**Problem**: LIKE with leading wildcard prevents index usage and forces full table scan.

**Bad Example**:
```sql
-- Leading wildcard = full table scan
SELECT employee_id, last_name, first_name
FROM employees
WHERE last_name LIKE '%son';

-- Bi-directional wildcards are even worse
SELECT employee_id, email
FROM employees
WHERE email LIKE '%example%';
```

**Good Example**:
```sql
-- Trailing wildcard can use index
SELECT employee_id, last_name, first_name
FROM employees
WHERE last_name LIKE 'John%';

-- For full-text search needs, use Full-Text Search
CREATE FULLTEXT INDEX ON employees(last_name, first_name, email)
KEY INDEX PK_employees;

SELECT employee_id, last_name, first_name
FROM employees
WHERE CONTAINS((last_name, first_name), 'son');
```

**Why It Matters**:
- Performance: Full table scans on large tables (100-1000x slower)
- Index usage: Leading wildcards prevent index seeks
- Scalability: Query time grows linearly with table size
- Alternative solutions: Full-text search for substring matching

**Performance Impact**: 10 million rows, indexed column:
- `LIKE 'John%'`: 0.01 seconds (index seek)
- `LIKE '%son'`: 45 seconds (full table scan)

---

### Anti-Pattern 8: DISTINCT as a Band-Aid

**Problem**: Using DISTINCT to hide duplicate rows instead of fixing the root cause (usually a JOIN problem).

**Bad Example**:
```sql
-- DISTINCT hides duplicate problem instead of fixing it
SELECT DISTINCT
    e.employee_id,
    e.first_name,
    e.last_name,
    d.department_name
FROM employees e
INNER JOIN departments d ON e.department_id = d.department_id
INNER JOIN employee_assignments ea ON e.employee_id = ea.employee_id;
-- Problem: Multiple assignments create duplicates!
```

**Good Example**:
```sql
-- Fix the root cause: Get most recent assignment only
WITH CurrentAssignment AS (
    SELECT
        employee_id,
        department_id,
        ROW_NUMBER() OVER (
            PARTITION BY employee_id
            ORDER BY assignment_start_date DESC
        ) AS rn
    FROM employee_assignments
    WHERE assignment_end_date IS NULL OR assignment_end_date > GETDATE()
)
SELECT
    e.employee_id,
    e.first_name,
    e.last_name,
    d.department_name
FROM employees e
INNER JOIN CurrentAssignment ca ON e.employee_id = ca.employee_id AND ca.rn = 1
INNER JOIN departments d ON ca.department_id = d.department_id;
```

**Why It Matters**:
- Root cause: Hides underlying data quality issues
- Performance: DISTINCT adds sorting/grouping overhead
- Semantics: Often indicates incorrect JOIN logic
- Data quality: Masking duplicates prevents fixing the real problem

**When DISTINCT is OK**:
- Intentional union of multiple sources
- Explicit deduplication requirement
- Aggregation prevention (GROUP BY alternative)

---

### Anti-Pattern 9: UNION instead of UNION ALL

**Problem**: Using UNION when duplicates don't exist adds unnecessary DISTINCT overhead.

**Bad Example**:
```sql
-- UNION automatically removes duplicates (expensive!)
SELECT employee_id, 'Full-Time' AS employment_type
FROM full_time_employees

UNION  -- Adds DISTINCT operation

SELECT employee_id, 'Part-Time' AS employment_type
FROM part_time_employees;
```

**Good Example**:
```sql
-- UNION ALL when you know there are no duplicates
SELECT employee_id, 'Full-Time' AS employment_type
FROM full_time_employees

UNION ALL  -- No deduplication needed

SELECT employee_id, 'Part-Time' AS employment_type
FROM part_time_employees;
```

**Why It Matters**:
- Performance: UNION adds implicit DISTINCT (sorting overhead)
- Memory: Requires additional memory for deduplication
- CPU: Extra processing for comparison operations
- Scalability: Overhead increases with result set size

**Performance Impact**: 100,000 rows:
- UNION: 5 seconds (with sorting/deduplication)
- UNION ALL: 0.5 seconds (no overhead)

**Rule of Thumb**: Use UNION ALL by default; only use UNION if duplicates must be removed

---

### Anti-Pattern 10: Cursor Loops Instead of Set-Based Operations

**Problem**: Using cursors for row-by-row processing instead of set-based operations.

**Bad Example**:
```sql
-- Cursor approach: Processes one row at a time (SLOW!)
DECLARE @employee_id INT, @salary DECIMAL(10,2);

DECLARE salary_cursor CURSOR FOR
    SELECT employee_id, salary
    FROM employees
    WHERE status = 'Active';

OPEN salary_cursor;
FETCH NEXT FROM salary_cursor INTO @employee_id, @salary;

WHILE @@FETCH_STATUS = 0
BEGIN
    -- Update one row at a time
    UPDATE employees
    SET salary = salary * 1.03  -- 3% raise
    WHERE employee_id = @employee_id;

    FETCH NEXT FROM salary_cursor INTO @employee_id, @salary;
END;

CLOSE salary_cursor;
DEALLOCATE salary_cursor;
```

**Good Example**:
```sql
-- Set-based approach: Processes all rows at once (FAST!)
UPDATE employees
SET salary = salary * 1.03  -- 3% raise
WHERE status = 'Active';
```

**Why It Matters**:
- Performance: Set-based is 10-100x faster
- Resources: Cursors hold locks longer, blocking other queries
- Maintenance: More code to maintain
- Scalability: Cursor overhead grows linearly with row count

**Performance Comparison**: 10,000 employees:
- Cursor: 45 seconds (10,000 separate updates)
- Set-based: 0.5 seconds (single update statement)

**When Cursors Are OK**:
- Complex business logic that truly requires row-by-row processing
- Calling stored procedures per row (last resort)
- Administrative tasks with explicit delays

---

### Anti-Pattern 11: Implicit Data Type Conversion

**Problem**: Mixing data types forces SQL Server to convert values, preventing index usage.

**Bad Example**:
```sql
-- employee_id is INT, but passing VARCHAR
SELECT employee_id, first_name, last_name
FROM employees
WHERE employee_id = '12345';  -- Implicit conversion!

-- phone is VARCHAR, comparing to INT
SELECT employee_id, phone
FROM employees
WHERE phone = 5551234;  -- Implicit conversion!

-- hire_date is DATE, but using VARCHAR
SELECT employee_id, hire_date
FROM employees
WHERE hire_date = '10/25/2024';  -- Ambiguous format!
```

**Good Example**:
```sql
-- Use correct data types
SELECT employee_id, first_name, last_name
FROM employees
WHERE employee_id = 12345;  -- INT literal

SELECT employee_id, phone
FROM employees
WHERE phone = '555-1234';  -- VARCHAR literal

-- Use ISO 8601 date format (unambiguous)
SELECT employee_id, hire_date
FROM employees
WHERE hire_date = '2024-10-25';  -- YYYY-MM-DD
```

**Why It Matters**:
- Performance: Implicit conversion prevents index seeks
- Data quality: Conversion errors can cause runtime failures
- Regional settings: Date/number formats vary by locale
- Maintenance: Hard to spot implicit conversions

**Finding Implicit Conversions**:
```sql
-- Check execution plan for CONVERT_IMPLICIT warnings
SET STATISTICS XML ON;
-- Run your query
-- Look for <Warnings><ColumnsWithNoStatistics>CONVERT_IMPLICIT</ColumnsWithNoStatistics></Warnings>
```

---

## Data Integrity Anti-Patterns

### Anti-Pattern 12: Using Flags Instead of Lookup Tables

**Problem**: Using flag columns (Y/N, 0/1) instead of proper foreign keys to lookup tables.

**Bad Example**:
```sql
-- Multiple flag columns = maintenance nightmare
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    first_name NVARCHAR(50),
    last_name NVARCHAR(50),
    is_full_time CHAR(1),      -- Y/N
    is_exempt CHAR(1),          -- Y/N
    is_union_member CHAR(1),    -- Y/N
    is_active CHAR(1),          -- Y/N
    has_benefits CHAR(1)        -- Y/N
);

-- Query becomes messy
SELECT *
FROM employees
WHERE is_full_time = 'Y'
  AND is_exempt = 'N'
  AND is_union_member = 'Y'
  AND is_active = 'Y';
```

**Good Example**:
```sql
-- Proper lookup tables with referential integrity
CREATE TABLE employment_types (
    employment_type_id INT PRIMARY KEY,
    employment_type_name NVARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE employee_status (
    status_id INT PRIMARY KEY,
    status_name NVARCHAR(50) NOT NULL UNIQUE,
    is_active BIT DEFAULT 1
);

CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    first_name NVARCHAR(50),
    last_name NVARCHAR(50),
    employment_type_id INT NOT NULL
        FOREIGN KEY REFERENCES employment_types(employment_type_id),
    status_id INT NOT NULL
        FOREIGN KEY REFERENCES employee_status(status_id),
    is_exempt BIT NOT NULL DEFAULT 0,
    is_union_member BIT NOT NULL DEFAULT 0
);

-- Query is clearer and type-safe
SELECT e.*
FROM employees e
INNER JOIN employment_types et ON e.employment_type_id = et.employment_type_id
INNER JOIN employee_status es ON e.status_id = es.status_id
WHERE et.employment_type_name = 'Full-Time'
  AND e.is_exempt = 0
  AND e.is_union_member = 1
  AND es.is_active = 1;
```

**Why It Matters**:
- Data integrity: Foreign keys enforce valid values
- Extensibility: Adding new types doesn't require schema changes
- Reporting: Easier to add descriptions and metadata
- Maintenance: Centralized type management

**When Simple Flags Are OK**:
- True binary states (is_deleted, is_active)
- Performance-critical columns (no JOIN needed)
- Flags that will never expand to multiple values

---

### Anti-Pattern 13: Storing Delimited Lists in Columns

**Problem**: Storing comma-separated values or JSON in a single column violates first normal form.

**Bad Example**:
```sql
-- Comma-separated credentials (denormalized)
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    first_name NVARCHAR(50),
    last_name NVARCHAR(50),
    credential_list VARCHAR(500)  -- 'MATH-001,ENG-002,SPED-003'
);

-- Queries are painful
SELECT *
FROM employees
WHERE credential_list LIKE '%MATH-001%';  -- No index usage!

-- Can't enforce referential integrity
-- Can't prevent duplicates
-- Can't easily count credentials per employee
```

**Good Example**:
```sql
-- Proper many-to-many relationship
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    first_name NVARCHAR(50),
    last_name NVARCHAR(50)
);

CREATE TABLE credentials (
    credential_id INT PRIMARY KEY,
    credential_code NVARCHAR(20) NOT NULL UNIQUE,
    credential_name NVARCHAR(100) NOT NULL
);

CREATE TABLE employee_credentials (
    employee_id INT NOT NULL
        FOREIGN KEY REFERENCES employees(employee_id),
    credential_id INT NOT NULL
        FOREIGN KEY REFERENCES credentials(credential_id),
    issue_date DATE,
    expiration_date DATE,
    PRIMARY KEY (employee_id, credential_id)
);

-- Queries are efficient and accurate
SELECT e.employee_id, e.first_name, e.last_name
FROM employees e
INNER JOIN employee_credentials ec ON e.employee_id = ec.employee_id
INNER JOIN credentials c ON ec.credential_id = c.credential_id
WHERE c.credential_code = 'MATH-001';

-- Easy to count credentials
SELECT e.employee_id, COUNT(*) AS credential_count
FROM employees e
INNER JOIN employee_credentials ec ON e.employee_id = ec.employee_id
GROUP BY e.employee_id;
```

**Why It Matters**:
- Data integrity: Can't enforce foreign keys on delimited values
- Performance: LIKE queries can't use indexes
- Querying: Complex string parsing required
- Normalization: Violates first normal form

**Modern Exception**: JSON columns are acceptable for document storage when:
- Data is truly hierarchical/nested
- Schema is dynamic or varies per row
- Using JSON querying capabilities (SQL Server 2016+, PostgreSQL, MySQL 5.7+)

---

### Anti-Pattern 14: No Primary Keys

**Problem**: Tables without primary keys lead to duplicate rows and poor performance.

**Bad Example**:
```sql
-- No primary key = duplicate nightmares
CREATE TABLE employee_assignments (
    employee_id INT,
    department_id INT,
    assignment_start_date DATE,
    assignment_end_date DATE
);

-- Can insert duplicates accidentally!
INSERT INTO employee_assignments VALUES (12345, 10, '2025-01-01', NULL);
INSERT INTO employee_assignments VALUES (12345, 10, '2025-01-01', NULL);  -- Duplicate!

-- No efficient way to update a specific row
-- No foreign keys can reference this table
```

**Good Example**:
```sql
-- Proper primary key ensures uniqueness
CREATE TABLE employee_assignments (
    assignment_id INT IDENTITY(1,1) PRIMARY KEY,  -- Surrogate key
    employee_id INT NOT NULL,
    department_id INT NOT NULL,
    assignment_start_date DATE NOT NULL,
    assignment_end_date DATE,
    -- Natural key as unique constraint
    CONSTRAINT UQ_employee_dept_date UNIQUE (employee_id, department_id, assignment_start_date)
);

-- Duplicates prevented by constraints
-- Efficient updates/deletes by assignment_id
-- Other tables can reference with foreign keys
```

**Why It Matters**:
- Data integrity: Primary keys prevent duplicates
- Performance: Clustered index (typically on PK) improves all queries
- Relationships: Other tables need PK to create foreign keys
- Updates/Deletes: No efficient way to target specific rows without PK

**Choosing Primary Keys**:
- Surrogate keys (INT IDENTITY): Simple, efficient, never change
- Natural keys (composite): Meaningful, but can be complex
- Best practice: Surrogate key + unique constraint on natural key

---

### Anti-Pattern 15: Generic Table Design (Entity-Attribute-Value)

**Problem**: Using EAV pattern to avoid schema changes creates a maintenance nightmare.

**Bad Example**:
```sql
-- EAV anti-pattern (flexibility gone wrong)
CREATE TABLE employee_attributes (
    employee_id INT NOT NULL,
    attribute_name VARCHAR(50) NOT NULL,
    attribute_value VARCHAR(MAX),
    PRIMARY KEY (employee_id, attribute_name)
);

-- Data looks like this:
-- employee_id | attribute_name | attribute_value
-- 12345       | first_name     | John
-- 12345       | last_name      | Doe
-- 12345       | salary         | 50000
-- 12345       | hire_date      | 2025-01-15

-- Queries are horrific
SELECT
    (SELECT attribute_value FROM employee_attributes
     WHERE employee_id = 12345 AND attribute_name = 'first_name') AS first_name,
    (SELECT attribute_value FROM employee_attributes
     WHERE employee_id = 12345 AND attribute_name = 'last_name') AS last_name,
    (SELECT attribute_value FROM employee_attributes
     WHERE employee_id = 12345 AND attribute_name = 'salary') AS salary;

-- No data types, no constraints, no foreign keys
```

**Good Example**:
```sql
-- Proper table design with strong typing
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    first_name NVARCHAR(50) NOT NULL,
    last_name NVARCHAR(50) NOT NULL,
    salary DECIMAL(10,2) NOT NULL,
    hire_date DATE NOT NULL,
    email VARCHAR(100) NOT NULL,
    CONSTRAINT CHK_salary_positive CHECK (salary > 0),
    CONSTRAINT CHK_email_format CHECK (email LIKE '%@%.%')
);

-- If truly need flexible attributes, use JSON (SQL Server 2016+)
ALTER TABLE employees ADD custom_attributes NVARCHAR(MAX)
    CONSTRAINT CHK_custom_attributes_json CHECK (ISJSON(custom_attributes) = 1);

-- Query JSON efficiently
SELECT
    employee_id,
    first_name,
    last_name,
    JSON_VALUE(custom_attributes, '$.preferred_pronouns') AS preferred_pronouns,
    JSON_VALUE(custom_attributes, '$.emergency_contact') AS emergency_contact
FROM employees;
```

**Why It Matters**:
- Performance: Queries require multiple subqueries or pivots (10-100x slower)
- Data types: Everything stored as VARCHAR (no type safety)
- Constraints: Can't enforce business rules
- Indexing: Extremely difficult to index effectively
- Maintenance: Simple queries become complex

**When EAV Is Acceptable**:
- Truly dynamic schemas (user-defined fields)
- Prototyping phase
- Very rare: Product catalogs with varying attributes by category (but JSON is better)

---

## Security Anti-Patterns

### Anti-Pattern 16: SQL Injection Vulnerability

**Problem**: Building SQL queries with string concatenation allows SQL injection attacks.

**Bad Example**:
```sql
-- NEVER do this! Vulnerable to SQL injection
CREATE PROCEDURE get_employee_by_name
    @last_name NVARCHAR(50)
AS
BEGIN
    DECLARE @sql NVARCHAR(1000);
    SET @sql = 'SELECT * FROM employees WHERE last_name = ''' + @last_name + '''';
    EXEC(@sql);
END;

-- Attack example:
-- EXEC get_employee_by_name @last_name = '''; DROP TABLE employees; --'
-- Results in: SELECT * FROM employees WHERE last_name = ''; DROP TABLE employees; --'
```

**Good Example**:
```sql
-- Use parameterized queries (always safe)
CREATE PROCEDURE get_employee_by_name
    @last_name NVARCHAR(50)
AS
BEGIN
    SELECT employee_id, first_name, last_name, email, hire_date
    FROM employees
    WHERE last_name = @last_name;  -- Parameterized, safe from injection
END;

-- If dynamic SQL is unavoidable, use sp_executesql with parameters
CREATE PROCEDURE get_employees_dynamic
    @last_name NVARCHAR(50),
    @department_id INT = NULL
AS
BEGIN
    DECLARE @sql NVARCHAR(1000);
    SET @sql = N'SELECT employee_id, first_name, last_name
                 FROM employees
                 WHERE last_name = @last_name_param';

    IF @department_id IS NOT NULL
        SET @sql = @sql + N' AND department_id = @department_id_param';

    -- Execute with parameters (safe)
    EXEC sp_executesql @sql,
         N'@last_name_param NVARCHAR(50), @department_id_param INT',
         @last_name_param = @last_name,
         @department_id_param = @department_id;
END;
```

**Why It Matters**:
- Security: SQL injection can delete/modify data, expose sensitive information
- Compliance: OWASP Top 10 vulnerability
- Trust: Breach of user trust and legal liability
- Damage: Attackers can drop tables, steal passwords, escalate privileges

**Real-World Impact**:
- Equifax breach (2017): 147 million records exposed
- TalkTalk hack (2015): £400,000 fine

**Rule of Thumb**: NEVER concatenate user input into SQL strings; always use parameters

---

### Anti-Pattern 17: Storing Passwords in Plain Text

**Problem**: Storing passwords without hashing allows exposure in case of data breach.

**Bad Example**:
```sql
-- Plain text passwords = catastrophic breach
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    username NVARCHAR(50) NOT NULL,
    password NVARCHAR(50) NOT NULL  -- Plain text! BAD!
);

INSERT INTO users VALUES (1, 'john.doe', 'Password123');  -- Readable by anyone with DB access!
```

**Good Example**:
```sql
-- Never store plain text passwords in the database at all!
-- Password hashing should be done in application layer, not SQL Server

-- If you must store authentication data in SQL:
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    username NVARCHAR(50) NOT NULL UNIQUE,
    password_hash BINARY(64) NOT NULL,  -- Store hash, never plain text
    password_salt BINARY(16) NOT NULL,  -- Unique salt per user
    created_date DATETIME DEFAULT GETDATE(),
    last_login_date DATETIME
);

-- Application layer (C#, Python, etc.) handles hashing:
-- password_hash = hash_function(password + salt)
-- Use bcrypt, PBKDF2, or Argon2 (NOT MD5 or SHA1)

-- SQL Server can validate, but should not hash
-- (Hashing belongs in application layer for security)
```

**Why It Matters**:
- Security: Breaches expose all passwords instantly
- Compliance: Violates PCI-DSS, HIPAA, GDPR requirements
- Liability: Legal and financial consequences
- Trust: Catastrophic loss of user trust

**Best Practices**:
- Use bcrypt, PBKDF2, or Argon2 (strong, slow hashing functions)
- Unique salt per user
- Store only hash + salt, never plain text
- Implement in application layer, not database
- Add password complexity requirements
- Use multi-factor authentication

---

### Anti-Pattern 18: Excessive Permissions

**Problem**: Granting db_owner or sysadmin permissions when users only need SELECT access.

**Bad Example**:
```sql
-- Granting excessive permissions (principle of least privilege violation)
ALTER ROLE db_owner ADD MEMBER reporting_user;  -- Can modify schema, drop tables!

-- Granting sysadmin to application account
ALTER SERVER ROLE sysadmin ADD MEMBER app_service_account;  -- Can do ANYTHING!
```

**Good Example**:
```sql
-- Grant minimum necessary permissions
-- Read-only reporting user
CREATE USER reporting_user WITHOUT LOGIN;
ALTER ROLE db_datareader ADD MEMBER reporting_user;  -- SELECT only

-- Application user with specific permissions
CREATE USER app_user WITHOUT LOGIN;
GRANT SELECT, INSERT, UPDATE ON employees TO app_user;
GRANT SELECT, INSERT, UPDATE ON departments TO app_user;
GRANT EXECUTE ON SCHEMA::dbo TO app_user;  -- Can execute stored procedures

-- Deny dangerous operations explicitly
DENY DELETE ON employees TO app_user;
DENY ALTER ON SCHEMA::dbo TO app_user;

-- Use application roles for privilege escalation when needed
CREATE APPLICATION ROLE admin_operations WITH PASSWORD = 'StrongPassword123!';
GRANT DELETE ON employees TO admin_operations;
```

**Why It Matters**:
- Security: Limits damage from compromised accounts
- Compliance: Required by SOX, HIPAA, PCI-DSS
- Auditing: Easier to track who can do what
- Mistakes: Reduces risk of accidental data loss

**Principle of Least Privilege**:
- Grant minimum permissions required for job function
- Use roles instead of granting permissions to individual users
- Review permissions regularly
- Implement application roles for elevated privileges

---

## Schema Design Anti-Patterns

### Anti-Pattern 19: Using Float/Real for Money

**Problem**: Floating-point types have rounding errors and should never be used for currency.

**Bad Example**:
```sql
-- Using FLOAT for money = rounding errors
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    salary FLOAT  -- BAD! Rounding errors!
);

INSERT INTO employees VALUES (1, 50000.10);
INSERT INTO employees VALUES (2, 50000.10);

-- Expect 100000.20, but get 100000.19999999999999 due to rounding!
SELECT SUM(salary) FROM employees;
```

**Good Example**:
```sql
-- Use DECIMAL or MONEY for currency
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    salary DECIMAL(10,2) NOT NULL  -- Exact precision
    -- Or: salary MONEY NOT NULL
);

INSERT INTO employees VALUES (1, 50000.10);
INSERT INTO employees VALUES (2, 50000.10);

-- Correctly returns 100000.20
SELECT SUM(salary) FROM employees;
```

**Why It Matters**:
- Precision: Financial calculations must be exact
- Auditing: Rounding errors compound over time
- Compliance: Financial reporting requires precision
- Legal: Rounding errors can violate regulations

**Data Type Recommendations**:
- Currency: Use DECIMAL(19,4) or MONEY
- Percentages: Use DECIMAL(5,2) for percentages (e.g., 99.99%)
- Scientific data: FLOAT is OK (measurements, approximations)

---

### Anti-Pattern 20: VARCHAR(MAX) Everywhere

**Problem**: Using VARCHAR(MAX) for all string columns wastes space and hurts performance.

**Bad Example**:
```sql
-- Everything is VARCHAR(MAX)
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    first_name VARCHAR(MAX),      -- Overkill!
    last_name VARCHAR(MAX),       -- Overkill!
    email VARCHAR(MAX),           -- Overkill!
    phone VARCHAR(MAX),           -- Overkill!
    notes VARCHAR(MAX)            -- Maybe OK for this one
);
```

**Good Example**:
```sql
-- Appropriate sizes based on data
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    first_name NVARCHAR(50) NOT NULL,    -- Reasonable max
    last_name NVARCHAR(50) NOT NULL,     -- Reasonable max
    email VARCHAR(100) NOT NULL,         -- Max for email standard
    phone VARCHAR(20),                   -- International format
    notes VARCHAR(MAX)                   -- Large text is OK here
    -- Consider separate table for large notes with FK to employees
);
```

**Why It Matters**:
- Performance: VARCHAR(MAX) stored off-row (slower access)
- Indexing: Can't create indexes on VARCHAR(MAX) columns
- Memory: In-memory operations require more RAM
- Validation: Appropriate size limits help data quality

**Guidelines**:
- Use appropriate sizes (50, 100, 255 are common)
- NVARCHAR for Unicode (international characters)
- VARCHAR for ASCII-only data (saves 50% space)
- VARCHAR(MAX) only when truly needed (documents, long text)

---

### Anti-Pattern 21: Using GUID/UUID as Clustered Index

**Problem**: GUIDs are random, causing page splits and index fragmentation.

**Bad Example**:
```sql
-- GUID as clustered index = massive fragmentation
CREATE TABLE employees (
    employee_id UNIQUEIDENTIFIER DEFAULT NEWID() PRIMARY KEY CLUSTERED,  -- BAD!
    first_name NVARCHAR(50),
    last_name NVARCHAR(50)
);

-- Inserts are random order, causing constant page splits
-- 40-50% fragmentation after 100,000 rows
```

**Good Example**:
```sql
-- Use INT IDENTITY for clustered index, GUID as alternate key
CREATE TABLE employees (
    employee_id INT IDENTITY(1,1) PRIMARY KEY CLUSTERED,  -- Sequential
    employee_guid UNIQUEIDENTIFIER DEFAULT NEWID() UNIQUE NONCLUSTERED,  -- For external references
    first_name NVARCHAR(50),
    last_name NVARCHAR(50)
);

-- Or use NEWSEQUENTIALID() if GUID must be clustered
CREATE TABLE employees_guid (
    employee_id UNIQUEIDENTIFIER DEFAULT NEWSEQUENTIALID() PRIMARY KEY CLUSTERED,
    first_name NVARCHAR(50),
    last_name NVARCHAR(50)
);
```

**Why It Matters**:
- Fragmentation: Random GUIDs cause 40-50% fragmentation
- Performance: Insert performance degrades 2-3x
- Index size: GUIDs are 16 bytes vs 4 bytes for INT
- Page splits: Constant splits require more maintenance

**When GUIDs Are OK**:
- Distributed systems with merge replication
- External identifiers (use as UNIQUE non-clustered)
- Use NEWSEQUENTIALID() to reduce fragmentation

---

## Maintenance Anti-Patterns

### Anti-Pattern 22: No Indexing Strategy

**Problem**: Creating indexes ad-hoc without a strategy leads to over-indexing or under-indexing.

**Bad Example**:
```sql
-- Creating indexes without thought
CREATE INDEX IX_whatever ON employees(employee_id);  -- Already in PK!
CREATE INDEX IX_random ON employees(first_name);     -- Low selectivity
CREATE INDEX IX_duplicate1 ON employees(last_name, first_name);
CREATE INDEX IX_duplicate2 ON employees(last_name);  -- Redundant!

-- Result: 50+ indexes, many redundant, slow INSERT/UPDATE
```

**Good Example**:
```sql
-- Strategic indexing based on query patterns
-- 1. Identify frequent WHERE/JOIN columns
CREATE NONCLUSTERED INDEX IX_employees_status_dept
ON employees(status, department_id)
INCLUDE (first_name, last_name, email);  -- Covering index

-- 2. Foreign keys for JOIN performance
CREATE NONCLUSTERED INDEX IX_employees_department_id
ON employees(department_id);

-- 3. Filtered index for active employees only
CREATE NONCLUSTERED INDEX IX_employees_active_hire_date
ON employees(hire_date)
WHERE status = 'Active';

-- Monitor index usage
SELECT
    OBJECT_NAME(s.object_id) AS table_name,
    i.name AS index_name,
    s.user_seeks,
    s.user_scans,
    s.user_lookups,
    s.user_updates
FROM sys.dm_db_index_usage_stats s
INNER JOIN sys.indexes i ON s.object_id = i.object_id AND s.index_id = i.index_id
ORDER BY s.user_updates DESC, s.user_seeks ASC;

-- Remove unused indexes
-- DROP INDEX IX_unused ON employees;
```

**Why It Matters**:
- Performance: Too many indexes slow INSERT/UPDATE/DELETE
- Maintenance: Index rebuilds take time and resources
- Storage: Each index consumes disk space
- Strategy: Indexes should match query patterns

**Indexing Best Practices**:
- Index foreign keys
- Index WHERE clause columns
- Use covering indexes for frequently-run queries
- Monitor index usage and remove unused indexes
- Rebuild fragmented indexes (>30% fragmentation)

---

### Anti-Pattern 23: No Error Handling

**Problem**: Stored procedures and scripts without error handling fail silently or partially complete.

**Bad Example**:
```sql
-- No error handling = silent failures
CREATE PROCEDURE update_employee_salary
    @employee_id INT,
    @new_salary DECIMAL(10,2)
AS
BEGIN
    -- What if employee doesn't exist?
    UPDATE employees
    SET salary = @new_salary
    WHERE employee_id = @employee_id;

    -- What if this fails?
    INSERT INTO salary_history (employee_id, old_salary, new_salary, change_date)
    VALUES (@employee_id, 0, @new_salary, GETDATE());

    -- No return value, no error info!
END;
```

**Good Example**:
```sql
-- Proper error handling with TRY/CATCH
CREATE PROCEDURE update_employee_salary
    @employee_id INT,
    @new_salary DECIMAL(10,2)
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @old_salary DECIMAL(10,2);

    BEGIN TRY
        BEGIN TRANSACTION;

        -- Validate employee exists
        SELECT @old_salary = salary
        FROM employees
        WHERE employee_id = @employee_id;

        IF @old_salary IS NULL
        BEGIN
            RAISERROR('Employee ID %d not found', 16, 1, @employee_id);
            RETURN -1;
        END;

        -- Update salary
        UPDATE employees
        SET salary = @new_salary
        WHERE employee_id = @employee_id;

        -- Record history
        INSERT INTO salary_history (employee_id, old_salary, new_salary, change_date)
        VALUES (@employee_id, @old_salary, @new_salary, GETDATE());

        COMMIT TRANSACTION;
        RETURN 0;  -- Success
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;

        -- Log error details
        DECLARE @error_message NVARCHAR(4000) = ERROR_MESSAGE();
        DECLARE @error_number INT = ERROR_NUMBER();
        DECLARE @error_severity INT = ERROR_SEVERITY();

        -- Re-raise error
        RAISERROR('Error updating employee salary: %s', @error_severity, 1, @error_message);
        RETURN -1;  -- Failure
    END CATCH;
END;
```

**Why It Matters**:
- Debugging: Error details help troubleshoot problems
- Data integrity: Transactions roll back on error
- Monitoring: Errors can be logged and alerted
- Reliability: Proper handling prevents partial updates

---

### Anti-Pattern 24: No Commenting or Documentation

**Problem**: Complex queries and stored procedures without comments are impossible to maintain.

**Bad Example**:
```sql
-- Cryptic query with no explanation
SELECT e.employee_id, e.last_name,
       (SELECT COUNT(*) FROM credentials c WHERE c.employee_id = e.employee_id
        AND c.expiration_date > GETDATE()) +
       (SELECT COUNT(*) FROM certifications cf WHERE cf.employee_id = e.employee_id) AS x,
       CASE WHEN EXISTS (SELECT 1 FROM leaves l WHERE l.employee_id = e.employee_id
                         AND l.leave_start_date <= GETDATE()
                         AND l.leave_end_date >= GETDATE()) THEN 1 ELSE 0 END AS y
FROM employees e
WHERE e.status = 'A';
```

**Good Example**:
```sql
/*
    Purpose: Employee Compliance Dashboard Query
    Author: John Doe
    Date: 2025-10-24
    Description: Retrieves employee compliance status including:
                 - Active credentials and certifications count
                 - Current leave status
                 Used by: HR Compliance Dashboard (reports/compliance.aspx)
*/

SELECT
    e.employee_id,
    e.last_name,
    -- Count valid credentials (not expired) + active certifications
    (SELECT COUNT(*)
     FROM credentials c
     WHERE c.employee_id = e.employee_id
       AND c.expiration_date > GETDATE()) +
    (SELECT COUNT(*)
     FROM certifications cf
     WHERE cf.employee_id = e.employee_id) AS total_valid_credentials,
    -- Check if employee is currently on leave (1 = on leave, 0 = not on leave)
    CASE
        WHEN EXISTS (
            SELECT 1
            FROM leaves l
            WHERE l.employee_id = e.employee_id
              AND l.leave_start_date <= GETDATE()
              AND l.leave_end_date >= GETDATE()
        ) THEN 1
        ELSE 0
    END AS is_currently_on_leave
FROM employees e
WHERE e.status = 'A';  -- A = Active status
```

**Why It Matters**:
- Maintenance: Future developers (including yourself) need to understand intent
- Debugging: Comments explain expected behavior
- Knowledge transfer: Reduces bus factor
- Compliance: Audit trails require documentation

**Documentation Best Practices**:
- Header comments: Purpose, author, date, dependencies
- Complex logic: Explain WHY, not just WHAT
- Business rules: Document requirements source
- Performance notes: Explain index usage, optimization decisions
- TODOs: Mark temporary solutions or future improvements

---

## Summary: Quick Reference

| Anti-Pattern | Fix | Impact |
|-------------|-----|--------|
| SELECT * | List columns explicitly | Performance, maintainability |
| Implicit INSERT columns | Specify column list | Schema resilience |
| OR in JOINs | Separate JOINs or UNION | Performance (10-100x) |
| Correlated subqueries | Use JOINs/CTEs | Performance (10-1000x) |
| NOT IN with NULLs | Use NOT EXISTS | Correctness |
| Functions on indexed columns | Rewrite to use indexes | Performance (10-100x) |
| Leading wildcards in LIKE | Full-text search | Performance (100-1000x) |
| DISTINCT as band-aid | Fix JOIN logic | Correctness, performance |
| UNION instead of UNION ALL | Use UNION ALL | Performance (2-10x) |
| Cursor loops | Set-based operations | Performance (10-100x) |
| Implicit conversions | Match data types | Performance, correctness |
| Flag columns everywhere | Lookup tables | Data integrity, extensibility |
| Delimited lists in columns | Many-to-many tables | Normalization, integrity |
| No primary keys | Add surrogate or natural PK | Data integrity, performance |
| EAV pattern | Proper schema or JSON | Performance, maintainability |
| SQL injection | Parameterized queries | Security (critical!) |
| Plain text passwords | Hash with bcrypt/PBKDF2 | Security (critical!) |
| Excessive permissions | Least privilege | Security, compliance |
| FLOAT for money | DECIMAL or MONEY | Precision, compliance |
| VARCHAR(MAX) everywhere | Appropriate sizes | Performance, indexing |
| GUID clustered index | INT IDENTITY or NEWSEQUENTIALID | Fragmentation, performance |
| No indexing strategy | Query-driven indexes | Performance, maintenance |
| No error handling | TRY/CATCH blocks | Reliability, debugging |
| No documentation | Comments and headers | Maintainability |

---

## Additional Resources

For more SQL best practices, see:
- `advanced_techniques.md` - 15 advanced SQL concepts and patterns
- `query_optimization.md` - Execution plan analysis and performance tuning
- `hr_education_patterns.md` - Common patterns for HR/education databases
