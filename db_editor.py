import sqlite3
import sys

DB_NAME = "pycart.db"

def print_help():
    print("\n--- MiniDB Editor ---")
    print("Commands:")
    print("  TABLES           - List all tables")
    print("  SELECT <table>   - Show all rows in a table")
    print("  SQL <query>      - Run raw SQL (e.g., SQL DELETE FROM users WHERE id=1)")
    print("  EXIT             - Quit")
    print("---------------------")

def run_editor():
    print("Welcome to the MiniDB Editor! Using database:", DB_NAME)
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    while True:
        try:
            command = input("\nDB> ").strip()
            if not command:
                continue

            parts = command.split()
            cmd = parts[0].upper()

            if cmd == "EXIT":
                break
            
            elif cmd == "TABLES":
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                print("Tables:", [t['name'] for t in tables])

            elif cmd == "SELECT":
                if len(parts) < 2:
                    print("Usage: SELECT <table>")
                    continue
                table_name = parts[1]
                try:
                    cursor.execute(f"SELECT * FROM {table_name}")
                    rows = cursor.fetchall()
                    if not rows:
                        print(f"Table '{table_name}' is empty.")
                    else:
                        # print the column names
                        headers = rows[0].keys()
                        print(" | ".join(headers))
                        print("-" * (len(headers) * 10))
                        for row in rows:
                            print(" | ".join([str(val) for val in row]))
                except Exception as e:
                    print(f"Error: {e}")

            elif cmd == "SQL":
                query = command[4:]
                try:
                    cursor.execute(query)
                    if query.strip().upper().startswith("SELECT"):
                        rows = cursor.fetchall()
                        for row in rows:
                            print(dict(row))
                    else:
                        conn.commit()
                        print(f"Executed. Rows affected: {cursor.rowcount}")
                except Exception as e:
                    print(f"Error: {e}")

            else:
                print_help()

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Unexpected Error: {e}")

    conn.close()
    print("Bye!")

if __name__ == "__main__":
    run_editor()
