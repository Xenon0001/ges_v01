"""
Login view for GES application
Handles user authentication interface
"""

import customtkinter as ctk
from tkinter import messagebox
from app.services.auth_service import AuthService
from database.models.person import UserModel


class LoginView:
    """Login window for GES application"""
    
    def __init__(self):
        self.auth_service = AuthService()
        self.root = None
        self.on_success_callback = None
    
    def show(self, on_success_callback=None):
        """Show login window"""
        self.on_success_callback = on_success_callback
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("GES - Sistema de Gestión Escolar")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        # Center window on screen
        self.center_window()
        
        # Create UI elements
        self.create_widgets()
        
        # Start the window
        self.root.mainloop()
    
    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (500 // 2)
        self.root.geometry(f"400x500+{x}+{y}")
    
    def create_widgets(self):
        """Create login form widgets"""
        # Main container
        main_frame = ctk.CTkFrame(self.root, corner_radius=10)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame, 
            text="GES", 
            font=ctk.CTkFont(size=40, weight="bold")
        )
        title_label.pack(pady=(20, 5))
        
        subtitle_label = ctk.CTkLabel(
            main_frame, 
            text="Sistema de Gestión Escolar", 
            font=ctk.CTkFont(size=16)
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Username field
        username_label = ctk.CTkLabel(main_frame, text="Usuario:")
        username_label.pack(pady=(20, 5), anchor="w", padx=20)
        
        self.username_entry = ctk.CTkEntry(
            main_frame, 
            placeholder_text="Ingrese su usuario",
            width=300,
            height=40
        )
        self.username_entry.pack(pady=5, padx=20)
        
        # Password field
        password_label = ctk.CTkLabel(main_frame, text="Contraseña:")
        password_label.pack(pady=(15, 5), anchor="w", padx=20)
        
        self.password_entry = ctk.CTkEntry(
            main_frame, 
            placeholder_text="Ingrese su contraseña",
            show="*",
            width=300,
            height=40
        )
        self.password_entry.pack(pady=5, padx=20)
        
        # Login button
        self.login_button = ctk.CTkButton(
            main_frame,
            text="Iniciar Sesión",
            width=300,
            height=40,
            command=self.handle_login
        )
        self.login_button.pack(pady=30, padx=20)
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda event: self.handle_login())
        
        # Focus on username field
        self.username_entry.focus()
        
        # Status label for error messages
        self.status_label = ctk.CTkLabel(main_frame, text="", text_color="red")
        self.status_label.pack(pady=10)
    
    def handle_login(self):
        """Handle login button click"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        # Validate input
        if not username or not password:
            self.show_error("Por favor ingrese usuario y contraseña")
            return
        
        try:
            # Disable login button during authentication
            self.login_button.configure(state="disabled", text="Autenticando...")
            self.root.update()
            
            # Authenticate using AuthService
            user = self.auth_service.authenticate(username, password)
            
            if user:
                # Success - close login and show main window
                self.show_success("Autenticación exitosa")
                self.root.after(1000, self.on_login_success, user)
            else:
                # Failed authentication
                self.show_error("Usuario o contraseña incorrectos")
                self.password_entry.delete(0, 'end')
                self.password_entry.focus()
                
        except Exception as e:
            self.show_error(f"Error de autenticación: {str(e)}")
        finally:
            # Re-enable login button
            self.login_button.configure(state="normal", text="Iniciar Sesión")
    
    def show_error(self, message):
        """Show error message"""
        self.status_label.configure(text=message)
        # Clear error after 5 seconds
        self.root.after(5000, lambda: self.status_label.configure(text=""))
    
    def show_success(self, message):
        """Show success message"""
        self.status_label.configure(text=message, text_color="green")
    
    def on_login_success(self, user: UserModel):
        """Handle successful login"""
        # Close login window
        self.root.destroy()
        
        # Call success callback with authenticated user
        if self.on_success_callback:
            self.on_success_callback(user)


def main():
    """Test login view"""
    def on_login_success(user):
        print(f"Login successful! User: {user.username} ({user.role})")
        print("Main window would open here...")
    
    login = LoginView()
    login.show(on_login_success)


if __name__ == "__main__":
    main()
