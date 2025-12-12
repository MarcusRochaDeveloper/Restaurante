import customtkinter as ctk
from tkinter import messagebox

# Importação das Views
from views.pedidos_view import PedidosView
from views.cardapio_view import CardapioView
from views.mesas_view import MesasView
from views.usuarios_view import UsuariosView

class MainView(ctk.CTkFrame):
    def __init__(self, master, usuario, session):
        super().__init__(master)
        self.session = session
        self.usuario = usuario
        
        # --- PALETA ---
        self.colors = {
            "primary": "#007BFF",       # Azul Corporativo Brilhante
            "primary_dark": "#0056b3",
            "sidebar_bg": "#181A1F",    # Cinza azulado muito escuro 
            "header_bg": "#21252B",     # Barra superior distinta
            "content_bg": "#282C34",    # Fundo principal (Dracula theme vibe)
            "text_main": "#ECEFF4",     # Branco gelo
            "text_muted": "#ABB2BF",    # Cinza claro para textos secundários
            "divider": "#2F333D",       # Linhas sutis
            "hover": "#2C313A",
            "active_bg": "#2F3542",     # Fundo do item ativo
            "danger": "#E06C75"
        }

        # Layout Principal: Sidebar Fixa | [Header + Conteúdo]
        self.grid_columnconfigure(0, weight=0) # Coluna 0: Sidebar
        self.grid_columnconfigure(1, weight=1) # Coluna 1: Área Principal
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_main_area() # Nova estrutura que contém Header + Conteúdo
        
        self.navegar_para("Mesas")

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self, 
            fg_color=self.colors["sidebar_bg"], 
            width=260, 
            corner_radius=0
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        # Grid Interno
        self.sidebar.grid_columnconfigure(0, weight=1)
        self.sidebar.grid_rowconfigure(3, weight=1) # Espaço flexível antes do footer

        # --- 1. LOGO AREA ---
        self.logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent", height=80)
        self.logo_frame.grid(row=0, column=0, sticky="ew", pady=(20, 10))
        self.logo_frame.pack_propagate(False)

        logo_content = ctk.CTkFrame(self.logo_frame, fg_color="transparent")
        logo_content.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(logo_content, text="❖", font=("Arial", 28), text_color=self.colors["primary"]).pack(side="left", padx=(0, 10))
        
        text_stack = ctk.CTkFrame(logo_content, fg_color="transparent")
        text_stack.pack(side="left")
        
        ctk.CTkLabel(text_stack, text="ERP SYSTEM", font=ctk.CTkFont(family="Roboto", size=14, weight="bold"), text_color="white").pack(anchor="w")
        ctk.CTkLabel(text_stack, text="Food Service v2.0", font=ctk.CTkFont(size=10), text_color=self.colors["text_muted"]).pack(anchor="w")

        # Separador
        ctk.CTkFrame(self.sidebar, height=1, fg_color=self.colors["divider"]).grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))

        # --- 2. MENU ---
        self.nav_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.nav_frame.grid(row=2, column=0, sticky="ew")

        self.menu_items = {} 
        
        # Menus com Ícones mais "sérios" (simulados com unicode)
        menus = [
            ("Mesas", "⣿  "), # Ícone de grid
            ("Pedidos", "📄  "),
            ("Cardápio", "❖  "),
            ("Funcionários", "👥  ")
        ]

        for key, icon in menus:
            # Container do Item
            item_btn = ctk.CTkButton(
                self.nav_frame,
                text=f"{icon}  {key.upper()}", # Caixa alta é muito usado em ERP
                anchor="w",
                font=ctk.CTkFont(family="Roboto", size=12, weight="bold"),
                fg_color="transparent",
                text_color=self.colors["text_muted"],
                hover_color=self.colors["hover"],
                corner_radius=6,
                height=45,
                border_spacing=20, # Padding interno texto
                command=lambda k=key: self.navegar_para(k)
            )
            item_btn.pack(fill="x", pady=2, padx=10)
            
            # Pequeno indicador lateral (fino)
            indicator = ctk.CTkFrame(self.nav_frame, width=3, height=25, fg_color="transparent", corner_radius=2)
            indicator.place(in_=item_btn, relx=0.0, rely=0.5, anchor="w", x=-10) # Posicionado relativo ao botão

            self.menu_items[key] = {"btn": item_btn, "indicator": indicator}

        # --- 3. RODAPÉ (USER PROFILE) ---
        self.footer = ctk.CTkFrame(self.sidebar, fg_color="#141619", height=70, corner_radius=0)
        self.footer.grid(row=4, column=0, sticky="ew")
        self.footer.pack_propagate(False)

        # Conteúdo Footer
        f_content = ctk.CTkFrame(self.footer, fg_color="transparent")
        f_content.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9)

        # Avatar
        lbl_avatar = ctk.CTkLabel(
            f_content, 
            text=self.usuario.nome[0].upper(), 
            width=32, height=32, 
            fg_color=self.colors["primary"], 
            font=("Arial", 14, "bold"),
            corner_radius=6 # Quadrado arredondado (estilo Jira/Slack)
        )
        lbl_avatar.pack(side="left")

        # Info
        info = ctk.CTkFrame(f_content, fg_color="transparent")
        info.pack(side="left", padx=10)
        ctk.CTkLabel(info, text=self.usuario.nome.split()[0], font=("Roboto", 13, "bold"), text_color="white").pack(anchor="w")
        cargo = "Administrador" if "admin" in self.usuario.email else "Operador"
        ctk.CTkLabel(info, text=cargo, font=("Roboto", 10), text_color=self.colors["text_muted"]).pack(anchor="w")

        # Logout Sutil
        ctk.CTkButton(
            f_content, text="✖", width=25, height=25, 
            fg_color="transparent", hover_color=self.colors["hover"], 
            text_color=self.colors["text_muted"],
            command=self.fazer_logout
        ).pack(side="right")

    def create_main_area(self):
        # Container da Direita (Header + Conteúdo)
        self.right_panel = ctk.CTkFrame(self, fg_color=self.colors["content_bg"], corner_radius=0)
        self.right_panel.grid(row=0, column=1, sticky="nsew")
        
        self.right_panel.grid_rowconfigure(1, weight=1) # Conteúdo expande
        self.right_panel.grid_columnconfigure(0, weight=1)

        # --- TOP BAR (HEADER) ---
        self.topbar = ctk.CTkFrame(self.right_panel, fg_color=self.colors["header_bg"], height=60, corner_radius=0)
        self.topbar.grid(row=0, column=0, sticky="ew")
        self.topbar.pack_propagate(False)

        # Breadcrumbs / Título da Página
        self.lbl_page_title = ctk.CTkLabel(
            self.topbar, 
            text="DASHBOARD", 
            font=ctk.CTkFont(family="Roboto", size=18, weight="bold"),
            text_color=self.colors["text_main"]
        )
        self.lbl_page_title.pack(side="left", padx=30)

        # Área de Status/Data (Direita da Topbar)
        import datetime
        data_hoje = datetime.datetime.now().strftime("%d/%m/%Y")
        
        status_frame = ctk.CTkFrame(self.topbar, fg_color="transparent")
        status_frame.pack(side="right", padx=30)
        
        ctk.CTkLabel(status_frame, text=f"📅 {data_hoje}", font=("Roboto", 12), text_color=self.colors["text_muted"]).pack(side="left", padx=15)
        ctk.CTkLabel(status_frame, text="● Online", font=("Roboto", 12, "bold"), text_color="#50FA7B").pack(side="left")

        # --- ÁREA DE CONTEÚDO ---
        self.content_area = ctk.CTkFrame(self.right_panel, fg_color="transparent", corner_radius=0)
        self.content_area.grid(row=1, column=0, sticky="nsew", padx=20, pady=20) # Padding interno do conteúdo
        
        # Grid para views filhas
        self.content_area.grid_rowconfigure(0, weight=1)
        self.content_area.grid_columnconfigure(0, weight=1)
        
        self.active_view = None

    def navegar_para(self, nome_tela):
        # Atualiza Título da Topbar
        self.lbl_page_title.configure(text=f"{nome_tela.upper()}")

        # Atualiza Menu Lateral
        for key, item in self.menu_items.items():
            btn = item["btn"]
            indicator = item["indicator"]
            
            if key == nome_tela:
                # ATIVO
                btn.configure(
                    fg_color=self.colors["active_bg"],
                    text_color=self.colors["primary"],
                    hover_color=self.colors["active_bg"] # Mantém cor se passar mouse
                )
                indicator.configure(fg_color=self.colors["primary"])
                indicator.place(x=0) # Mostra a barra
            else:
                # INATIVO
                btn.configure(
                    fg_color="transparent",
                    text_color=self.colors["text_muted"],
                    hover_color=self.colors["hover"]
                )
                indicator.place(x=-10) # Esconde a barra

        # Troca View
        if self.active_view:
            self.active_view.destroy()

        view_args = {"master": self.content_area, "session": self.session}
        if nome_tela == "Pedidos": view_args["usuario"] = self.usuario
        
        view_classes = {
            "Mesas": MesasView,
            "Pedidos": PedidosView,
            "Cardápio": CardapioView,
            "Funcionários": UsuariosView
        }
        
        ViewClass = view_classes.get(nome_tela)
        if ViewClass:
            if nome_tela == "Pedidos":
                self.active_view = ViewClass(self.content_area, self.session, self.usuario)
            else:
                self.active_view = ViewClass(self.content_area, self.session)
            
            self.active_view.grid(row=0, column=0, sticky="nsew")

    def fazer_logout(self):
        if messagebox.askyesno("Logout", "Encerrar sessão no ERP?"):
            self.master.mostrar_login()