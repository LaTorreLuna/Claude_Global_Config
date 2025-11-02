#!/usr/bin/env python3
"""
SQL Query Optimizer - Analyzes SQL queries and suggests performance improvements

Dependencies:
    - Python 3.8+
    - sqlparse (pip install sqlparse)

Usage:
    python query_optimizer.py --query "SELECT * FROM employees WHERE YEAR(hire_date) = 2024"
    python query_optimizer.py --file query.sql
    python query_optimizer.py --interactive

Author: Advanced SQL Skill
Date: 2025-10-24
"""

import re
import sys
import argparse
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class OptimizationIssue:
    """Represents a performance issue found in SQL query"""
    severity: str  # 'high', 'medium', 'low'
    issue_type: str
    description: str
    location: str
    suggestion: str
    example_fix: str = ""


class QueryOptimizer:
    """Analyzes SQL queries and provides optimization recommendations"""

    def __init__(self):
        self.issues: List[OptimizationIssue] = []

    def analyze(self, sql_query: str) -> List[OptimizationIssue]:
        """Main analysis function - runs all optimization checks"""
        self.issues = []
        sql_normalized = self._normalize_sql(sql_query)

        # Run all analysis checks
        self._check_select_star(sql_normalized, sql_query)
        self._check_functions_on_columns(sql_normalized, sql_query)
        self._check_leading_wildcards(sql_normalized, sql_query)
        self._check_correlated_subqueries(sql_normalized, sql_query)
        self._check_not_in_usage(sql_normalized, sql_query)
        self._check_implicit_conversions(sql_normalized, sql_query)
        self._check_or_in_joins(sql_normalized, sql_query)
        self._check_distinct_usage(sql_normalized, sql_query)
        self._check_union_vs_union_all(sql_normalized, sql_query)
        self._check_cursor_usage(sql_normalized, sql_query)
        self._check_select_top_without_order(sql_normalized, sql_query)

        return sorted(self.issues, key=lambda x: {'high': 0, 'medium': 1, 'low': 2}[x.severity])

    def _normalize_sql(self, sql: str) -> str:
        """Normalize SQL for easier pattern matching"""
        # Remove comments
        sql = re.sub(r'--[^\n]*', '', sql)
        sql = re.sub(r'/\*.*?\*/', '', sql, flags=re.DOTALL)
        # Normalize whitespace
        sql = re.sub(r'\s+', ' ', sql)
        return sql.strip()

    def _check_select_star(self, sql_normalized: str, sql_original: str):
        """Check for SELECT * usage"""
        pattern = r'\bSELECT\s+\*\s+FROM\b'
        if re.search(pattern, sql_normalized, re.IGNORECASE):
            self.issues.append(OptimizationIssue(
                severity='medium',
                issue_type='SELECT *',
                description='Using SELECT * returns all columns, even those not needed',
                location='SELECT clause',
                suggestion='List only the columns you actually need',
                example_fix="""
-- Instead of:
SELECT * FROM employees WHERE status = 'Active'

-- Use:
SELECT employee_id, first_name, last_name, email
FROM employees
WHERE status = 'Active'
                """
            ))

    def _check_functions_on_columns(self, sql_normalized: str, sql_original: str):
        """Check for functions applied to indexed columns in WHERE clause"""
        # Common function patterns that prevent index usage
        patterns = [
            (r'\bWHERE.*?\b(YEAR|MONTH|DAY|DATEPART)\s*\(', 'Date function on column'),
            (r'\bWHERE.*?\b(UPPER|LOWER|LTRIM|RTRIM|TRIM)\s*\(', 'String function on column'),
            (r'\bWHERE.*?\b(CAST|CONVERT)\s*\(', 'Type conversion on column'),
            (r'\bWHERE.*?\b(SUBSTRING|LEFT|RIGHT)\s*\(', 'String manipulation on column'),
        ]

        for pattern, func_type in patterns:
            if re.search(pattern, sql_normalized, re.IGNORECASE):
                self.issues.append(OptimizationIssue(
                    severity='high',
                    issue_type='Function on Indexed Column',
                    description=f'{func_type} in WHERE clause prevents index usage',
                    location='WHERE clause',
                    suggestion='Rewrite to make the predicate SARGable (Search ARGument-able)',
                    example_fix="""
-- Instead of:
WHERE YEAR(hire_date) = 2024

-- Use range comparison:
WHERE hire_date >= '2024-01-01' AND hire_date < '2025-01-01'

-- Instead of:
WHERE UPPER(email) = 'JOHN@EXAMPLE.COM'

-- Use case-insensitive collation or computed column:
WHERE email = 'john@example.com' COLLATE SQL_Latin1_General_CP1_CI_AS
                    """
                ))

    def _check_leading_wildcards(self, sql_normalized: str, sql_original: str):
        """Check for leading wildcards in LIKE predicates"""
        pattern = r"\bLIKE\s+['\"]%"
        if re.search(pattern, sql_normalized, re.IGNORECASE):
            self.issues.append(OptimizationIssue(
                severity='high',
                issue_type='Leading Wildcard in LIKE',
                description='Leading wildcard (LIKE \'%....\') forces full table scan',
                location='WHERE clause',
                suggestion='Use trailing wildcard or full-text search instead',
                example_fix="""
-- Instead of:
WHERE last_name LIKE '%son'

-- If possible, rewrite with trailing wildcard:
WHERE last_name LIKE 'John%'

-- Or use full-text search:
WHERE CONTAINS(last_name, 'son')
                """
            ))

    def _check_correlated_subqueries(self, sql_normalized: str, sql_original: str):
        """Check for correlated subqueries in SELECT list (N+1 problem)"""
        # Pattern: SELECT ..., (SELECT ... FROM ... WHERE ... = alias.column)
        pattern = r'\bSELECT\s+.*?\(\s*SELECT\s+.*?\bFROM\b.*?\bWHERE\b.*?=\s*\w+\.\w+'
        if re.search(pattern, sql_normalized, re.IGNORECASE | re.DOTALL):
            self.issues.append(OptimizationIssue(
                severity='high',
                issue_type='Correlated Subquery in SELECT',
                description='Subquery executes once per row (N+1 problem), causing severe performance issues',
                location='SELECT list',
                suggestion='Use JOINs or window functions instead',
                example_fix="""
-- Instead of:
SELECT e.employee_id,
       (SELECT COUNT(*) FROM credentials c WHERE c.employee_id = e.employee_id)
FROM employees e

-- Use JOIN with GROUP BY:
WITH CredCounts AS (
    SELECT employee_id, COUNT(*) AS cred_count
    FROM credentials
    GROUP BY employee_id
)
SELECT e.employee_id, ISNULL(cc.cred_count, 0)
FROM employees e
LEFT JOIN CredCounts cc ON e.employee_id = cc.employee_id
                """
            ))

    def _check_not_in_usage(self, sql_normalized: str, sql_original: str):
        """Check for NOT IN with subqueries (NULL handling issue)"""
        pattern = r'\bNOT\s+IN\s*\(\s*SELECT\b'
        if re.search(pattern, sql_normalized, re.IGNORECASE):
            self.issues.append(OptimizationIssue(
                severity='medium',
                issue_type='NOT IN with Subquery',
                description='NOT IN returns no results if subquery contains NULL values',
                location='WHERE clause',
                suggestion='Use NOT EXISTS instead (NULL-safe)',
                example_fix="""
-- Instead of:
WHERE employee_id NOT IN (SELECT manager_id FROM employees)

-- Use NOT EXISTS:
WHERE NOT EXISTS (
    SELECT 1
    FROM employees e2
    WHERE e2.manager_id = employees.employee_id
)
                """
            ))

    def _check_implicit_conversions(self, sql_normalized: str, sql_original: str):
        """Check for potential implicit conversions"""
        # Look for quoted numbers (likely VARCHAR comparison with INT column)
        pattern = r"=\s*['\"][0-9]+['\"]"
        if re.search(pattern, sql_normalized):
            self.issues.append(OptimizationIssue(
                severity='medium',
                issue_type='Potential Implicit Conversion',
                description='Comparing numeric column to quoted number causes implicit conversion',
                location='WHERE clause',
                suggestion='Use correct data type (unquoted for numeric columns)',
                example_fix="""
-- Instead of:
WHERE employee_id = '12345'  -- employee_id is INT

-- Use:
WHERE employee_id = 12345  -- Correct type, no conversion
                """
            ))

    def _check_or_in_joins(self, sql_normalized: str, sql_original: str):
        """Check for OR conditions in JOIN predicates"""
        pattern = r'\bJOIN\b.*?\bON\b.*?\bOR\b'
        if re.search(pattern, sql_normalized, re.IGNORECASE | re.DOTALL):
            self.issues.append(OptimizationIssue(
                severity='high',
                issue_type='OR in JOIN Condition',
                description='OR in JOIN prevents index usage and indicates confused logic',
                location='JOIN clause',
                suggestion='Use separate JOINs or UNION instead',
                example_fix="""
-- Instead of:
FROM employees e
JOIN credentials c ON e.employee_id = c.employee_id
                   OR e.email = c.email_used

-- Use UNION for different join paths:
SELECT ... FROM employees e
JOIN credentials c ON e.employee_id = c.employee_id

UNION ALL

SELECT ... FROM employees e
JOIN credentials c ON e.email = c.email_used
                """
            ))

    def _check_distinct_usage(self, sql_normalized: str, sql_original: str):
        """Check if DISTINCT is being used to hide duplicate problems"""
        # DISTINCT with multiple JOINs often indicates a problem
        if re.search(r'\bSELECT\s+DISTINCT\b', sql_normalized, re.IGNORECASE):
            join_count = len(re.findall(r'\bJOIN\b', sql_normalized, re.IGNORECASE))
            if join_count >= 2:
                self.issues.append(OptimizationIssue(
                    severity='medium',
                    issue_type='DISTINCT with Multiple JOINs',
                    description='DISTINCT may be hiding duplicate rows from incorrect JOINs',
                    location='SELECT clause',
                    suggestion='Fix the root cause instead of using DISTINCT as a band-aid',
                    example_fix="""
-- Review your JOINs to ensure they don't create duplicates
-- Use window functions like ROW_NUMBER to get specific rows:

WITH RankedData AS (
    SELECT ...,
           ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY assignment_date DESC) AS rn
    FROM employees e
    JOIN assignments a ON e.employee_id = a.employee_id
)
SELECT ... FROM RankedData WHERE rn = 1
                    """
                ))

    def _check_union_vs_union_all(self, sql_normalized: str, sql_original: str):
        """Check if UNION should be UNION ALL"""
        if re.search(r'\bUNION\s+(?!ALL\b)', sql_normalized, re.IGNORECASE):
            self.issues.append(OptimizationIssue(
                severity='low',
                issue_type='UNION without ALL',
                description='UNION adds implicit DISTINCT operation (sorting overhead)',
                location='UNION operator',
                suggestion='Use UNION ALL if duplicates are impossible or acceptable',
                example_fix="""
-- If you know there are no duplicates:
SELECT employee_id FROM full_time_employees
UNION ALL  -- Faster, no deduplication
SELECT employee_id FROM part_time_employees

-- Only use UNION if duplicates must be removed
                """
            ))

    def _check_cursor_usage(self, sql_normalized: str, sql_original: str):
        """Check for cursor usage (anti-pattern for set-based operations)"""
        if re.search(r'\bDECLARE\s+\w+\s+CURSOR\b', sql_normalized, re.IGNORECASE):
            self.issues.append(OptimizationIssue(
                severity='high',
                issue_type='Cursor Usage',
                description='Cursors process rows one at a time (10-100x slower than set-based)',
                location='Procedure/Script',
                suggestion='Rewrite using set-based operations',
                example_fix="""
-- Instead of cursor loop:
DECLARE @employee_id INT
DECLARE c CURSOR FOR SELECT employee_id FROM employees
OPEN c
FETCH NEXT FROM c INTO @employee_id
WHILE @@FETCH_STATUS = 0
BEGIN
    UPDATE employees SET salary = salary * 1.03 WHERE employee_id = @employee_id
    FETCH NEXT FROM c INTO @employee_id
END
CLOSE c
DEALLOCATE c

-- Use set-based operation:
UPDATE employees
SET salary = salary * 1.03
WHERE status = 'Active'
                """
            ))

    def _check_select_top_without_order(self, sql_normalized: str, sql_original: str):
        """Check for SELECT TOP without ORDER BY (non-deterministic results)"""
        # Pattern: SELECT TOP ... but no ORDER BY
        if re.search(r'\bSELECT\s+TOP\s+\d+\b', sql_normalized, re.IGNORECASE):
            if not re.search(r'\bORDER\s+BY\b', sql_normalized, re.IGNORECASE):
                self.issues.append(OptimizationIssue(
                    severity='low',
                    issue_type='SELECT TOP without ORDER BY',
                    description='SELECT TOP without ORDER BY returns non-deterministic results',
                    location='SELECT clause',
                    suggestion='Always use ORDER BY with TOP to get consistent results',
                    example_fix="""
-- Instead of:
SELECT TOP 10 * FROM employees

-- Use:
SELECT TOP 10 employee_id, first_name, last_name
FROM employees
ORDER BY hire_date DESC  -- Explicit ordering
                    """
                ))

    def print_report(self):
        """Print formatted optimization report"""
        if not self.issues:
            print("\n✓ No optimization issues found! Query looks good.")
            return

        print(f"\n⚠️  Found {len(self.issues)} optimization issue(s):\n")
        print("=" * 80)

        for i, issue in enumerate(self.issues, 1):
            severity_emoji = {
                'high': '🔴',
                'medium': '🟡',
                'low': '🟢'
            }.get(issue.severity, '⚪')

            print(f"\n{i}. {severity_emoji} {issue.issue_type} [{issue.severity.upper()} SEVERITY]")
            print(f"   Location: {issue.location}")
            print(f"   Issue: {issue.description}")
            print(f"   Suggestion: {issue.suggestion}")

            if issue.example_fix:
                print(f"\n   Example Fix:{issue.example_fix}")

            print("-" * 80)

    def suggest_indexes(self, sql_normalized: str):
        """Suggest potential indexes based on WHERE and JOIN clauses"""
        print("\n📊 Index Suggestions:")
        print("=" * 80)

        # Extract WHERE clause columns
        where_match = re.search(r'\bWHERE\b(.*?)(?:\bGROUP\s+BY\b|\bORDER\s+BY\b|\bHAVING\b|$)',
                                sql_normalized, re.IGNORECASE | re.DOTALL)
        if where_match:
            where_clause = where_match.group(1)
            # Extract column references (table.column or just column)
            columns = re.findall(r'\b(\w+)\.(\w+)\b|\b(\w+)\s*=', where_clause)
            unique_cols = set()
            for match in columns:
                if match[0] and match[1]:  # table.column
                    unique_cols.add(f"{match[0]}.{match[1]}")
                elif match[2]:  # just column
                    unique_cols.add(match[2])

            if unique_cols:
                print("\nConsider indexes on WHERE clause columns:")
                for col in sorted(unique_cols):
                    print(f"  • {col}")

        # Extract JOIN columns
        join_matches = re.findall(r'\bJOIN\b.*?\bON\b(.*?)(?:\bWHERE\b|\bJOIN\b|$)',
                                  sql_normalized, re.IGNORECASE | re.DOTALL)
        if join_matches:
            print("\nConsider indexes on JOIN columns:")
            for join_clause in join_matches:
                columns = re.findall(r'\b(\w+)\.(\w+)\b', join_clause)
                for table, col in columns:
                    print(f"  • {table}.{col} (foreign key index)")

        print("\nNote: These are suggestions based on query structure.")
        print("Verify with execution plans and actual query performance.\n")


def main():
    parser = argparse.ArgumentParser(
        description='Analyze SQL queries for performance optimization opportunities',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python query_optimizer.py --query "SELECT * FROM employees WHERE YEAR(hire_date) = 2024"
  python query_optimizer.py --file query.sql
  python query_optimizer.py --interactive
        """
    )

    parser.add_argument('--query', '-q', help='SQL query string to analyze')
    parser.add_argument('--file', '-f', help='File containing SQL query')
    parser.add_argument('--interactive', '-i', action='store_true',
                        help='Interactive mode - paste query and press Ctrl+D (Unix) or Ctrl+Z (Windows)')
    parser.add_argument('--suggest-indexes', action='store_true',
                        help='Suggest potential indexes based on query')

    args = parser.parse_args()

    # Get SQL query from appropriate source
    sql_query = None
    if args.query:
        sql_query = args.query
    elif args.file:
        try:
            with open(args.file, 'r') as f:
                sql_query = f.read()
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found")
            sys.exit(1)
    elif args.interactive or not sys.stdin.isatty():
        print("Enter SQL query (Ctrl+D on Unix or Ctrl+Z on Windows to finish):")
        sql_query = sys.stdin.read()
    else:
        parser.print_help()
        sys.exit(1)

    if not sql_query or not sql_query.strip():
        print("Error: No SQL query provided")
        sys.exit(1)

    # Analyze query
    optimizer = QueryOptimizer()
    optimizer.analyze(sql_query)
    optimizer.print_report()

    # Optionally suggest indexes
    if args.suggest_indexes:
        optimizer.suggest_indexes(optimizer._normalize_sql(sql_query))


if __name__ == '__main__':
    main()
