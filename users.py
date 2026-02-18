import hashlib
from storage import load_data, save_data

USER_FILE = 'users.json'

class UserManager:
    def __init__(self):
        self.users = load_data(USER_FILE)

    def _hash_password(self, password):
        # Used SHA256 logic here as BONUS EXTENSION.
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username, password):
        # this function makes a new user and puts them in the list.
        if len(password) < 6:
            print("Error: Password must be at least 6 characters.")
            return False
        
        for user in self.users:
            if user['username'] == username:
                print("Error: Username already exists.")
                return False

        new_user = {
            "username": username,
            "password": self._hash_password(password)
        }
        self.users.append(new_user)
        save_data(USER_FILE, self.users)  # saving to the file
        print("Registration successful!")
        return True

    def login(self, username, password):
        # checking if names and passwords match so they can login to the mini mall.
        hashed_pw = self._hash_password(password)
        for user in self.users:
            if user['username'] == username and user['password'] == hashed_pw:
                return True
        return False