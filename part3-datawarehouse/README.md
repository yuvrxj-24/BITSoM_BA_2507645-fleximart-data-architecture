# Part 3 - Data Warehouse (Star Schema)

Files:
- star_schema_design.md: Star schema documentation (Task 3.1)
- warehouse_schema.sql: Creates DW tables in leximart_dw (Task 3.2)
- warehouse_data.sql: Inserts required dimension/fact rows (Task 3.2)
- analytics_queries.sql: OLAP queries (Task 3.3)

How to run:
1) Create schema:
   mysql -u root -p fleximart_dw < warehouse_schema.sql
2) Load data:
   mysql -u root -p fleximart_dw < warehouse_data.sql
3) Run analytics:
   mysql -u root -p fleximart_dw < analytics_queries.sql
