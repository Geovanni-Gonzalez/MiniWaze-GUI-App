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
        if username in self.users:
            if self.users[username] == password:
                return True
        return False
