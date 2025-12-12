import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import os
from models import CardapioItem

class CardapioView(ctk.CTkFrame):
    def __init__(self, master, session):
        super().__init__(master)
        self.session = session
        
        self.colors = {
            "primary": "#EA1D2C",
            "primary_hover": "#C21522",
            "bg_dark": "#121212",
            "card_bg": "#1A1A1A",
            "card_hover": "#222222",
            "placeholder": "#262626",
            "price_text": "#50A773",
            "text_title": "#FFFFFF",
            "text_desc": "#A6A6A6",
            "tag_bg": "#2A2A2A",
            "input_bg": "#2B2B2B",
            "border": "#404040"
        }

        self.configure(fg_color="transparent")
        self.pack(fill="both", expand=True, padx=30, pady=30)
        
        self.create_widgets()
        self.listar_itens()
    
    def create_widgets(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 25))
        
        title_box = ctk.CTkFrame(header, fg_color="transparent")
        title_box.pack(side="left")
        
        ctk.CTkLabel(title_box, text="Cardápio Visual", font=ctk.CTkFont(family="Roboto", size=32, weight="bold"), text_color="white").pack(anchor="w")
        ctk.CTkLabel(title_box, text="Gerencie produtos com fotos reais", font=ctk.CTkFont(size=14), text_color=self.colors["text_desc"]).pack(anchor="w")
        
        ctk.CTkButton(
            header, text="+ Novo Produto", command=lambda: self.abrir_modal_novo(None),
            width=160, height=45, corner_radius=25,
            fg_color=self.colors["primary"], hover_color=self.colors["primary_hover"],
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="right")
        
        self.lista_frame = ctk.CTkScrollableFrame(self, fg_color="transparent", label_text="")
        self.lista_frame.pack(fill="both", expand=True)
    
    def listar_itens(self):
        for widget in self.lista_frame.winfo_children():
            widget.destroy()
        
        itens = self.session.query(CardapioItem).order_by(CardapioItem.nome).all()
        
        if not itens:
            self._mostrar_empty_state()
            return
        
        for item in itens:
            self.criar_card_delivery(item)
    
    def criar_card_delivery(self, item):
        card = ctk.CTkFrame(self.lista_frame, fg_color=self.colors["card_bg"], corner_radius=12, height=110)
        card.pack(fill="x", pady=8, padx=5)
        card.grid_columnconfigure(1, weight=1)
        
        # Imagem
        img_container = ctk.CTkFrame(card, width=90, height=90, corner_radius=12, fg_color=self.colors["placeholder"])
        img_container.grid(row=0, column=0, padx=(20, 15), pady=10)
        img_container.pack_propagate(False)
        
        tem_imagem = False
        if item.imagem_path and os.path.exists(item.imagem_path):
            try:
                pil_img = Image.open(item.imagem_path)
                ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(90, 90))
                ctk.CTkLabel(img_container, text="", image=ctk_img).place(relx=0.5, rely=0.5, anchor="center")
                tem_imagem = True
            except: pass 
        
        if not tem_imagem:
            icone = "🍔" if item.categoria and "Lanche" in item.categoria else "🍽️"
            ctk.CTkLabel(img_container, text=icone, font=("Arial", 36)).place(relx=0.5, rely=0.5, anchor="center")
        
        # Info
        info_box = ctk.CTkFrame(card, fg_color="transparent")
        info_box.grid(row=0, column=1, sticky="nsew", pady=12, padx=20)
        
        ctk.CTkLabel(info_box, text=item.nome, font=ctk.CTkFont(family="Roboto", size=18, weight="bold"), text_color="white", anchor="w").pack(fill="x")
        
        desc = (item.descricao[:70] + "...") if item.descricao and len(item.descricao) > 70 else (item.descricao or "Sem descrição.")
        ctk.CTkLabel(info_box, text=desc, font=ctk.CTkFont(size=13), text_color=self.colors["text_desc"], anchor="w").pack(fill="x", pady=(2, 5))
        
        if item.categoria:
            tag_frame = ctk.CTkFrame(info_box, fg_color="transparent")
            tag_frame.pack(anchor="w")
            tag = ctk.CTkFrame(tag_frame, fg_color=self.colors["tag_bg"], corner_radius=8, height=22)
            tag.pack(side="left")
            ctk.CTkLabel(tag, text=item.categoria, font=ctk.CTkFont(size=11), text_color=self.colors["text_desc"]).pack(padx=8, pady=2)

        # Ações
        action_box = ctk.CTkFrame(card, fg_color="transparent")
        action_box.grid(row=0, column=2, padx=20, sticky="e")
        
        ctk.CTkLabel(action_box, text=f"R$ {item.preco:.2f}", font=ctk.CTkFont(family="Roboto", size=18, weight="bold"), text_color=self.colors["price_text"]).pack(anchor="e", pady=(0, 5))
        
        ctk.CTkButton(
            action_box, text="Editar", width=80, height=25, fg_color="transparent", 
            border_width=1, border_color=self.colors["border"], text_color="white", font=ctk.CTkFont(size=12),
            hover_color=self.colors["card_hover"], command=lambda: self.abrir_modal_novo(item)
        ).pack(anchor="e", pady=(0, 5))

        ctk.CTkButton(
            action_box, text="Remover", width=80, height=25, fg_color="transparent", 
            hover_color=self.colors["card_hover"], text_color="#FF5555", font=ctk.CTkFont(size=12),
            command=lambda: self.excluir_item(item)
        ).pack(anchor="e")

        def hover(e, start=True): card.configure(fg_color=self.colors["card_hover"] if start else self.colors["card_bg"])
        card.bind("<Enter>", lambda e: hover(e, True))
        card.bind("<Leave>", lambda e: hover(e, False))

    def _mostrar_empty_state(self):
        box = ctk.CTkFrame(self.lista_frame, fg_color="transparent")
        box.pack(pady=80)
        ctk.CTkLabel(box, text="📸", font=("Arial", 60)).pack()
        ctk.CTkLabel(box, text="Comece adicionando itens com fotos!", text_color="white", font=ctk.CTkFont(size=16)).pack(pady=(10,0))

    def excluir_item(self, item):
        if messagebox.askyesno("Remover", f"Excluir '{item.nome}'?"):
            self.session.delete(item)
            self.session.commit()
            self.listar_itens()

    def abrir_modal_novo(self, item_para_editar=None):
        modal = ctk.CTkToplevel(self)
        titulo = "Editar Produto" if item_para_editar else "Adicionar Produto"
        modal.title(titulo)
        
        # Centralizar e configurar modal
        modal.update_idletasks()
        width, height = 450, 650
        x = self.master.winfo_x() + (self.master.winfo_width() // 2) - (width // 2)
        y = self.master.winfo_y() + (self.master.winfo_height() // 2) - (height // 2)
        modal.geometry(f"{width}x{height}+{x}+{y}")
        modal.configure(fg_color="#121212")
        modal.transient(self)
        modal.grab_set()
        
        f = ctk.CTkFrame(modal, fg_color="transparent")
        f.pack(fill="both", expand=True, padx=30, pady=30)
        
        ctk.CTkLabel(f, text=titulo, font=ctk.CTkFont(size=22, weight="bold"), text_color="white").pack(anchor="w", pady=(0, 20))
        
        self.caminho_imagem_temp = item_para_editar.imagem_path if item_para_editar else None
        
        # --- PREVIEW VISUAL DA IMAGEM ---
        lbl_img_title = ctk.CTkLabel(f, text="Foto do Produto", font=ctk.CTkFont(weight="bold", size=12), text_color="#DDDDDD")
        lbl_img_title.pack(anchor="w", pady=(0, 5))
        
        preview_container = ctk.CTkFrame(f, height=150, fg_color=self.colors["input_bg"], corner_radius=10)
        preview_container.pack(fill="x", pady=(0, 10))
        preview_container.pack_propagate(False) # Mantém altura fixa
        
        # Label para exibir a imagem ou o texto placeholder
        self.lbl_preview_img = ctk.CTkLabel(preview_container, text="Nenhuma imagem", text_color="#666")
        self.lbl_preview_img.place(relx=0.5, rely=0.5, anchor="center")

        def atualizar_preview(caminho):
            if caminho and os.path.exists(caminho):
                try:
                    pil = Image.open(caminho)
                    # Redimensiona para caber no preview (altura máx 140)
                    ratio = min(140 / pil.height, 400 / pil.width)
                    new_size = (int(pil.width * ratio), int(pil.height * ratio))
                    ctk_img = ctk.CTkImage(light_image=pil, dark_image=pil, size=new_size)
                    
                    self.lbl_preview_img.configure(image=ctk_img, text="")
                except:
                    self.lbl_preview_img.configure(image=None, text="Erro ao carregar")
            else:
                self.lbl_preview_img.configure(image=None, text="Sem imagem")

        # Carrega imagem inicial se existir
        if self.caminho_imagem_temp:
            atualizar_preview(self.caminho_imagem_temp)

        def selecionar_imagem():
            path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png *.jpg *.jpeg")])
            if path:
                self.caminho_imagem_temp = path
                atualizar_preview(path)

        ctk.CTkButton(
            f, text="📂 Escolher Arquivo...", command=selecionar_imagem,
            height=35, fg_color="#333333", hover_color="#444444", width=400
        ).pack(pady=(0, 15))

        # Inputs
        def create_input(lbl, val=""):
            ctk.CTkLabel(f, text=lbl, font=ctk.CTkFont(weight="bold", size=12), text_color="#DDDDDD").pack(anchor="w", pady=(5, 2))
            e = ctk.CTkEntry(f, height=40, fg_color=self.colors["input_bg"], border_width=0, text_color="white")
            if val: e.insert(0, val)
            e.pack(fill="x")
            return e

        nome_e = create_input("Nome", item_para_editar.nome if item_para_editar else "")
        desc_e = create_input("Descrição", item_para_editar.descricao if item_para_editar else "")
        cat_e = create_input("Categoria", item_para_editar.categoria if item_para_editar else "")
        
        ctk.CTkLabel(f, text="Preço (R$)", font=ctk.CTkFont(weight="bold", size=12), text_color="#DDDDDD").pack(anchor="w", pady=(10, 2))
        preco_e = ctk.CTkEntry(f, height=40, fg_color=self.colors["input_bg"], border_width=0, text_color=self.colors["price_text"], font=("Arial", 14, "bold"))
        if item_para_editar: preco_e.insert(0, str(item_para_editar.preco))
        preco_e.pack(fill="x")
        
        def salvar():
            try:
                p = float(preco_e.get().replace(",", "."))
                n = nome_e.get().strip()
                if not n or p <= 0: raise ValueError
                
                if item_para_editar:
                    item_para_editar.nome = n
                    item_para_editar.descricao = desc_e.get().strip()
                    item_para_editar.categoria = cat_e.get().strip()
                    item_para_editar.preco = p
                    item_para_editar.imagem_path = self.caminho_imagem_temp
                else:
                    item = CardapioItem(
                        nome=n, descricao=desc_e.get().strip(), categoria=cat_e.get().strip(),
                        preco=p, imagem_path=self.caminho_imagem_temp
                    )
                    self.session.add(item)
                
                self.session.commit()
                modal.destroy()
                self.listar_itens()
            except Exception as e:
                messagebox.showerror("Erro", f"Verifique os dados: {e}")
        
        btn_txt = "SALVAR ALTERAÇÕES" if item_para_editar else "CADASTRAR PRODUTO"
        ctk.CTkButton(
            f, text=btn_txt, command=salvar, height=50, corner_radius=25, 
            fg_color=self.colors["primary"], hover_color=self.colors["primary_hover"], 
            font=ctk.CTkFont(weight="bold", size=14)
        ).pack(side="bottom", fill="x", pady=(20, 0))