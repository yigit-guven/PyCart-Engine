import hashlib
from database import get_db_connection

class UserManager:
    def _hash_password(self, password):
        # Used SHA256 logic here as BONUS EXTENSION.
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username, password):
        # this function makes a new user and puts them in the database.
        if len(password) < 6:
            print("Error: Password must be at least 6 characters.")
            return False

        hashed_pw = self._hash_password(password)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
            conn.commit()
            print("Registration successful!")
            return True
        except Exception as e:
            # probably user already exists. oops.
            print("Error: Username already exists.")
            return False
        finally:
            conn.close()

    def login(self, username, password):
        # checking if names and passwords match so they can login to the mini mall.
        hashed_pw = self._hash_password(password)
        
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_pw)).fetchone()
        conn.close()
        
        if user:
            return True
        return False