#Criar o nosso app
from fastapi import FastAPI

#Criar a criptografia
from passlib.context import CryptContext

from dotenv import load_dotenv
import os

#Schema para o Oauth2 para manda no header o formatdo correto com os bearer
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

#CRIANDO TOKEN
ALGORITHM = os.getenv("ALGORITHM")

#TEMPO DO TOKEN (como vamos fazer a conta desse valor precisamos tranforma em int )
ACESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACESS_TOKEN_EXPIRE_MINUTES"))

#Crinado schema OAuth2
schema_OAuth2 = OAuth2PasswordBearer(tokenUrl="auth/login-form")


# Criandp a instancia do nosso app em FastAPI
app = FastAPI()

#Criptografia
"""schemes=["bcrypt"] escolhe a criptografia
deprecated="auto" caso o modelo de criptografia esteja defasado ele escolhe um novo
"""
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#comando para rodar o nosso codigo no terminal uvicorn main:app --reload
#alembic init alembic inicializa o alembic, criando a pasta alembic e o arquivo env.py
#alembic revision --autogenerate -m "initial magrations" inicia as migrations
#alembic upgrade head

'''
Destrinchando o comando:
uvicorn: é o servidor ASGI serve para rodar o nosso app pois sem ele não conseguimos rodar o FastAPI
main: é o nome do arquivo onde está o nosso app, no caso main.py
app: é o nome da instancia do nosso app que criamos no arquivo main.py
--reload: é um comando que faz com que o servidor reinicie automaticamente sempre que houver uma alteração no código, facilitando o desenvolvimento

'''

#Importando as rotas que criamos

#So pode ser importado depois de criar a instancia do app
from auth_routes import auth_router
from order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)



