import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import sqlite3
from config.settings import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS dim_product (
            product_id TEXT PRIMARY KEY,
            brand TEXT,
            category TEXT,
            segment TEXT
        );

        CREATE TABLE IF NOT EXISTS dim_retailer (
            retailer_id TEXT PRIMARY KEY,
            retailer_name TEXT,
            channel TEXT
        );

        CREATE TABLE IF NOT EXISTS fact_sellout (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            week TEXT,
            product_id TEXT,
            retailer_id TEXT,
            region TEXT,
            channel TEXT,
            units INTEGER,
            net_sales REAL,
            distribution REAL,
            price_index REAL,
            promo_flag INTEGER,
            FOREIGN KEY(product_id) REFERENCES dim_product(product_id),
            FOREIGN KEY(retailer_id) REFERENCES dim_retailer(retailer_id)
        );
    """)
    conn.commit()
    conn.close()
    print("Database tables initialized successfully.")

if __name__ == "__main__":
    init_db()
