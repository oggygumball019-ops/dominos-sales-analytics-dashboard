import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

# 1. Scraped store metadata for Chennai delivery hubs
outlets_data = [
    {"outlet_id": "OUT-001", "outlet_area": "Velachery", "zone": "South Chennai", "lat": 12.9815, "lon": 80.2180},
    {"outlet_id": "OUT-002", "outlet_area": "OMR Kandanchavadi", "zone": "IT Corridor", "lat": 12.9649, "lon": 80.2464},
    {"outlet_id": "OUT-003", "outlet_area": "Anna Nagar", "zone": "North-West Chennai", "lat": 13.0878, "lon": 80.2170},
    {"outlet_id": "OUT-004", "outlet_area": "T. Nagar", "zone": "Central Chennai", "lat": 13.0418, "lon": 80.2341},
    {"outlet_id": "OUT-005", "outlet_area": "Adyar", "zone": "South Chennai", "lat": 13.0012, "lon": 80.2565},
    {"outlet_id": "OUT-006", "outlet_area": "Nungambakkam", "zone": "Central Chennai", "lat": 13.0569, "lon": 80.2425},
    {"outlet_id": "OUT-007", "outlet_area": "Tambaram", "zone": "Outer South", "lat": 12.9229, "lon": 80.1275}
]

df_outlets = pd.DataFrame(outlets_data)
df_outlets.to_csv("dim_outlets.csv", index=False)

# 2. Synthetic Event Generation (10,000 orders, 1,500 customers)
n_orders = 10000
n_customers = 1500

customer_ids = [f"CUST-{i:04d}" for i in range(1, n_customers + 1)]
start_date = datetime(2026, 1, 1)

customer_cohort_map = {
    c_id: start_date + timedelta(days=int(np.random.randint(0, 180)))
    for c_id in customer_ids
}

menu_items = [
    {"category": "Veg Pizza", "price_min": 199, "price_max": 499},
    {"category": "Non-Veg Pizza", "price_min": 299, "price_max": 699},
    {"category": "Pizza Mania", "price_min": 109, "price_max": 250},
    {"category": "Sides & Desserts", "price_min": 99, "price_max": 299},
    {"category": "Beverages", "price_min": 60, "price_max": 120}
]

acquisition_channels = ["Organic Web", "Mobile App", "Paid Social Ads", "Referral", "Google Search"]

order_records = []
for i in range(1, n_orders + 1):
    c_id = np.random.choice(customer_ids)
    c_signup = customer_cohort_map[c_id]
    
    days_after_signup = int(np.random.exponential(scale=35))
    order_timestamp = c_signup + timedelta(
        days=days_after_signup,
        hours=int(np.random.choice([12, 13, 14, 18, 19, 20, 21], p=[0.1, 0.15, 0.1, 0.15, 0.2, 0.2, 0.1])),
        minutes=np.random.randint(0, 60)
    )
    
    if order_timestamp > datetime(2026, 9, 30):
        order_timestamp = datetime(2026, 9, 30, 19, 30)

    outlet = np.random.choice(df_outlets["outlet_area"].values)
    item = np.random.choice(menu_items, p=[0.35, 0.30, 0.15, 0.12, 0.08])
    amount = round(np.random.uniform(item["price_min"], item["price_max"]), 2)
    channel = np.random.choice(acquisition_channels, p=[0.30, 0.40, 0.15, 0.10, 0.05])
    
    order_records.append({
        "order_id": f"ORD-{i:06d}",
        "customer_id": c_id,
        "signup_date": c_signup.strftime("%Y-%m-%d"),
        "order_timestamp": order_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "order_date": order_timestamp.strftime("%Y-%m-%d"),
        "outlet_area": outlet,
        "category": item["category"],
        "channel": channel,
        "amount": amount
    })

df_raw_orders = pd.DataFrame(order_records)
df_raw_orders.to_csv("raw_pos_transactions.csv", index=False)
print("SUCCESS: dim_outlets.csv and raw_pos_transactions.csv generated!")