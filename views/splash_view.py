import customtkinter as ctk

class SplashView(ctk.CTkFrame):
    def __init__(self, master, on_finished):
        super().__init__(master)
        self.on_finished = on_finished
        
        self.colors = {
            "bg": "#121212",
            "accent": "#0055D4", 
            "text": "#FFFFFF",
            "text_muted": "#666666"
        }
        
        self.configure(fg_color=self.colors["bg"])
        self.pack(fill="both", expand=True)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.criar_interface()
        self.iniciar_sistema()

    def criar_interface(self):
        self.main_box = ctk.CTkFrame(self, fg_color="transparent")
        self.main_box.grid(row=0, column=0)
        
        # Logo Nexora (N)
        self.logo_box = ctk.CTkFrame(
            self.main_box, width=80, height=80, 
            corner_radius=20, fg_color=self.colors["accent"]
        )
        self.logo_box.pack(pady=(0, 20))
        
        ctk.CTkLabel(
            self.logo_box, text="N", 
            font=("Arial", 40, "bold"), text_color="white"
        ).place(relx=0.5, rely=0.5, anchor="center")
        
        # Nome da Marca
        ctk.CTkLabel(
            self.main_box, text="NEXORA", 
            font=ctk.CTkFont(family="Roboto", size=26, weight="bold"),
            text_color="white"
        ).pack(pady=(0, 5))
        
        # Subtítulo
        ctk.CTkLabel(
            self.main_box, text="ENTERPRISE ERP", 
            font=ctk.CTkFont(family="Roboto", size=12),
            text_color=self.colors["text_muted"]
        ).pack(pady=(0, 40))
        
        self.progress = ctk.CTkProgressBar(
            self.main_box, width=300, height=4, 
            corner_radius=2, progress_color=self.colors["accent"],
            fg_color="#1F1F1F", mode="determinate"
        )
        self.progress.pack(pady=(0, 10))
        self.progress.set(0)
        
        self.lbl_status = ctk.CTkLabel(
            self.main_box, text="Iniciando...", 
            font=("Roboto", 11), text_color=self.colors["text_muted"]
        )
        self.lbl_status.pack()
        
        self.footer = ctk.CTkLabel(
            self, text="© 2025 Nexora Systems • v2.4.0", 
            font=("Roboto", 10), text_color="#333333"
        )
        self.footer.place(relx=0.5, rely=0.95, anchor="center")

    def iniciar_sistema(self):
        self.etapa = 0
        self.mensagens = [
            "Carregando módulos do sistema...",
            "Verificando credenciais de segurança...",
            "Conectando ao banco de dados...",
            "Renderizando interface Nexora...",
            "Finalizando inicialização..."
        ]
        self._animar()

    def _animar(self):
        if self.etapa < 100:
            self.etapa += 1.5 
            self.progress.set(self.etapa / 100)
            
            idx = int((self.etapa / 100) * len(self.mensagens))
            idx = min(idx, len(self.mensagens) - 1)
            self.lbl_status.configure(text=self.mensagens[idx])
            
            self.after(30, self._animar)
        else:
            self.on_finished()