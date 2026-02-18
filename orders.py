import datetime
from database import get_db_connection

ORDER_FILE = 'orders.json' # unused

class OrderManager:
    # Removed __init__ loading

    def create_order(self, username, cart_items, total_cost):
        # making up an ID. using O0001+ because its how its shown
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Generate ID
            # Count existing orders
            count = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
            next_id_num = count + 1
            order_id = f"O{next_id_num:04d}"
            
            # Insert Order
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("INSERT INTO orders (order_id, username, total, timestamp) VALUES (?, ?, ?, ?)",
                           (order_id, username, total_cost, timestamp))
            
            # Insert Items
            for item in cart_items:
                # cart_items come from cart.get_user_cart which has product_id / qty / price (as unit_price)
                p_id = item['product_id']
                qty = item['qty']
                u_price = item['price'] # cart join returns 'price'
                
                cursor.execute("INSERT INTO order_items (order_id, product_id, qty, unit_price) VALUES (?, ?, ?, ?)",
                               (order_id, p_id, qty, u_price))
            
            conn.commit()
            return order_id
        except Exception as e:
            print(f"Error creating order: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()

    def view_history(self, username):
        conn = get_db_connection()
        
        # Get orders
        orders = conn.execute("SELECT * FROM orders WHERE username = ?", (username,)).fetchall()
        
        if not orders:
            print("No order history found.")
        else:
            print(f"\n--- Order History for {username} ---")
            for order in orders:
                print(f"Order ID: {order['order_id']} | Date: {order['timestamp']} | Total: ${order['total']:.2f}")
                
                # finding product names again because we didn't save them. using a JOIN here
                query = '''
                    SELECT oi.qty, oi.unit_price, p.name 
                    FROM order_items oi
                    LEFT JOIN products p ON oi.product_id = p.product_id
                    WHERE oi.order_id = ?
                '''
                items = conn.execute(query, (order['order_id'],)).fetchall()
                
                for item in items:
                    name = item['name'] if item['name'] else "Unknown Product"
                    print(f"  - {name} (x{item['qty']}) @ ${item['unit_price']:.2f}")
            print("-----------------------------------")
        conn.close()