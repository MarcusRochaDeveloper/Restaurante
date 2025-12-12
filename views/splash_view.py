import customtkinter as ctk
import random

class SplashView(ctk.CTkFrame):
    def __init__(self, master, on_finished):
        super().__init__(master)
        self.on_finished = on_finished
        
        # --- PALETA DE CORES ---
        self.colors = {
            "bg_dark": "#121212",      # Fundo Principal
            "primary": "#0055D4",      # Azul Marca
            "primary_dim": "#003E9C",  # Azul Escuro
            "accent": "#00E5FF",       # Cyan para detalhes tecnológicos
            "text_white": "#FFFFFF",
            "text_gray": "#666666",    # Cinza para logs
            "tip_bg": "#1E1E1E"        # Fundo da caixa de dicas
        }
        
        self.configure(fg_color=self.colors["bg_dark"])
        self.pack(fill="both", expand=True)
        
        # Grid Centralizado
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Dados para animação
        self.dicas = [
            "💡 DICA: Use as setas do teclado para navegar nas listas.",
            "🔥 SABIA? O sistema faz backup automático a cada 24h.",
            "🚀 PRO: Clique em 'Cardápio' para adicionar fotos aos pratos.",
            "📊 GESTÃO: O painel de Mesas mostra ocupação em tempo real.",
            "🔒 SEGURANÇA: Todos os dados trafegam criptografados.",
            "⚡ ATALHO: Pressione F11 para alternar o modo tela cheia.",
            "👥 EQUIPE: Gerentes podem ver logs de acesso dos funcionários."
        ]
        
        self.logs_tecnicos = [
            "Loading assets/fonts/roboto.ttf...",
            "Initializing SQLAlchemy Core...",
            "Verifying database schema integrity...",
            "Allocating memory pools for UI...",
            "Establishing secure handshake...",
            "Loading user_preferences.json...",
            "Mounting file system drivers...",
            "Pre-caching thumbnails...",
            "Optimizing render pipeline...",
            "Checking network latency...",
            "Syncing local timestamps...",
            "Validating license signature...",
            "Starting background workers...",
            "System ready."
        ]

        self.create_ui()
        self.iniciar_animacoes()

    def create_ui(self):
        # Container Central
        self.center_box = ctk.CTkFrame(self, fg_color="transparent")
        self.center_box.grid(row=0, column=0)
        
        # --- 1. LOGO PULSANTE ---
        self.logo_border = ctk.CTkFrame(
            self.center_box, 
            width=108, height=108, 
            corner_radius=29,
            fg_color=self.colors["primary_dim"]
        )
        self.logo_border.pack(pady=(0, 25))
        
        self.logo_inner = ctk.CTkFrame(
            self.logo_border, 
            width=100, height=100, 
            corner_radius=25,
            fg_color=self.colors["primary"]
        )
        self.logo_inner.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(
            self.logo_inner,
            text="RP",
            font=ctk.CTkFont(family="Arial", size=40, weight="bold"),
            text_color="white"
        ).place(relx=0.5, rely=0.5, anchor="center")
        
        # Título
        ctk.CTkLabel(
            self.center_box,
            text="RESTAURANTE PRO",
            font=ctk.CTkFont(family="Roboto", size=28, weight="bold"),
            text_color="white"
        ).pack(pady=(0, 5))

        ctk.CTkLabel(
            self.center_box,
            text="Enterprise Edition v2.4",
            font=ctk.CTkFont(family="Roboto", size=12),
            text_color=self.colors["text_gray"]
        ).pack(pady=(0, 40))
        
        # --- 2. BARRA DE CARREGAMENTO ---
        self.progress_bar = ctk.CTkProgressBar(
            self.center_box,
            width=400,
            height=6,
            corner_radius=3,
            progress_color=self.colors["accent"],
            fg_color="#222222",
            mode="determinate"
        )
        self.progress_bar.pack(pady=(0, 10))
        self.progress_bar.set(0)
        
        # Log Técnico
        self.lbl_log = ctk.CTkLabel(
            self.center_box,
            text="Initializing...",
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color="#444444"
        )
        self.lbl_log.pack(anchor="w", padx=5)

        # --- 3. ÁREA DE DICAS (FIXA NO RODAPÉ) ---
        self.tip_frame = ctk.CTkFrame(
            self, 
            fg_color=self.colors["tip_bg"], 
            height=60, 
            corner_radius=0
        )
        self.tip_frame.place(relx=0, rely=0.9, relwidth=1.0, anchor="sw")
        
        ctk.CTkLabel(
            self.tip_frame, 
            text="💡", 
            font=("Arial", 24)
        ).place(relx=0.05, rely=0.5, anchor="center")
        
        self.lbl_dica = ctk.CTkLabel(
            self.tip_frame,
            text=self.dicas[0],
            font=ctk.CTkFont(family="Roboto", size=14, slant="italic"),
            text_color="#DDDDDD"
        )
        self.lbl_dica.place(relx=0.08, rely=0.5, anchor="w")

    def iniciar_animacoes(self):
        self.progresso = 0
        self.log_index = 0
        self.dica_index = 0
        
        self._animar_barra()
        self._animar_logs()
        self._animar_dicas()
        self._animar_logo_pulse()

    def _animar_barra(self):
        if self.progresso < 100:
            
            # Usei random para dar uma leve variação "orgânica"
            incremento = random.uniform(0.25, 0.45) 
            self.progresso += incremento
            
            # Pequena "freada" no final para suspense (95% a 99%)
            if self.progresso > 95:
                self.progresso -= 0.15 

            self.progress_bar.set(self.progresso / 100)
            
            # Chama novamente em 50ms
            self.after(50, self._animar_barra)
        else:
            # Terminou
            self.after(500, self.on_finished)

    def _animar_logs(self):
        # Logs passam rápido 
        if self.progresso < 98:
            texto = random.choice(self.logs_tecnicos)
            self.lbl_log.configure(text=f"> {texto}")
            
            # Atualiza log a cada 120ms 
            self.after(120, self._animar_logs)
        else:
            self.lbl_log.configure(text="> Starting user interface...")

    def _animar_dicas(self):
        # Dicas trocam mais devagar para dar tempo de ler
        if self.progresso < 95:
            self.dica_index = (self.dica_index + 1) % len(self.dicas)
            nova_dica = self.dicas[self.dica_index]
            self.lbl_dica.configure(text=nova_dica)
            
            # --- TIMER DAS DICAS: 2000ms 
            self.after(2000, self._animar_dicas)

    def _animar_logo_pulse(self):
        if self.progresso < 100:
            cor_atual = self.logo_border.cget("fg_color")
            nova_cor = self.colors["primary"] if cor_atual == self.colors["primary_dim"] else self.colors["primary_dim"]
            
            self.logo_border.configure(fg_color=nova_cor)
            self.after(800, self._animar_logo_pulse)