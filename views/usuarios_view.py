import customtkinter as ctk
from tkinter import messagebox
from models import Usuario
from utils.security import security_manager

class UsuariosView(ctk.CTkFrame):
    def __init__(self, master, session):
        super().__init__(master)
        self.session = session
        
        # --- PALETA DE CORES (Consistência) ---
        self.colors = {
            "primary": "#0055D4",
            "primary_hover": "#0044AA",
            "bg_dark": "#121212",      # Fundo da view
            "card_bg": "#1E1E1E",      # Fundo do cartão
            "input_bg": "#2B2B2B",
            "text_light": "#FFFFFF",
            "text_gray": "#A0A0A0",
            "danger": "#D32F2F"        # Cor para ações perigosas 
        }

        # Configura o fundo do frame principal
        self.configure(fg_color="transparent")
        
        # Layout principal preenchendo o espaço
        self.pack(fill="both", expand=True, padx=30, pady=30)
        
        self.create_widgets()
        self.listar_usuarios()
    
    def create_widgets(self):
        # ================= HEADER =================
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Título e Subtítulo
        title_box = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_box.pack(side="left")
        
        ctk.CTkLabel(
            title_box, 
            text="👥 Gestão de Equipe", 
            font=ctk.CTkFont(family="Roboto", size=24, weight="bold"),
            text_color="white"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_box, 
            text="Gerencie o acesso e as credenciais dos funcionários", 
            font=ctk.CTkFont(family="Roboto", size=14),
            text_color=self.colors["text_gray"]
        ).pack(anchor="w")
        
        # Botão de Adicionar (Estilo 'Primary')
        self.btn_add = ctk.CTkButton(
            header_frame,
            text="+ NOVO FUNCIONÁRIO",
            command=self.abrir_modal_novo,
            width=200,
            height=40,
            corner_radius=20,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"]
        )
        self.btn_add.pack(side="right", anchor="e") # Alinhado à direita
        
        # ================= LISTA (SCROLL) =================
        # Frame rolável com fundo transparente para fundir com o app
        self.lista_frame = ctk.CTkScrollableFrame(
            self, 
            fg_color="transparent", 
            label_text="" 
        )
        self.lista_frame.pack(fill="both", expand=True)
    
    def listar_usuarios(self):
        # Limpa lista atual
        for widget in self.lista_frame.winfo_children():
            widget.destroy()
        
        usuarios = self.session.query(Usuario).all()
        
        if not usuarios:
            # Estado vazio (Empty State) bonito
            empty_frame = ctk.CTkFrame(self.lista_frame, fg_color="transparent")
            empty_frame.pack(pady=50)
            ctk.CTkLabel(empty_frame, text="📭", font=("Arial", 48)).pack()
            ctk.CTkLabel(
                empty_frame, 
                text="Nenhum funcionário encontrado.", 
                text_color=self.colors["text_gray"]
            ).pack()
            return
        
        for usuario in usuarios:
            self.criar_card_usuario(usuario)
    
    def criar_card_usuario(self, usuario):
        # --- CARD DO USUÁRIO ---
        card = ctk.CTkFrame(
            self.lista_frame, 
            fg_color=self.colors["card_bg"], 
            corner_radius=15,
            border_width=1,
            border_color="#2A2A2A" # Borda sutil
        )
        card.pack(fill="x", pady=8, padx=5) # Espaçamento entre cards
        
       
        card.grid_columnconfigure(1, weight=1) # Coluna do nome expande
        
        # 1. Ícone/Avatar (Lado Esquerdo)
        avatar_frame = ctk.CTkFrame(card, width=50, height=50, corner_radius=25, fg_color=self.colors["primary"])
        avatar_frame.grid(row=0, column=0, padx=20, pady=20)
        ctk.CTkLabel(avatar_frame, text="👤", font=("Arial", 24)).place(relx=0.5, rely=0.5, anchor="center")
        
        # 2. Informações (Centro)
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.grid(row=0, column=1, sticky="w", padx=10)
        
        ctk.CTkLabel(
            info_frame, 
            text=usuario.nome, 
            font=ctk.CTkFont(family="Roboto", size=16, weight="bold"),
            text_color="white"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            info_frame, 
            text=usuario.email, 
            font=ctk.CTkFont(family="Roboto", size=13),
            text_color=self.colors["text_gray"]
        ).pack(anchor="w")
        
        
        # Se for admin hardcoded, mostra badge diferente
        cargo_text = "Administrador" if "admin" in usuario.email else "Funcionário"
        cargo_color = "#FF9800" if "admin" in usuario.email else "#4CAF50" # Laranja ou Verde
        
        badge = ctk.CTkLabel(
            card,
            text=cargo_text.upper(),
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=cargo_color,
            fg_color="transparent"
        )
        badge.grid(row=0, column=2, padx=20)

        # 4. Ações (Lado Direito)
        btn_ver_senha = ctk.CTkButton(
            card,
            text="Ver Senha",
            image=None, # Poderia adicionar ícone de olho aqui
            command=lambda: self.mostrar_senha(usuario),
            width=100,
            height=30,
            fg_color="transparent",
            border_width=1,
            border_color=self.colors["text_gray"],
            text_color=self.colors["text_light"],
            hover_color=self.colors["input_bg"]
        )
        btn_ver_senha.grid(row=0, column=3, padx=(0, 20))
    
    def mostrar_senha(self, usuario):
        try:
            senha = security_manager.desencriptar(usuario.senha_encriptada)
            messagebox.showinfo("Credenciais", f"Usuário: {usuario.nome}\nSenha: {senha}")
        except:
            messagebox.showerror("Erro", "Não foi possível descriptografar a senha (chave inválida ou antiga).")
    
    def abrir_modal_novo(self):
        # --- MODAL ESTILIZADO ---
        modal = ctk.CTkToplevel(self)
        modal.title("Novo Cadastro")
        modal.geometry("450x450")
        modal.configure(fg_color=self.colors["bg_dark"]) # Fundo escuro igual ao app
        modal.transient(self)
        
        # Centralizar Modal 
        modal.update_idletasks()
        x = self.master.winfo_x() + (self.master.winfo_width() // 2) - 225
        y = self.master.winfo_y() + (self.master.winfo_height() // 2) - 225
        modal.geometry(f"+{x}+{y}")
        
        modal.grab_set()
        modal.focus()
        
        # Conteúdo do Modal
        container = ctk.CTkFrame(modal, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Título Modal
        ctk.CTkLabel(
            container, 
            text="Novo Colaborador", 
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(0, 20), anchor="w")
        
        # --- INPUTS REUTILIZÁVEIS ---
        def criar_input(parent, label, is_pass=False):
            ctk.CTkLabel(parent, text=label, text_color=self.colors["text_gray"], font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(10, 5))
            entry = ctk.CTkEntry(
                parent, 
                height=40, 
                corner_radius=8, 
                fg_color=self.colors["input_bg"], 
                border_width=0,
                text_color="white",
                show="*" if is_pass else ""
            )
            entry.pack(fill="x")
            return entry

        nome_entry = criar_input(container, "NOME COMPLETO")
        email_entry = criar_input(container, "EMAIL CORPORATIVO")
        senha_entry = criar_input(container, "SENHA TEMPORÁRIA", is_pass=True)
        
        # Função Salvar Interna
        def salvar():
            nome = nome_entry.get().strip()
            email = email_entry.get().strip()
            senha = senha_entry.get()
            
            if not nome or not email or not senha:
                messagebox.showwarning("Atenção", "Todos os campos são obrigatórios.")
                return
            
            if self.session.query(Usuario).filter_by(email=email).first():
                messagebox.showerror("Duplicidade", "Este email já está cadastrado no sistema.")
                return
            
            try:
                hash_senha = security_manager.hash_senha(senha)
                senha_enc = security_manager.encriptar(senha)
                
                usuario = Usuario(
                    nome=nome,
                    email=email,
                    senha_hash=hash_senha,
                    senha_encriptada=senha_enc
                )
                self.session.add(usuario)
                self.session.commit()
                
                messagebox.showinfo("Sucesso", "Funcionário cadastrado com sucesso!")
                modal.destroy()
                self.listar_usuarios() # Atualiza a lista atrás
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar: {e}")
        
        # Botão Salvar Modal
        ctk.CTkButton(
            container,
            text="CADASTRAR",
            command=salvar,
            width=350,
            height=45,
            corner_radius=22,
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"],
            font=ctk.CTkFont(weight="bold")
        ).pack(pady=(40, 0))