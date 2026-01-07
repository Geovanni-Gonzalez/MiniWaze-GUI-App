import tkinter as tk
from models.user_manager import UserManager
from ui.login_window import LoginWindow
from ui.main_window import MainWindow
import sys
import os

def main():
    root = tk.Tk()
    
    # Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    users_path = os.path.join(base_dir, "data", "Usuarios.txt")
    
    # Managers
    user_manager = UserManager(users_path)

    def start_app(username):
        # Clear the current window (Login)
        for widget in root.winfo_children():
            widget.destroy()
        
        # Initialize MainWindow using the SAME root
        app = MainWindow(root, username)
        
        # Load default map for convenience if exists
        map_path = os.path.join(base_dir, "data", "mapa.csv")
        if os.path.exists(map_path):
            app._load_map(map_path)
            
        # No extra mainloop needed, we are already inside root.mainloop()

    # Login
    login_window = LoginWindow(root, user_manager, start_app)
    
    root.mainloop()

if __name__ == "__main__":
    main()
