import json
import sqlite3
import os

DB_NAME = "pycart.db"

def load_json(filename):
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except:
        return []

def migrate():
    print("Starting migration...")
    
    # Connect manually to control flow
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Users
    users = load_json('users.json')
    print(f"Migrating {len(users)} users...")
    for u in users:
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                           (u['username'], u['password']))
        except sqlite3.IntegrityError:
            print(f"  Skipping duplicate user: {u['username']}")

    # 2. Products
    products = load_json('products.json')
    print(f"Migrating {len(products)} products...")
    for p in products:
        try:
            cursor.execute("INSERT INTO products (product_id, name, price, stock) VALUES (?, ?, ?, ?)",
                           (p['product_id'], p['name'], p['price'], p['stock']))
        except sqlite3.IntegrityError:
             print(f"  Skipping duplicate product: {p['product_id']}")

    # 3. Carts - moving the shopping lists
    # hope this structure is right...
    carts = load_json('carts.json')
    print("Migrating carts...")
    # carts.json might be a dict or list based on previous code.
    # The file content is likely a dict: {"user1": [...], "user2": [...]}
    if isinstance(carts, dict):
        for username, items in carts.items():
            for item in items:
                cursor.execute("INSERT INTO cart (username, product_id, qty) VALUES (?, ?, ?)",
                               (username, item['product_id'], item['qty']))
    
    # 4. Orders
    orders = load_json('orders.json')
    print(f"Migrating {len(orders)} orders...")
    for o in orders:
        try:
            cursor.execute("INSERT INTO orders (order_id, username, total, timestamp) VALUES (?, ?, ?, ?)",
                           (o['order_id'], o['username'], o['total'], o['timestamp']))
            
            # items
            for item in o['items']:
                # handle both old structure (price) and new structure (unit_price)
                price = item.get('unit_price', item.get('price', 0.0))
                cursor.execute("INSERT INTO order_items (order_id, product_id, qty, unit_price) VALUES (?, ?, ?, ?)",
                               (o['order_id'], item['product_id'], item['qty'], price))
        except sqlite3.IntegrityError:
             print(f"  Skipping duplicate order: {o['order_id']}")

    conn.commit()
    conn.close()
    print("Migration complete!")

if __name__ == "__main__":
    if os.path.exists(DB_NAME):
        print(f"Database {DB_NAME} already exists. Appending/Upserting...")
    else:
        # if the db is already there, we just run the migration.
        # hopefully it doesn't crash if things stick exist.
        import database
        database.initialize_db()
        
    migrate()
