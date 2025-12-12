import customtkinter as ctk
from tkinter import messagebox
from models import Pedido, Mesa, PedidoItem, CardapioItem
from sqlalchemy.orm import joinedload

class PedidosView(ctk.CTkFrame):
    def __init__(self, master, session, usuario):
        super().__init__(master)
        self.session = session
        self.usuario = usuario
        
        # --- PALETA DE CORES (Consistência Global) ---
        self.colors = {
            "primary": "#0055D4",
            "primary_hover": "#0044AA",
            "danger": "#C62828",       # Vermelho para fechar conta
            "danger_hover": "#B71C1C",
            "success": "#2E7D32",
            "bg_dark": "#121212",
            "card_bg": "#1E1E1E",      # Fundo do Card
            "input_bg": "#2B2B2B",
            "text_light": "#FFFFFF",
            "text_gray": "#A0A0A0",
            "border": "#333333"
        }

        self.configure(fg_color="transparent")
        self.pack(fill="both", expand=True, padx=30, pady=30)
        
        self.create_widgets()
        self.listar_pedidos()
    
    def create_widgets(self):
        # ================= HEADER =================
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Título
        title_box = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_box.pack(side="left")
        
        ctk.CTkLabel(
            title_box, 
            text="🍽️ Pedidos em Aberto", 
            font=ctk.CTkFont(family="Roboto", size=24, weight="bold"),
            text_color="white"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_box, 
            text="Gerencie as mesas e itens de consumo em tempo real", 
            font=ctk.CTkFont(family="Roboto", size=14),
            text_color=self.colors["text_gray"]
        ).pack(anchor="w")
        
        # Botão Novo Pedido
        ctk.CTkButton(
            header_frame,
            text="+ ABRIR MESA",
            command=self.abrir_modal_novo_pedido,
            width=180,
            height=40,
            corner_radius=20,
            font=ctk.CTkFont(weight="bold"),
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"]
        ).pack(side="right")
        
        # ================= LISTA SCROLLÁVEL =================
        self.lista_frame = ctk.CTkScrollableFrame(
            self, 
            fg_color="transparent",
            label_text="" 
        )
        self.lista_frame.pack(fill="both", expand=True)
    
    def listar_pedidos(self):
        # Limpa widgets anteriores
        for widget in self.lista_frame.winfo_children():
            widget.destroy()
        
        # Query Otimizada
        pedidos = self.session.query(Pedido).options(
            joinedload(Pedido.mesa),
            joinedload(Pedido.usuario),
            joinedload(Pedido.itens).joinedload(PedidoItem.item)
        ).filter_by(status="ABERTO").all()
        
        if not pedidos:
            # Empty State
            empty_frame = ctk.CTkFrame(self.lista_frame, fg_color="transparent")
            empty_frame.pack(pady=60)
            ctk.CTkLabel(empty_frame, text="✅", font=("Arial", 48)).pack(pady=10)
            ctk.CTkLabel(
                empty_frame, 
                text="Todas as mesas estão livres!", 
                font=ctk.CTkFont(size=16),
                text_color=self.colors["text_gray"]
            ).pack()
            return
        
        # Grid System para os Cards (2 colunas se houver espaço, ou empilhado)
        # Por simplicidade no Tkinter, vamos empilhar com boa margem, 
        # mas daria para fazer um grid complexo.
        for pedido in pedidos:
            self.criar_card_pedido(pedido)
    
    def criar_card_pedido(self, pedido):
        # --- CARD PRINCIPAL ---
        card = ctk.CTkFrame(
            self.lista_frame, 
            fg_color=self.colors["card_bg"],
            corner_radius=15,
            border_width=1,
            border_color=self.colors["border"]
        )
        card.pack(fill="x", pady=10, padx=5)
        
        # Layout interno: Coluna Esquerda (Info Mesa) | Coluna Direita (Itens e Ações)
        card.grid_columnconfigure(1, weight=1)
        
        # --- COLUNA 1: DESTAQUE DA MESA ---
        left_panel = ctk.CTkFrame(card, fg_color="transparent", width=150)
        left_panel.grid(row=0, column=0, sticky="ns", padx=20, pady=20)
        
        # Número da Mesa (Bem Grande)
        ctk.CTkLabel(
            left_panel,
            text=f"MESA",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.colors["text_gray"]
        ).pack()
        
        ctk.CTkLabel(
            left_panel,
            text=f"{pedido.mesa.numero:02d}", # Ex: 05
            font=ctk.CTkFont(family="Roboto", size=48, weight="bold"),
            text_color=self.colors["primary"]
        ).pack()
        
        # Info Atendente
        ctk.CTkLabel(
            left_panel,
            text=f"👤 {pedido.usuario.nome.split()[0]}", # Apenas primeiro nome
            font=ctk.CTkFont(size=12),
            text_color="white"
        ).pack(pady=(10, 0))
        
        ctk.CTkLabel(
            left_panel,
            text=f"Pedido #{pedido.id}",
            font=ctk.CTkFont(size=11),
            text_color=self.colors["text_gray"]
        ).pack()

        # Separador Vertical visual
        separator = ctk.CTkFrame(card, width=2, fg_color=self.colors["input_bg"])
        separator.grid(row=0, column=0, sticky="nse", padx=(148, 0), pady=15) # Gambiarra visual de layout

        # --- COLUNA 2: ITENS E AÇÕES ---
        right_panel = ctk.CTkFrame(card, fg_color="transparent")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=20, pady=15)
        
        # Lista de Itens
        itens_container = ctk.CTkFrame(right_panel, fg_color="transparent")
        itens_container.pack(fill="both", expand=True)
        
        total_conta = 0
        
        if not pedido.itens:
            ctk.CTkLabel(
                itens_container, 
                text="Nenhum item lançado.", 
                text_color=self.colors["text_gray"],
                font=ctk.CTkFont(slant="italic")
            ).pack(anchor="w", pady=10)
        else:
            for item in pedido.itens:
                subtotal = item.quantidade * item.preco_unitario
                total_conta += subtotal
                
                # Linha do Item
                item_row = ctk.CTkFrame(itens_container, fg_color="transparent", height=25)
                item_row.pack(fill="x", pady=2)
                
                # Qtd e Nome
                ctk.CTkLabel(
                    item_row, 
                    text=f"{item.quantidade}x  {item.item.nome}", 
                    font=ctk.CTkFont(size=13),
                    text_color="white"
                ).pack(side="left")
                
                # Preço
                ctk.CTkLabel(
                    item_row, 
                    text=f"R$ {subtotal:.2f}", 
                    font=ctk.CTkFont(size=13, weight="bold"),
                    text_color="white"
                ).pack(side="right")
        
        # Linha Divisória
        ctk.CTkFrame(right_panel, height=2, fg_color=self.colors["border"]).pack(fill="x", pady=10)
        
        # Footer: Total e Botões
        footer = ctk.CTkFrame(right_panel, fg_color="transparent")
        footer.pack(fill="x")
        
        # Total Grande
        total_frame = ctk.CTkFrame(footer, fg_color="transparent")
        total_frame.pack(side="left")
        ctk.CTkLabel(total_frame, text="TOTAL", font=ctk.CTkFont(size=11, weight="bold"), text_color=self.colors["text_gray"]).pack(anchor="w")
        ctk.CTkLabel(total_frame, text=f"R$ {total_conta:.2f}", font=ctk.CTkFont(size=20, weight="bold"), text_color=self.colors["success"]).pack(anchor="w")
        
        # Botões de Ação
        btn_box = ctk.CTkFrame(footer, fg_color="transparent")
        btn_box.pack(side="right")
        
        ctk.CTkButton(
            btn_box,
            text="+ ITEM",
            command=lambda: self.adicionar_item(pedido),
            width=100,
            height=35,
            fg_color=self.colors["input_bg"],
            hover_color="#3A3A3A",
            text_color="white"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_box,
            text="FECHAR CONTA",
            command=lambda: self.fechar_pedido(pedido),
            width=120,
            height=35,
            fg_color=self.colors["danger"], # Vermelho
            hover_color=self.colors["danger_hover"]
        ).pack(side="left", padx=5)
    
    # -----------------------------------------------------------
    # AUXILIAR: CENTRALIZAR MODAL
    # -----------------------------------------------------------
    def _center_modal(self, modal, width=400, height=300):
        modal.update_idletasks()
        x = self.master.winfo_x() + (self.master.winfo_width() // 2) - (width // 2)
        y = self.master.winfo_y() + (self.master.winfo_height() // 2) - (height // 2)
        modal.geometry(f"{width}x{height}+{x}+{y}")
        modal.configure(fg_color=self.colors["bg_dark"])

    # -----------------------------------------------------------
    # MODAL NOVO PEDIDO
    # -----------------------------------------------------------
    def abrir_modal_novo_pedido(self):
        mesas_livres = self.session.query(Mesa).filter_by(status="LIVRE").all()
        
        if not mesas_livres:
            messagebox.showwarning("Casa Cheia", "Não há mesas livres no momento!")
            return
        
        modal = ctk.CTkToplevel(self)
        modal.title("Abrir Nova Mesa")
        self._center_modal(modal, 350, 250)
        modal.transient(self)
        modal.grab_set()
        
        frame = ctk.CTkFrame(modal, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=25, pady=25)
        
        ctk.CTkLabel(frame, text="Selecione a Mesa", font=ctk.CTkFont(weight="bold"), text_color="white").pack(anchor="w", pady=(0, 5))
        
        mesa_var = ctk.StringVar(value=f"Mesa {mesas_livres[0].numero}")
        mesa_menu = ctk.CTkOptionMenu(
            frame,
            values=[f"Mesa {m.numero}" for m in mesas_livres],
            variable=mesa_var,
            width=300,
            height=40,
            fg_color=self.colors["input_bg"],
            button_color=self.colors["primary"],
            button_hover_color=self.colors["primary_hover"],
            text_color="white"
        )
        mesa_menu.pack(pady=(0, 20))
        
        def criar():
            numero = int(mesa_var.get().split()[-1])
            mesa = self.session.query(Mesa).filter_by(numero=numero).first()
            
            pedido = Pedido(mesa_id=mesa.id, usuario_id=self.usuario.id)
            mesa.status = "OCUPADA"
            self.session.add(pedido)
            self.session.commit()
            
            modal.destroy()
            self.listar_pedidos()
            # Opcional: Toast notification aqui
        
        ctk.CTkButton(
            frame, 
            text="ABRIR PEDIDO", 
            command=criar, 
            width=300, 
            height=45,
            corner_radius=22,
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"],
            font=ctk.CTkFont(weight="bold")
        ).pack(side="bottom")

    # -----------------------------------------------------------
    # MODAL ADICIONAR ITEM
    # -----------------------------------------------------------
    def adicionar_item(self, pedido):
        itens = self.session.query(CardapioItem).all()
        if not itens:
            messagebox.showwarning("Erro", "Cardápio vazio.")
            return
        
        modal = ctk.CTkToplevel(self)
        modal.title(f"Adicionar à Mesa {pedido.mesa.numero}")
        self._center_modal(modal, 400, 350)
        modal.transient(self)
        modal.grab_set()
        
        frame = ctk.CTkFrame(modal, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Select Item
        ctk.CTkLabel(frame, text="Item do Cardápio", font=ctk.CTkFont(size=12, weight="bold"), text_color=self.colors["text_gray"]).pack(anchor="w", pady=(0,5))
        item_var = ctk.StringVar(value=f"{itens[0].nome} - R$ {itens[0].preco:.2f}")
        item_menu = ctk.CTkOptionMenu(
            frame,
            values=[f"{i.nome} - R$ {i.preco:.2f}" for i in itens],
            variable=item_var,
            width=350,
            height=40,
            fg_color=self.colors["input_bg"],
            button_color=self.colors["primary"],
            text_color="white"
        )
        item_menu.pack(pady=(0, 15))
        
        # Input Quantidade
        ctk.CTkLabel(frame, text="Quantidade", font=ctk.CTkFont(size=12, weight="bold"), text_color=self.colors["text_gray"]).pack(anchor="w", pady=(0,5))
        qtd_entry = ctk.CTkEntry(
            frame, 
            width=350, 
            height=40,
            fg_color=self.colors["input_bg"],
            border_width=0,
            text_color="white",
            justify="center"
        )
        qtd_entry.insert(0, "1")
        qtd_entry.pack(pady=(0, 20))
        
        def adicionar():
            try:
                qtd = int(qtd_entry.get())
                if qtd <= 0: raise ValueError
                
                # Extrair nome do item (lógica simples baseada na string do menu)
                item_nome = item_var.get().split(" - R$")[0]
                item = self.session.query(CardapioItem).filter_by(nome=item_nome).first()
                
                pedido_item = PedidoItem(
                    pedido_id=pedido.id,
                    cardapio_id=item.id,
                    quantidade=qtd,
                    preco_unitario=item.preco,
                    subtotal=item.preco * qtd
                )
                self.session.add(pedido_item)
                self.session.commit()
                
                modal.destroy()
                self.listar_pedidos()
            except ValueError:
                messagebox.showerror("Erro", "Quantidade inválida.")
        
        ctk.CTkButton(
            frame, 
            text="ADICIONAR ITEM", 
            command=adicionar, 
            width=350, 
            height=45,
            corner_radius=22,
            fg_color=self.colors["primary"],
            font=ctk.CTkFont(weight="bold")
        ).pack(side="bottom")

    # -----------------------------------------------------------
    # FECHAR PEDIDO
    # -----------------------------------------------------------
    def fechar_pedido(self, pedido):
        # Confirmação customizada poderia ser feita, mas usaremos a padrão do sistema por enquanto
        if not messagebox.askyesno("Confirmar Fechamento", f"Deseja fechar a conta da Mesa {pedido.mesa.numero}?"):
            return
            
        total = sum(item.subtotal for item in pedido.itens)
        
        pedido.status = "FECHADO"
        pedido.mesa.status = "LIVRE"
        pedido.total = total
        self.session.commit()
        
        messagebox.showinfo("Conta Fechada", f"Pedido encerrado com sucesso!\nTotal Recebido: R$ {total:.2f}")
        self.listar_pedidos()