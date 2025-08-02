''' o create_engine é usado para criar uma conexão com o banco de dados
    Column é usado para definir as colunas da tabela
    Integer, String, Boolean e Float são tipos de dados para as colunas
'''
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, ForeignKey,Enum

#Criando a base do nosso banco de dados
from sqlalchemy.orm import declarative_base, relationship

# Importando o ChoiceTypes para usar tipos de dados personalizados, se necessário
import enum

# Criando a conexão com o banco de dados SQLite onde ele será salvo no meu diretório atual
db = create_engine("sqlite:///banco.db")

# Armazenando a base declarativa na variável Base
Base = declarative_base()


#criando a classe de modelo do banco de dados
class Usuario(Base):
    #Modelo de Usuário
    
    # Definindo o nome da tabela no banco de dados
    __tablename__ = "usuarios"
    id  = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String, nullable=False, unique=True)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean )
    admin = Column("admin", Boolean, default=False)

    # Método construtor para inicializar os atributos do usuário(sempre que iniciar a classe, ele vai receber esses parâmetros)
    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin


# Enum nativo do Python para status do pedido
class StatusPedidoEnum(enum.Enum):
    PENDENTE = "Pendente"
    CANCELADO = "Cancelado"
    FINALIZADO = "Finalizado"

#Pedido

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", Enum(StatusPedidoEnum), nullable=False)
    usuario = Column("usuario", ForeignKey("usuarios.id")) 
    preco =  Column("preco", Float)
    itens = relationship("ItemPedido", cascade="all, delete")

    def __init__(self, usuario,status=StatusPedidoEnum.PENDENTE, preco = 0):
        self.status = status
        self.usuario = usuario
        self.preco = preco

    def calcularPreco(self):
        #relação vinda do relationship(pegando o item que tem desse pedido)
        preco_pedido = 0
        for iten in self.itens:
            preco_item = iten.preco_unitario * iten.quantidade
            preco_pedido += preco_item
        
        self.preco = preco_pedido

#ItemPedido
class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantidade = Column("quantidade", Integer)
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float)
    pedido = Column("pedido", ForeignKey("pedidos.id"))

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido
