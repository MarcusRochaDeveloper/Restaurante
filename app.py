import customtkinter as ctk
from tkinter import messagebox
from database import db
from models import Usuario
from utils.security import security_manager

from views.splash_view import SplashView
from views.config_view import ConfigView
from views.login_view import LoginView
from views.main_view import MainView
from views.register_view import RegisterView 

class RestauranteApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Sistema de Restaurante Pro")
        self.colors = {"primary": "#0055D4", "background": "#121212"}
        
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        self.configure(fg_color=self.colors["background"])
        
        width, height = 1200, 700
        self.minsize(1000, 600)
        self.center_window(width, height)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.current_view = None
        self.session = None
        
        self.mostrar_splash()

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width/2) - (width/2))
        y = int((screen_height/2) - (height/2))
        self.geometry(f"{width}x{height}+{x}+{y}")

    def limpar_view(self):
        if self.current_view:
            self.current_view.destroy()
            self.current_view = None

    def mostrar_splash(self):
        self.limpar_view()
        self.current_view = SplashView(self, on_finished=self.mostrar_config)
        self.current_view.grid(row=0, column=0, sticky="nsew")

    def mostrar_config(self):
        self.limpar_view()
        self.current_view = ConfigView(self, self.on_database_connect)
        self.current_view.grid(row=0, column=0, sticky="nsew")
    
    def mostrar_login(self):
        self.limpar_view()
        self.current_view = LoginView(
            self, 
            on_login_success=self.on_login, 
            on_register_click=self.mostrar_cadastro 
        )
        self.current_view.grid(row=0, column=0, sticky="nsew")
        
    def mostrar_cadastro(self):
        self.limpar_view()
        self.current_view = RegisterView(
            self, 
            on_register=self.on_register_submit,
            on_back_to_login=self.mostrar_login
        )
        self.current_view.grid(row=0, column=0, sticky="nsew")

    def mostrar_main(self, usuario):
        self.limpar_view()
        self.current_view = MainView(self, usuario, self.session)
        self.current_view.grid(row=0, column=0, sticky="nsew")

    def on_database_connect(self, config):
        try:
            db.conectar(config['host'], config['port'], config['user'], config['password'], config['dbname'])
            self.session = db.get_session()
            self.mostrar_login()
        except Exception as e:
            messagebox.showerror("Erro de Conexão", f"Falha:\n{str(e)}")

    def on_register_submit(self, nome, email, senha):
        if self.session.query(Usuario).filter_by(email=email).first():
            messagebox.showerror("Erro", "Este email já está cadastrado.")
            return

        try:
            novo_usuario = Usuario(
                nome=nome,
                email=email,
                senha_hash=security_manager.hash_senha(senha),
                senha_encriptada=security_manager.encriptar(senha)
            )
            self.session.add(novo_usuario)
            self.session.commit()
            
            messagebox.showinfo("Sucesso", "Conta criada com sucesso!")
            self.mostrar_login()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar conta: {e}")

    def on_login(self, email, senha):
        if not self.session: return

        usuario = self.session.query(Usuario).filter_by(email=email).first()
        
        if not usuario:
            messagebox.showerror("Login", "Usuário não encontrado.")
            return

        try:
            if security_manager.verificar_senha(senha, usuario.senha_hash):
                self.mostrar_main(usuario)
            else:
                messagebox.showerror("Login", "Senha incorreta.")
        except ValueError:
            messagebox.showerror("Erro", "Dados de login corrompidos.")

if __name__ == "__main__":
    app = RestauranteApp()
    app.mainloop()