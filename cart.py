from database import get_db_connection

CART_FILE = 'carts.json' # unused now

class CartManager:
    # Removed __init__ loading

    def get_user_cart(self, username):
        conn = get_db_connection()
        # getting cart items AND product info at the same time.
        #joined tables to get the price.
        query = '''
            SELECT c.product_id, c.qty, p.name, p.price 
            FROM cart c
            JOIN products p ON c.product_id = p.product_id
            WHERE c.username = ?
        '''
        items = conn.execute(query, (username,)).fetchall()
        conn.close()
        return [dict(i) for i in items]

    def add_to_cart(self, username, product, quantity):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # check stock first (db has latest)
        db_product = conn.execute("SELECT stock FROM products WHERE product_id = ?", (product['product_id'],)).fetchone()
        if not db_product:
            print("Error: Product not found.")
            conn.close()
            return

        current_stock = db_product['stock']
        
        # Check existing cart qty
        existing_item = conn.execute("SELECT qty FROM cart WHERE username = ? AND product_id = ?", 
                                     (username, product['product_id'])).fetchone()
        
        current_cart_qty = existing_item['qty'] if existing_item else 0
        
        if current_cart_qty + quantity > current_stock:
             print(f"Error: Not enough stock. You have {current_cart_qty} in cart, stock is {current_stock}.")
             conn.close()
             return

        if existing_item:
            # Update existing
            new_qty = current_cart_qty + quantity
            cursor.execute("UPDATE cart SET qty = ? WHERE username = ? AND product_id = ?", 
                           (new_qty, username, product['product_id']))
            print("Updated quantity in cart.")
        else:
            # Insert new
            cursor.execute("INSERT INTO cart (username, product_id, qty) VALUES (?, ?, ?)",
                           (username, product['product_id'], quantity))
            print("Item added to cart.")
            
        conn.commit()
        conn.close()

    def remove_from_cart(self, username, product_id):
        conn = get_db_connection()
        cursor = conn.execute("DELETE FROM cart WHERE username = ? AND product_id = ?", (username, product_id))
        conn.commit()
        
        if cursor.rowcount > 0:
            print("Item removed.")
        else:
            print("Item not found in cart.")
        conn.close()

    def clear_cart(self, username):
        conn = get_db_connection()
        conn.execute("DELETE FROM cart WHERE username = ?", (username,))
        conn.commit()
        conn.close()

    def _save(self):
        # No longer needed, DB saves immediately
        pass