from storage import load_data, save_data

CART_FILE = 'carts.json'

class CartManager:
    def __init__(self):
        # Load all the carts
        self.all_carts = load_data(CART_FILE)
        if isinstance(self.all_carts, list):
            # if it was a list we gotta fix it. JSON is hard.
            self.all_carts = {} if not self.all_carts else self.all_carts

    def get_user_cart(self, username):
        return self.all_carts.get(username, [])

    def add_to_cart(self, username, product, quantity):
        if username not in self.all_carts:
            self.all_carts[username] = []
        
        cart = self.all_carts[username]
        
        # check if they already have it, if yes, just add the numbers
        for item in cart:
            if item['product_id'] == product['product_id']:
                # total stock limit including what's already in cart:
                if item['qty'] + quantity > product['stock']:
                    print(f"Error: Not enough stock. You have {item['qty']} in cart, stock is {product['stock']}.")
                    return
                item['qty'] += quantity
                print("Updated quantity in cart.")
                self._save()
                return

        # new item adding to cart
        if quantity > product['stock']:
            print("Error: Not enough stock.")
            return

        cart.append({
            "product_id": product['product_id'],
            "name": product['name'],
            "price": product['price'],
            "qty": quantity
        })
        print("Item added to cart.")
        self._save()

    def remove_from_cart(self, username, product_id):
        if username in self.all_carts:
            # filter from stackoverflow
            original_len = len(self.all_carts[username])
            self.all_carts[username] = [item for item in self.all_carts[username] if item['product_id'] != product_id]
            
            if len(self.all_carts[username]) < original_len:
                print("Item removed.")
                self._save()
            else:
                print("Item not found in cart.")

    def clear_cart(self, username):
        if username in self.all_carts:
            self.all_carts[username] = []
            self._save()

    def _save(self):
        save_data(CART_FILE, self.all_carts)