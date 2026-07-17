import hashlib


class UserManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.users = {}
        self.load_users()

    def load_users(self):
        self.users = {}
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if ';' in line:
                        user, pwd = line.strip().split(';')
                        self.users[user] = pwd
        except FileNotFoundError:
            print(f"Error: User file {self.file_path} not found.")

    def authenticate(self, username, password):
        """Compara el SHA-256 de la contraseña ingresada contra el hash almacenado."""
        if username in self.users:
            hashed = hashlib.sha256(password.encode("utf-8")).hexdigest()
            if self.users[username] == hashed:
                return True
        return False
