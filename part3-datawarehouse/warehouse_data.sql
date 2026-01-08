USE fleximart_dw;

-- =========================================================
-- 1) dim_date (30 dates: Jan 1–15 and Feb 1–15, 2024)
-- =========================================================
INSERT INTO dim_date
(date_key, full_date, day_of_week, day_of_month, month, month_name, quarter, year, is_weekend)
VALUES
(20240101,'2024-01-01','Monday',1,1,'January','Q1',2024,FALSE),
(20240102,'2024-01-02','Tuesday',2,1,'January','Q1',2024,FALSE),
(20240103,'2024-01-03','Wednesday',3,1,'January','Q1',2024,FALSE),
(20240104,'2024-01-04','Thursday',4,1,'January','Q1',2024,FALSE),
(20240105,'2024-01-05','Friday',5,1,'January','Q1',2024,FALSE),
(20240106,'2024-01-06','Saturday',6,1,'January','Q1',2024,TRUE),
(20240107,'2024-01-07','Sunday',7,1,'January','Q1',2024,TRUE),
(20240108,'2024-01-08','Monday',8,1,'January','Q1',2024,FALSE),
(20240109,'2024-01-09','Tuesday',9,1,'January','Q1',2024,FALSE),
(20240110,'2024-01-10','Wednesday',10,1,'January','Q1',2024,FALSE),
(20240111,'2024-01-11','Thursday',11,1,'January','Q1',2024,FALSE),
(20240112,'2024-01-12','Friday',12,1,'January','Q1',2024,FALSE),
(20240113,'2024-01-13','Saturday',13,1,'January','Q1',2024,TRUE),
(20240114,'2024-01-14','Sunday',14,1,'January','Q1',2024,TRUE),
(20240115,'2024-01-15','Monday',15,1,'January','Q1',2024,FALSE),

(20240201,'2024-02-01','Thursday',1,2,'February','Q1',2024,FALSE),
(20240202,'2024-02-02','Friday',2,2,'February','Q1',2024,FALSE),
(20240203,'2024-02-03','Saturday',3,2,'February','Q1',2024,TRUE),
(20240204,'2024-02-04','Sunday',4,2,'February','Q1',2024,TRUE),
(20240205,'2024-02-05','Monday',5,2,'February','Q1',2024,FALSE),
(20240206,'2024-02-06','Tuesday',6,2,'February','Q1',2024,FALSE),
(20240207,'2024-02-07','Wednesday',7,2,'February','Q1',2024,FALSE),
(20240208,'2024-02-08','Thursday',8,2,'February','Q1',2024,FALSE),
(20240209,'2024-02-09','Friday',9,2,'February','Q1',2024,FALSE),
(20240210,'2024-02-10','Saturday',10,2,'February','Q1',2024,TRUE),
(20240211,'2024-02-11','Sunday',11,2,'February','Q1',2024,TRUE),
(20240212,'2024-02-12','Monday',12,2,'February','Q1',2024,FALSE),
(20240213,'2024-02-13','Tuesday',13,2,'February','Q1',2024,FALSE),
(20240214,'2024-02-14','Wednesday',14,2,'February','Q1',2024,FALSE),
(20240215,'2024-02-15','Thursday',15,2,'February','Q1',2024,FALSE);

-- =========================================================
-- 2) dim_product (15 products across 3 categories)
-- Categories: Electronics, Fashion, Home
-- Prices vary from ₹199 to ₹99,999
-- =========================================================
INSERT INTO dim_product (product_id, product_name, category, subcategory, unit_price) VALUES
('ELEC001','Samsung Galaxy S21 Ultra','Electronics','Smartphones',79999.00),
('ELEC002','Apple MacBook Air M2','Electronics','Laptops',99999.00),
('ELEC003','Sony WH-1000XM5 Headphones','Electronics','Audio',29990.00),
('ELEC004','Dell 27-inch 4K Monitor','Electronics','Monitors',32999.00),
('ELEC005','USB-C Fast Charger 65W','Electronics','Accessories',1299.00),

('FASH001','Levi''s 511 Slim Fit Jeans','Fashion','Clothing',3499.00),
('FASH002','Nike Air Max 270 Sneakers','Fashion','Footwear',12995.00),
('FASH003','Adidas Originals T-Shirt','Fashion','Clothing',1499.00),
('FASH004','Fossil Analog Watch','Fashion','Accessories',7999.00),
('FASH005','H&M Slim Fit Formal Shirt','Fashion','Clothing',1999.00),

('HOME001','Philips Air Fryer 4.1L','Home','Kitchen Appliances',8999.00),
('HOME002','Prestige Cookware Set (5 pc)','Home','Kitchen',5999.00),
('HOME003','LED Bulb 9W','Home','Lighting',199.00),
('HOME004','Memory Foam Pillow','Home','Home Comfort',1299.00),
('HOME005','Kent Water Purifier','Home','Appliances',15999.00);

-- =========================================================
-- 3) dim_customer (12 customers across 4 cities)
-- Cities: Mumbai, Delhi, Bangalore, Chennai
-- =========================================================
INSERT INTO dim_customer (customer_id, customer_name, city, state, customer_segment) VALUES
('CUST001','Aarav Mehta','Mumbai','Maharashtra','Returning'),
('CUST002','Isha Sharma','Mumbai','Maharashtra','New'),
('CUST003','Rohan Patel','Mumbai','Maharashtra','Loyal'),

('CUST004','Ananya Singh','Delhi','Delhi','Returning'),
('CUST005','Kabir Verma','Delhi','Delhi','New'),
('CUST006','Neha Gupta','Delhi','Delhi','Loyal'),

('CUST007','Arjun Rao','Bangalore','Karnataka','Returning'),
('CUST008','Sanya Nair','Bangalore','Karnataka','New'),
('CUST009','Vivek Iyer','Bangalore','Karnataka','Loyal'),

('CUST010','Priya Menon','Chennai','Tamil Nadu','Returning'),
('CUST011','Karthik Raj','Chennai','Tamil Nadu','New'),
('CUST012','Divya Krishnan','Chennai','Tamil Nadu','Loyal');

-- =========================================================
-- 4) fact_sales (40 transactions)
-- Important: product_key and customer_key are AUTO_INCREMENT,
-- so we reference them by assuming insert order created keys 1..15 and 1..12.
-- total_amount = quantity_sold * unit_price - discount_amount
-- Weekends have slightly higher activity.
-- =========================================================
INSERT INTO fact_sales
(date_key, product_key, customer_key, quantity_sold, unit_price, discount_amount, total_amount)
VALUES
-- January (20 rows)
(20240101, 6, 1, 1, 3499.00, 0.00, 3499.00),
(20240102, 3, 7, 1, 29990.00, 500.00, 29490.00),
(20240103, 12, 10, 2, 5999.00, 0.00, 11998.00),
(20240104, 5, 2, 2, 1299.00, 0.00, 2598.00),
(20240105, 7, 4, 1, 12995.00, 1000.00, 11995.00),

-- weekend spike
(20240106, 1, 3, 1, 79999.00, 3000.00, 76999.00),
(20240106, 11, 8, 1, 8999.00, 500.00, 8499.00),
(20240106, 8, 5, 3, 1499.00, 0.00, 4497.00),

(20240107, 2, 9, 1, 99999.00, 5000.00, 94999.00),
(20240107, 15, 6, 1, 15999.00, 1000.00, 14999.00),
(20240107, 14, 1, 2, 1299.00, 0.00, 2598.00),

(20240108, 4, 7, 1, 32999.00, 2000.00, 30999.00),
(20240109, 6, 10, 2, 3499.00, 0.00, 6998.00),
(20240110, 13, 9, 10, 199.00, 0.00, 1990.00),
(20240111, 5, 5, 1, 1299.00, 0.00, 1299.00),
(20240112, 9, 8, 1, 7999.00, 0.00, 7999.00),

-- weekend spike
(20240113, 1, 6, 1, 79999.00, 4000.00, 75999.00),
(20240113, 7, 3, 2, 12995.00, 0.00, 25990.00),
(20240114, 3, 1, 1, 29990.00, 0.00, 29990.00),
(20240115, 12, 7, 1, 5999.00, 0.00, 5999.00),

-- February (20 rows)
(20240201, 6, 2, 1, 3499.00, 0.00, 3499.00),
(20240202, 5, 8, 3, 1299.00, 0.00, 3897.00),

-- weekend spike
(20240203, 4, 9, 1, 32999.00, 1500.00, 31499.00),
(20240203, 11, 10, 2, 8999.00, 0.00, 17998.00),
(20240203, 13, 4, 8, 199.00, 0.00, 1592.00),

(20240204, 1, 7, 1, 79999.00, 2500.00, 77499.00),
(20240204, 2, 3, 1, 99999.00, 6000.00, 93999.00),
(20240204, 14, 12, 3, 1299.00, 0.00, 3897.00),

(20240205, 8, 11, 1, 1499.00, 0.00, 1499.00),
(20240206, 10, 6, 1, 7999.00, 0.00, 7999.00),
(20240207, 12, 9, 1, 5999.00, 0.00, 5999.00),
(20240208, 9, 8, 2, 7999.00, 0.00, 15998.00),
(20240209, 6, 10, 1, 3499.00, 0.00, 3499.00),

-- weekend spike
(20240210, 2, 1, 1, 99999.00, 8000.00, 91999.00),
(20240210, 7, 10, 1, 12995.00, 1000.00, 11995.00),
(20240211, 1, 9, 1, 79999.00, 3500.00, 76499.00),
(20240211, 15, 4, 1, 15999.00, 1500.00, 14499.00),

(20240212, 5, 5, 1, 1299.00, 0.00, 1299.00),
(20240213, 13, 8, 20, 199.00, 0.00, 3980.00),
(20240214, 12, 7, 2, 5999.00, 0.00, 11998.00),
(20240215, 3, 2, 1, 29990.00, 0.00, 29990.00);
