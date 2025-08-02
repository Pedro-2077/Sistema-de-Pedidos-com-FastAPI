#Criando um arquivo roteaor para organizar as rotas de autenticação
from fastapi import APIRouter

#Informando que o parmentro da minha função vai precisar de uma dependencia
from fastapi import Depends
from fastapi import HTTPException

from models import Usuario
from dependencies import pegar_sessao
from dependencies import verificar_token
from main import bcrypt_context
from main import ALGORITHM
from main import ACESS_TOKEN_EXPIRE_MINUTES
from main import SECRET_KEY
from schemas import UsuarioSchema
from schemas import SchemaLogin
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime,timedelta,timezone
from fastapi.security import OAuth2PasswordRequestForm

# Adicionando as rotas de autenticação ao app
auth_router = APIRouter(prefix="/auth", tags=["auth"])

#Criando Token 
def criar_token(usuario_id, duracao_token = timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)):
    #Definindo a data da expiração 
    data_expiracao = datetime.now(timezone.utc) + duracao_token

    
    #Criando os dados para passar para o JWT
    dict_info = {"sub": str(usuario_id), "exp":data_expiracao}
    
    #Codificação do JWT (passando o dicionario que criamos , nossa secret e o algoritimo)
    jwt_codificado = jwt.encode(dict_info,SECRET_KEY,ALGORITHM)
    
    return jwt_codificado

def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()

    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    else:
        return usuario


'''
Destrinchando o código:
APIRouter: é uma classe do FastAPI que permite criar um grupo de rotas com um prefixo comum, facilitando a organização do código
prefico: é o prefixo que será adicionado a todas as rotas deste roteador
tags: são usadas para agrupar as rotas na documentação gerada pelo FastAPI, facilitando a navegação e compreensão das rotas disponíveis

'''

@auth_router.get("/")
async def main():
    """Rota de autenticação
    
    Esta rota é usada para verificar se a autenticação está funcionando corretamente.

    """
    return {"mensagem": "Rota de autenticação!", "status": False}

@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema:UsuarioSchema, session: Session = Depends(pegar_sessao)):
    """
    Criar conta 
    """
    #Verifica o se existe o usuario com aquele email
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()

    if usuario:
        raise HTTPException(status_code=400, detail="Email do usuario ja cadastrado")
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email,senha_criptografada,usuario_schema.ativo,usuario_schema.admin)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem":"Usuario cadastrado com sucesso"}
    
@auth_router.post("/login")
async def login(schema_login:SchemaLogin, session:Session=Depends(pegar_sessao)):
    """WIKTEN GOSTOSO"""
    usuario = autenticar_usuario(schema_login.email, schema_login.senha, session)

    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario não encontrado ou Credencias erradas")
    else:
        acess_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
        return {
            "acess_token": acess_token,
            "refresh_token":refresh_token,
            "token_type": "Bearer" #É o tipo do token
        }

#LOGIN DO FORMULARIO DO FASTAPI    
@auth_router.post("/login-form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)

    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")

    access_token = criar_token(usuario.id)

    return {
        "access_token": access_token,  
        "token_type": "bearer"         
    }

#Criar um novo acess_token do usuario usando o refresh_token    
@auth_router.get("/refresh")
async def use_refresh_token(usuario:Usuario = Depends(verificar_token)):
    acess_token = criar_token(usuario.id)
    return{
        "acess_token":acess_token,
        "token_type": "Bearer"
    }

