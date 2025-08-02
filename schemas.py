from pydantic import BaseModel

#Option tipo de dados opcionais
from typing import Optional, List


class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    #Informa que é o mesmo que a nossa model criada 
    class Config:
        from_attributes = True 

class PedidoSchema(BaseModel):
    usuario: int

    class Config:
        from_attributes = True

class SchemaLogin(BaseModel):
    email: str
    senha: str

    class Config:
        from_attributes = True

class SchemaItemPedido(BaseModel):
    quantidade : int
    sabor: str
    tamanho: str
    preco_unitario: float
    
    class Config:
        from_attributes = True

#Fazendo um schema personalizado para exiber apenas os campos que eu quero 
class ResponsePedidosSchema(BaseModel):
    id: int
    status: str
    preco: float
    itens: List[SchemaItemPedido]

    class Config:
        from_attributes = True
