from database import get_db_connection

PRODUCT_FILE = 'products.json' # keeping this variable just in case, but not using it.

class ProductManager:
    # Removed __init__ since we don't load a list anymore

    def list_products(self):
        # list of stuff we are selling
        conn = get_db_connection()
        products = conn.execute("SELECT * FROM products").fetchall()
        conn.close()
        # converting to list of dicts to keep compatible with main.py
        return [dict(p) for p in products]

    def search_products(self, keyword):
        # search thingy. not case senseticve
        conn = get_db_connection()
        # SQL LIKE is case insensitive in SQLite usually
        products = conn.execute("SELECT * FROM products WHERE name LIKE ?", ('%' + keyword + '%',)).fetchall()
        conn.close()
        return [dict(p) for p in products]

    def get_product_by_id(self, product_id):
        # finding a specific item by its code
        conn = get_db_connection()
        product = conn.execute("SELECT * FROM products WHERE product_id = ?", (product_id,)).fetchone()
        conn.close()
        if product:
            return dict(product)
        return None

    def update_stock(self, product_id, quantity_sold):
        # reducing stock when someone buys. return True if we have enough, else False.
        conn = get_db_connection()
        product = conn.execute("SELECT stock FROM products WHERE product_id = ?", (product_id,)).fetchone()
        
        if product and product['stock'] >= quantity_sold:
            new_stock = product['stock'] - quantity_sold
            conn.execute("UPDATE products SET stock = ? WHERE product_id = ?", (new_stock, product_id))
            conn.commit()
            conn.close()
            return True
        
        conn.close()
        return False

    # Admin features, BONUS EXTENSION
    def add_product(self, name, price, stock):
        # admin add. now with auto-id generation. fancy!
        conn = get_db_connection()
        
        # find the biggest id logic (Pxxxx)
        # doing it in python because i know how loops work better than sql.
        try:
            # Get all ids to find max
            products = conn.execute("SELECT product_id FROM products").fetchall()
            max_id = 0
            for p in products:
                try:
                    pid_str = p['product_id']
                    if pid_str.startswith('P'):
                        pid = int(pid_str[1:])
                        if pid > max_id:
                            max_id = pid
                except ValueError:
                    pass
            new_id = f"P{max_id + 1}"
            
            conn.execute("INSERT INTO products (product_id, name, price, stock) VALUES (?, ?, ?, ?)",
                         (new_id, name, float(price), int(stock)))
            conn.commit()
            print(f"Product added with ID: {new_id}")
            return True
        except Exception as e:
            print(f"Error adding product: {e}")
            return False
        finally:
            conn.close()

    def delete_product(self, product_id):
        # admin delete
        conn = get_db_connection()
        # check fields to see if it exists first? or just delete.
        cursor = conn.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
        conn.commit()
        deleted = cursor.rowcount > 0
        conn.close()
        return deleted

    def update_product(self, product_id, name=None, price=None, stock=None):
        # admin update details
        conn = get_db_connection()
        product = conn.execute("SELECT * FROM products WHERE product_id = ?", (product_id,)).fetchone()
        
        if not product:
            conn.close()
            return False
            
        # building the query piece by piece.
        updates = []
        params = []
        
        if name:
            updates.append("name = ?")
            params.append(name)
        if price:
            try:
                updates.append("price = ?")
                params.append(float(price))
            except ValueError:
                conn.close()
                return False
        if stock:
            try:
                updates.append("stock = ?")
                params.append(int(stock))
            except ValueError:
                conn.close()
                return False
                
        if not updates:
            conn.close()
            return True # nothing to update
            
        params.append(product_id)
        query = f"UPDATE products SET {', '.join(updates)} WHERE product_id = ?"
        
        conn.execute(query, params)
        conn.commit()
        conn.close()
        return True