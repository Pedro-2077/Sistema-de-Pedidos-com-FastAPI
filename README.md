Perfeito, Pedro! Com base no seu repositório e as observações — **não subir o `banco.db`** nem o **arquivo `.env`** — aqui está a versão atualizada e profissional do seu `README.md`:

---


# 🍕 Sistema de Pedidos com FastAPI

Este repositório contém um sistema completo de gerenciamento de pedidos desenvolvido com **FastAPI** e **SQLAlchemy**, incluindo autenticação com JWT, controle de acesso e manipulação de pedidos e itens.

🔗 Repositório: [github.com/Pedro-2077/Sistema-de-Pedidos-com-FastAPI](https://github.com/Pedro-2077/Sistema-de-Pedidos-com-FastAPI)

---

## 🚀 Funcionalidades

- ✅ Cadastro e login de usuários
- 🔐 Autenticação segura com JWT
- 👤 Diferenciação entre usuários comuns e administradores
- 📦 Criação e gerenciamento de pedidos
- 🧾 Adição, remoção e visualização de itens por pedido
- 📊 Controle de status dos pedidos: Pendente, Cancelado, Finalizado

---

## 🛠 Tecnologias Utilizadas

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [SQLite](https://www.sqlite.org/index.html)
- [Pydantic](https://docs.pydantic.dev/)
- [bcrypt](https://pypi.org/project/bcrypt/)
- [python-jose](https://python-jose.readthedocs.io/en/latest/)

---

## 📦 Instalação

> ⚠️ **Atenção:** O projeto não inclui o arquivo `.env` nem o banco de dados `banco.db`. Você deve criá-los localmente.

1. **Clone o repositório:**

```bash
git clone https://github.com/Pedro-2077/Sistema-de-Pedidos-com-FastAPI.git
cd Sistema-de-Pedidos-com-FastAPI
````

2. **Crie e ative um ambiente virtual:**

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

4. **Configure seu ambiente:**

Crie um arquivo `.env` com as seguintes variáveis (exemplo):

```env
SECRET_KEY=sua_chave_secreta_aqui
ALGORITHM=HS256
ACESS_TOKEN_EXPIRE_MINUTES=30
```

5. **Crie o banco de dados localmente:**

Execute um script para inicializar o banco ou insira isso em seu `main.py`:

```python
from models import Base, db
Base.metadata.create_all(bind=db)
```

6. **Execute o servidor:**

```bash
uvicorn main:app --reload
```

Acesse a documentação automática do FastAPI em:

📍 [`http://localhost:8000/docs`](http://localhost:8000/docs)

---

## 🔐 Autenticação

* Login e registro disponíveis via `/auth`
* JWT gerado após login para autenticação segura
* Tokens de acesso e refresh disponíveis

**Cabeçalho de autenticação:**

```http
Authorization: Bearer <seu_token>
```

---

## 📁 Rotas Disponíveis

### 🔐 `/auth` (Autenticação)

| Método | Rota                | Descrição                         |
| ------ | ------------------- | --------------------------------- |
| GET    | `/auth/`            | Verifica se rota está online      |
| POST   | `/auth/criar_conta` | Cria um novo usuário              |
| POST   | `/auth/login`       | Realiza login com email/senha     |
| POST   | `/auth/login-form`  | Login via formulário OAuth2       |
| GET    | `/auth/refresh`     | Gera novo token com refresh token |

### 📦 `/pedidos` (Pedidos)

| Método | Rota                               | Descrição                              |
| ------ | ---------------------------------- | -------------------------------------- |
| GET    | `/pedidos/`                        | Teste de rota                          |
| POST   | `/pedidos/criar_pedidos`           | Cria um novo pedido                    |
| POST   | `/pedidos/cancelar_pedido/{id}`    | Cancela um pedido                      |
| POST   | `/pedidos/finalizar_pedido/{id}`   | Finaliza um pedido                     |
| GET    | `/pedidos/listar`                  | Lista todos os pedidos (admin)         |
| GET    | `/pedidos/listar/pedidos_usuarios` | Lista pedidos do usuário logado        |
| POST   | `/pedidos/adicionar_item/{id}`     | Adiciona item ao pedido                |
| POST   | `/pedidos/remover_item/{id}`       | Remove item do pedido                  |
| POST   | `/pedidos/pedido/{id}`             | Exibe detalhes de um pedido específico |

---



## 📌 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

## 👤 Autor

Desenvolvido por [Pedro V.](https://github.com/Pedro-2077) 💻

---
