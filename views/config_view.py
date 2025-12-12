import customtkinter as ctk
from tkinter import messagebox

class ConfigView(ctk.CTkFrame):
    def __init__(self, master, on_connect):
        super().__init__(master)
        self.on_connect = on_connect
        
        # --- PALETA ENTERPRISE ---
        self.colors = {
            "primary": "#0055D4",      # Azul Royal
            "primary_hover": "#0044AA",
            "bg_left": "#0049B7",      # Azul um pouco mais escuro para o painel esquerdo
            "bg_right": "#121212",     # Preto Profundo
            "input_bg": "#1F1F1F",     # Inputs mais claros que o fundo
            "text_light": "#FFFFFF",
            "text_gray": "#888888",
            "border": "#333333"
        }
        
        # Configuração de Layout Split Screen (40% | 60%)
        self.grid_columnconfigure(0, weight=4) 
        self.grid_columnconfigure(1, weight=6) 
        self.grid_rowconfigure(0, weight=1)
        
        self.create_left_panel()
        self.create_right_panel()
        
    def create_left_panel(self):
        # --- LADO ESQUERDO: CONTEXTO TÉCNICO ---
        self.left_frame = ctk.CTkFrame(self, fg_color=self.colors["primary"], corner_radius=0)
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        
        # Centralizar conteúdo verticalmente
        self.left_frame.grid_columnconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(0, weight=1)
        
        content_box = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        content_box.grid(row=0, column=0, padx=40)
        
        # Ícone de Servidor
        ctk.CTkLabel(
            content_box, 
            text="🖥️", 
            font=("Arial", 80)
        ).pack(pady=(0, 20))
        
        ctk.CTkLabel(
            content_box,
            text="Configuração\nde Ambiente",
            font=ctk.CTkFont(family="Roboto", size=32, weight="bold"),
            text_color="white",
            justify="center"
        ).pack(pady=(0, 20))
        
        status_box = ctk.CTkFrame(
            content_box, 
            fg_color="#003285", # Um azul bem escuro para simular a sombra/box
            corner_radius=10
        )
        status_box.pack(fill="x", pady=20)
        
        ctk.CTkLabel(
            status_box,
            text="STATUS ATUAL:",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="#ADD8E6" # Azul claro
        ).pack(anchor="w", padx=15, pady=(10, 0))
        
        ctk.CTkLabel(
            status_box,
            text="🔴 Desconectado",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#FFCCCC" # Vermelho claro
        ).pack(anchor="w", padx=15, pady=(0, 10))
        
        ctk.CTkLabel(
            content_box,
            text="Defina os parâmetros de conexão\ncom seu servidor SQL para iniciar.",
            font=ctk.CTkFont(size=14),
            text_color="#E0E0E0",
            justify="center"
        ).pack()

    def create_right_panel(self):
        # --- LADO DIREITO: FORMULÁRIO ---
        self.right_frame = ctk.CTkFrame(self, fg_color=self.colors["bg_right"], corner_radius=0)
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        
        # Centralização
        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)
        
        # Container do Form
        self.form_box = ctk.CTkFrame(self.right_frame, fg_color="transparent", width=400)
        self.form_box.grid(row=0, column=0, sticky="ew", padx=60)
        
        # Título do Form
        ctk.CTkLabel(
            self.form_box, 
            text="Database Connection", 
            font=ctk.CTkFont(family="Roboto", size=24, weight="bold"),
            text_color="white"
        ).pack(anchor="w", pady=(0, 30))
        
        self.entries = {}
        
        # Campos
        self.create_input("HOST (IP/URL)", "localhost", "host")
        self.create_input("PORTA", "3306", "port")
        self.create_input("USUÁRIO", "root", "user")
        self.create_input("SENHA", "", "password", show="●")
        self.create_input("NOME DO BANCO", "restaurante_db", "dbname")
        
        # Botão Conectar
        ctk.CTkButton(
            self.form_box,
            text="CONECTAR AO SERVIDOR",
            height=50,
            corner_radius=25,
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"],
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.conectar
        ).pack(fill="x", pady=(30, 0))

    def create_input(self, label_text, default_val, key, show=None):
        # Label
        ctk.CTkLabel(
            self.form_box, 
            text=label_text, 
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=self.colors["text_gray"]
        ).pack(anchor="w", pady=(10, 5))
        
        # Entry Style
        entry = ctk.CTkEntry(
            self.form_box,
            height=40,
            corner_radius=8,
            fg_color=self.colors["input_bg"],
            border_width=1,
            border_color=self.colors["border"],
            text_color="white",
            placeholder_text="...",
            show=show
        )
        if default_val:
            entry.insert(0, default_val)
            
        entry.pack(fill="x")
        self.entries[key] = entry # Salva referência

    def conectar(self):
        # Extrai dados
        config = {k: v.get().strip() for k, v in self.entries.items()}
        
        if not all([config['host'], config['port'], config['user'], config['dbname']]):
            messagebox.showwarning("Atenção", "Preencha os campos obrigatórios.")
            return
        
        self.on_connect(config)