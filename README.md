# PyCart Engine

A Python-powered mini-mall that lives in your terminal. This project simulates a backend e-commerce system with a command-line interface.

> **Note**: This is the **SQLite Version** (Branch: `SQLite`).
> For the original JSON file-based version, check the [main branch](https://github.com/yigit-guven/PyCart-Engine/tree/main).

## How to run the program?

1.  **Prerequisites**: Ensure you have Python 3.x installed. No external libraries are required (uses standard library only).
2.  **Clone/Download**: Get the project files to your local machine.
3.  **Execute**:
    ```bash
    python main.py
    ```
4.  **Interact**: Follow the on-screen prompts to login, register, shop, and checkout.

> **Tip**: An **admin** account is automatically created for you (password: `123456`). Use it to add or update products.

## Features implemented

### User System (`users.py`)
-   **Authentication**: Secure login and registration.
-   **Security**: Passwords are hashed using **SHA-256** before storage (bonus feature).
-   **Validation**: Prevents duplicate usernames and ensures password strength.

### Product Catalog (`products.py`)
-   **Browsing**: View a formatted list of available products with real-time stock levels.
-   **Search**: Case-insensitive keyword search to find items quickly.
-   **Admin Mode**: Detects if the logged-in user is "admin" and unlocks the ability to add new products directly from the CLI.

### Cart System (`cart.py`)
-   **Persistence**: Cart data is saved to `pycart.db`, so your items remain even if you restart the program.
-   **Stock Validation**: Prevents adding more items than are currently available in stock.
-   **Management**: Add items, view accumulated costs, remove items, or clear the cart.

### Checkout System (`orders.py` & `main.py`)
-   **Checkout Workflow**:
    1.  Re-validates stock levels (in case they changed).
    2.  Calculates final total.
    3.  Deducts purchased quantity from global product stock.
    4.  Generates a unique Order ID.
    5.  Archives the transaction to `pycart.db`.
-   **History**: Users can view their past order history.

## How data is stored?

Data is stored in a single **SQLite Database** (`pycart.db`) instead of loose JSON files. This makes it safer and faster!

-   **`pycart.db`**: Stores `users`, `products`, `orders`, and `carts` in relational tables.
-   **`db_editor.py`**: I wrote a custom tool to peek inside the database since you can't open `.db` files in Notepad.
    -   Run: `python db_editor.py`
    -   Type `TABLES` to see what's there, or `SELECT products` to see items.

## Known limitations

- **Only one user at a time**: SQLite handles multiple people better than JSON, but this is still just a local CLI program.
- **No GUI**: It's all in the black box (terminal).
- **No password recovery**: If you forget your password, there's no "Forgot Password" button. You'll have to manually find yourself in `pycart.db` or just make a new account.
- **Order history is just a list**: You can't search through your old orders. If you buy a lot of stuff, you'll have to scroll a long way to find something from last week.
- **Deleting files wipes everything**: There's no "cloud backup." if you delete the `pycart.db` file, the whole store is basically gone forever.