import os
import re
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

DATA_DIR = "data"
CUSTOMERS_PATH = os.path.join(DATA_DIR, "customers_raw.csv")
PRODUCTS_PATH  = os.path.join(DATA_DIR, "products_raw.csv")
SALES_PATH     = os.path.join(DATA_DIR, "sales_raw.csv")
REPORT_PATH    = "data_quality_report.txt"



def read_csv_smart(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, encoding="utf-8-sig")

    
    if df.shape[1] == 1 and isinstance(df.columns[0], str) and "," in df.columns[0]:
        header = [h.strip() for h in df.columns[0].split(",")]
        split_data = df.iloc[:, 0].astype(str).str.split(",", expand=True)
        split_data.columns = header[:split_data.shape[1]]
        df = split_data

    df.columns = [c.strip() for c in df.columns]
    return df


def blanks_to_na(df: pd.DataFrame) -> pd.DataFrame:
    return df.replace(r"^\s*$", pd.NA, regex=True)



def standardize_phone(phone) -> str | None:
    if pd.isna(phone):
        return None
    s = str(phone).strip()
    if not s:
        return None
    digits = re.sub(r"\D", "", s)

    if len(digits) == 10:
        return f"+91-{digits}"
    if len(digits) == 11 and digits.startswith("0"):
        return f"+91-{digits[-10:]}"
    if len(digits) == 12 and digits.startswith("91"):
        return f"+91-{digits[-10:]}"
    return None


def parse_date_any(x) -> str | None:
    if pd.isna(x):
        return None
    s = str(x).strip()
    if not s:
        return None

    
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y", "%m/%d/%Y", "%d-%m-%Y"):
        try:
            dt = pd.to_datetime(s, format=fmt)
            return dt.strftime("%Y-%m-%d")
        except Exception:
            pass

    
    dt = pd.to_datetime(s, errors="coerce", dayfirst=True)
    if pd.isna(dt):
        return None
    return dt.strftime("%Y-%m-%d")


def standardize_category(cat) -> str:
    if pd.isna(cat):
        return "Uncategorized"
    s = str(cat).strip().lower()
    if not s:
        return "Uncategorized"
    return s.title()


def generate_email(first_name: str, last_name: str, raw_customer_id: str) -> str:
    fn = re.sub(r"[^a-zA-Z0-9]", "", str(first_name).strip().lower())
    ln = re.sub(r"[^a-zA-Z0-9]", "", str(last_name).strip().lower())
    cid = re.sub(r"[^a-zA-Z0-9]", "", str(raw_customer_id).strip().lower())
    return f"{fn}.{ln}.{cid}@noemail.fleximart"



def transform_customers(customers_raw: pd.DataFrame):
    df = blanks_to_na(customers_raw.copy())
    df = df.rename(columns={"customer_id": "raw_customer_id"})

    df["first_name"] = df["first_name"].astype("string").str.strip()
    df["last_name"]  = df["last_name"].astype("string").str.strip()
    df["email"]      = df["email"].astype("string").str.strip().str.lower()
    df["phone"]      = df["phone"].apply(standardize_phone)
    df["city"]       = df["city"].astype("string").str.strip().str.title()
    df["registration_date"] = df["registration_date"].apply(parse_date_any)

    missing_email_before = int(df["email"].isna().sum())
    df.loc[df["email"].isna(), "email"] = df[df["email"].isna()].apply(
        lambda r: generate_email(r["first_name"], r["last_name"], r["raw_customer_id"]),
        axis=1
    )
    missing_email_filled = missing_email_before

    before = len(df)
    df = df.drop_duplicates(subset=["email"], keep="first")
    dups_removed = before - len(df)

    before2 = len(df)
    df = df.dropna(subset=["first_name", "last_name", "email"])
    dropped_required = before2 - len(df)

    return df, {
        "customers_processed": len(customers_raw),
        "customers_dups_removed": dups_removed,
        "customers_missing_email_filled": missing_email_filled,
        "customers_dropped_required": dropped_required,
        "customers_final": len(df)
    }


def transform_products(products_raw: pd.DataFrame):
    df = blanks_to_na(products_raw.copy())
    df = df.rename(columns={"product_id": "raw_product_id"})

    df["product_name"] = df["product_name"].astype("string").str.strip()
    df["category"] = df["category"].apply(standardize_category)

    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["stock_quantity"] = pd.to_numeric(df["stock_quantity"], errors="coerce")

    missing_stock = int(df["stock_quantity"].isna().sum())
    df["stock_quantity"] = df["stock_quantity"].fillna(0).astype(int)

    missing_price_before = int(df["price"].isna().sum())
    df["price"] = df["price"].fillna(df.groupby("category")["price"].transform("median"))
    overall_median = df["price"].median()
    if pd.isna(overall_median):
        overall_median = 0.0
    df["price"] = df["price"].fillna(overall_median)
    missing_price_filled = missing_price_before

    before = len(df)
    df = df.drop_duplicates(subset=["product_name", "category"], keep="first")
    dups_removed = before - len(df)

    before2 = len(df)
    df = df.dropna(subset=["product_name", "category", "price"])
    dropped_required = before2 - len(df)

    return df, {
        "products_processed": len(products_raw),
        "products_dups_removed": dups_removed,
        "products_missing_price_filled": missing_price_filled,
        "products_missing_stock_filled": missing_stock,
        "products_dropped_required": dropped_required,
        "products_final": len(df)
    }


def transform_sales(sales_raw: pd.DataFrame):
    df = blanks_to_na(sales_raw.copy())

    df["transaction_id"] = df["transaction_id"].astype("string").str.strip()
    df["customer_id"] = df["customer_id"].astype("string").str.strip()
    df["product_id"] = df["product_id"].astype("string").str.strip()
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df["transaction_date"] = df["transaction_date"].apply(parse_date_any)
    df["status"] = df["status"].astype("string").str.strip().str.title()

    before = len(df)
    df = df.drop_duplicates(subset=["transaction_id", "customer_id", "product_id", "transaction_date"], keep="first")
    dups_removed = before - len(df)

    missing_customer = int(df["customer_id"].isna().sum())
    missing_product  = int(df["product_id"].isna().sum())

    before2 = len(df)
    df = df.dropna(subset=["transaction_id", "customer_id", "product_id", "transaction_date", "quantity", "unit_price"])
    dropped_required = before2 - len(df)

    return df, {
        "sales_processed": len(sales_raw),
        "sales_dups_removed": dups_removed,
        "sales_missing_customer": missing_customer,
        "sales_missing_product": missing_product,
        "sales_dropped_required": dropped_required,
        "sales_final": len(df)
    }



def get_engine():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL env var not set.")
    return create_engine(db_url, future=True)


def truncate_tables(engine):
    
    with engine.begin() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS=0;"))
        conn.execute(text("TRUNCATE TABLE order_items;"))
        conn.execute(text("TRUNCATE TABLE orders;"))
        conn.execute(text("TRUNCATE TABLE products;"))
        conn.execute(text("TRUNCATE TABLE customers;"))
        conn.execute(text("SET FOREIGN_KEY_CHECKS=1;"))


def load_customers(engine, customers_clean: pd.DataFrame) -> int:
    inserted = 0
    sql = text("""
        INSERT INTO customers (first_name, last_name, email, phone, city, registration_date)
        VALUES (:first_name, :last_name, :email, :phone, :city, :registration_date)
    """)
    with engine.begin() as conn:
        for _, r in customers_clean.iterrows():
            conn.execute(sql, {
                "first_name": r["first_name"],
                "last_name": r["last_name"],
                "email": r["email"],
                "phone": r["phone"],
                "city": r["city"],
                "registration_date": r["registration_date"]
            })
            inserted += 1
    return inserted


def load_products(engine, products_clean: pd.DataFrame) -> int:
    inserted = 0
    sql = text("""
        INSERT INTO products (product_name, category, price, stock_quantity)
        VALUES (:product_name, :category, :price, :stock_quantity)
    """)
    with engine.begin() as conn:
        for _, r in products_clean.iterrows():
            conn.execute(sql, {
                "product_name": r["product_name"],
                "category": r["category"],
                "price": float(r["price"]),
                "stock_quantity": int(r["stock_quantity"])
            })
            inserted += 1
    return inserted


def build_id_maps(engine, customers_clean, products_clean):
    
    with engine.begin() as conn:
        c_rows = conn.execute(text("SELECT customer_id, email FROM customers")).fetchall()
        p_rows = conn.execute(text("SELECT product_id, product_name, category FROM products")).fetchall()

    email_to_cid = {str(email).lower(): int(cid) for cid, email in c_rows}
    prodkey_to_pid = {(str(pn), str(cat)): int(pid) for pid, pn, cat in p_rows}

    raw_customer_to_db = {}
    for _, r in customers_clean.iterrows():
        raw_customer_to_db[r["raw_customer_id"]] = email_to_cid.get(str(r["email"]).lower())

    raw_product_to_db = {}
    for _, r in products_clean.iterrows():
        raw_product_to_db[r["raw_product_id"]] = prodkey_to_pid.get((str(r["product_name"]), str(r["category"])))

    return raw_customer_to_db, raw_product_to_db


def load_orders_and_items(engine, sales_clean: pd.DataFrame, raw_c_map, raw_p_map):
    
    df = sales_clean.copy()
    df["customer_db_id"] = df["customer_id"].map(raw_c_map)
    df["product_db_id"] = df["product_id"].map(raw_p_map)

    
    before = len(df)
    df = df.dropna(subset=["customer_db_id", "product_db_id"])
    dropped_unmapped = before - len(df)

    df["customer_db_id"] = df["customer_db_id"].astype(int)
    df["product_db_id"] = df["product_db_id"].astype(int)

    
    orders = (
        df.groupby(["transaction_id", "customer_db_id", "transaction_date", "status"], as_index=False)
          .apply(lambda g: pd.Series({"total_amount": float((g["quantity"] * g["unit_price"]).sum())}))
          .reset_index(drop=True)
    )

    
    txn_to_orderid = {}
    with engine.begin() as conn:
        for _, r in orders.iterrows():
            conn.execute(
                text("""
                    INSERT INTO orders (customer_id, order_date, total_amount, status)
                    VALUES (:customer_id, :order_date, :total_amount, :status)
                """),
                {
                    "customer_id": int(r["customer_db_id"]),
                    "order_date": r["transaction_date"],
                    "total_amount": float(r["total_amount"]),
                    "status": r["status"]
                }
            )
            oid = conn.execute(text("SELECT LAST_INSERT_ID();")).scalar()
            txn_to_orderid[r["transaction_id"]] = int(oid)

    
    df["order_id"] = df["transaction_id"].map(txn_to_orderid)
    df["subtotal"] = (df["quantity"] * df["unit_price"]).astype(float)

    item_inserted = 0
    with engine.begin() as conn:
        for _, r in df.iterrows():
            conn.execute(
                text("""
                    INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal)
                    VALUES (:order_id, :product_id, :quantity, :unit_price, :subtotal)
                """),
                {
                    "order_id": int(r["order_id"]),
                    "product_id": int(r["product_db_id"]),
                    "quantity": int(r["quantity"]),
                    "unit_price": float(r["unit_price"]),
                    "subtotal": float(r["subtotal"])
                }
            )
            item_inserted += 1

    return len(orders), item_inserted, dropped_unmapped


def write_report(stats: dict, loaded: dict):
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("FlexiMart Data Quality Report\n")
        f.write("====================================\n\n")

        f.write("Records Processed\n-----------------\n")
        f.write(f"customers_raw.csv: {stats['customers_processed']}\n")
        f.write(f"products_raw.csv:  {stats['products_processed']}\n")
        f.write(f"sales_raw.csv:     {stats['sales_processed']}\n\n")

        f.write("Duplicates Removed\n------------------\n")
        f.write(f"customers: {stats['customers_dups_removed']}\n")
        f.write(f"products:  {stats['products_dups_removed']}\n")
        f.write(f"sales:     {stats['sales_dups_removed']}\n\n")

        f.write("Missing Values Handled\n----------------------\n")
        f.write(f"customers missing emails filled: {stats['customers_missing_email_filled']}\n")
        f.write(f"products missing prices filled:  {stats['products_missing_price_filled']}\n")
        f.write(f"products missing stock filled:   {stats['products_missing_stock_filled']}\n")
        f.write(f"sales missing customer_id:       {stats['sales_missing_customer']}\n")
        f.write(f"sales missing product_id:        {stats['sales_missing_product']}\n")
        f.write(f"sales dropped (missing required): {stats['sales_dropped_required']}\n\n")

        f.write("Records Loaded Successfully\n---------------------------\n")
        for k, v in loaded.items():
            f.write(f"{k}: {v}\n")

    print(f"\n✅ Report generated: {REPORT_PATH}")


def main():
    
    customers_raw = read_csv_smart(CUSTOMERS_PATH)
    products_raw  = read_csv_smart(PRODUCTS_PATH)
    sales_raw     = read_csv_smart(SALES_PATH)

    
    customers_clean, c_stats = transform_customers(customers_raw)
    products_clean,  p_stats = transform_products(products_raw)
    sales_clean,     s_stats = transform_sales(sales_raw)

    stats = {}
    stats.update(c_stats)
    stats.update(p_stats)
    stats.update(s_stats)

    
    engine = get_engine()

    
    truncate_tables(engine)

    loaded = {}
    loaded["customers_loaded"] = load_customers(engine, customers_clean)
    loaded["products_loaded"]  = load_products(engine, products_clean)

    raw_c_map, raw_p_map = build_id_maps(engine, customers_clean, products_clean)
    orders_loaded, items_loaded, unmapped = load_orders_and_items(engine, sales_clean, raw_c_map, raw_p_map)

    loaded["orders_loaded"] = orders_loaded
    loaded["order_items_loaded"] = items_loaded
    loaded["sales_rows_unmapped_dropped"] = unmapped

    
    write_report(stats, loaded)

    print("\n✅ ETL Load Complete")
    print("Loaded:", loaded)


if __name__ == "__main__":
    main()
