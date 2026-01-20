import customtkinter as ctk
from tkinter import messagebox
from services.auth_service import AuthService


class LoginWindow:
    def __init__(self):
        self.auth_service = AuthService()
        self.root = None
        self.on_success_callback = None
        
    def create_window(self, on_success_callback):
        """Create login window"""
        self.on_success_callback = on_success_callback
        
        self.root = ctk.CTk()
        self.root.title("GES - Sistema de Gestión Escolar")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Configure grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Main frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame, 
            text="GES - Login", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=10, pady=(20, 30))
        
        # Username
        username_label = ctk.CTkLabel(main_frame, text="Usuario:")
        username_label.grid(row=1, column=0, padx=10, pady=(0, 5), sticky="w")
        
        self.username_entry = ctk.CTkEntry(main_frame, width=300)
        self.username_entry.grid(row=2, column=0, padx=10, pady=(0, 20))
        
        # Password
        password_label = ctk.CTkLabel(main_frame, text="Contraseña:")
        password_label.grid(row=3, column=0, padx=10, pady=(0, 5), sticky="w")
        
        self.password_entry = ctk.CTkEntry(main_frame, width=300, show="*")
        self.password_entry.grid(row=4, column=0, padx=10, pady=(0, 30))
        
        # Login button
        login_button = ctk.CTkButton(
            main_frame, 
            text="Iniciar Sesión", 
            command=self.login,
            width=300,
            height=40
        )
        login_button.grid(row=5, column=0, padx=10, pady=(0, 10))
        
        # Bind Enter key
        self.root.bind("<Return>", lambda event: self.login())
        
        # Focus on username entry
        self.username_entry.focus()
        
        return self.root
    
    def login(self):
        """Handle login attempt"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Por favor ingrese usuario y contraseña")
            return
        
        try:
            user = self.auth_service.authenticate(username, password)
            
            if user:
                messagebox.showinfo("Éxito", f"Bienvenido, {user.username}!")
                self.root.destroy()
                if self.on_success_callback:
                    self.on_success_callback(user)
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos")
                self.password_entry.delete(0, 'end')
                self.password_entry.focus()
                
        except Exception as e:
            messagebox.showerror("Error", f"Error de autenticación: {str(e)}")
    
    def run(self, on_success_callback):
        """Run the login window"""
        window = self.create_window(on_success_callback)
        window.mainloop()
