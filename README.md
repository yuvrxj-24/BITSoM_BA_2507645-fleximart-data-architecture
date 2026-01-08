FlexiMart Data Architecture Project

Student Name: YUVRAAJ KUAMR SINGH
Student ID: BITSoM_BA_2507645
Email: yuvraaj.ks1@gmail.com

Date: 08/01/26

Project Overview
This project builds an end-to-end data architecture for FlexiMart, starting from raw CSV files and delivering a clean relational database, a NoSQL product catalog in MongoDB, and a star-schema data warehouse for OLAP analytics. The pipeline includes data cleaning, schema documentation, business SQL queries, MongoDB operations, and analytical reporting from a dimensional model.
## Repository Structure

├── data/  
│   ├── customers_raw.csv  
│   ├── products_raw.csv  
│   └── sales_raw.csv  
├── part1-database-etl/  
│   ├── etl_pipeline.py  
│   ├── schema_documentation.md  
│   ├── business_queries.sql  
│   ├── data_quality_report.txt  
│   └── requirements.txt  
├── part2-nosql/  
│   ├── nosql_analysis.md  
│   ├── mongodb_operations.js  
│   └── products_catalog.json  
├── part3-datawarehouse/  
│   ├── star_schema_design.md  
│   ├── warehouse_schema.sql  
│   ├── warehouse_data.sql  
│   └── analytics_queries.sql  
├── .gitignore  
└── README.md  

## Technologies Used

- Python 3.x, pandas, SQLAlchemy, PyMySQL  
- MySQL 8.0  
- MongoDB (mongosh)

## Setup Instructions



Database Setup (MySQL)

Create databases

```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS fleximart;"
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS fleximart_dw;"
--->Run Part 1 - ETL Pipeline (loads cleaned data into fleximart)
python part1-database-etl/etl_pipeline.py

--->Run Part 1 - Business Queries
mysql -u root -p fleximart < part1-database-etl/business_queries.sql

--->Run Part 3 - Data Warehouse (schema + data + analytics queries)
mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_schema.sql
mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_data.sql
mysql -u root -p fleximart_dw < part3-datawarehouse/analytics_queries.sql
```
MongoDB Setup
Run MongoDB script for Task 2.2
mongosh < part2-nosql/mongodb_operations.js
(Ensure MongoDB server is running locally and mongosh is available.)

Key Learnings
This project helped me understand how raw operational data is cleaned and standardized before loading into relational tables with constraints and relationships. I also learned how document databases like MongoDB handle flexible product attributes and nested reviews more naturally than relational schemas. Finally, building a star schema made it clear how data warehouses enable fast OLAP analysis using fact/dimension modeling and aggregation queries.

Challenges Faced

Data quality issues in CSVs (missing IDs/emails, inconsistent date formats, duplicates)
Solution: Implemented transformation rules for deduplication, missing value handling, and date/phone standardization with reporting.

Ensuring foreign key correctness in the data warehouse
Solution: Loaded dimensions first (date/product/customer), then inserted fact rows referencing valid keys only, and validated counts and joins using OLAP queries.
Verification: See verification_steps.md for quick validation queries.
