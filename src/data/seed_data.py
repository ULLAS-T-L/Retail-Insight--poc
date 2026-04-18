import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import sqlite3
import random
from datetime import datetime, timedelta
from config.settings import DB_PATH

def seed_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM dim_product")
    if cursor.fetchone()[0] > 0:
        print("Database already contains data, skipping seed.")
        conn.close()
        return

    # Seed dim_product
    # 2 brands (AlphaBrand, BetaBrand)
    products = [
        ("P001", "AlphaBrand", "Beverage", "Premium"),
        ("P002", "AlphaBrand", "Beverage", "Value"),
        ("P003", "BetaBrand", "Beverage", "Premium"),
        ("P004", "BetaBrand", "Beverage", "Value"),
    ]
    cursor.executemany("INSERT INTO dim_product VALUES (?, ?, ?, ?)", products)

    # Seed dim_retailer
    # 2 channels (Hypermarket, E-commerce)
    retailers = [
        ("R001", "MegaMart", "Hypermarket"),
        ("R002", "QuickPantry", "Hypermarket"),
        ("R003", "ShopOnline", "E-commerce"),
        ("R004", "WebRetail", "E-commerce"),
    ]
    cursor.executemany("INSERT INTO dim_retailer VALUES (?, ?, ?)", retailers)

    # Seed fact_sellout
    # 2 regions: North, South
    regions = ["North", "South"]

    # Generate 12 weeks of data
    start_date = datetime.now() - timedelta(weeks=12)
    start_date = start_date - timedelta(days=start_date.weekday()) # Set to Monday

    sellouts = []
    
    for week_offset in range(12):
        week_start = start_date + timedelta(weeks=week_offset)
        week_str = f"W{week_start.strftime('%W-%Y')}"
        
        # Daily data
        for day_offset in range(7):
            current_date = week_start + timedelta(days=day_offset)
            date_str = current_date.strftime("%Y-%m-%d")
            
            for p in products:
                prod_id = p[0]
                brand = p[1]
                
                for r in retailers:
                    ret_id = r[0]
                    channel = r[2]
                    
                    for reg in regions:
                        # Baseline units realistic logic
                        # AlphaBrand sells more in North, BetaBrand sells more in South
                        base_units = random.randint(50, 200)
                        if brand == "AlphaBrand" and reg == "North":
                            base_units += 100
                        if brand == "BetaBrand" and reg == "South":
                            base_units += 80
                            
                        # WebRetail has variance
                        if ret_id == "R004":
                            base_units = int(base_units * random.uniform(0.5, 1.5))
                            
                        # Promo increases units, lower price relative to index
                        promo_flag = 1 if random.random() < 0.2 else 0
                        price_index = round(random.uniform(0.8, 1.2), 2)
                        
                        if promo_flag:
                            base_units = int(base_units * 1.5)
                            price_index = round(random.uniform(0.7, 0.95), 2)
                            
                        if price_index > 1.05:
                            base_units = int(base_units * 0.8)
                            
                        distribution = round(random.uniform(0.6, 1.0), 2)
                        
                        # Actual units tied to distribution availability
                        units = int(base_units * distribution)
                        
                        # Compliance check data (anomaly logic e.g., returns)
                        # occasionally negative units
                        if random.random() < 0.01:
                            units = -random.randint(1, 10)
                            
                        net_sales = round(units * random.uniform(5.0, 15.0), 2)
                        
                        sellouts.append((
                            date_str, week_str, prod_id, ret_id, reg, channel,
                            units, net_sales, distribution, price_index, promo_flag
                        ))

    cursor.executemany("""
        INSERT INTO fact_sellout (date, week, product_id, retailer_id, region, channel, units, net_sales, distribution, price_index, promo_flag)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, sellouts)

    conn.commit()
    conn.close()
    print(f"Database seeded with {len(sellouts)} fact_sellout records.")

if __name__ == "__main__":
    seed_db()
