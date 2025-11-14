import json
import random
from datetime import datetime, timedelta

# Set random seed for reproducibility (optional)
random.seed(42)

# Sample data pools for realistic generation
first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", 
               "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
               "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa",
               "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra"]

last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
              "Rodriguez", "Martinez", "Hernandez", "Lopez", "Wilson", "Anderson", "Thomas",
              "Taylor", "Moore", "Jackson", "Martin", "Lee", "Thompson", "White", "Harris",
              "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young"]

cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio",
          "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville", "Fort Worth", "Columbus",
          "Charlotte", "San Francisco", "Indianapolis", "Seattle", "Denver", "Washington",
          "Boston", "El Paso", "Nashville", "Detroit", "Oklahoma City", "Portland", "Las Vegas",
          "Memphis", "Louisville", "Baltimore"]

product_names = [
    "Wireless Headphones", "Smartphone Case", "Laptop Stand", "USB-C Cable", "Wireless Mouse",
    "Mechanical Keyboard", "Monitor Stand", "Desk Organizer", "Phone Charger", "Tablet Stand",
    "Bluetooth Speaker", "Webcam HD", "External Hard Drive", "SSD 1TB", "Memory Card 128GB",
    "Gaming Chair", "Standing Desk", "LED Desk Lamp", "Cable Management", "Laptop Sleeve",
    "Backpack Laptop", "Wireless Earbuds", "Smart Watch", "Fitness Tracker", "Power Bank",
    "Car Phone Mount", "Screen Protector", "Phone Grip", "Laptop Cooling Pad", "USB Hub"
]

categories = ["Electronics", "Computer Accessories", "Audio", "Mobile Accessories", "Furniture",
              "Storage", "Wearables", "Cables & Adapters", "Office Supplies", "Travel"]

payment_methods = ["Credit Card", "Debit Card", "PayPal", "Apple Pay", "Google Pay", "Bank Transfer"]

payment_statuses = ["Completed", "Pending", "Failed", "Refunded"]

shipment_statuses = ["Pending", "Processing", "Shipped", "In Transit", "Delivered", "Cancelled"]

# Generate customers.json
def generate_customers(num_records=25):
    customers = []
    used_emails = set()
    
    for i in range(1, num_records + 1):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        name = f"{first_name} {last_name}"
        
        # Generate unique email
        email_base = f"{first_name.lower()}.{last_name.lower()}"
        email_num = random.randint(1, 999)
        email = f"{email_base}{email_num}@example.com"
        while email in used_emails:
            email_num = random.randint(1, 999)
            email = f"{email_base}{email_num}@example.com"
        used_emails.add(email)
        
        city = random.choice(cities)
        
        customers.append({
            "id": i,
            "name": name,
            "email": email,
            "city": city
        })
    
    return customers

# Generate products.json
def generate_products(num_records=25):
    products = []
    
    for i in range(1, num_records + 1):
        name = random.choice(product_names)
        category = random.choice(categories)
        # Price between $9.99 and $499.99
        price = round(random.uniform(9.99, 499.99), 2)
        
        products.append({
            "id": i,
            "name": name,
            "category": category,
            "price": price
        })
    
    return products

# Generate orders.json
def generate_orders(num_records=30, num_customers=25, num_products=25):
    orders = []
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    
    for i in range(1, num_records + 1):
        customer_id = random.randint(1, num_customers)
        product_id = random.randint(1, num_products)
        qty = random.randint(1, 5)
        
        # Random date between start and end date
        time_between = end_date - start_date
        days_between = time_between.days
        random_days = random.randrange(days_between)
        order_date = start_date + timedelta(days=random_days)
        
        orders.append({
            "order_id": i,
            "customer_id": customer_id,
            "product_id": product_id,
            "qty": qty,
            "date": order_date.strftime("%Y-%m-%d")
        })
    
    return orders

# Generate payments.json
def generate_payments(orders, products):
    payments = []
    
    for order in orders:
        order_id = order["order_id"]
        product_id = order["product_id"]
        qty = order["qty"]
        
        # Find product price
        product = next((p for p in products if p["id"] == product_id), None)
        if product:
            amount = round(product["price"] * qty, 2)
        else:
            amount = round(random.uniform(10.00, 500.00), 2)
        
        payment_method = random.choice(payment_methods)
        status = random.choice(payment_statuses)
        
        payments.append({
            "order_id": order_id,
            "amount": amount,
            "payment_method": payment_method,
            "status": status
        })
    
    return payments

# Generate shipments.json
def generate_shipments(orders):
    shipments = []
    
    for order in orders:
        order_id = order["order_id"]
        order_date = datetime.strptime(order["date"], "%Y-%m-%d")
        
        shipment_status = random.choice(shipment_statuses)
        
        # Shipment date is typically 1-7 days after order date
        if shipment_status in ["Shipped", "In Transit", "Delivered"]:
            days_after = random.randint(1, 7)
            shipment_date = order_date + timedelta(days=days_after)
        else:
            # For pending/processing, shipment date might be null or same as order date
            shipment_date = order_date + timedelta(days=random.randint(0, 2))
        
        shipments.append({
            "order_id": order_id,
            "shipment_status": shipment_status,
            "shipment_date": shipment_date.strftime("%Y-%m-%d")
        })
    
    return shipments

# Main execution
if __name__ == "__main__":
    import os
    
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    print("Generating synthetic e-commerce data...")
    
    # Generate all data
    customers = generate_customers(25)
    products = generate_products(25)
    orders = generate_orders(30, 25, 25)
    payments = generate_payments(orders, products)
    shipments = generate_shipments(orders)
    
    # Write to JSON files
    files_data = {
        "customers.json": customers,
        "products.json": products,
        "orders.json": orders,
        "payments.json": payments,
        "shipments.json": shipments
    }
    
    for filename, data in files_data.items():
        filepath = os.path.join("data", filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Generated {filepath} with {len(data)} records")
    
    print("\nAll data files generated successfully!")

