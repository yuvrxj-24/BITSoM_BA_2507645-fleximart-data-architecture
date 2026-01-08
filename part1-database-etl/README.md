# Part 1 - Database ETL (MySQL)

Files:
- etl_pipeline.py: Cleans raw CSVs and loads data into MySQL database leximart
- business_queries.sql: Business SQL queries (Task 1.3)
- schema_documentation.md: ER + 3NF explanation (Task 1.2)
- data_quality_report.txt: ETL run report

How to run:
1) Set DATABASE_URL (example):
   mysql+pymysql://root:<password>@localhost:3306/fleximart
2) Run:
   python etl_pipeline.py
3) Run queries:
   mysql -u root -p fleximart < business_queries.sql
