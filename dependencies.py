from models import db
from sqlalchemy.orm import sessionmaker
from models import Usuario
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from main import SECRET_KEY, ALGORITHM, schema_OAuth2
from jose import JWTError, jwt

def pegar_sessao():
    
    try:
        #Abrindo uma sesão com o banco de dados 
        Session = sessionmaker(bind=db)
        session = Session()

        yield session

    finally:
        session.close()

def verificar_token(token : str = Depends(schema_OAuth2), session: Session=Depends(pegar_sessao)):
    
    #Como o token contem as infrmações do usario preciso decodifcar para saber se de fato esse token era dele 
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)

        #Pegando id do usuario
        id_usuario = int(dic_info.get("sub"))

    #Caso o token não seja do usuário  ou o token tenha expirado
    except JWTError as erro:
        print(erro)
        raise HTTPException(status_code=401, detail="Acesso negado, verifique a validade do token")
    
    #Caso tenha o token mais o usuario não existe 
    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()

    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso Invalido")
    return usuario
