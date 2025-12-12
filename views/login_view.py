import customtkinter as ctk
from tkinter import messagebox

class LoginView(ctk.CTkFrame):
    # ATENÇÃO: Adicionado o parâmetro 'on_register_click'
    def __init__(self, master, on_login_success, on_register_click):
        super().__init__(master)
        self.on_login_success = on_login_success
        self.on_register_click = on_register_click # Callback para ir para o cadastro
        
        # --- PALETA DE CORES (Enterprise Dark) ---
        self.colors = {
            "primary": "#0055D4",      # Azul Royal
            "primary_hover": "#0044AA",
            "bg_dark": "#121212",      # Fundo Esquerdo
            "bg_form": "#181818",      # Fundo Direito (Sutilmente mais claro para contraste)
            "input_bg": "#252525",     # Inputs
            "text_light": "#FFFFFF",
            "text_gray": "#888888"     # Texto secundário mais discreto
        }
        
        # Layout Split Screen
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=4) # Lado Azul (40%)
        self.grid_columnconfigure(1, weight=6) # Lado Preto (60%)
        
        self.create_widgets()
        
    def create_widgets(self):
        # ============================================================
        # 🟦 LADO ESQUERDO: BRANDING & VALOR
        # ============================================================
        self.brand_panel = ctk.CTkFrame(self, fg_color=self.colors["primary"], corner_radius=0)
        self.brand_panel.grid(row=0, column=0, sticky="nsew")
        
        # Centralização
        self.brand_panel.grid_columnconfigure(0, weight=1)
        self.brand_panel.grid_rowconfigure(0, weight=1)
        
        content_box = ctk.CTkFrame(self.brand_panel, fg_color="transparent")
        content_box.grid(row=0, column=0, padx=40)

        # Ícone/Logo Minimalista
        ctk.CTkLabel(content_box, text="🍽️", font=("Arial", 60)).pack(pady=(0, 20))

        # Título de Impacto
        ctk.CTkLabel(
            content_box,
            text="Gestão Inteligente\npara seu Negócio",
            font=ctk.CTkFont(family="Roboto", size=30, weight="bold"),
            text_color="white",
            justify="center"
        ).pack(pady=(0, 15))

        # Subtítulo 
        ctk.CTkLabel(
            content_box,
            text="Otimize o atendimento, controle\nmesas e acompanhe seu faturamento\nem tempo real.",
            font=ctk.CTkFont(family="Roboto", size=15),
            text_color="#E0E0E0",
            justify="center"
        ).pack()

        # ============================================================
        # ⬛ LADO DIREITO: LOGIN
        # ============================================================
        self.form_panel = ctk.CTkFrame(self, fg_color=self.colors["bg_dark"], corner_radius=0)
        self.form_panel.grid(row=0, column=1, sticky="nsew")
        
        self.form_panel.grid_columnconfigure(0, weight=1)
        self.form_panel.grid_rowconfigure(0, weight=1)
        
        # Container do Formulário
        self.login_box = ctk.CTkFrame(self.form_panel, fg_color="transparent")
        self.login_box.grid(row=0, column=0, sticky="ew", padx=80) # Margem lateral maior para elegância
        self.login_box.grid_columnconfigure(0, weight=1)

        # Cabeçalho do Form
        ctk.CTkLabel(
            self.login_box,
            text="Bem-vindo",
            font=ctk.CTkFont(family="Roboto", size=32, weight="bold"),
            text_color="white"
        ).pack(anchor="w", pady=(0, 5))
        
        ctk.CTkLabel(
            self.login_box,
            text="Insira suas credenciais para continuar.",
            font=ctk.CTkFont(size=14),
            text_color=self.colors["text_gray"]
        ).pack(anchor="w", pady=(0, 30))

        # --- INPUTS ---
        def create_label(text):
            return ctk.CTkLabel(
                self.login_box, text=text, 
                font=ctk.CTkFont(size=12, weight="bold"), 
                text_color=self.colors["text_gray"]
            )

        # Email
        create_label("EMAIL CORPORATIVO").pack(anchor="w", pady=(0, 5))
        self.email_entry = ctk.CTkEntry(
            self.login_box,
            placeholder_text="seu@email.com",
            height=45,
            corner_radius=8,
            fg_color=self.colors["input_bg"],
            border_width=0,
            text_color="white"
        )
        self.email_entry.pack(fill="x", pady=(0, 20))

        # Senha
        create_label("SENHA DE ACESSO").pack(anchor="w", pady=(0, 5))
        self.senha_entry = ctk.CTkEntry(
            self.login_box,
            placeholder_text="••••••••",
            show="●",
            height=45,
            corner_radius=8,
            fg_color=self.colors["input_bg"],
            border_width=0,
            text_color="white"
        )
        self.senha_entry.pack(fill="x", pady=(0, 30)) 

        # --- AÇÕES ---
        self.btn_login = ctk.CTkButton(
            self.login_box,
            text="ENTRAR NO SISTEMA",
            height=50,
            corner_radius=25,
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"],
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.fazer_login
        )
        self.btn_login.pack(fill="x", pady=(0, 20))

        # --- RODAPÉ: CADASTRAR-SE ---
        footer_frame = ctk.CTkFrame(self.login_box, fg_color="transparent")
        footer_frame.pack()

        ctk.CTkLabel(
            footer_frame, 
            text="Ainda não possui acesso?", 
            text_color=self.colors["text_gray"],
            font=ctk.CTkFont(size=13)
        ).pack(side="left")

        ctk.CTkButton(
            footer_frame,
            text="Criar uma conta",
            width=100,
            fg_color="transparent",
            text_color=self.colors["primary"],
            hover_color=self.colors["input_bg"],
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.on_register_click # Chama a função de navegação
        ).pack(side="left", padx=5)

        # Binds
        self.senha_entry.bind("<Return>", lambda e: self.fazer_login())
        self.email_entry.bind("<Return>", lambda e: self.senha_entry.focus_set())
    
    def fazer_login(self):
        email = self.email_entry.get().strip()
        senha = self.senha_entry.get()
        
        if not email or not senha:
            messagebox.showwarning("Atenção", "Informe suas credenciais para entrar.")
            return
        
        self.on_login_success(email, senha)