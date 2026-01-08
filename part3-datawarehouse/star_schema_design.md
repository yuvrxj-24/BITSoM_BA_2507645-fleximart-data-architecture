FlexiMart Data Warehouse — Star Schema Design (Task 3.1)
SECTION 1: SCHEMA OVERVIEW (Text Format)
FACT TABLE: fact_sales
Grain: One row per product per order line item (each record represents a single product sold in a specific order on a specific date).
Business Process: Sales transactions (line-item level sales activity).
Measures (Numeric Facts):


quantity_sold: Number of units sold for that product in that order line.
unit_price: Price per unit at the time of the sale.
discount_amount: Discount applied on that line item (0 if no discount).
total_amount: Final amount for that line item = (quantity_sold × unit_price) − discount_amount.

Foreign Keys (Links to Dimensions):

date_key → dim_date (links sale to the date it happened)
product_key → dim_product (links sale to the product sold)
customer_key → dim_customer (links sale to the customer who purchased)

Common Columns in fact_sales:

sale_key (Primary Key, auto-increment surrogate key)
date_key (FK)
product_key (FK)
customer_key (FK)
quantity_sold
unit_price
discount_amount
total_amount


DIMENSION TABLE: dim_date
Purpose: Stores time-related attributes to support time-based analysis like daily/monthly/quarterly/yearly reporting.
Type: Conformed dimension (can be reused across multiple fact tables if FlexiMart adds more facts later such as returns or shipments).
Attributes:


date_key (PK): Surrogate key in integer format YYYYMMDD (example: 20240115)
full_date: Actual date value (YYYY-MM-DD)
day_of_week: Day name (Monday, Tuesday, etc.)
day_of_month: Day number in month (1–31)
month: Month number (1–12)
month_name: Month name (January, February, etc.)
quarter: Quarter label (Q1, Q2, Q3, Q4)
year: Year number (2023, 2024, etc.)
is_weekend: Boolean (TRUE for Saturday/Sunday, FALSE otherwise)

DIMENSION TABLE: dim_product
Purpose: Stores descriptive product attributes so sales can be analyzed by product, category, subcategory, and pricing.
Attributes:


product_key (PK): Warehouse surrogate key (auto-increment)
product_id: Natural/business key from source system (e.g., ELEC001, P001)
product_name: Product name
category: Product category (Electronics, Fashion, etc.)
subcategory: More detailed grouping (Smartphones, Laptops, Footwear, etc.)
unit_price: Standard/list unit price (Note: actual sale unit price is stored in fact_sales.unit_price)


Relationship:


One product (dim_product) can have many sales rows (fact_sales) → 1:M


DIMENSION TABLE: dim_customer
Purpose: Stores customer descriptive attributes to support analysis by geography and segmentation.
Attributes:


customer_key (PK): Warehouse surrogate key (auto-increment)
customer_id: Natural/business key from source system (e.g., C001)
customer_name: Full name of the customer
city: Customer city (e.g., Mumbai, Delhi, Bangalore, Chennai)
state: Customer state (e.g., Maharashtra, Delhi, Karnataka, Tamil Nadu)
customer_segment: Business segmentation label (e.g., New, Returning, Loyal)


Relationship:


One customer (dim_customer) can have many sales rows (fact_sales) → 1:M


SECTION 2: DESIGN DECISIONS 
This star schema uses transaction line-item granularity (one row per product per order item) because it preserves maximum detail for analytics. With this grain, FlexiMart can analyze sales at multiple levels: product-level performance, category trends, customer buying behavior, and time-based patterns such as weekend vs weekday demand. If the warehouse stored data only at order level, it would lose product-level insights like which items drive revenue or which categories sell more units.
Surrogate keys are used for date_key, product_key, and customer_key because they provide stable identifiers even if source system identifiers or attributes change (for example, customer email updates or product renaming). Surrogate keys also improve join performance and keep warehouse relationships consistent over time.
This design supports drill-down and roll-up operations naturally. Analysts can roll up from day to month to quarter to year using dim_date, and drill down from category to subcategory to individual products using dim_product.
SECTION 3: SAMPLE DATA FLOW 
Source Transaction (from operational system):
Order #101
Customer: John Doe (Mumbai)
Product: Laptop
Quantity: 2
Unit Price: 50000
Discount: 0
Order Date: 2024-01-15
Becomes in Data Warehouse:


dim_date record:
date_key: 20240115
full_date: 2024-01-15
day_of_week: Monday
day_of_month: 15
month: 1
month_name: January
quarter: Q1
year: 2024
is_weekend: FALSE


dim_product record:
product_key: 5
product_id: ELEC002
product_name: Laptop
category: Electronics
subcategory: Laptops
unit_price: 50000


dim_customer record:
customer_key: 12
customer_id: C012
customer_name: John Doe
city: Mumbai
state: Maharashtra
customer_segment: Returning


fact_sales record (line item):
date_key: 20240115
product_key: 5
customer_key: 12
quantity_sold: 2
unit_price: 50000
discount_amount: 0
total_amount: 100000


This shows how a single source order line becomes one fact row linked to three dimension rows using surrogate keys.