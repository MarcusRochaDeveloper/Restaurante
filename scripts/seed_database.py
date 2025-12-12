import sys
import os

# --- CORREÇÃO DE CAMINHO ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)
# ---------------------------

from database import db
# Importamos Base do models, pois é lá que ele foi definido
from models import Usuario, Mesa, CardapioItem, Base
from utils.security import security_manager

def seed():
    print(f"Iniciando seed no banco de dados...")
    
    # --- CONEXÃO ---
    try:
        # Host, Porta, Usuário, SENHA, Banco
        db.conectar('localhost', '3306', 'root', '123456', 'restaurante_db')
        session = db.get_session()
        print("✓ Conectado ao MySQL")
    except Exception as e:
        print(f"Erro ao conectar: {e}")
        return

    # --- 1. CRIAR TABELAS (CORRIGIDO) ---
    # Usamos db.engine aqui, pois o engine foi criado na linha db.conectar acima
    print("Verificando tabelas...")
    Base.metadata.create_all(db.engine)

    # --- 2. Criar Usuário Admin ---
    if not session.query(Usuario).filter_by(email='admin@restaurante.com').first():
        hash_senha = security_manager.hash_senha('admin123')
        senha_enc = security_manager.encriptar('admin123')
        
        admin = Usuario(
            nome='Administrador',
            email='admin@restaurante.com',
            senha_hash=hash_senha,
            senha_encriptada=senha_enc
        )
        session.add(admin)
        print("✓ Usuário admin criado")
    else:
        print("✓ Admin já existia")
    
    # --- 3. Criar Mesas ---
    if session.query(Mesa).count() == 0:
        for i in range(1, 13): 
            cap = 4 if i % 2 != 0 else 6 
            mesa = Mesa(numero=i, capacidade=cap)
            session.add(mesa)
        print(f"✓ 12 mesas criadas")
    else:
        print("✓ Mesas já existiam")
    
    # --- 4. Criar Cardápio ---
    if session.query(CardapioItem).count() == 0:
        itens = [
            ("Pizza Margherita", "Molho de tomate, mussarela e manjericão fresco.", "Pizza", 45.90),
            ("Pizza Calabresa", "Molho especial, mussarela, calabresa e cebola roxa.", "Pizza", 48.90),
            ("Hambúrguer Clássico", "Pão brioche, carne 180g, queijo cheddar e salada.", "Lanche", 28.90),
            ("X-Bacon Artesanal", "Pão australiano, carne, bacon crocante e molho barbecue.", "Lanche", 32.90),
            ("Refrigerante Lata", "Coca-Cola, Guaraná ou Fanta (350ml).", "Bebida", 6.00),
            ("Suco Natural", "Laranja, limão ou maracujá (500ml).", "Bebida", 8.50),
            ("Batata Frita Rústica", "Porção grande com alho e alecrim.", "Acompanhamento", 18.90),
            ("Salada Caesar", "Alface americana, croutons, parmesão e molho caesar.", "Prato", 22.90),
            ("Petit Gâteau", "Bolo de chocolate com sorvete de creme.", "Sobremesa", 19.90),
        ]
        
        for nome, desc, cat, preco in itens:
            item = CardapioItem(nome=nome, descricao=desc, categoria=cat, preco=preco)
            session.add(item)
        print("✓ Itens do cardápio criados")
    else:
        print("✓ Cardápio já existia")
    
    session.commit()
    print("\n✅ Banco de dados populado com sucesso!")
    print("-" * 30)
    print("LOGIN: admin@restaurante.com")
    print("SENHA: admin123")
    print("-" * 30)

if __name__ == "__main__":
    seed()