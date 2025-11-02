# Advanced SQL Techniques - Comprehensive Reference

This reference covers 15 advanced SQL concepts essential for data engineers, analysts, and database developers working with complex queries and large datasets.

---

## 1. Subqueries (Nested Queries)

**Definition**: A complete SELECT statement embedded within another SQL statement.

**Use Cases**:
- Filter results based on aggregate calculations
- Create derived tables for complex joins
- Perform row-by-row comparisons

**Example - Correlated Subquery**:
```sql
-- Find employees earning above department average
SELECT
    e.employee_id,
    e.first_name,
    e.last_name,
    e.salary,
    e.department_id
FROM employees e
WHERE e.salary > (
    SELECT AVG(salary)
    FROM employees
    WHERE department_id = e.department_id
);
```

**Example - Subquery in FROM Clause**:
```sql
-- Department salary statistics
SELECT
    dept_stats.department_id,
    dept_stats.avg_salary,
    dept_stats.max_salary,
    COUNT(e.employee_id) AS employee_count
FROM (
    SELECT
        department_id,
        AVG(salary) AS avg_salary,
        MAX(salary) AS max_salary
    FROM employees
    GROUP BY department_id
) dept_stats
JOIN employees e ON dept_stats.department_id = e.department_id
GROUP BY dept_stats.department_id, dept_stats.avg_salary, dept_stats.max_salary;
```

**Best Practices**:
- Prefer JOINs over correlated subqueries for better performance
- Use EXISTS instead of IN for large result sets
- Consider materializing complex subqueries as temporary tables

---

## 2. Advanced Joins

**Types**: INNER, LEFT, RIGHT, FULL OUTER, CROSS, SELF

**Complex Join Example - Multiple Conditions**:
```sql
-- Find credential mismatches between systems
SELECT
    e.employee_id,
    e.full_name,
    fc.credential_code AS fcoe_credential,
    hr.credential_code AS hr_credential,
    CASE
        WHEN fc.credential_code IS NULL THEN 'Missing in FCOE'
        WHEN hr.credential_code IS NULL THEN 'Missing in HR'
        WHEN fc.credential_code <> hr.credential_code THEN 'Mismatch'
        ELSE 'Match'
    END AS status
FROM employees e
LEFT JOIN fcoe_credentials fc
    ON e.employee_id = fc.employee_id
    AND fc.is_active = 1
LEFT JOIN hr_credentials hr
    ON e.employee_id = hr.employee_id
    AND hr.status = 'Active'
WHERE fc.credential_code IS NULL
   OR hr.credential_code IS NULL
   OR fc.credential_code <> hr.credential_code;
```

**Self-Join Example - Hierarchical Data**:
```sql
-- Find employees and their managers
SELECT
    e.employee_id,
    e.first_name + ' ' + e.last_name AS employee_name,
    m.first_name + ' ' + m.last_name AS manager_name,
    e.department_id
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.employee_id
ORDER BY e.department_id, e.employee_id;
```

**Best Practices**:
- Always specify join conditions explicitly
- Use LEFT JOIN instead of RIGHT JOIN for readability
- Consider join order: smaller tables first in nested loops
- Index foreign key columns used in joins

---

## 3. UNION and UNION ALL

**UNION**: Combines result sets, removes duplicates
**UNION ALL**: Combines result sets, keeps duplicates (faster)

**Example - Combining Multiple Sources**:
```sql
-- Combine active employees from multiple systems
SELECT employee_id, first_name, last_name, 'Payroll' AS source
FROM payroll_system.employees
WHERE status = 'Active'

UNION ALL

SELECT emp_id, fname, lname, 'HR System' AS source
FROM hr_system.staff
WHERE employment_status = 'Current'

UNION ALL

SELECT id, given_name, family_name, 'LMS' AS source
FROM learning_mgmt.users
WHERE role = 'Faculty' AND active = 1;
```

**Best Practices**:
- Use UNION ALL when duplicates don't matter (better performance)
- Ensure column counts and types match across all queries
- Use aliases for clarity when combining disparate sources
- Consider indexing columns used in WHERE clauses

---

## 4. Aggregate Functions with GROUP BY

**Functions**: COUNT, SUM, AVG, MIN, MAX, STRING_AGG, ARRAY_AGG

**Advanced Grouping Example**:
```sql
-- Department credential statistics
SELECT
    d.department_name,
    COUNT(DISTINCT e.employee_id) AS total_employees,
    COUNT(DISTINCT c.credential_id) AS total_credentials,
    COUNT(DISTINCT CASE WHEN c.expiration_date < GETDATE() THEN c.credential_id END) AS expired_count,
    CAST(AVG(DATEDIFF(day, c.issue_date, c.expiration_date)) AS INT) AS avg_validity_days,
    STRING_AGG(c.credential_type, ', ') WITHIN GROUP (ORDER BY c.credential_type) AS credential_types
FROM departments d
LEFT JOIN employees e ON d.department_id = e.department_id
LEFT JOIN credentials c ON e.employee_id = c.employee_id
GROUP BY d.department_id, d.department_name
HAVING COUNT(DISTINCT e.employee_id) > 0
ORDER BY expired_count DESC;
```

**GROUPING SETS Example**:
```sql
-- Multi-level aggregation
SELECT
    department_id,
    job_title,
    credential_type,
    COUNT(*) AS employee_count,
    AVG(salary) AS avg_salary
FROM employee_credentials
GROUP BY GROUPING SETS (
    (department_id, job_title, credential_type),  -- Detail level
    (department_id, credential_type),              -- Department summary
    (credential_type),                             -- Credential summary
    ()                                              -- Grand total
);
```

**Best Practices**:
- Include all non-aggregated columns in GROUP BY
- Use HAVING for filtering aggregated results
- Consider performance impact of multiple aggregations
- Use filtered aggregates (CASE WHEN) instead of multiple queries

---

## 5. Window Functions

**Definition**: Perform calculations across rows related to the current row without collapsing the result set.

**Components**:
- **PARTITION BY**: Divides rows into groups
- **ORDER BY**: Defines row sequence within partitions
- **Frame Clause**: Specifies calculation window (ROWS, RANGE, GROUPS)

**Common Functions**:
- **Ranking**: ROW_NUMBER(), RANK(), DENSE_RANK(), NTILE()
- **Offset**: LAG(), LEAD(), FIRST_VALUE(), LAST_VALUE()
- **Aggregate**: SUM(), AVG(), COUNT() OVER()

**Example - Ranking**:
```sql
-- Rank employees by salary within each department
SELECT
    employee_id,
    first_name,
    last_name,
    department_id,
    salary,
    ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) AS salary_rank,
    RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS salary_rank_with_ties,
    DENSE_RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS dense_salary_rank,
    NTILE(4) OVER (PARTITION BY department_id ORDER BY salary DESC) AS salary_quartile
FROM employees;
```

**Example - Running Totals**:
```sql
-- Calculate cumulative hires by department
SELECT
    hire_date,
    department_id,
    employee_id,
    first_name,
    last_name,
    COUNT(*) OVER (
        PARTITION BY department_id
        ORDER BY hire_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_hires,
    SUM(salary) OVER (
        PARTITION BY department_id
        ORDER BY hire_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_salary_cost
FROM employees
ORDER BY department_id, hire_date;
```

**Example - Moving Averages**:
```sql
-- 90-day rolling average of daily registrations
SELECT
    registration_date,
    daily_count,
    AVG(daily_count) OVER (
        ORDER BY registration_date
        ROWS BETWEEN 89 PRECEDING AND CURRENT ROW
    ) AS moving_avg_90_days
FROM (
    SELECT
        CAST(created_date AS DATE) AS registration_date,
        COUNT(*) AS daily_count
    FROM student_registrations
    GROUP BY CAST(created_date AS DATE)
) daily_registrations
ORDER BY registration_date;
```

**Example - Year-over-Year Comparison**:
```sql
-- Compare enrollment to previous year
SELECT
    academic_year,
    semester,
    program_name,
    enrollment_count,
    LAG(enrollment_count, 1) OVER (
        PARTITION BY program_name, semester
        ORDER BY academic_year
    ) AS prior_year_enrollment,
    enrollment_count - LAG(enrollment_count, 1) OVER (
        PARTITION BY program_name, semester
        ORDER BY academic_year
    ) AS year_over_year_change,
    ROUND(
        100.0 * (enrollment_count - LAG(enrollment_count, 1) OVER (
            PARTITION BY program_name, semester
            ORDER BY academic_year
        )) / NULLIF(LAG(enrollment_count, 1) OVER (
            PARTITION BY program_name, semester
            ORDER BY academic_year
        ), 0),
        2
    ) AS pct_change
FROM enrollment_summary
ORDER BY program_name, semester, academic_year;
```

**Best Practices**:
- Window functions preserve row-level detail unlike GROUP BY
- Use appropriate frame clauses for moving calculations
- Consider performance impact on large datasets
- Combine with CTEs for complex multi-step calculations

---

## 6. Common Table Expressions (CTEs)

**Definition**: Temporary named result sets that exist within a single query execution.

**Advantages**:
- Improved readability and maintainability
- Support for recursion
- Can be referenced multiple times in the same query
- Easier debugging than nested subqueries

**Simple CTE Example**:
```sql
-- Calculate department budgets with CTEs
WITH department_costs AS (
    SELECT
        department_id,
        SUM(salary) AS total_salary,
        COUNT(*) AS employee_count
    FROM employees
    WHERE status = 'Active'
    GROUP BY department_id
),
department_info AS (
    SELECT
        d.department_id,
        d.department_name,
        d.budget_allocated,
        dc.total_salary,
        dc.employee_count
    FROM departments d
    JOIN department_costs dc ON d.department_id = dc.department_id
)
SELECT
    department_name,
    budget_allocated,
    total_salary,
    budget_allocated - total_salary AS remaining_budget,
    ROUND(100.0 * total_salary / budget_allocated, 2) AS budget_utilization_pct,
    employee_count,
    ROUND(total_salary / employee_count, 2) AS avg_salary_per_employee
FROM department_info
WHERE budget_allocated - total_salary < 10000  -- Departments near budget limit
ORDER BY budget_utilization_pct DESC;
```

**Multiple CTEs Example**:
```sql
-- Complex credential analysis with multiple CTEs
WITH active_employees AS (
    SELECT employee_id, full_name, department_id, hire_date
    FROM employees
    WHERE status = 'Active'
),
credential_summary AS (
    SELECT
        employee_id,
        COUNT(*) AS total_credentials,
        COUNT(CASE WHEN expiration_date < GETDATE() THEN 1 END) AS expired_count,
        COUNT(CASE WHEN expiration_date BETWEEN GETDATE() AND DATEADD(day, 90, GETDATE()) THEN 1 END) AS expiring_soon_count,
        MAX(expiration_date) AS latest_expiration
    FROM credentials
    GROUP BY employee_id
),
department_stats AS (
    SELECT
        d.department_id,
        d.department_name,
        COUNT(DISTINCT ae.employee_id) AS total_employees,
        AVG(cs.total_credentials) AS avg_credentials_per_employee,
        SUM(cs.expired_count) AS total_expired,
        SUM(cs.expiring_soon_count) AS total_expiring_soon
    FROM departments d
    LEFT JOIN active_employees ae ON d.department_id = ae.department_id
    LEFT JOIN credential_summary cs ON ae.employee_id = cs.employee_id
    GROUP BY d.department_id, d.department_name
)
SELECT
    department_name,
    total_employees,
    ROUND(avg_credentials_per_employee, 2) AS avg_credentials,
    total_expired,
    total_expiring_soon,
    ROUND(100.0 * total_expired / NULLIF(total_employees, 0), 2) AS expired_pct
FROM department_stats
WHERE total_expired > 0 OR total_expiring_soon > 0
ORDER BY expired_pct DESC, total_expired DESC;
```

**Best Practices**:
- Use CTEs for complex queries requiring multiple steps
- Name CTEs descriptively to improve readability
- Break complex logic into multiple CTEs rather than one massive query
- Consider performance: CTEs may be materialized or inlined depending on optimizer

---

## 7. Recursive CTEs

**Definition**: CTEs that reference themselves to process hierarchical or iterative data.

**Structure**:
1. **Anchor member**: Base case (executed once)
2. **UNION ALL**: Combines results
3. **Recursive member**: References the CTE itself
4. **Termination condition**: Prevents infinite loops

**Example - Organizational Hierarchy**:
```sql
-- Employee reporting structure
WITH EmployeeHierarchy AS (
    -- Anchor: Top-level managers
    SELECT
        employee_id,
        first_name,
        last_name,
        manager_id,
        job_title,
        1 AS level,
        CAST(first_name + ' ' + last_name AS NVARCHAR(1000)) AS hierarchy_path
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive: Employees reporting to managers
    SELECT
        e.employee_id,
        e.first_name,
        e.last_name,
        e.manager_id,
        e.job_title,
        eh.level + 1,
        CAST(eh.hierarchy_path + ' > ' + e.first_name + ' ' + e.last_name AS NVARCHAR(1000))
    FROM employees e
    INNER JOIN EmployeeHierarchy eh ON e.manager_id = eh.employee_id
    WHERE eh.level < 10  -- Prevent infinite recursion
)
SELECT
    level,
    employee_id,
    first_name + ' ' + last_name AS employee_name,
    job_title,
    hierarchy_path
FROM EmployeeHierarchy
ORDER BY level, employee_id;
```

**Example - Date Series Generation**:
```sql
-- Generate all dates in a range
WITH DateSeries AS (
    SELECT CAST('2024-01-01' AS DATE) AS report_date

    UNION ALL

    SELECT DATEADD(day, 1, report_date)
    FROM DateSeries
    WHERE report_date < '2024-12-31'
)
SELECT
    ds.report_date,
    DATENAME(weekday, ds.report_date) AS day_of_week,
    COALESCE(COUNT(a.attendance_id), 0) AS attendance_count
FROM DateSeries ds
LEFT JOIN attendance_records a ON CAST(a.check_in_time AS DATE) = ds.report_date
GROUP BY ds.report_date
ORDER BY ds.report_date
OPTION (MAXRECURSION 365);  -- Allow up to 365 recursions
```

**Example - Bill of Materials (BOM)**:
```sql
-- Expand course prerequisites recursively
WITH CoursePrerequisites AS (
    -- Anchor: Target course
    SELECT
        course_id,
        course_code,
        course_name,
        prerequisite_course_id,
        0 AS prerequisite_level
    FROM courses
    WHERE course_id = 'CS401'

    UNION ALL

    -- Recursive: Prerequisites of prerequisites
    SELECT
        c.course_id,
        c.course_code,
        c.course_name,
        c.prerequisite_course_id,
        cp.prerequisite_level + 1
    FROM courses c
    INNER JOIN CoursePrerequisites cp ON c.course_id = cp.prerequisite_course_id
    WHERE cp.prerequisite_level < 5
)
SELECT
    prerequisite_level,
    course_code,
    course_name
FROM CoursePrerequisites
WHERE prerequisite_course_id IS NOT NULL
ORDER BY prerequisite_level, course_code;
```

**Best Practices**:
- Always include a termination condition (level limits or date bounds)
- Use MAXRECURSION hint to prevent runaway queries
- Index columns used in recursive joins
- Consider performance for deep hierarchies (>100 levels)

---

## 8. PIVOT and UNPIVOT

**PIVOT**: Transforms rows into columns (crosstab reports)
**UNPIVOT**: Transforms columns into rows (normalizing data)

**PIVOT Example**:
```sql
-- Credential counts by department and type (columns)
SELECT
    department_name,
    [Teaching Credential],
    [Administrative Credential],
    [Counseling Credential],
    [Special Education]
FROM (
    SELECT
        d.department_name,
        c.credential_type,
        c.credential_id
    FROM departments d
    JOIN employees e ON d.department_id = e.department_id
    JOIN credentials c ON e.employee_id = c.employee_id
    WHERE c.status = 'Active'
) AS source_data
PIVOT (
    COUNT(credential_id)
    FOR credential_type IN (
        [Teaching Credential],
        [Administrative Credential],
        [Counseling Credential],
        [Special Education]
    )
) AS pivot_table
ORDER BY department_name;
```

**Dynamic PIVOT Example**:
```sql
-- Generate pivot query dynamically for unknown column values
DECLARE @columns NVARCHAR(MAX), @sql NVARCHAR(MAX);

-- Get distinct credential types
SELECT @columns = STRING_AGG(QUOTENAME(credential_type), ', ')
FROM (SELECT DISTINCT credential_type FROM credentials) AS types;

-- Build dynamic query
SET @sql = '
SELECT department_name, ' + @columns + '
FROM (
    SELECT d.department_name, c.credential_type, c.credential_id
    FROM departments d
    JOIN employees e ON d.department_id = e.department_id
    JOIN credentials c ON e.employee_id = c.employee_id
) AS source_data
PIVOT (
    COUNT(credential_id)
    FOR credential_type IN (' + @columns + ')
) AS pivot_table
ORDER BY department_name;';

EXEC sp_executesql @sql;
```

**UNPIVOT Example**:
```sql
-- Convert quarterly enrollment columns to rows
SELECT
    academic_year,
    program_name,
    quarter,
    enrollment_count
FROM (
    SELECT
        academic_year,
        program_name,
        Q1_enrollment,
        Q2_enrollment,
        Q3_enrollment,
        Q4_enrollment
    FROM annual_enrollment_summary
) AS source_data
UNPIVOT (
    enrollment_count
    FOR quarter IN (Q1_enrollment, Q2_enrollment, Q3_enrollment, Q4_enrollment)
) AS unpivot_table
ORDER BY academic_year, program_name, quarter;
```

**Best Practices**:
- Use PIVOT for creating crosstab reports
- Consider performance impact on large datasets
- Use dynamic SQL for unknown column values
- UNPIVOT is useful for normalizing denormalized data

---

## 9. String Manipulation Functions

**Common Functions**: CONCAT, SUBSTRING, REPLACE, TRIM, UPPER, LOWER, LEN, CHARINDEX, STUFF, STRING_SPLIT

**Advanced String Example**:
```sql
-- Parse and clean employee names
SELECT
    employee_id,
    original_name,
    UPPER(TRIM(SUBSTRING(original_name, 1, CHARINDEX(',', original_name) - 1))) AS last_name,
    UPPER(TRIM(SUBSTRING(original_name, CHARINDEX(',', original_name) + 1, LEN(original_name)))) AS first_name,
    CONCAT(
        UPPER(SUBSTRING(TRIM(SUBSTRING(original_name, CHARINDEX(',', original_name) + 1, LEN(original_name))), 1, 1)),
        LOWER(SUBSTRING(TRIM(SUBSTRING(original_name, CHARINDEX(',', original_name) + 1, LEN(original_name))), 2, LEN(original_name)))
    ) AS formatted_first_name,
    REPLACE(REPLACE(REPLACE(phone_number, '-', ''), '(', ''), ')', '') AS clean_phone,
    STUFF(email, CHARINDEX('@', email), 0, '+notifications@') AS notification_email
FROM employees_raw;
```

**STRING_SPLIT Example** (SQL Server 2016+):
```sql
-- Parse comma-separated credential codes
SELECT
    e.employee_id,
    e.full_name,
    s.value AS credential_code
FROM employees e
CROSS APPLY STRING_SPLIT(e.credential_codes, ',') s
WHERE TRIM(s.value) <> '';
```

**Pattern Matching with LIKE**:
```sql
-- Find credentials with specific patterns
SELECT
    credential_id,
    credential_code,
    credential_name
FROM credentials
WHERE
    credential_code LIKE 'MS-%'  -- Starts with MS-
    OR credential_code LIKE '%[0-9][0-9][0-9][0-9]'  -- Ends with 4 digits
    OR credential_name LIKE '%[[]Preliminary[]]%'  -- Contains [Preliminary]
ORDER BY credential_code;
```

**Best Practices**:
- Use CONCAT instead of + for null-safe concatenation
- TRIM removes leading/trailing spaces
- STRING_SPLIT is more efficient than custom parsing functions
- Consider PATINDEX for complex pattern matching

---

## 10. Date and Time Functions

**Common Functions**: GETDATE, DATEADD, DATEDIFF, DATEPART, EOMONTH, FORMAT, CONVERT

**Date Calculations Example**:
```sql
-- Credential expiration analysis
SELECT
    credential_id,
    employee_id,
    credential_type,
    issue_date,
    expiration_date,
    DATEDIFF(day, issue_date, expiration_date) AS validity_period_days,
    DATEDIFF(day, GETDATE(), expiration_date) AS days_until_expiration,
    DATEDIFF(month, GETDATE(), expiration_date) AS months_until_expiration,
    DATEADD(day, -90, expiration_date) AS renewal_reminder_date,
    EOMONTH(expiration_date) AS end_of_expiration_month,
    DATEPART(year, expiration_date) AS expiration_year,
    DATEPART(quarter, expiration_date) AS expiration_quarter,
    CASE
        WHEN expiration_date < GETDATE() THEN 'Expired'
        WHEN DATEDIFF(day, GETDATE(), expiration_date) <= 90 THEN 'Expiring Soon'
        ELSE 'Current'
    END AS status
FROM credentials
ORDER BY days_until_expiration;
```

**Fiscal Year Calculations**:
```sql
-- Calculate fiscal year (July 1 - June 30)
SELECT
    transaction_date,
    CASE
        WHEN MONTH(transaction_date) >= 7
        THEN YEAR(transaction_date) + 1
        ELSE YEAR(transaction_date)
    END AS fiscal_year,
    CASE
        WHEN MONTH(transaction_date) BETWEEN 7 AND 9 THEN 'Q1'
        WHEN MONTH(transaction_date) BETWEEN 10 AND 12 THEN 'Q2'
        WHEN MONTH(transaction_date) BETWEEN 1 AND 3 THEN 'Q3'
        WHEN MONTH(transaction_date) BETWEEN 4 AND 6 THEN 'Q4'
    END AS fiscal_quarter
FROM financial_transactions;
```

**Date Formatting**:
```sql
-- Format dates for reporting
SELECT
    employee_id,
    hire_date,
    FORMAT(hire_date, 'yyyy-MM-dd') AS iso_date,
    FORMAT(hire_date, 'MMMM d, yyyy') AS long_date,
    FORMAT(hire_date, 'MM/dd/yyyy') AS us_date,
    CONVERT(VARCHAR(10), hire_date, 120) AS iso_date_convert,
    CONVERT(VARCHAR(20), hire_date, 107) AS month_day_year
FROM employees;
```

**Best Practices**:
- Store dates in DATE or DATETIME columns, not strings
- Use DATEADD/DATEDIFF for date arithmetic
- Consider time zones for distributed systems
- Use FORMAT for display purposes only (slower than CONVERT)

---

## 11. CASE Statements

**Definition**: Implement conditional logic (if-then-else) within queries.

**Simple CASE Example**:
```sql
-- Categorize employees by salary
SELECT
    employee_id,
    full_name,
    salary,
    CASE
        WHEN salary >= 100000 THEN 'Executive'
        WHEN salary >= 75000 THEN 'Senior'
        WHEN salary >= 50000 THEN 'Mid-Level'
        WHEN salary >= 30000 THEN 'Junior'
        ELSE 'Entry-Level'
    END AS salary_band,
    CASE
        WHEN DATEDIFF(year, hire_date, GETDATE()) >= 10 THEN 'Veteran'
        WHEN DATEDIFF(year, hire_date, GETDATE()) >= 5 THEN 'Experienced'
        WHEN DATEDIFF(year, hire_date, GETDATE()) >= 2 THEN 'Established'
        ELSE 'New'
    END AS tenure_category
FROM employees
ORDER BY salary DESC;
```

**Complex CASE in Aggregation**:
```sql
-- Conditional counting and summing
SELECT
    department_id,
    COUNT(*) AS total_employees,
    COUNT(CASE WHEN status = 'Active' THEN 1 END) AS active_count,
    COUNT(CASE WHEN status = 'On Leave' THEN 1 END) AS on_leave_count,
    COUNT(CASE WHEN status = 'Terminated' THEN 1 END) AS terminated_count,
    SUM(CASE WHEN status = 'Active' THEN salary ELSE 0 END) AS active_payroll,
    AVG(CASE WHEN status = 'Active' THEN salary END) AS avg_active_salary,
    SUM(CASE WHEN credential_expiration < GETDATE() THEN 1 ELSE 0 END) AS expired_credentials
FROM employees
GROUP BY department_id;
```

**Nested CASE Example**:
```sql
-- Complex credential status logic
SELECT
    credential_id,
    credential_type,
    expiration_date,
    CASE
        WHEN expiration_date IS NULL THEN 'No Expiration'
        WHEN expiration_date < GETDATE() THEN
            CASE
                WHEN DATEDIFF(day, expiration_date, GETDATE()) > 365 THEN 'Expired >1 Year'
                WHEN DATEDIFF(day, expiration_date, GETDATE()) > 180 THEN 'Expired >6 Months'
                ELSE 'Recently Expired'
            END
        WHEN DATEDIFF(day, GETDATE(), expiration_date) <= 30 THEN 'Critical - 30 Days'
        WHEN DATEDIFF(day, GETDATE(), expiration_date) <= 90 THEN 'Warning - 90 Days'
        ELSE 'Current'
    END AS status_detail
FROM credentials
ORDER BY expiration_date;
```

**Best Practices**:
- Order CASE conditions from most to least specific
- Use BETWEEN for range conditions
- Consider using lookup tables for complex categorization
- CASE can be used in SELECT, WHERE, ORDER BY, and HAVING

---

## 12. User-Defined Functions (UDFs)

**Types**:
- **Scalar Functions**: Return a single value
- **Table-Valued Functions**: Return a table
- **Inline Table-Valued Functions**: Single SELECT statement

**Scalar Function Example**:
```sql
-- Calculate credential validity period
CREATE FUNCTION dbo.GetCredentialValidityDays
(
    @IssueDate DATE,
    @ExpirationDate DATE
)
RETURNS INT
AS
BEGIN
    DECLARE @ValidityDays INT;

    IF @ExpirationDate IS NULL
        SET @ValidityDays = NULL;
    ELSE
        SET @ValidityDays = DATEDIFF(day, @IssueDate, @ExpirationDate);

    RETURN @ValidityDays;
END;
GO

-- Usage
SELECT
    credential_id,
    dbo.GetCredentialValidityDays(issue_date, expiration_date) AS validity_days
FROM credentials;
```

**Inline Table-Valued Function Example**:
```sql
-- Get employees by department with calculated fields
CREATE FUNCTION dbo.GetDepartmentEmployees
(
    @DepartmentID INT
)
RETURNS TABLE
AS
RETURN
(
    SELECT
        employee_id,
        full_name,
        hire_date,
        salary,
        DATEDIFF(year, hire_date, GETDATE()) AS years_of_service,
        CASE
            WHEN DATEDIFF(year, hire_date, GETDATE()) >= 10 THEN 'Veteran'
            ELSE 'Regular'
        END AS employee_category
    FROM employees
    WHERE department_id = @DepartmentID
      AND status = 'Active'
);
GO

-- Usage
SELECT * FROM dbo.GetDepartmentEmployees(5);
```

**Multi-Statement Table-Valued Function Example**:
```sql
-- Get credential status summary for an employee
CREATE FUNCTION dbo.GetEmployeeCredentialSummary
(
    @EmployeeID INT
)
RETURNS @CredentialSummary TABLE
(
    CredentialType NVARCHAR(100),
    TotalCount INT,
    ActiveCount INT,
    ExpiredCount INT,
    ExpiringSoonCount INT
)
AS
BEGIN
    INSERT INTO @CredentialSummary
    SELECT
        credential_type,
        COUNT(*) AS TotalCount,
        COUNT(CASE WHEN expiration_date >= GETDATE() THEN 1 END) AS ActiveCount,
        COUNT(CASE WHEN expiration_date < GETDATE() THEN 1 END) AS ExpiredCount,
        COUNT(CASE WHEN expiration_date BETWEEN GETDATE() AND DATEADD(day, 90, GETDATE()) THEN 1 END) AS ExpiringSoonCount
    FROM credentials
    WHERE employee_id = @EmployeeID
    GROUP BY credential_type;

    RETURN;
END;
GO

-- Usage
SELECT * FROM dbo.GetEmployeeCredentialSummary(12345);
```

**Best Practices**:
- Use inline TVFs when possible (better performance)
- Avoid scalar UDFs in WHERE clauses (performance impact)
- Consider views or CTEs as alternatives
- Document function purpose and parameters

---

## 13. Temporary Tables vs Table Variables

**Temporary Tables**: Session-scoped, support indexes, statistics
**Table Variables**: Function/batch-scoped, limited statistics

**Temporary Table Example**:
```sql
-- Create temporary staging table
CREATE TABLE #CredentialStaging
(
    employee_id INT,
    credential_code NVARCHAR(50),
    expiration_date DATE,
    processed BIT DEFAULT 0,
    INDEX IX_EmployeeID (employee_id),
    INDEX IX_ExpirationDate (expiration_date)
);

-- Load data
INSERT INTO #CredentialStaging (employee_id, credential_code, expiration_date)
SELECT employee_id, credential_code, expiration_date
FROM imported_credentials
WHERE import_batch_id = 12345;

-- Process data
UPDATE #CredentialStaging
SET processed = 1
WHERE expiration_date < GETDATE();

-- Use in complex query
SELECT
    e.employee_id,
    e.full_name,
    cs.credential_code,
    cs.expiration_date
FROM employees e
JOIN #CredentialStaging cs ON e.employee_id = cs.employee_id
WHERE cs.processed = 1;

-- Cleanup (automatic at session end)
DROP TABLE #CredentialStaging;
```

**Table Variable Example**:
```sql
-- For smaller datasets and simple operations
DECLARE @DepartmentStats TABLE
(
    department_id INT PRIMARY KEY,
    employee_count INT,
    avg_salary DECIMAL(10,2)
);

INSERT INTO @DepartmentStats
SELECT
    department_id,
    COUNT(*) AS employee_count,
    AVG(salary) AS avg_salary
FROM employees
WHERE status = 'Active'
GROUP BY department_id;

-- Use immediately
SELECT
    d.department_name,
    ds.employee_count,
    ds.avg_salary
FROM departments d
JOIN @DepartmentStats ds ON d.department_id = ds.department_id
ORDER BY ds.avg_salary DESC;
```

**Best Practices**:
- Use temp tables for large datasets (>1000 rows)
- Use table variables for small result sets and simple logic
- Temp tables support indexes and statistics (better optimization)
- Consider transaction log impact for large temp table operations

---

## 14. Query Performance Tuning

**Key Concepts**:
- Execution plan analysis
- Index optimization
- Query refactoring
- Predicate pushdown

**Execution Plan Analysis**:
```sql
-- Enable actual execution plan
SET STATISTICS TIME ON;
SET STATISTICS IO ON;

-- Your query
SELECT * FROM large_table WHERE complex_condition;

SET STATISTICS IO OFF;
SET STATISTICS TIME OFF;
```

**Index Recommendations**:
```sql
-- Find missing indexes
SELECT
    migs.avg_user_impact,
    migs.avg_total_user_cost,
    migs.user_seeks + migs.user_scans AS total_reads,
    mid.statement AS table_name,
    mid.equality_columns,
    mid.inequality_columns,
    mid.included_columns
FROM sys.dm_db_missing_index_group_stats migs
JOIN sys.dm_db_missing_index_groups mig ON migs.group_handle = mig.index_group_handle
JOIN sys.dm_db_missing_index_details mid ON mig.index_handle = mid.index_handle
WHERE migs.avg_user_impact > 50
ORDER BY migs.avg_total_user_cost * (migs.user_seeks + migs.user_scans) DESC;
```

**Query Refactoring Example**:
```sql
-- BEFORE: Multiple subqueries (slow)
SELECT
    e.employee_id,
    (SELECT COUNT(*) FROM credentials WHERE employee_id = e.employee_id) AS credential_count,
    (SELECT MAX(expiration_date) FROM credentials WHERE employee_id = e.employee_id) AS latest_expiration,
    (SELECT AVG(DATEDIFF(day, issue_date, expiration_date)) FROM credentials WHERE employee_id = e.employee_id) AS avg_validity
FROM employees e;

-- AFTER: Single join with aggregation (fast)
SELECT
    e.employee_id,
    COUNT(c.credential_id) AS credential_count,
    MAX(c.expiration_date) AS latest_expiration,
    AVG(DATEDIFF(day, c.issue_date, c.expiration_date)) AS avg_validity
FROM employees e
LEFT JOIN credentials c ON e.employee_id = c.employee_id
GROUP BY e.employee_id;
```

**Best Practices**:
- Analyze execution plans before optimization
- Focus on high-cost operations first
- Test performance changes with production-size datasets
- Monitor query performance over time

---

## 15. Advanced Data Manipulation

**MERGE Statement** (Upsert Operations):
```sql
-- Synchronize credentials from external source
MERGE INTO credentials AS target
USING external_credentials AS source
ON target.employee_id = source.employee_id
   AND target.credential_code = source.credential_code
WHEN MATCHED AND target.expiration_date <> source.expiration_date THEN
    UPDATE SET
        expiration_date = source.expiration_date,
        last_updated = GETDATE()
WHEN NOT MATCHED BY TARGET THEN
    INSERT (employee_id, credential_code, expiration_date, issue_date)
    VALUES (source.employee_id, source.credential_code, source.expiration_date, source.issue_date)
WHEN NOT MATCHED BY SOURCE AND target.source_system = 'External' THEN
    DELETE
OUTPUT $action, inserted.*, deleted.*;
```

**Bulk Insert with Error Handling**:
```sql
BEGIN TRY
    BEGIN TRANSACTION;

    -- Bulk insert with validation
    INSERT INTO credentials (employee_id, credential_code, issue_date, expiration_date)
    SELECT
        employee_id,
        credential_code,
        issue_date,
        expiration_date
    FROM staging_credentials
    WHERE employee_id IN (SELECT employee_id FROM employees WHERE status = 'Active')
      AND credential_code IS NOT NULL
      AND expiration_date > issue_date;

    COMMIT TRANSACTION;

    PRINT 'Insert successful: ' + CAST(@@ROWCOUNT AS VARCHAR) + ' rows';
END TRY
BEGIN CATCH
    ROLLBACK TRANSACTION;

    PRINT 'Error: ' + ERROR_MESSAGE();

    -- Log error
    INSERT INTO error_log (error_message, error_procedure, error_time)
    VALUES (ERROR_MESSAGE(), ERROR_PROCEDURE(), GETDATE());
END CATCH;
```

**Best Practices**:
- Use MERGE for synchronization operations
- Implement error handling for data integrity
- Consider batch processing for large datasets
- Test with transactions before production deployment

---

## Summary

These 15 advanced SQL techniques provide powerful tools for:
- **Complex data analysis** (Window functions, CTEs)
- **Performance optimization** (Indexing, execution plans)
- **Data transformation** (PIVOT, recursive queries)
- **Business logic implementation** (CASE, UDFs)
- **Error handling and reliability** (Transactions, TRY/CATCH)

**Next Steps**:
1. Practice these techniques on your own datasets
2. Analyze execution plans for your most expensive queries
3. Implement CTEs to simplify complex nested queries
4. Use window functions to replace cursor-based operations
5. Monitor and optimize based on query performance metrics

For detailed HR/education-specific patterns, see `hr_education_patterns.md`.
For query optimization strategies, see `query_optimization.md`.
For common mistakes to avoid, see `sql_antipatterns.md`.
