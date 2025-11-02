#!/usr/bin/env python3
"""
SQL Schema Documenter - Generates markdown documentation from database schemas

Dependencies:
    - Python 3.8+
    - pyodbc (SQL Server: pip install pyodbc)
    - psycopg2 (PostgreSQL: pip install psycopg2-binary)
    - mysql-connector-python (MySQL: pip install mysql-connector-python)

Usage:
    python schema_documenter.py --server localhost --database mydb --output schema.md
    python schema_documenter.py --server localhost --database mydb --postgres --username myuser
    python schema_documenter.py --connection "Server=localhost;Database=mydb;Trusted_Connection=yes;"

Features:
    - Generates markdown documentation for all tables and views
    - Documents columns (types, nullability, defaults, descriptions)
    - Lists primary keys and foreign key relationships
    - Documents indexes and their columns
    - Creates entity-relationship diagram (Mermaid syntax)
    - Identifies missing indexes on foreign keys
    - Calculates table/index sizes

Author: Advanced SQL Skill
Date: 2025-10-24
"""

import sys
import argparse
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Column:
    """Database column information"""
    name: str
    data_type: str
    max_length: Optional[int]
    precision: Optional[int]
    scale: Optional[int]
    is_nullable: bool
    default_value: Optional[str]
    description: Optional[str]
    is_primary_key: bool
    is_foreign_key: bool


@dataclass
class ForeignKey:
    """Foreign key relationship"""
    name: str
    from_table: str
    from_column: str
    to_table: str
    to_column: str


@dataclass
class Index:
    """Index information"""
    name: str
    table_name: str
    columns: List[str]
    is_unique: bool
    is_primary_key: bool
    included_columns: List[str]
    filter_definition: Optional[str]


@dataclass
class Table:
    """Database table information"""
    schema: str
    name: str
    type: str  # 'TABLE' or 'VIEW'
    row_count: Optional[int]
    data_size_kb: Optional[float]
    index_size_kb: Optional[float]
    columns: List[Column]
    primary_key: Optional[str]
    foreign_keys: List[ForeignKey]
    indexes: List[Index]
    description: Optional[str]


class SchemaDocumenter:
    """Generates markdown documentation from database schema"""

    def __init__(self, connection_string: str = None, db_type: str = 'sqlserver'):
        self.connection_string = connection_string
        self.db_type = db_type
        self.conn = None
        self.tables: List[Table] = []

    def connect(self):
        """Establish database connection"""
        try:
            if self.db_type == 'sqlserver':
                import pyodbc
                self.conn = pyodbc.connect(self.connection_string)
            elif self.db_type == 'postgres':
                import psycopg2
                self.conn = psycopg2.connect(self.connection_string)
            elif self.db_type == 'mysql':
                import mysql.connector
                # Parse connection string for MySQL
                parts = dict(item.split('=') for item in self.connection_string.split(';') if '=' in item)
                self.conn = mysql.connector.connect(
                    host=parts.get('Server', 'localhost'),
                    database=parts.get('Database', ''),
                    user=parts.get('Username', ''),
                    password=parts.get('Password', '')
                )
        except ImportError as e:
            print(f"Error: Required database driver not installed. {e}")
            print("Install: pip install pyodbc (SQL Server) or psycopg2-binary (PostgreSQL) or mysql-connector-python (MySQL)")
            sys.exit(1)
        except Exception as e:
            print(f"Error connecting to database: {e}")
            sys.exit(1)

    def extract_schema(self):
        """Extract complete schema information"""
        if not self.conn:
            self.connect()

        cursor = self.conn.cursor()

        # Get all tables and views
        tables_query = self._get_tables_query()
        cursor.execute(tables_query)

        for row in cursor.fetchall():
            schema = row[0]
            table_name = row[1]
            table_type = row[2]

            table = Table(
                schema=schema,
                name=table_name,
                type=table_type,
                row_count=None,
                data_size_kb=None,
                index_size_kb=None,
                columns=[],
                primary_key=None,
                foreign_keys=[],
                indexes=[],
                description=None
            )

            # Get columns
            table.columns = self._get_columns(schema, table_name, cursor)

            # Get primary key
            table.primary_key = self._get_primary_key(schema, table_name, cursor)

            # Get foreign keys
            table.foreign_keys = self._get_foreign_keys(schema, table_name, cursor)

            # Get indexes
            table.indexes = self._get_indexes(schema, table_name, cursor)

            # Get table size (SQL Server only for now)
            if self.db_type == 'sqlserver':
                table.row_count, table.data_size_kb, table.index_size_kb = \
                    self._get_table_size(schema, table_name, cursor)

            self.tables.append(table)

        cursor.close()

    def _get_tables_query(self) -> str:
        """Get query to retrieve tables and views"""
        if self.db_type == 'sqlserver':
            return """
                SELECT s.name AS schema_name,
                       t.name AS table_name,
                       t.type_desc AS table_type
                FROM sys.tables t
                INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
                WHERE s.name NOT IN ('sys', 'INFORMATION_SCHEMA')

                UNION ALL

                SELECT s.name AS schema_name,
                       v.name AS view_name,
                       'VIEW' AS table_type
                FROM sys.views v
                INNER JOIN sys.schemas s ON v.schema_id = s.schema_id
                WHERE s.name NOT IN ('sys', 'INFORMATION_SCHEMA')

                ORDER BY schema_name, table_name
            """
        elif self.db_type == 'postgres':
            return """
                SELECT table_schema, table_name, table_type
                FROM information_schema.tables
                WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
                ORDER BY table_schema, table_name
            """
        elif self.db_type == 'mysql':
            return """
                SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE
                FROM information_schema.TABLES
                WHERE TABLE_SCHEMA NOT IN ('mysql', 'information_schema', 'performance_schema', 'sys')
                ORDER BY TABLE_SCHEMA, TABLE_NAME
            """

    def _get_columns(self, schema: str, table: str, cursor) -> List[Column]:
        """Get column information for a table"""
        if self.db_type == 'sqlserver':
            query = """
                SELECT
                    c.name AS column_name,
                    t.name AS data_type,
                    c.max_length,
                    c.precision,
                    c.scale,
                    c.is_nullable,
                    dc.definition AS default_value,
                    CAST(ep.value AS NVARCHAR(500)) AS description,
                    CASE WHEN pk.column_id IS NOT NULL THEN 1 ELSE 0 END AS is_primary_key,
                    CASE WHEN fk.parent_column_id IS NOT NULL THEN 1 ELSE 0 END AS is_foreign_key
                FROM sys.columns c
                INNER JOIN sys.types t ON c.user_type_id = t.user_type_id
                INNER JOIN sys.tables tbl ON c.object_id = tbl.object_id
                INNER JOIN sys.schemas s ON tbl.schema_id = s.schema_id
                LEFT JOIN sys.default_constraints dc ON c.default_object_id = dc.object_id
                LEFT JOIN sys.extended_properties ep ON c.object_id = ep.major_id
                                                      AND c.column_id = ep.minor_id
                                                      AND ep.name = 'MS_Description'
                LEFT JOIN (
                    SELECT ic.object_id, ic.column_id
                    FROM sys.index_columns ic
                    INNER JOIN sys.indexes i ON ic.object_id = i.object_id AND ic.index_id = i.index_id
                    WHERE i.is_primary_key = 1
                ) pk ON c.object_id = pk.object_id AND c.column_id = pk.column_id
                LEFT JOIN sys.foreign_key_columns fk ON c.object_id = fk.parent_object_id
                                                      AND c.column_id = fk.parent_column_id
                WHERE s.name = ? AND tbl.name = ?
                ORDER BY c.column_id
            """
            cursor.execute(query, (schema, table))
        elif self.db_type == 'postgres':
            query = """
                SELECT column_name, data_type, character_maximum_length,
                       numeric_precision, numeric_scale, is_nullable, column_default,
                       NULL as description, 0 as is_primary_key, 0 as is_foreign_key
                FROM information_schema.columns
                WHERE table_schema = %s AND table_name = %s
                ORDER BY ordinal_position
            """
            cursor.execute(query, (schema, table))

        columns = []
        for row in cursor.fetchall():
            col = Column(
                name=row[0],
                data_type=row[1],
                max_length=row[2] if row[2] != -1 else None,
                precision=row[3],
                scale=row[4],
                is_nullable=bool(row[5]),
                default_value=row[6],
                description=row[7],
                is_primary_key=bool(row[8]),
                is_foreign_key=bool(row[9])
            )
            columns.append(col)

        return columns

    def _get_primary_key(self, schema: str, table: str, cursor) -> Optional[str]:
        """Get primary key name"""
        if self.db_type == 'sqlserver':
            query = """
                SELECT kc.name
                FROM sys.key_constraints kc
                INNER JOIN sys.tables t ON kc.parent_object_id = t.object_id
                INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
                WHERE kc.type = 'PK' AND s.name = ? AND t.name = ?
            """
            cursor.execute(query, (schema, table))
            row = cursor.fetchone()
            return row[0] if row else None
        return None

    def _get_foreign_keys(self, schema: str, table: str, cursor) -> List[ForeignKey]:
        """Get foreign key relationships"""
        if self.db_type == 'sqlserver':
            query = """
                SELECT
                    fk.name AS fk_name,
                    OBJECT_NAME(fk.parent_object_id) AS from_table,
                    COL_NAME(fkc.parent_object_id, fkc.parent_column_id) AS from_column,
                    OBJECT_NAME(fk.referenced_object_id) AS to_table,
                    COL_NAME(fkc.referenced_object_id, fkc.referenced_column_id) AS to_column
                FROM sys.foreign_keys fk
                INNER JOIN sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
                INNER JOIN sys.tables t ON fk.parent_object_id = t.object_id
                INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
                WHERE s.name = ? AND t.name = ?
            """
            cursor.execute(query, (schema, table))

            fks = []
            for row in cursor.fetchall():
                fk = ForeignKey(
                    name=row[0],
                    from_table=row[1],
                    from_column=row[2],
                    to_table=row[3],
                    to_column=row[4]
                )
                fks.append(fk)
            return fks
        return []

    def _get_indexes(self, schema: str, table: str, cursor) -> List[Index]:
        """Get index information"""
        if self.db_type == 'sqlserver':
            query = """
                SELECT
                    i.name AS index_name,
                    i.is_unique,
                    i.is_primary_key,
                    i.filter_definition,
                    STRING_AGG(CASE WHEN ic.is_included_column = 0 THEN c.name ELSE NULL END, ', ')
                        WITHIN GROUP (ORDER BY ic.key_ordinal) AS key_columns,
                    STRING_AGG(CASE WHEN ic.is_included_column = 1 THEN c.name ELSE NULL END, ', ')
                        AS included_columns
                FROM sys.indexes i
                INNER JOIN sys.index_columns ic ON i.object_id = ic.object_id AND i.index_id = ic.index_id
                INNER JOIN sys.columns c ON ic.object_id = c.object_id AND ic.column_id = c.column_id
                INNER JOIN sys.tables t ON i.object_id = t.object_id
                INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
                WHERE s.name = ? AND t.name = ? AND i.type > 0
                GROUP BY i.name, i.is_unique, i.is_primary_key, i.filter_definition
                ORDER BY i.name
            """
            cursor.execute(query, (schema, table))

            indexes = []
            for row in cursor.fetchall():
                idx = Index(
                    name=row[0],
                    table_name=table,
                    columns=row[4].split(', ') if row[4] else [],
                    is_unique=bool(row[1]),
                    is_primary_key=bool(row[2]),
                    included_columns=row[5].split(', ') if row[5] else [],
                    filter_definition=row[3]
                )
                indexes.append(idx)
            return indexes
        return []

    def _get_table_size(self, schema: str, table: str, cursor) -> Tuple[int, float, float]:
        """Get table size information (SQL Server only)"""
        query = """
            SELECT
                SUM(p.rows) AS row_count,
                SUM(a.total_pages) * 8 AS total_space_kb,
                SUM(a.used_pages) * 8 AS data_space_kb
            FROM sys.tables t
            INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
            INNER JOIN sys.indexes i ON t.object_id = i.object_id
            INNER JOIN sys.partitions p ON i.object_id = p.object_id AND i.index_id = p.index_id
            INNER JOIN sys.allocation_units a ON p.partition_id = a.container_id
            WHERE s.name = ? AND t.name = ?
            GROUP BY t.name
        """
        cursor.execute(query, (schema, table))
        row = cursor.fetchone()
        if row:
            return int(row[0] or 0), float(row[2] or 0), float((row[1] or 0) - (row[2] or 0))
        return 0, 0.0, 0.0

    def generate_markdown(self, output_file: str, database_name: str):
        """Generate markdown documentation"""
        with open(output_file, 'w', encoding='utf-8') as f:
            # Header
            f.write(f"# Database Schema Documentation\n\n")
            f.write(f"**Database:** {database_name}\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Total Tables:** {len([t for t in self.tables if t.type == 'TABLE'])}\n\n")
            f.write(f"**Total Views:** {len([t for t in self.tables if t.type == 'VIEW'])}\n\n")

            # Table of Contents
            f.write("## Table of Contents\n\n")
            for table in sorted(self.tables, key=lambda x: (x.schema, x.name)):
                f.write(f"- [{table.schema}.{table.name}](#{table.schema.lower()}{table.name.lower()})\n")
            f.write("\n---\n\n")

            # Entity-Relationship Diagram (Mermaid)
            f.write("## Entity-Relationship Diagram\n\n")
            f.write("```mermaid\nerDiagram\n")
            for table in self.tables:
                if table.type == 'TABLE':
                    for fk in table.foreign_keys:
                        f.write(f"    {fk.from_table} ||--o{{ {fk.to_table} : \"{fk.name}\"\n")
            f.write("```\n\n---\n\n")

            # Table Details
            f.write("## Table Details\n\n")
            for table in sorted(self.tables, key=lambda x: (x.schema, x.name)):
                self._write_table_documentation(f, table)

            # Missing Index Report
            self._write_missing_index_report(f)

        print(f"\n✅ Schema documentation generated: {output_file}")

    def _write_table_documentation(self, f, table: Table):
        """Write documentation for a single table"""
        f.write(f"### {table.schema}.{table.name}\n\n")

        if table.description:
            f.write(f"**Description:** {table.description}\n\n")

        f.write(f"**Type:** {table.type}\n\n")

        if table.row_count is not None:
            f.write(f"**Row Count:** {table.row_count:,}\n\n")
            f.write(f"**Data Size:** {table.data_size_kb / 1024:.2f} MB\n\n")
            f.write(f"**Index Size:** {table.index_size_kb / 1024:.2f} MB\n\n")

        # Columns
        f.write("#### Columns\n\n")
        f.write("| Column | Type | Nullable | Default | Description | Keys |\n")
        f.write("|--------|------|----------|---------|-------------|------|\n")

        for col in table.columns:
            type_str = col.data_type
            if col.max_length and col.max_length > 0:
                type_str += f"({col.max_length})"
            elif col.precision:
                type_str += f"({col.precision},{col.scale})"

            nullable = "Yes" if col.is_nullable else "No"
            default = col.default_value or ""
            description = col.description or ""

            keys = []
            if col.is_primary_key:
                keys.append("PK")
            if col.is_foreign_key:
                keys.append("FK")
            keys_str = ", ".join(keys)

            f.write(f"| {col.name} | {type_str} | {nullable} | {default} | {description} | {keys_str} |\n")

        f.write("\n")

        # Primary Key
        if table.primary_key:
            f.write(f"**Primary Key:** {table.primary_key}\n\n")

        # Foreign Keys
        if table.foreign_keys:
            f.write("#### Foreign Keys\n\n")
            for fk in table.foreign_keys:
                f.write(f"- **{fk.name}**: {fk.from_column} → {fk.to_table}.{fk.to_column}\n")
            f.write("\n")

        # Indexes
        if table.indexes:
            f.write("#### Indexes\n\n")
            f.write("| Index Name | Type | Columns | Included Columns | Filter |\n")
            f.write("|------------|------|---------|------------------|--------|\n")

            for idx in table.indexes:
                idx_type = []
                if idx.is_primary_key:
                    idx_type.append("PK")
                if idx.is_unique:
                    idx_type.append("UNIQUE")
                if not idx_type:
                    idx_type.append("NONCLUSTERED")

                type_str = ", ".join(idx_type)
                cols_str = ", ".join(idx.columns)
                included_str = ", ".join(idx.included_columns) if idx.included_columns else ""
                filter_str = idx.filter_definition or ""

                f.write(f"| {idx.name} | {type_str} | {cols_str} | {included_str} | {filter_str} |\n")

            f.write("\n")

        f.write("---\n\n")

    def _write_missing_index_report(self, f):
        """Write report on foreign keys without indexes"""
        f.write("## Missing Index Report\n\n")
        f.write("Foreign keys without supporting indexes:\n\n")

        missing_count = 0
        for table in self.tables:
            for fk in table.foreign_keys:
                # Check if foreign key column has an index
                has_index = any(fk.from_column in idx.columns for idx in table.indexes)
                if not has_index:
                    missing_count += 1
                    f.write(f"- **{table.schema}.{table.name}.{fk.from_column}** (FK to {fk.to_table}.{fk.to_column})\n")
                    f.write(f"  ```sql\n")
                    f.write(f"  CREATE NONCLUSTERED INDEX IX_{table.name}_{fk.from_column}\n")
                    f.write(f"  ON {table.schema}.{table.name}({fk.from_column});\n")
                    f.write(f"  ```\n\n")

        if missing_count == 0:
            f.write("✅ All foreign keys have supporting indexes!\n\n")
        else:
            f.write(f"\n⚠️  Found {missing_count} foreign key(s) without indexes.\n\n")


def main():
    parser = argparse.ArgumentParser(
        description='Generate markdown documentation from database schema',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # SQL Server with Windows Authentication
  python schema_documenter.py --server localhost --database AdventureWorks --output docs.md

  # SQL Server with SQL Authentication
  python schema_documenter.py --server localhost --database mydb --username sa --password MyPass --output docs.md

  # PostgreSQL
  python schema_documenter.py --postgres --server localhost --database mydb --username postgres --password pass --output docs.md

  # MySQL
  python schema_documenter.py --mysql --server localhost --database mydb --username root --password pass --output docs.md

  # Connection string
  python schema_documenter.py --connection "Server=localhost;Database=mydb;Trusted_Connection=yes;" --output docs.md
        """
    )

    parser.add_argument('--server', '-s', help='Database server hostname')
    parser.add_argument('--database', '-d', help='Database name')
    parser.add_argument('--username', '-u', help='Database username')
    parser.add_argument('--password', '-p', help='Database password')
    parser.add_argument('--connection', '-c', help='Full connection string')
    parser.add_argument('--output', '-o', required=True, help='Output markdown file')
    parser.add_argument('--postgres', action='store_true', help='Use PostgreSQL')
    parser.add_argument('--mysql', action='store_true', help='Use MySQL')

    args = parser.parse_args()

    # Determine database type
    db_type = 'sqlserver'
    if args.postgres:
        db_type = 'postgres'
    elif args.mysql:
        db_type = 'mysql'

    # Build connection string
    if args.connection:
        connection_string = args.connection
    elif args.server and args.database:
        if db_type == 'sqlserver':
            if args.username and args.password:
                connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={args.server};DATABASE={args.database};UID={args.username};PWD={args.password}"
            else:
                connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={args.server};DATABASE={args.database};Trusted_Connection=yes"
        elif db_type == 'postgres':
            connection_string = f"host={args.server} dbname={args.database} user={args.username} password={args.password}"
        elif db_type == 'mysql':
            connection_string = f"Server={args.server};Database={args.database};Username={args.username};Password={args.password}"
    else:
        print("Error: Either --connection or --server/--database required")
        parser.print_help()
        sys.exit(1)

    # Generate documentation
    print(f"\nConnecting to {db_type} database...")
    documenter = SchemaDocumenter(connection_string, db_type)
    print("Extracting schema information...")
    documenter.extract_schema()
    print(f"Generating markdown documentation...")
    documenter.generate_markdown(args.output, args.database)


if __name__ == '__main__':
    main()
