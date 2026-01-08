# Verification Checks

MySQL - fleximart (Part 1):
- SELECT COUNT(*) FROM customers;
- SELECT COUNT(*) FROM products;
- SELECT COUNT(*) FROM orders;
- SELECT COUNT(*) FROM order_items;

MySQL - fleximart_dw (Part 3):
- SELECT COUNT(*) FROM dim_date;      -- expected 30
- SELECT COUNT(*) FROM dim_product;   -- expected 15
- SELECT COUNT(*) FROM dim_customer;  -- expected 12
- SELECT COUNT(*) FROM fact_sales;    -- expected >= 40

MongoDB (Part 2):
- show dbs
- use fleximart_nosql
- db.products.countDocuments()
