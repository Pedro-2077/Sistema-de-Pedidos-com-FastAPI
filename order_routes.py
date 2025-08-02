from fastapi import APIRouter,HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from schemas import PedidoSchema,SchemaItemPedido, ResponsePedidosSchema
from models import Pedido, StatusPedidoEnum, Usuario, ItemPedido
from typing import List

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"], dependencies=[Depends(verificar_token)])

'''Destrinchando o código:
@order_router: é um decorador que define uma rota GET,POST ... para o caminho raiz do roteador de pedidos.
(/): é o caminho relativo para esta rota, que será acessível em /pedidos/ quando o servidor estiver rodando. 
''' 
@order_router.get("/")
async def pedidos():
    """Rota de pedidos
    
    Esta rota é usada para verificar se a rota de pedidos está funcionando corretamente.

    """
    return {"mensagem": "Rota de pedidos funcionando!"}


@order_router.post("criar_pedidos")
async def criar_pedidos(pedido_schema:PedidoSchema, session:Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario=pedido_schema.usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem":"Pedido criado"}

#Cancelar pedido
@order_router.post("/cancelar_pedido/{id_pedido}")
async def cancelar_pedido(id_pedido:int,session :Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não existe")
    
    #Verificando se o usuario que criou pedido é de fato que esta cancelando ou se é admin 
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Vou não tem autorização para cancelar")
    
    pedido.status = StatusPedidoEnum.CANCELADO

    session.commit()

    return{
        #pedido_id mesmo com o laze_load agente consegue carregar todo o objeto 
        "mensagem":f"Pedido do numero: {pedido.id} cancelado com sucesso",
        "pedido": pedido
    }

#Listar Pedidos
@order_router.get("/listar")
async def listar_pedidos(session :Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer operação")
    else:
        pedidos = session.query(Pedido).all()
        return{
            "pedidos":pedidos
        }
    
#Adiciona Pedido
@order_router.post("/adicionar_item/{id_pedido}")
async def adicionar_item_pedido(id_pedido:int,
                                item_pedido_schema: SchemaItemPedido,
                                session :Session = Depends(pegar_sessao),
                                usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()

    if not pedido:
        raise HTTPException(status_code=401, detail="Pedido não existe")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização")
    
    item_pedido = ItemPedido(item_pedido_schema.quantidade,
                             item_pedido_schema.sabor,
                             item_pedido_schema.tamanho,
                             item_pedido_schema.preco_unitario,
                             id_pedido)
    
    session.add(item_pedido)
    pedido.calcularPreco()
    session.commit()
    return{
        "mensagem": "Item criado com sucesso",
        "item_id": item_pedido.id,
        "preço do pedido": pedido.preco
    }


#Remover Pedido
@order_router.post("/remover_item/{id_item_pedido}")
async def remover_item_pedido(id_item_pedido:int,
                                session :Session = Depends(pegar_sessao),
                                usuario: Usuario = Depends(verificar_token)):
    item_pedido = session.query(ItemPedido).filter(ItemPedido.id == id_item_pedido).first()
    pedido = session.query(Pedido).filter(Pedido.id == item_pedido.pedido).first()
    if not item_pedido:
        raise HTTPException(status_code=401, detail="Pedido não existe")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização")
    
    session.delete(item_pedido)
    pedido.calcularPreco() 
    session.commit()
    return{
        "mensagem": "Item removido com sucesso",
        "quantidades itens_pedidos": len(pedido.itens),
        "pedido": pedido
    }

#FINALIZAR PEDIDO
@order_router.post("/finalizar_pedido/{id_pedido}")
async def finalizar_pedido(id_pedido : int, session:Session=Depends(pegar_sessao), usuario:Usuario=Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=401, detail="Pedido nao encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Voce nao pode acessar")
    
    pedido.status = StatusPedidoEnum.FINALIZADO
    session.commit()
    return{
        "mensagem":f"Pedido do numero:{pedido.id} finalizado com sucesso",
        "pedido": pedido
    }

#Vizualizar 1 pedido
@order_router.post("/pedido/{id_pedido}")
async def pedido(id_pedido : int, session:Session=Depends(pegar_sessao), usuario:Usuario=Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=401, detail="Pedido nao encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Voce nao pode acessar")
    
    return{
        "quantidades de itens_pedido": len(pedido.itens),
        "pedidos": pedido
    }

#Vizualizar todos os pedidos de um usuario
@order_router.get("/listar/pedidos_usuarios", response_model=List[ResponsePedidosSchema])#O response_model e nosso schema personalizado
async def listar_pedidos(session : Session = Depends(pegar_sessao), usuario : Usuario = Depends(verificar_token)):
    pedidos = session.query(Pedido).filter(Pedido.usuario == usuario.id).all()
    print(type(pedidos))
    return pedidos #como estamos usando response model aqui ele vai retorna um lista de pedidos 

