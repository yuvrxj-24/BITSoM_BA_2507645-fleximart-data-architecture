TASK 1.2 — DATABASE SCHEMA DOCUMENTATION 

ENTITY-RELATIONSHIP DESCRIPTION 

ENTITY: customers
Purpose: Stores customer profile and contact information for FlexiMart users.
Attributes:

customer_id: Unique identifier for each customer (Primary Key, auto-increment).
first_name: Customer’s first name (NOT NULL).
last_name: Customer’s last name (NOT NULL).
email: Customer email address (UNIQUE, NOT NULL).
phone: Customer phone number (nullable; stored in standardized format).
city: Customer city (nullable).
registration_date: Date the customer registered (nullable).

Relationships:

One customer can place MANY orders (1:M relationship with orders table via orders.customer_id).

ENTITY: products
Purpose: Stores product catalog information available for purchase.
Attributes:

product_id: Unique identifier for each product (Primary Key, auto-increment).
product_name: Name of the product (NOT NULL).
category: Product category such as Electronics/Fashion (NOT NULL, standardized).
price: Product price (DECIMAL, NOT NULL).
stock_quantity: Number of units in stock (default 0 if missing).

Relationships:

One product can appear in MANY order_items rows (1:M with order_items via order_items.product_id).

ENTITY: orders
Purpose: Stores order-level transaction information for each customer purchase. One order belongs to one customer and can have multiple items.
Attributes:

order_id: Unique identifier for each order (Primary Key, auto-increment).
customer_id: Customer who placed the order (Foreign Key → customers.customer_id, NOT NULL).
order_date: Date of the order (NOT NULL).
total_amount: Total value of the order (NOT NULL).
status: Order status (default ‘Pending’ if missing).

Relationships:

Many orders belong to ONE customer (M:1 to customers).

One order can have MANY order items (1:M relationship with order_items via order_items.order_id).

ENTITY: order_items
Purpose: Stores item-level details of each order (which products were purchased, quantity, and pricing).
Attributes:

order_item_id: Unique identifier for each order line item (Primary Key, auto-increment).
order_id: The order this item belongs to (Foreign Key → orders.order_id, NOT NULL).
product_id: Product purchased (Foreign Key → products.product_id, NOT NULL).
quantity: Number of units purchased (NOT NULL).
unit_price: Price per unit at purchase time (NOT NULL).
subtotal: Line total (quantity × unit_price) (NOT NULL).

Relationships:

Many order_items belong to ONE order (M:1 to orders).

Many order_items reference ONE product (M:1 to products).

NORMALIZATION EXPLANATION 

This database design follows Third Normal Form (3NF) because each table stores facts about a single entity and non-key attributes depend only on the primary key, not on other non-key attributes. In the customers table, attributes like first_name, last_name, email, phone, city, and registration_date depend only on customer_id. In the products table, product_name, category, price, and stock_quantity depend only on product_id. In the orders table, order_date, total_amount, and status depend only on order_id, while customer_id is a foreign key identifying which customer placed the order. In the order_items table, quantity, unit_price, and subtotal depend only on order_item_id (and logically on the combination of order_id and product_id), and foreign keys link each row to a valid order and product.

Functional dependencies include:

customer_id → first_name, last_name, email, phone, city, registration_date
product_id → product_name, category, price, stock_quantity
order_id → customer_id, order_date, total_amount, status
order_item_id → order_id, product_id, quantity, unit_price, subtotal

This design avoids anomalies. Update anomalies are reduced because customer details are stored once in customers and product details are stored once in products, so changing a customer email or product price does not require updating many rows in sales data. Insert anomalies are avoided because a new product or customer can be added without requiring an order to exist. Delete anomalies are avoided because deleting an order does not remove the customer or product master records; only dependent order_items are removed (or restricted by FK rules depending on configuration).

SAMPLE DATA REPRESENTATION 

customers (sample)
customer_id | first_name | last_name | email | phone | city | registration_date
1 | Rahul | Sharma | rahul.sharma@gmail.com
 | +91-9876543210 | Bangalore | 2023-01-15
2 | Priya | Patel | priya.patel@yahoo.com
 | +91-9988776655 | Mumbai | 2023-02-20
3 | Amit | Kumar | amit.kumar@missing.com
 | +91-9765432109 | Delhi | 2023-10-03

products (sample)
product_id | product_name | category | price | stock_quantity
1 | Samsung Galaxy S21 | Electronics | 45999.00 | 150
4 | Levi’s Jeans | Fashion | 2999.00 | 120
13 | (example) Grocery Item | Groceries | 499.00 | 0

orders (sample)
order_id | customer_id | order_date | total_amount | status
1 | 1 | 2024-01-15 | 45999.00 | Completed
2 | 2 | 2024-01-16 | 5998.00 | Completed
3 | 3 | 2024-01-15 | 52999.00 | Completed

order_items (sample)
order_item_id | order_id | product_id | quantity | unit_price | subtotal
1 | 1 | 1 | 1 | 45999.00 | 45999.00
2 | 2 | 4 | 2 | 2999.00 | 5998.00
3 | 3 | 7 | 1 | 52999.00 | 52999.00

