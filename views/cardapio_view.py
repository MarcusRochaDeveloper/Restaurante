import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import os
from models import CardapioItem

class CardapioView(ctk.CTkFrame):
    def __init__(self, master, session):
        super().__init__(master)
        self.session = session
        
        # Paleta de cores
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
            "input_bg": "#2B2B2B"
        }

        self.configure(fg_color="transparent")
        self.pack(fill="both", expand=True, padx=30, pady=30)
        
        self.create_widgets()
        self.listar_itens()
    
    def create_widgets(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 25))
        
        title_box = ctk.CTkFrame(header, fg_color="transparent")
        title_box.pack(side="left")
        
        ctk.CTkLabel(
            title_box, 
            text="Cardápio Visual", 
            font=ctk.CTkFont(family="Roboto", size=32, weight="bold"),
            text_color="white"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_box, 
            text="Gerencie produtos com fotos reais", 
            font=ctk.CTkFont(size=14), 
            text_color=self.colors["text_desc"]
        ).pack(anchor="w")
        
        ctk.CTkButton(
            header,
            text="+ Novo Produto",
            command=self.abrir_modal_novo,
            width=160, height=45, corner_radius=25,
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"],
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="right")
        
        # Área de listagem
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
        card = ctk.CTkFrame(
            self.lista_frame, 
            fg_color=self.colors["card_bg"],
            corner_radius=12,
            height=110
        )
        card.pack(fill="x", pady=8, padx=5)
        card.grid_columnconfigure(1, weight=1)
        
        # Imagem do produto
        img_container = ctk.CTkFrame(
            card, 
            width=90, height=90, 
            corner_radius=12,
            fg_color=self.colors["placeholder"]
        )
        img_container.grid(row=0, column=0, padx=(20, 15), pady=10)
        img_container.pack_propagate(False)
        
        # Tenta carregar a imagem, se existir e for válida
        tem_imagem = False
        if hasattr(item, 'imagem_path') and item.imagem_path and os.path.exists(item.imagem_path):
            try:
                pil_img = Image.open(item.imagem_path)
                ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(90, 90))
                lbl_img = ctk.CTkLabel(img_container, text="", image=ctk_img)
                lbl_img.place(relx=0.5, rely=0.5, anchor="center")
                tem_imagem = True
            except Exception:
                pass 
        
        # Fallback para ícone se não houver imagem
        if not tem_imagem:
            icone = "🍔" if item.categoria and "Lanche" in item.categoria else "🥤" if "Bebida" in str(item.categoria) else "🍽️"
            ctk.CTkLabel(img_container, text=icone, font=("Arial", 36)).place(relx=0.5, rely=0.5, anchor="center")
        
        # Informações do item
        info_box = ctk.CTkFrame(card, fg_color="transparent")
        info_box.grid(row=0, column=1, sticky="nsew", pady=12, padx=20)
        
        ctk.CTkLabel(
            info_box, 
            text=item.nome, 
            font=ctk.CTkFont(family="Roboto", size=18, weight="bold"),
            text_color="white", anchor="w"
        ).pack(fill="x")
        
        desc_text = item.descricao if item.descricao else "Sem descrição."
        if len(desc_text) > 70: desc_text = desc_text[:70] + "..."
        
        ctk.CTkLabel(
            info_box, 
            text=desc_text, 
            font=ctk.CTkFont(size=13),
            text_color=self.colors["text_desc"], anchor="w"
        ).pack(fill="x", pady=(2, 5))
        
        if item.categoria:
            tag_frame = ctk.CTkFrame(info_box, fg_color="transparent")
            tag_frame.pack(anchor="w")
            tag = ctk.CTkFrame(tag_frame, fg_color=self.colors["tag_bg"], corner_radius=8, height=22)
            tag.pack(side="left")
            ctk.CTkLabel(tag, text=item.categoria, font=ctk.CTkFont(size=11), text_color=self.colors["text_desc"]).pack(padx=8, pady=2)

        # Preço e Ações
        action_box = ctk.CTkFrame(card, fg_color="transparent")
        action_box.grid(row=0, column=2, padx=20, sticky="e")
        
        ctk.CTkLabel(
            action_box, 
            text=f"R$ {item.preco:.2f}", 
            font=ctk.CTkFont(family="Roboto", size=18, weight="bold"),
            text_color=self.colors["price_text"]
        ).pack(anchor="e")
        
        btn_delete = ctk.CTkButton(
            action_box, text="Remover", width=80, height=25,
            fg_color="transparent", hover_color=self.colors["card_hover"],
            text_color="#FF5555", font=ctk.CTkFont(size=12),
            command=lambda: self.excluir_item(item)
        )
        btn_delete.pack(anchor="e", pady=(5, 0))

        # Efeitos de hover
        def on_enter(e): card.configure(fg_color=self.colors["card_hover"])
        def on_leave(e): card.configure(fg_color=self.colors["card_bg"])
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

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

    # --- Modal de Cadastro ---
    def _center_modal(self, modal, width, height):
        modal.update_idletasks()
        x = self.master.winfo_x() + (self.master.winfo_width() // 2) - (width // 2)
        y = self.master.winfo_y() + (self.master.winfo_height() // 2) - (height // 2)
        modal.geometry(f"{width}x{height}+{x}+{y}")
        modal.configure(fg_color="#121212")

    def abrir_modal_novo(self):
        modal = ctk.CTkToplevel(self)
        modal.title("Adicionar Produto")
        self._center_modal(modal, 450, 600)
        modal.transient(self)
        modal.grab_set()
        
        f = ctk.CTkFrame(modal, fg_color="transparent")
        f.pack(fill="both", expand=True, padx=30, pady=30)
        
        ctk.CTkLabel(f, text="Novo Produto", font=ctk.CTkFont(size=22, weight="bold"), text_color="white").pack(anchor="w", pady=(0, 20))
        
        self.caminho_imagem_temp = None
        
        # Upload de imagem
        lbl_img = ctk.CTkLabel(f, text="Imagem do Produto", font=ctk.CTkFont(weight="bold", size=12), text_color="#DDDDDD")
        lbl_img.pack(anchor="w", pady=(0, 5))
        
        preview_frame = ctk.CTkFrame(f, height=100, fg_color=self.colors["input_bg"], corner_radius=8)
        preview_frame.pack(fill="x", pady=(0, 15))
        preview_frame.pack_propagate(False) 
        
        self.lbl_preview = ctk.CTkLabel(preview_frame, text="Nenhuma imagem selecionada", text_color="#777")
        self.lbl_preview.place(relx=0.5, rely=0.5, anchor="center")

        def selecionar_imagem():
            file_path = filedialog.askopenfilename(
                title="Selecione uma imagem",
                filetypes=[("Imagens", "*.png *.jpg *.jpeg")]
            )
            if file_path:
                self.caminho_imagem_temp = file_path
                nome_arquivo = os.path.basename(file_path)
                self.lbl_preview.configure(text=f"📷 {nome_arquivo}", text_color=self.colors["price_text"])

        btn_upload = ctk.CTkButton(
            f, text="📂 Escolher Arquivo...", command=selecionar_imagem,
            height=35, fg_color="#333333", hover_color="#444444", 
            width=400
        )
        btn_upload.pack(pady=(0, 15))

        # Campos de texto
        def input_field(label):
            ctk.CTkLabel(f, text=label, font=ctk.CTkFont(weight="bold", size=12), text_color="#DDDDDD").pack(anchor="w", pady=(5, 5))
            e = ctk.CTkEntry(f, height=40, fg_color=self.colors["input_bg"], border_width=0, text_color="white")
            e.pack(fill="x")
            return e

        nome_e = input_field("Nome")
        desc_e = input_field("Descrição")
        cat_e = input_field("Categoria")
        
        ctk.CTkLabel(f, text="Preço (R$)", font=ctk.CTkFont(weight="bold", size=12), text_color="#DDDDDD").pack(anchor="w", pady=(10, 5))
        preco_e = ctk.CTkEntry(f, height=40, fg_color=self.colors["input_bg"], border_width=0, text_color=self.colors["price_text"], font=("Arial", 14, "bold"))
        preco_e.pack(fill="x")
        
        def salvar():
            try:
                p = float(preco_e.get().replace(",", "."))
                n = nome_e.get().strip()
                if not n or p <= 0: raise ValueError
                
                item = CardapioItem(
                    nome=n, 
                    descricao=desc_e.get().strip(), 
                    categoria=cat_e.get().strip(), 
                    preco=p,
                    imagem_path=self.caminho_imagem_temp
                )
                self.session.add(item)
                self.session.commit()
                modal.destroy()
                self.listar_itens()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar: {e}")
        
        ctk.CTkButton(
            f, text="SALVAR PRODUTO", command=salvar, 
            height=50, corner_radius=25, 
            fg_color=self.colors["primary"], hover_color=self.colors["primary_hover"],
            font=ctk.CTkFont(weight="bold", size=14)
        ).pack(side="bottom", fill="x", pady=(20, 0))