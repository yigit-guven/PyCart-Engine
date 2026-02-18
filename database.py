import sqlite3
import hashlib

DB_NAME = "pycart.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # making the table for users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # table for the items we sell.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    ''')

    # cart table. just linking users to product ids
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            product_id TEXT NOT NULL,
            qty INTEGER NOT NULL
        )
    ''')

    # orders
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT UNIQUE NOT NULL,
            username TEXT NOT NULL,
            total REAL NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')

    # linking items to orders
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT NOT NULL,
            product_id TEXT NOT NULL,
            qty INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (order_id)
        )
    ''')

    # seed data if tables are empty
    # adding default products for testing
    if conn.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 0:
        print("Seeding default products...")
        conn.execute("INSERT INTO products (product_id, name, price, stock) VALUES ('P1001', 'USB-C Cable', 9.99, 30)")
        conn.execute("INSERT INTO products (product_id, name, price, stock) VALUES ('P1002', 'Wireless Mouse', 19.99, 15)")

    # adding admin user if not exists
    if conn.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'").fetchone()[0] == 0:
        print("Creating admin account...")
        # password is '123456', hashed with sha256
        admin_pass = hashlib.sha256('123456'.encode()).hexdigest()
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', admin_pass))

    conn.commit()
    conn.close()

# running init on import to make sure tables exist
initialize_db()
