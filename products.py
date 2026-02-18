from storage import load_data, save_data

PRODUCT_FILE = 'products.json'

class ProductManager:
    def __init__(self):
        self.products = load_data(PRODUCT_FILE)

    def list_products(self):
        # list of stuff we are selling
        return self.products

    def search_products(self, keyword):
        # search thingy. not case senseticve
        results = []
        for p in self.products:
            if keyword.lower() in p['name'].lower():
                results.append(p)
        return results

    def get_product_by_id(self, product_id):
        # finding a specific item by its code
        for p in self.products:
            if p['product_id'] == product_id:
                return p
        return None

    def update_stock(self, product_id, quantity_sold):
        # reducing stock when someone buys. return True if we have enough, else False.
        for p in self.products:
            if p['product_id'] == product_id:
                if p['stock'] >= quantity_sold:
                    p['stock'] -= quantity_sold
                    save_data(PRODUCT_FILE, self.products)  # save it again!
                    return True
                return False
        return False

    # Admin features, BONUS EXTENSION
    def add_product(self, name, price, stock):
        # admin add
        if not self.products:
            new_id = "P1001"
        else:
            # find the biggest id and add 1
            max_id = 0
            for p in self.products:
                try:
                    # remove the P and turn into number
                    pid_str = p['product_id']
                    if pid_str.startswith('P'):
                        pid = int(pid_str[1:])
                        if pid > max_id:
                            max_id = pid
                except ValueError:
                    pass # ignore weird ids
            
            # format it back to Pxxxx
            new_id = f"P{max_id + 1}"

        new_product = {
            "product_id": new_id,
            "name": name,
            "price": float(price),
            "stock": int(stock)
        }
        self.products.append(new_product)
        save_data(PRODUCT_FILE, self.products)
        return True

    def delete_product(self, product_id):
        # admin delete
        for i, p in enumerate(self.products):
            if p['product_id'] == product_id:
                del self.products[i]
                save_data(PRODUCT_FILE, self.products)
                return True
        return False

    def update_product(self, product_id, name=None, price=None, stock=None):
        # admin update details
        for p in self.products:
            if p['product_id'] == product_id:
                if name:
                    p['name'] = name
                if price:
                    try:
                        p['price'] = float(price)
                    except ValueError:
                        return False
                if stock:
                    try:
                        p['stock'] = int(stock)
                    except ValueError:
                        return False
                
                save_data(PRODUCT_FILE, self.products)
                return True
        return False