import datetime
from storage import load_data, save_data

ORDER_FILE = 'orders.json'

class OrderManager:
    def __init__(self):
        self.orders = load_data(ORDER_FILE)

    def create_order(self, username, cart_items, total_cost):
        # making up an ID. using O0001+ because its how its shown
        next_id_num = len(self.orders) + 1
        order_id = f"O{next_id_num:04d}"
        
        # Clean items is how it should be stored: remove name, rename price -> unit_price
        clean_items = []
        for item in cart_items:
            clean_items.append({
                "product_id": item['product_id'],
                "qty": item['qty'],
                "unit_price": item['price']
            })

        order = {
            "order_id": order_id,
            "username": username,
            "items": clean_items,
            "total": total_cost,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.orders.append(order)
        save_data(ORDER_FILE, self.orders)  # permanent save
        return order_id

    def view_history(self, username):
        user_orders = [o for o in self.orders if o['username'] == username]
        if not user_orders:
            print("No order history found.")
        else:
            # Need to import ProductManager here to look up names
            from products import ProductManager
            pm = ProductManager()
            
            print(f"\n--- Order History for {username} ---")
            for order in user_orders:
                print(f"Order ID: {order['order_id']} | Date: {order['timestamp']} | Total: ${order['total']:.2f}")
                for item in order['items']:
                    # try to find the name from products.json
                    product = pm.get_product_by_id(item['product_id'])
                    name = product['name'] if product else "Unknown Product"
                    print(f"  - {name} (x{item['qty']}) @ ${item['unit_price']:.2f}")
            print("-----------------------------------")