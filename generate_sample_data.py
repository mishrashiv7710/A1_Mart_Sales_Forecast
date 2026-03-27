import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_data(num_rows=200):
    np.random.seed(42)
    categories = ['Electronics', 'Groceries', 'Clothing', 'Home Decor']
    subcategories = {
        'Electronics': ['Mobiles', 'Laptops', 'Headphones'],
        'Groceries': ['Vegetables', 'Fruits', 'Dairy'],
        'Clothing': ['T-shirts', 'Jeans', 'Dresses'],
        'Home Decor': ['Lamps', 'Curtains', 'Vases']
    }
    products = {
        'Mobiles': ['iPhone 13', 'Samsung S22', 'OnePlus 9'],
        'Laptops': ['MacBook Air', 'Dell XPS', 'HP Spectre'],
        'Headphones': ['Sony WH-1000XM4', 'Bose QC35', 'AirPods Pro'],
        'Vegetables': ['Tomato', 'Potato', 'Onion'],
        'Fruits': ['Apple', 'Banana', 'Mango'],
        'Dairy': ['Milk', 'Cheese', 'Butter'],
        'T-shirts': ['Nike Tee', 'Adidas Tee', 'Puma Tee'],
        'Jeans': ['Levi\'s 501', 'Lee Cooper', 'Wrangler'],
        'Dresses': ['Zara Dress', 'H&M Maxi', 'M&S Casual'],
        'Lamps': ['Table Lamp', 'Floor Lamp', 'Smart LED'],
        'Curtains': ['Blackout', 'Sheer', 'Velvet'],
        'Vases': ['Ceramic', 'Glass', 'Metal']
    }

    data = []
    base_date = datetime(2025, 1, 1)

    for i in range(num_rows):
        cat = np.random.choice(categories)
        subcat = np.random.choice(subcategories[cat])
        prod = np.random.choice(products[subcat])
        
        qty = np.random.randint(1, 10)
        base_price = np.random.randint(500, 50000)
        sales_price = base_price * qty
        discount = np.random.uniform(0.05, 0.2)
        discounted_price = sales_price * (1 - discount)
        
        date = base_date + timedelta(days=np.random.randint(0, 365))
        
        data.append({
            "Quantity Purchased": qty,
            "Product Name": prod,
            "Date and Time": date.strftime('%Y-%m-%d %H:%M:%S'),
            "Sales Price": sales_price,
            "Subcategory": subcat,
            "Category": cat,
            "Discounted Price": discounted_price
        })

    df = pd.DataFrame(data)
    df.to_csv('sample_sales_data.csv', index=False)
    print("Sample data generated successfully!")

if __name__ == "__main__":
    generate_sample_data()
