import customtkinter as ctk
from tkinter import messagebox
from views.pedidos_view import PedidosView
from views.cardapio_view import CardapioView
from views.mesas_view import MesasView
from views.usuarios_view import UsuariosView
import datetime

class MainView(ctk.CTkFrame):
    def __init__(self, master, usuario, session):
        super().__init__(master)
        self.session = session
        self.usuario = usuario
        
        self.colors = {
            "primary": "#007BFF",
            "primary_dark": "#0056b3",
            "sidebar_bg": "#181A1F",
            "header_bg": "#21252B",
            "content_bg": "#282C34",
            "text_main": "#ECEFF4",
            "text_muted": "#ABB2BF",
            "divider": "#2F333D",
            "hover": "#2C313A",
            "active_bg": "#2F3542",
            "danger": "#E06C75"
        }

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_main_area()
        self.navegar_para("Mesas")

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, fg_color=self.colors["sidebar_bg"], width=260, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        self.sidebar.grid_columnconfigure(0, weight=1)
        self.sidebar.grid_rowconfigure(3, weight=1)

        # --- LOGO AREA ---
        self.logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent", height=80)
        self.logo_frame.grid(row=0, column=0, sticky="ew", pady=(20, 10))
        self.logo_frame.pack_propagate(False)

        logo_content = ctk.CTkFrame(self.logo_frame, fg_color="transparent")
        logo_content.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(logo_content, text="❖", font=("Arial", 28), text_color=self.colors["primary"]).pack(side="left", padx=(0, 10))
        
        text_stack = ctk.CTkFrame(logo_content, fg_color="transparent")
        text_stack.pack(side="left")
        
        ctk.CTkLabel(text_stack, text="NEXORA", font=ctk.CTkFont(family="Roboto", size=16, weight="bold"), text_color="white").pack(anchor="w")
        ctk.CTkLabel(text_stack, text="ENTERPRISE ERP", font=ctk.CTkFont(size=10, weight="bold"), text_color=self.colors["text_muted"]).pack(anchor="w")

        ctk.CTkFrame(self.sidebar, height=1, fg_color=self.colors["divider"]).grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))

        # --- MENU ---
        self.nav_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.nav_frame.grid(row=2, column=0, sticky="ew")

        self.menu_items = {} 
        
        menus = [
            ("Mesas", "🪑  "),
            ("Pedidos", "📄  "),
            ("Cardápio", "🛎️  "),
            ("Funcionários", "👥  ")
        ]

        for key, icon in menus:
            item_btn = ctk.CTkButton(
                self.nav_frame,
                text=f"{icon}  {key.upper()}",
                anchor="w",
                font=ctk.CTkFont(family="Roboto", size=12, weight="bold"),
                fg_color="transparent",
                text_color=self.colors["text_muted"],
                hover_color=self.colors["hover"],
                corner_radius=6,
                height=45,
                border_spacing=20,
                command=lambda k=key: self.navegar_para(k)
            )
            item_btn.pack(fill="x", pady=2, padx=10)
            
            indicator = ctk.CTkFrame(self.nav_frame, width=3, height=25, fg_color="transparent", corner_radius=2)
            indicator.place(in_=item_btn, relx=0.0, rely=0.5, anchor="w", x=-10)

            self.menu_items[key] = {"btn": item_btn, "indicator": indicator}

        # --- USER PROFILE ---
        self.footer = ctk.CTkFrame(self.sidebar, fg_color="#141619", height=70, corner_radius=0)
        self.footer.grid(row=4, column=0, sticky="ew")
        self.footer.pack_propagate(False)

        f_content = ctk.CTkFrame(self.footer, fg_color="transparent")
        f_content.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9)

        initial = self.usuario.nome[0].upper() if self.usuario.nome else "U"
        ctk.CTkLabel(f_content, text=initial, width=32, height=32, fg_color=self.colors["primary"], font=("Arial", 14, "bold"), corner_radius=6).pack(side="left")

        info = ctk.CTkFrame(f_content, fg_color="transparent")
        info.pack(side="left", padx=10)
        
        display_name = self.usuario.nome.split()[0]
        ctk.CTkLabel(info, text=display_name, font=("Roboto", 13, "bold"), text_color="white").pack(anchor="w")
        
        role = "Administrador" if "admin" in self.usuario.email else "Operador"
        ctk.CTkLabel(info, text=role, font=("Roboto", 10), text_color=self.colors["text_muted"]).pack(anchor="w")

        ctk.CTkButton(
            f_content, text="✖", width=25, height=25, 
            fg_color="transparent", hover_color=self.colors["hover"], text_color=self.colors["text_muted"],
            command=self.fazer_logout
        ).pack(side="right")

    def create_main_area(self):
        self.right_panel = ctk.CTkFrame(self, fg_color=self.colors["content_bg"], corner_radius=0)
        self.right_panel.grid(row=0, column=1, sticky="nsew")
        
        self.right_panel.grid_rowconfigure(1, weight=1)
        self.right_panel.grid_columnconfigure(0, weight=1)

        # --- TOP BAR ---
        self.topbar = ctk.CTkFrame(self.right_panel, fg_color=self.colors["header_bg"], height=60, corner_radius=0)
        self.topbar.grid(row=0, column=0, sticky="ew")
        self.topbar.pack_propagate(False)

        self.lbl_page_title = ctk.CTkLabel(
            self.topbar, text="DASHBOARD", 
            font=ctk.CTkFont(family="Roboto", size=18, weight="bold"), text_color=self.colors["text_main"]
        )
        self.lbl_page_title.pack(side="left", padx=30)

        data_hoje = datetime.datetime.now().strftime("%d/%m/%Y")
        status_frame = ctk.CTkFrame(self.topbar, fg_color="transparent")
        status_frame.pack(side="right", padx=30)
        
        ctk.CTkLabel(status_frame, text=f"📅 {data_hoje}", font=("Roboto", 12), text_color=self.colors["text_muted"]).pack(side="left", padx=15)
        ctk.CTkLabel(status_frame, text="● Online", font=("Roboto", 12, "bold"), text_color="#50FA7B").pack(side="left")

        # --- CONTENT AREA ---
        self.content_area = ctk.CTkFrame(self.right_panel, fg_color="transparent", corner_radius=0)
        self.content_area.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        
        self.content_area.grid_rowconfigure(0, weight=1)
        self.content_area.grid_columnconfigure(0, weight=1)
        self.active_view = None

    def navegar_para(self, nome_tela):
        self.lbl_page_title.configure(text=f"{nome_tela.upper()}")

        for key, item in self.menu_items.items():
            btn = item["btn"]
            indicator = item["indicator"]
            
            if key == nome_tela:
                btn.configure(fg_color=self.colors["active_bg"], text_color=self.colors["primary"], hover_color=self.colors["active_bg"])
                indicator.configure(fg_color=self.colors["primary"])
                indicator.place(x=0)
            else:
                btn.configure(fg_color="transparent", text_color=self.colors["text_muted"], hover_color=self.colors["hover"])
                indicator.place(x=-10)

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