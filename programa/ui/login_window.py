import tkinter as tk
from tkinter import messagebox

class LoginWindow:
    def __init__(self, root, user_manager, on_login_success):
        self.root = root
        self.user_manager = user_manager
        self.on_login_success = on_login_success
        
        self.root.title("MiniWaze - Login")
        self.root.geometry("300x200")
        
        self._build_ui()

    def _build_ui(self):
        # Frame
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True, fill='both')

        # Title
        tk.Label(frame, text="Iniciar Sesión", font=("Arial", 16)).pack(pady=10)

        # Username
        tk.Label(frame, text="Usuario:").pack(anchor='w')
        self.entry_user = tk.Entry(frame)
        self.entry_user.pack(fill='x', pady=5)

        # Password
        tk.Label(frame, text="Contraseña:").pack(anchor='w')
        self.entry_pwd = tk.Entry(frame, show="*")
        self.entry_pwd.pack(fill='x', pady=5)

        # Button
        tk.Button(frame, text="Ingresar", command=self._login, bg="#4CAF50", fg="white").pack(fill='x', pady=15)

    def _login(self):
        user = self.entry_user.get().strip()
        pwd = self.entry_pwd.get().strip()

        if self.user_manager.authenticate(user, pwd):
            self.on_login_success(user)
        else:
            messagebox.showerror("Error", "Credenciales inválidas")
