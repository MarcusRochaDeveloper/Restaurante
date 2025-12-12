import customtkinter as ctk
from tkinter import messagebox

class RegisterView(ctk.CTkFrame):
    def __init__(self, master, on_register, on_back_to_login):
        super().__init__(master)
        self.on_register = on_register
        self.on_back_to_login = on_back_to_login
        
        # --- PALETA DE CORES ---
        self.colors = {
            "primary": "#0055D4",
            "primary_hover": "#0044AA",
            "bg_dark": "#121212",
            "input_bg": "#2B2B2B",
            "text_gray": "#A0A0A0"
        }
        
        # Layout Split Screen (Igual ao Login)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=4) # Lado Azul
        self.grid_columnconfigure(1, weight=6) # Lado Preto
        
        self.create_widgets()
        
    def create_widgets(self):
        # ============================================================
        # 🟦 LADO ESQUERDO: BRANDING (AZUL)
        # ============================================================
        self.brand_frame = ctk.CTkFrame(self, fg_color=self.colors["primary"], corner_radius=0)
        self.brand_frame.grid(row=0, column=0, sticky="nsew")
        
        self.brand_frame.grid_columnconfigure(0, weight=1)
        self.brand_frame.grid_rowconfigure(0, weight=1)
        
        content_box = ctk.CTkFrame(self.brand_frame, fg_color="transparent")
        content_box.grid(row=0, column=0)
        
        ctk.CTkLabel(
            content_box,
            text="Junte-se a nós!",
            font=ctk.CTkFont(family="Roboto", size=32, weight="bold"),
            text_color="white"
        ).pack(pady=(0, 15))
        
        ctk.CTkLabel(
            content_box,
            text="Crie sua conta administrativa\ne comece a gerenciar seu\nrestaurante hoje mesmo.",
            font=ctk.CTkFont(family="Roboto", size=16),
            text_color="#E0E0E0",
            justify="center"
        ).pack()

        # ============================================================
        # ⬛ LADO DIREITO: FORMULÁRIO (PRETO)
        # ============================================================
        self.form_frame = ctk.CTkFrame(self, fg_color=self.colors["bg_dark"], corner_radius=0)
        self.form_frame.grid(row=0, column=1, sticky="nsew")
        
        self.form_frame.grid_columnconfigure(0, weight=1)
        self.form_frame.grid_rowconfigure(0, weight=1)
        
        # Box Centralizado
        form_box = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        form_box.grid(row=0, column=0, sticky="ew", padx=60)
        form_box.grid_columnconfigure(0, weight=1)

        # Título
        ctk.CTkLabel(
            form_box, 
            text="Nova Conta", 
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.colors["primary"]
        ).pack(anchor="w", pady=(0, 30))

        # --- INPUTS ---
        def create_input(label, placeholder, show=None):
            ctk.CTkLabel(form_box, text=label, font=ctk.CTkFont(size=12, weight="bold"), text_color=self.colors["text_gray"]).pack(anchor="w", pady=(10, 5))
            entry = ctk.CTkEntry(
                form_box, 
                height=45, 
                corner_radius=8, 
                fg_color=self.colors["input_bg"], 
                border_width=0, 
                text_color="white",
                placeholder_text=placeholder,
                show=show
            )
            entry.pack(fill="x")
            return entry

        self.nome_entry = create_input("Nome Completo", "Ex: João Silva")
        self.email_entry = create_input("Email Corporativo", "seu@email.com")
        self.senha_entry = create_input("Senha", "Mínimo 6 caracteres", show="●")
        self.confirm_entry = create_input("Confirmar Senha", "Repita a senha", show="●")

        # --- BOTÕES ---
        ctk.CTkButton(
            form_box,
            text="CRIAR CONTA",
            height=50,
            corner_radius=25,
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"],
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.registrar
        ).pack(fill="x", pady=(30, 15))
        
        # Link Voltar
        link_frame = ctk.CTkFrame(form_box, fg_color="transparent")
        link_frame.pack()
        ctk.CTkLabel(link_frame, text="Já tem uma conta?", text_color="gray").pack(side="left")
        ctk.CTkButton(
            link_frame,
            text="Fazer Login",
            width=80,
            fg_color="transparent",
            text_color=self.colors["primary"],
            hover_color=self.colors["input_bg"],
            font=ctk.CTkFont(weight="bold"),
            command=self.on_back_to_login
        ).pack(side="left", padx=5)

    def registrar(self):
        nome = self.nome_entry.get().strip()
        email = self.email_entry.get().strip()
        senha = self.senha_entry.get()
        confirm = self.confirm_entry.get()
        
        if not nome or not email or not senha:
            messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios.")
            return
        
        if senha != confirm:
            messagebox.showerror("Erro", "As senhas não coincidem.")
            return
            
        if len(senha) < 4:
            messagebox.showwarning("Segurança", "A senha deve ter pelo menos 4 caracteres.")
            return

        self.on_register(nome, email, senha)