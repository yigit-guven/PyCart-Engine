# PyCart-Engine

A Python-powered mini-mall that lives in your terminal and thinks in JSON. This project simulates a backend e-commerce system with a command-line interface, demonstrating core programming concepts like file I/O, data management, and modular architecture.

## How to run the program?

1.  **Prerequisites**: Ensure you have Python 3.x installed. No external libraries are required (uses standard library only).
2.  **Clone/Download**: Get the project files to your local machine.
3.  **Execute**:
    ```bash
    python main.py
    ```
4.  **Interact**: Follow the on-screen prompts to login, register, shop, and checkout.

> **Tip**: An `admin` account exists in the `users.json` file. Log in as `username: admin, password: 123456` to access special product management features.

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
-   **Persistence**: Cart data is saved to `carts.json`, so your items remain even if you restart the program.
-   **Stock Validation**: Prevents adding more items than are currently available in stock.
-   **Management**: Add items, view accumulated costs, remove items, or clear the cart.

### Checkout System (`orders.py` & `main.py`)
-   **Checkout Workflow**:
    1.  Re-validates stock levels (in case they changed).
    2.  Calculates final total.
    3.  Deducts purchased quantity from global product stock.
    4.  Generates a unique Order ID.
    5.  Archives the transaction to `orders.json`.
-   **History**: Users can view their past order history.

## How data is stored?

Data is stored in local JSON files to simulate a database:

-   **`users.json`**: Stores user credentials (hashed passwords).
-   **`products.json`**: inventory database containing product IDs, names, prices, and stock counts.
-   **`carts.json`**: Temporary storage for active shopping sessions.
-   **`orders.json`**: Permanent record of completed transactions.

## Known limitations

-   **Concurrency**: The system uses loose file-based storage. Simultaneous writes by multiple instances could theoretically cause race conditions or data corruption (though unlikely in a single-user CLI environment).
-   **Interface**: Strictly command-line based. No graphical user interface (GUI) or web frontend.
-   **Scalability**: JSON files are loaded entirely into memory. This works great for small datasets but would need migration to a SQL database (like SQLite or PostgreSQL) for millions of records.
