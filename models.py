from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    senha_encriptada = Column(String(255), nullable=False)
    criado_em = Column(DateTime, default=datetime.now)

    pedidos = relationship("Pedido", back_populates="usuario")


class Mesa(Base):
    __tablename__ = "mesas"

    id = Column(Integer, primary_key=True)
    numero = Column(Integer, unique=True, nullable=False)
    capacidade = Column(Integer, default=4)
    status = Column(Enum("LIVRE", "OCUPADA", name="status_mesa"), default="LIVRE")

    pedidos = relationship("Pedido", back_populates="mesa")


class CardapioItem(Base):
    __tablename__ = "cardapio"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(255))
    preco = Column(Float, nullable=False)
    categoria = Column(String(50))
    
    # --- NOVA COLUNA PARA A IMAGEM ---
    imagem_path = Column(String(500), nullable=True)
    # ---------------------------------

    itens = relationship("PedidoItem", back_populates="item")


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True)
    mesa_id = Column(Integer, ForeignKey("mesas.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    status = Column(Enum("ABERTO", "FECHADO", name="status_pedido"), default="ABERTO")
    criado_em = Column(DateTime, default=datetime.now)
    total = Column(Float, default=0.0)

    mesa = relationship("Mesa", back_populates="pedidos")
    usuario = relationship("Usuario", back_populates="pedidos")
    itens = relationship("PedidoItem", back_populates="pedido", cascade="all, delete-orphan")


class PedidoItem(Base):
    __tablename__ = "pedido_itens"

    id = Column(Integer, primary_key=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    cardapio_id = Column(Integer, ForeignKey("cardapio.id"))
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

    pedido = relationship("Pedido", back_populates="itens")
    item = relationship("CardapioItem", back_populates="itens")