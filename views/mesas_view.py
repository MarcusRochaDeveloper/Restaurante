import customtkinter as ctk
from tkinter import messagebox
from models import Mesa

class MesasView(ctk.CTkFrame):
    def __init__(self, master, session):
        super().__init__(master)
        self.session = session

        # --- PALETA DE CORES PRO ---
        self.colors = {
            "primary": "#0055D4",
            "bg_dark": "#121212",
            "card_bg": "#1E1E1E",      # Fundo dos Cards
            "kpi_bg": "#252525",       # Fundo dos KPIs (mais claro que o fundo)
            "table_free": "#2E7D32",   # Verde
            "table_busy": "#C62828",   # Vermelho
            "text_white": "#FFFFFF",
            "text_gray": "#9E9E9E",
            "text_light_gray": "#D1D1D1"
        }

        self.configure(fg_color="transparent")
        self.pack(fill="both", expand=True, padx=30, pady=30)
        
        self.create_header()
        self.create_metrics_bar() 
        self.create_grid()
        self.listar_mesas()

    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 25))

        title_box = ctk.CTkFrame(header, fg_color="transparent")
        title_box.pack(side="left")
        
        ctk.CTkLabel(
            title_box, 
            text="Planta do Salão", 
            font=ctk.CTkFont(family="Roboto", size=28, weight="bold"),
            text_color="white"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_box, 
            text="Visão geral da ocupação em tempo real", 
            font=ctk.CTkFont(size=14), 
            text_color=self.colors["text_gray"]
        ).pack(anchor="w")

        ctk.CTkButton(
            header, 
            text="+ NOVA MESA", 
            command=self.abrir_modal_nova, 
            width=160, height=45, corner_radius=8, 
            fg_color=self.colors["primary"], 
            font=ctk.CTkFont(weight="bold")
        ).pack(side="right")

    # -----------------------------------------------------------
    # 🔥 AQUI ESTÁ A MUDANÇA: DASHBOARD KPI BAR
    # -----------------------------------------------------------
    def create_metrics_bar(self):
        # Container horizontal
        self.metrics_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.metrics_frame.pack(fill="x", pady=(0, 30))
        
        # Configurar grid para que os cards se estiquem igualmente
        self.metrics_frame.grid_columnconfigure(0, weight=1)
        self.metrics_frame.grid_columnconfigure(1, weight=1)
        self.metrics_frame.grid_columnconfigure(2, weight=1)

        # Criar os 3 Cards de KPI (Key Performance Indicators)
        # Passamos ícones (emojis por enquanto, mas preparados para imagens)
        self.kpi_total = self._criar_kpi_card(0, "TOTAL DE MESAS", "🏢", self.colors["primary"])
        self.kpi_livres = self._criar_kpi_card(1, "DISPONÍVEIS", "✅", self.colors["table_free"])
        self.kpi_ocupadas = self._criar_kpi_card(2, "OCUPADAS", "🚫", self.colors["table_busy"])

    def _criar_kpi_card(self, col_index, titulo, icone, cor_destaque):
        # Card Base
        card = ctk.CTkFrame(
            self.metrics_frame, 
            height=100, 
            fg_color=self.colors["kpi_bg"], 
            corner_radius=10,
            border_width=0
        )
        card.grid(row=0, column=col_index, sticky="ew", padx=(0 if col_index == 0 else 15, 0))
        
        # Borda Colorida Lateral (Indicador Visual)
        barra_lateral = ctk.CTkFrame(
            card, 
            width=6, 
            fg_color=cor_destaque, 
            corner_radius=6 # Arredondar só um pouco
        )
        barra_lateral.pack(side="left", fill="y", padx=(0, 15)) # Cola na esquerda
        
        # Conteúdo de Texto
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(side="left", fill="both", expand=True, pady=15)
        
        # Título (Label pequeno)
        ctk.CTkLabel(
            content_frame, 
            text=titulo, 
            font=ctk.CTkFont(family="Roboto", size=12, weight="bold"), 
            text_color=self.colors["text_gray"]
        ).pack(anchor="w")
        
        # Valor (Label Grande - Será atualizado depois)
        lbl_valor = ctk.CTkLabel(
            content_frame, 
            text="0", 
            font=ctk.CTkFont(family="Roboto", size=32, weight="bold"), 
            text_color="white"
        )
        lbl_valor.pack(anchor="w")

        # Ícone Decorativo (Direita)
        icon_frame = ctk.CTkFrame(card, fg_color="transparent", width=50)
        icon_frame.pack(side="right", padx=20)
        
        ctk.CTkLabel(
            icon_frame, 
            text=icone, 
            font=ctk.CTkFont(size=30)
        ).pack()

        return lbl_valor

    def create_grid(self):
        self.grid_frame = ctk.CTkScrollableFrame(self, fg_color="transparent", label_text="")
        self.grid_frame.pack(fill="both", expand=True)

    def listar_mesas(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        mesas = self.session.query(Mesa).order_by(Mesa.numero).all()

        # Atualizar KPIs com dados reais
        total = len(mesas)
        ocupadas = len([m for m in mesas if m.status == "OCUPADA"])
        livres = total - ocupadas
        
        self.kpi_total.configure(text=str(total))
        self.kpi_livres.configure(text=str(livres))
        self.kpi_ocupadas.configure(text=str(ocupadas))

        if not mesas:
            self._mostrar_empty_state()
            return

        # Grid Responsivo
        col = 0
        row = 0
        columns_count = 5 

        for mesa in mesas:
            self.criar_card_mesa_visual(mesa, row, col)
            col += 1
            if col >= columns_count:
                col = 0
                row += 1
        
        for i in range(columns_count):
            self.grid_frame.grid_columnconfigure(i, weight=1)

    def criar_card_mesa_visual(self, mesa, row, col):
        is_free = mesa.status == "LIVRE"
        cor_mesa = self.colors["table_free"] if is_free else self.colors["table_busy"]
        
        # CARD CONTAINER
        card = ctk.CTkFrame(
            self.grid_frame, 
            width=200, height=220, 
            fg_color=self.colors["card_bg"],
            corner_radius=15
        )
        card.grid(row=row, column=col, padx=10, pady=10)
        card.grid_propagate(False)

        # Evento Hover
        def on_enter(e): card.configure(fg_color="#2A2A2A")
        def on_leave(e): card.configure(fg_color=self.colors["card_bg"])
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        card.bind("<Button-1>", lambda e: self.abrir_modal_editar(mesa))

        # --- VISUAL PLANTA BAIXA (GEOMÉTRICO) ---
        table_shape = ctk.CTkFrame(
            card, 
            width=100, height=100, 
            corner_radius=50, 
            fg_color=cor_mesa
        )
        table_shape.place(relx=0.5, rely=0.4, anchor="center")
        
        # Número da Mesa
        ctk.CTkLabel(
            table_shape, 
            text=f"{mesa.numero}", 
            font=ctk.CTkFont(family="Arial", size=36, weight="bold"),
            text_color="white"
        ).place(relx=0.5, rely=0.5, anchor="center")

        # --- DETALHES INFERIORES ---
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.place(relx=0.5, rely=0.8, anchor="center")

        status_row = ctk.CTkFrame(info_frame, fg_color="transparent")
        status_row.pack()
        
        status_dot = ctk.CTkFrame(status_row, width=8, height=8, corner_radius=4, fg_color=cor_mesa)
        status_dot.pack(side="left", padx=(0,5))
        
        ctk.CTkLabel(
            status_row, 
            text="Disponível" if is_free else "Ocupada",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=cor_mesa
        ).pack(side="left")

        ctk.CTkLabel(
            info_frame, 
            text=f"{mesa.capacidade} Lugares",
            font=ctk.CTkFont(size=11),
            text_color=self.colors["text_gray"]
        ).pack(pady=(2,0))
        
        # Propagar eventos
        for w in [table_shape, info_frame, status_row, status_dot] + list(table_shape.winfo_children()) + list(status_row.winfo_children()) + list(info_frame.winfo_children()):
             w.bind("<Button-1>", lambda e: self.abrir_modal_editar(mesa))
             w.bind("<Enter>", on_enter)
             w.bind("<Leave>", on_leave)

    def _mostrar_empty_state(self):
        box = ctk.CTkFrame(self.grid_frame, fg_color="transparent")
        box.pack(pady=80)
        ctk.CTkLabel(box, text="🏢", font=("Arial", 60)).pack()
        ctk.CTkLabel(box, text="O salão está vazio. Cadastre mesas.", text_color=self.colors["text_gray"]).pack()

    # --- MODALS (Mantendo consistência visual) ---
    def _center_modal(self, modal, width, height):
        modal.update_idletasks()
        x = self.master.winfo_x() + (self.master.winfo_width() // 2) - (width // 2)
        y = self.master.winfo_y() + (self.master.winfo_height() // 2) - (height // 2)
        modal.geometry(f"{width}x{height}+{x}+{y}")
        modal.configure(fg_color="#121212")

    def abrir_modal_nova(self):
        modal = ctk.CTkToplevel(self)
        modal.title("Nova Mesa")
        self._center_modal(modal, 350, 300)
        modal.transient(self)
        modal.grab_set()
        
        f = ctk.CTkFrame(modal, fg_color="transparent")
        f.pack(fill="both", expand=True, padx=25, pady=25)
        
        def entry_style(lbl):
            ctk.CTkLabel(f, text=lbl, font=ctk.CTkFont(weight="bold"), text_color="white").pack(anchor="w", pady=(10,5))
            e = ctk.CTkEntry(f, fg_color="#2B2B2B", border_width=0, text_color="white", height=40)
            e.pack(fill="x")
            return e

        n = entry_style("Número da Mesa")
        c = entry_style("Capacidade (Pessoas)")
        c.insert(0, "4")

        def save():
            try:
                num = int(n.get())
                cap = int(c.get())
                if self.session.query(Mesa).filter_by(numero=num).first():
                    messagebox.showerror("Erro", "Mesa já existe")
                    return
                self.session.add(Mesa(numero=num, capacidade=cap))
                self.session.commit()
                modal.destroy()
                self.listar_mesas()
            except: messagebox.showerror("Erro", "Inválido")
            
        ctk.CTkButton(f, text="CRIAR MESA", command=save, height=45, corner_radius=22, fg_color=self.colors["primary"], font=ctk.CTkFont(weight="bold")).pack(side="bottom", fill="x", pady=(20,0))

    def abrir_modal_editar(self, mesa):
        modal = ctk.CTkToplevel(self)
        modal.title(f"Mesa {mesa.numero}")
        self._center_modal(modal, 350, 400)
        modal.transient(self)
        modal.grab_set()
        
        f = ctk.CTkFrame(modal, fg_color="transparent")
        f.pack(fill="both", expand=True, padx=25, pady=25)
        
        ctk.CTkLabel(f, text="Capacidade", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        c = ctk.CTkEntry(f, fg_color="#2B2B2B", border_width=0, height=40)
        c.insert(0, str(mesa.capacidade))
        c.pack(fill="x", pady=(5, 15))

        ctk.CTkLabel(f, text="Status", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        s = ctk.CTkComboBox(f, values=["LIVRE", "OCUPADA"], fg_color="#2B2B2B", button_color=self.colors["primary"], height=40)
        s.set(mesa.status)
        s.pack(fill="x", pady=(5, 30))

        def save():
            mesa.capacidade = int(c.get())
            mesa.status = s.get()
            self.session.commit()
            modal.destroy()
            self.listar_mesas()
            
        def delete():
            if messagebox.askyesno("Excluir", "Remover mesa?"):
                self.session.delete(mesa)
                self.session.commit()
                modal.destroy()
                self.listar_mesas()

        ctk.CTkButton(f, text="SALVAR", command=save, height=45, corner_radius=22, fg_color=self.colors["primary"], font=ctk.CTkFont(weight="bold")).pack(fill="x", pady=(0,10))
        ctk.CTkButton(f, text="EXCLUIR", command=delete, height=45, corner_radius=22, fg_color="transparent", border_width=1, border_color="#C62828", text_color="#C62828", hover_color="#2e0a0a").pack(fill="x")