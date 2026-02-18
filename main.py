import sys
from users import UserManager
from products import ProductManager
from cart import CartManager
from orders import OrderManager

user_mgr = UserManager()
prod_mgr = ProductManager()
cart_mgr = CartManager()
order_mgr = OrderManager()

def print_header(title):
    print("\n" + "="*30)
    print(f" {title} ")
    print("="*30)

def checkout(username):
    cart = cart_mgr.get_user_cart(username)
    if not cart:
        print("Cart is empty.")
        return

    print_header("Checkout")
    total = 0
    final_items = []

    # check the stock
    for item in cart:
        product = prod_mgr.get_product_by_id(item['product_id'])
        if not product or product['stock'] < item['qty']:
            print(f"Error: {item['name']} is out of stock or insufficient quantity.")
            print("Transaction cancelled. Please update your cart.")
            return
        
        item_total = item['qty'] * item['price']
        total += item_total
        final_items.append(item)

    # User Confirmation
    print(f"Total Amount to Pay: ${total:.2f}")
    confirm = input("Confirm purchase? (yes/no): ").lower()
    
    if confirm == 'yes':
        # taking items out of the inventory.
        for item in final_items:
            success = prod_mgr.update_stock(item['product_id'], item['qty'])
            if not success:
                print("Critical Error: Stock changed during checkout.")
                return

        # order done, save it
        order_id = order_mgr.create_order(username, final_items, total)
        
        # empty the cart
        cart_mgr.clear_cart(username)
        
        print(f"Order placed successfully! Order ID: {order_id}")
    else:
        print("Checkout cancelled.")

def store_menu(username):
    while True:
        print_header(f"Store Menu ({username})")
        print("1. Browse Products")
        print("2. Search Products")
        print("3. View Cart")
        print("4. Checkout")
        print("5. Order History")
        print("6. Logout")
        
        # Additional admin mode to add or update products, BONUS EXTENSION.
        if username == "admin":
            print("7. [ADMIN] Add Product")
            print("8. [ADMIN] Update Product")
            print("9. [ADMIN] Delete Product")

        choice = input("Choose an option: ")

        if choice == '1':
            products = prod_mgr.list_products()
            print("\nAvailable Products:")
            print(f"{'ID':<8} {'Name':<20} {'Price':<10} {'Stock':<5}")
            print("-" * 45)
            for p in products:
                print(f"{p['product_id']:<8} {p['name']:<20} ${p['price']:<9.2f} {p['stock']:<5}")

            buy = input("\nEnter Product ID to add to cart (or Press Enter to go back): ")
            if buy:
                qty = input("Quantity: ")
                if qty.isdigit() and int(qty) > 0:
                    prod = prod_mgr.get_product_by_id(buy)
                    if prod:
                        cart_mgr.add_to_cart(username, prod, int(qty))
                    else:
                        print("Invalid Product ID.")
                else:
                    print("Invalid quantity.")

        elif choice == '2':
            keyword = input("Enter search keyword: ")
            results = prod_mgr.search_products(keyword)
            if results:
                for p in results:
                    print(f"{p['product_id']}: {p['name']} - ${p['price']} ({p['stock']} left)")
            else:
                print("No products found.")

        elif choice == '3':
            cart = cart_mgr.get_user_cart(username)
            if not cart:
                print("\nYour cart is empty.")
            else:
                print("\n--- Your Cart ---")
                total = 0
                for item in cart:
                    subtotal = item['qty'] * item['price']
                    total += subtotal
                    print(f"{item['product_id']}: {item['name']} x{item['qty']} = ${subtotal:.2f}")
                print(f"Total: ${total:.2f}")
                
                action = input("\nType Product ID to remove item, or Enter to go back: ")
                if action:
                    cart_mgr.remove_from_cart(username, action)

        elif choice == '4':
            checkout(username)

        elif choice == '5':
            order_mgr.view_history(username)

        elif choice == '6':
            print("Logging out...")
            break
        
        elif choice == '7' and username == "admin":
            name = input("Name: ")
            price = input("Price: ")
            stock = input("Stock: ")
            try:
                prod_mgr.add_product(name, price, stock)
                print("Product added.")
            except ValueError:
                print("Invalid input for price or stock.")

        elif choice == '8' and username == "admin":
            pid = input("Enter Product ID to Update: ")
            if prod_mgr.get_product_by_id(pid):
                name = input("New Name (Leave empty to keep current): ")
                price = input("New Price (Leave empty to keep current): ")
                stock = input("New Stock (Leave empty to keep current): ")
                if prod_mgr.update_product(pid, name if name else None, price if price else None, stock if stock else None):
                    print("Product updated successfully.")
                else:
                    print("Failed to update product. Check inputs.")
            else:
                print("Product ID not found.")

        elif choice == '9' and username == "admin":
            pid = input("Enter Product ID to Delete: ")
            confirm = input(f"Are you sure you want to delete {pid}? (yes/no): ").lower()
            if confirm == 'yes':
                if prod_mgr.delete_product(pid):
                    print("Product deleted successfully.")
                else:
                    print("Product ID not found.")
            else:
                print("Deletion cancelled.")

        else:
            print("Invalid option.")

def main():
    while True:
        print_header("Mini-Amazon Welcome")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        
        choice = input("Choose an option: ")

        if choice == '1':
            user = input("Username: ")
            pwd = input("Password: ")
            if user_mgr.login(user, pwd):
                store_menu(user)
            else:
                print("Invalid credentials.")

        elif choice == '2':
            user = input("Choose Username: ")
            pwd = input("Choose Password: ")
            user_mgr.register(user, pwd)

        elif choice == '3':
            print("Goodbye!")
            sys.exit()
        
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()