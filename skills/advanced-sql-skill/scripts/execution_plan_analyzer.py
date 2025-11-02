#!/usr/bin/env python3
"""
SQL Execution Plan Analyzer - Parses and analyzes SQL Server execution plans

Dependencies:
    - Python 3.8+
    - lxml (pip install lxml)

Usage:
    python execution_plan_analyzer.py --file execution_plan.sqlplan
    python execution_plan_analyzer.py --file plan.xml --threshold 10

Features:
    - Identifies expensive operators (>10% cost by default)
    - Detects table scans and index scans
    - Finds missing indexes
    - Highlights implicit conversions
    - Reports on key lookup operations
    - Analyzes parallelism and blocking operators

Author: Advanced SQL Skill
Date: 2025-10-24
"""

import sys
import argparse
import xml.etree.ElementTree as ET
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class OperatorInfo:
    """Information about an operator in the execution plan"""
    name: str
    cost_percentage: float
    estimated_rows: int
    actual_rows: Optional[int]
    object_name: str
    index_name: str
    warnings: List[str]
    details: Dict[str, str]


@dataclass
class MissingIndex:
    """Information about a missing index suggestion"""
    impact: float
    table_name: str
    equality_columns: List[str]
    inequality_columns: List[str]
    included_columns: List[str]
    create_statement: str


class ExecutionPlanAnalyzer:
    """Analyzes SQL Server execution plans (XML format)"""

    # SQL Server execution plan namespace
    NAMESPACES = {
        'p': 'http://schemas.microsoft.com/sqlserver/2004/07/showplan'
    }

    def __init__(self, threshold_percentage: float = 10.0):
        self.threshold_percentage = threshold_percentage
        self.expensive_operators: List[OperatorInfo] = []
        self.missing_indexes: List[MissingIndex] = []
        self.warnings: List[str] = []
        self.total_cost: float = 0.0

    def analyze_file(self, file_path: str):
        """Analyze execution plan from file"""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            self.analyze_plan(root)
        except ET.ParseError as e:
            print(f"Error parsing XML file: {e}")
            sys.exit(1)
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found")
            sys.exit(1)

    def analyze_plan(self, root: ET.Element):
        """Analyze execution plan XML"""
        # Find all RelOp elements (operators)
        self._extract_total_cost(root)
        self._analyze_operators(root)
        self._extract_missing_indexes(root)
        self._extract_warnings(root)

    def _extract_total_cost(self, root: ET.Element):
        """Extract total query cost"""
        # Look for StatementSubTreeCost
        for stmt in root.findall('.//p:StmtSimple', self.NAMESPACES):
            cost = stmt.get('StatementSubTreeCost')
            if cost:
                self.total_cost = float(cost)
                break

    def _analyze_operators(self, root: ET.Element):
        """Analyze all operators in the plan"""
        for relop in root.findall('.//p:RelOp', self.NAMESPACES):
            operator_info = self._extract_operator_info(relop)
            if operator_info and operator_info.cost_percentage >= self.threshold_percentage:
                self.expensive_operators.append(operator_info)

            # Check for specific problem operators
            self._check_problem_operators(relop, operator_info)

    def _extract_operator_info(self, relop: ET.Element) -> Optional[OperatorInfo]:
        """Extract information from a RelOp element"""
        physical_op = relop.get('PhysicalOp', '')
        estimated_cost = float(relop.get('EstimatedTotalSubtreeCost', 0))
        estimated_rows = int(float(relop.get('EstimateRows', 0)))

        # Calculate cost percentage
        cost_percentage = 0.0
        if self.total_cost > 0:
            cost_percentage = (estimated_cost / self.total_cost) * 100

        # Extract object and index names
        object_name = ''
        index_name = ''
        for obj in relop.findall('.//p:Object', self.NAMESPACES):
            object_name = obj.get('Table', obj.get('Index', ''))
            index_name = obj.get('Index', '')

        # Extract warnings
        warnings = []
        for warning in relop.findall('.//p:Warnings', self.NAMESPACES):
            for column in warning.findall('.//p:ColumnsWithNoStatistics', self.NAMESPACES):
                for col in column.findall('.//p:ColumnReference', self.NAMESPACES):
                    col_name = col.get('Column', '')
                    warnings.append(f"No statistics on column: {col_name}")

        # Extract actual rows if available (from actual execution plan)
        actual_rows = None
        actual_rows_attr = relop.get('ActualRows')
        if actual_rows_attr:
            actual_rows = int(float(actual_rows_attr))

        details = {
            'logical_op': relop.get('LogicalOp', ''),
            'physical_op': physical_op,
            'estimated_cost': f"{estimated_cost:.4f}",
            'estimated_cpu': relop.get('EstimateCPU', '0'),
            'estimated_io': relop.get('EstimateIO', '0'),
        }

        return OperatorInfo(
            name=physical_op,
            cost_percentage=cost_percentage,
            estimated_rows=estimated_rows,
            actual_rows=actual_rows,
            object_name=object_name,
            index_name=index_name,
            warnings=warnings,
            details=details
        )

    def _check_problem_operators(self, relop: ET.Element, operator_info: Optional[OperatorInfo]):
        """Check for specific problematic operators"""
        if not operator_info:
            return

        physical_op = operator_info.name

        # Table Scan (full table read - very expensive)
        if physical_op == 'Table Scan':
            self.warnings.append(
                f"🔴 TABLE SCAN on {operator_info.object_name} "
                f"({operator_info.estimated_rows:,} rows, {operator_info.cost_percentage:.1f}% cost) - "
                f"Consider adding an index"
            )

        # Clustered Index Scan (reading entire index)
        elif physical_op == 'Clustered Index Scan':
            if operator_info.cost_percentage > 20:
                self.warnings.append(
                    f"🟡 CLUSTERED INDEX SCAN on {operator_info.object_name} "
                    f"({operator_info.estimated_rows:,} rows, {operator_info.cost_percentage:.1f}% cost) - "
                    f"Consider adding a non-clustered index"
                )

        # Key Lookup (bookmark lookup - requires nested loop)
        elif physical_op == 'Key Lookup' or physical_op == 'RID Lookup':
            self.warnings.append(
                f"🟡 KEY LOOKUP on {operator_info.object_name} "
                f"({operator_info.estimated_rows:,} rows, {operator_info.cost_percentage:.1f}% cost) - "
                f"Consider creating a covering index with INCLUDE columns"
            )

        # Sort operator (expensive for large result sets)
        elif physical_op == 'Sort':
            if operator_info.estimated_rows > 100000:
                self.warnings.append(
                    f"🟡 SORT operation on {operator_info.estimated_rows:,} rows "
                    f"({operator_info.cost_percentage:.1f}% cost) - "
                    f"Consider adding an index to avoid sorting"
                )

        # Hash Match (expensive for large joins)
        elif physical_op == 'Hash Match':
            if operator_info.cost_percentage > 25:
                self.warnings.append(
                    f"🟡 HASH MATCH join "
                    f"({operator_info.estimated_rows:,} rows, {operator_info.cost_percentage:.1f}% cost) - "
                    f"Consider adding indexes to enable merge or nested loop joins"
                )

        # Implicit conversion warning
        if operator_info.warnings:
            for warning in operator_info.warnings:
                if 'CONVERT_IMPLICIT' in warning.upper():
                    self.warnings.append(
                        f"🔴 IMPLICIT CONVERSION on {operator_info.object_name} - "
                        f"Prevents index usage and degrades performance"
                    )

        # Row count estimation issues (actual vs estimated)
        if operator_info.actual_rows is not None and operator_info.estimated_rows > 0:
            ratio = operator_info.actual_rows / operator_info.estimated_rows
            if ratio > 10 or ratio < 0.1:  # 10x difference
                self.warnings.append(
                    f"🟡 ROW ESTIMATION ERROR on {operator_info.object_name}: "
                    f"estimated {operator_info.estimated_rows:,}, actual {operator_info.actual_rows:,} - "
                    f"Update statistics or check for parameter sniffing"
                )

    def _extract_missing_indexes(self, root: ET.Element):
        """Extract missing index recommendations"""
        for missing_idx in root.findall('.//p:MissingIndexes/p:MissingIndexGroup', self.NAMESPACES):
            impact = float(missing_idx.get('Impact', 0))

            for idx in missing_idx.findall('.//p:MissingIndex', self.NAMESPACES):
                table = idx.get('Table', '').strip('[]')

                # Extract column groups
                equality_cols = []
                inequality_cols = []
                included_cols = []

                for col_group in idx.findall('.//p:ColumnGroup', self.NAMESPACES):
                    usage = col_group.get('Usage', '')
                    columns = [col.get('Name', '').strip('[]')
                               for col in col_group.findall('.//p:Column', self.NAMESPACES)]

                    if usage == 'EQUALITY':
                        equality_cols = columns
                    elif usage == 'INEQUALITY':
                        inequality_cols = columns
                    elif usage == 'INCLUDE':
                        included_cols = columns

                # Generate CREATE INDEX statement
                create_stmt = self._generate_create_index(table, equality_cols, inequality_cols, included_cols)

                self.missing_indexes.append(MissingIndex(
                    impact=impact,
                    table_name=table,
                    equality_columns=equality_cols,
                    inequality_columns=inequality_cols,
                    included_columns=included_cols,
                    create_statement=create_stmt
                ))

    def _generate_create_index(self, table: str, equality: List[str],
                                inequality: List[str], included: List[str]) -> str:
        """Generate CREATE INDEX statement"""
        # Clean table name
        table_parts = table.split('.')
        if len(table_parts) >= 2:
            table_name = table_parts[-1]
        else:
            table_name = table

        # Generate index name
        index_name = f"IX_{table_name}_{'_'.join(equality[:3])}".replace('[', '').replace(']', '')
        if len(index_name) > 60:
            index_name = index_name[:60]

        # Build column list
        key_columns = equality + inequality
        key_cols_str = ', '.join(f"[{col}]" for col in key_columns)

        # Build INCLUDE clause
        include_clause = ''
        if included:
            include_cols_str = ', '.join(f"[{col}]" for col in included)
            include_clause = f"\nINCLUDE ({include_cols_str})"

        return f"CREATE NONCLUSTERED INDEX {index_name}\nON {table} ({key_cols_str}){include_clause};"

    def _extract_warnings(self, root: ET.Element):
        """Extract general warnings from the plan"""
        for warning in root.findall('.//p:Warnings', self.NAMESPACES):
            # No join predicate
            if warning.find('.//p:NoJoinPredicate', self.NAMESPACES) is not None:
                self.warnings.append(
                    "🔴 NO JOIN PREDICATE - Cartesian product detected! "
                    "This will multiply all rows from both tables."
                )

            # Unmatched indexes
            for unmatched in warning.findall('.//p:UnmatchedIndexes', self.NAMESPACES):
                self.warnings.append(
                    "🟡 UNMATCHED INDEXES - Some indexes could not be matched to query"
                )

    def print_report(self):
        """Print formatted analysis report"""
        print("\n" + "=" * 80)
        print("EXECUTION PLAN ANALYSIS REPORT")
        print("=" * 80)

        # Summary
        print(f"\n📊 Summary:")
        print(f"   Total Query Cost: {self.total_cost:.4f}")
        print(f"   Expensive Operators (>{self.threshold_percentage}%): {len(self.expensive_operators)}")
        print(f"   Missing Indexes: {len(self.missing_indexes)}")
        print(f"   Warnings: {len(self.warnings)}")

        # Expensive operators
        if self.expensive_operators:
            print(f"\n🔥 Expensive Operators (>{self.threshold_percentage}% cost):")
            print("-" * 80)
            for op in sorted(self.expensive_operators, key=lambda x: x.cost_percentage, reverse=True):
                print(f"\n   Operator: {op.name}")
                print(f"   Cost: {op.cost_percentage:.1f}%")
                print(f"   Object: {op.object_name or 'N/A'}")
                if op.index_name:
                    print(f"   Index: {op.index_name}")
                print(f"   Estimated Rows: {op.estimated_rows:,}")
                if op.actual_rows is not None:
                    print(f"   Actual Rows: {op.actual_rows:,}")
                if op.warnings:
                    for warning in op.warnings:
                        print(f"   ⚠️  {warning}")

        # Warnings
        if self.warnings:
            print(f"\n⚠️  Warnings and Recommendations:")
            print("-" * 80)
            for i, warning in enumerate(self.warnings, 1):
                print(f"\n{i}. {warning}")

        # Missing indexes
        if self.missing_indexes:
            print(f"\n📋 Missing Index Recommendations:")
            print("-" * 80)
            for i, idx in enumerate(sorted(self.missing_indexes, key=lambda x: x.impact, reverse=True), 1):
                print(f"\n{i}. Table: {idx.table_name}")
                print(f"   Impact: {idx.impact:.1f}%")
                if idx.equality_columns:
                    print(f"   Equality Columns: {', '.join(idx.equality_columns)}")
                if idx.inequality_columns:
                    print(f"   Inequality Columns: {', '.join(idx.inequality_columns)}")
                if idx.included_columns:
                    print(f"   Include Columns: {', '.join(idx.included_columns)}")
                print(f"\n   Suggested Index:\n   {idx.create_statement}")

        # Best practices
        print(f"\n💡 Best Practices:")
        print("-" * 80)
        print("1. Focus on operators with >25% cost first")
        print("2. Table scans and index scans indicate missing indexes")
        print("3. Key lookups can be fixed with covering indexes (INCLUDE clause)")
        print("4. Implicit conversions prevent index usage - match data types")
        print("5. Large row estimation errors suggest outdated statistics")
        print("6. Test index changes in non-production environment first")

        print("\n" + "=" * 80 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='Analyze SQL Server execution plans for performance issues',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python execution_plan_analyzer.py --file execution_plan.sqlplan
  python execution_plan_analyzer.py --file plan.xml --threshold 5

How to get execution plan:
  1. In SQL Server Management Studio:
     - Right-click query → "Include Actual Execution Plan" (Ctrl+M)
     - Execute query
     - Right-click execution plan → "Save Execution Plan As..." → Save as .sqlplan

  2. Via T-SQL:
     SET SHOWPLAN_XML ON;
     GO
     -- Your query here
     GO
     SET SHOWPLAN_XML OFF;
     -- Copy XML output to file
        """
    )

    parser.add_argument('--file', '-f', required=True, help='Execution plan file (.sqlplan or .xml)')
    parser.add_argument('--threshold', '-t', type=float, default=10.0,
                        help='Cost percentage threshold for expensive operators (default: 10.0)')

    args = parser.parse_args()

    # Validate file exists
    if not Path(args.file).exists():
        print(f"Error: File '{args.file}' not found")
        sys.exit(1)

    # Analyze execution plan
    print(f"\nAnalyzing execution plan: {args.file}")
    analyzer = ExecutionPlanAnalyzer(threshold_percentage=args.threshold)
    analyzer.analyze_file(args.file)
    analyzer.print_report()


if __name__ == '__main__':
    main()
