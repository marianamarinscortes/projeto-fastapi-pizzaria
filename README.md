# Pizzaria API

API REST desenvolvida com **Python e FastAPI** para simular o funcionamento de um sistema de pedidos de uma pizzaria.

O projeto foi desenvolvido com foco em praticar desenvolvimento **back-end**, construção de APIs REST, autenticação, banco de dados e relacionamento entre entidades.

## Funcionalidades

* Cadastro e autenticação de usuários
* Autenticação utilizando JWT
* Controle de acesso entre usuários e administradores
* Criação e gerenciamento de pedidos
* Adição e remoção de itens dos pedidos
* Cálculo automático do valor dos pedidos
* Cardápio com pizzas, tamanhos, preços e bebidas
* Controle de disponibilidade dos itens
* Consulta dos pedidos do usuário
* Gerenciamento de pedidos por administradores

## Tecnologias

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* SQLite
* Alembic
* JWT
* Git e GitHub

## Objetivo

Este projeto foi desenvolvido como parte dos meus estudos de desenvolvimento back-end com Python, com o objetivo de praticar a construção de APIs REST utilizando FastAPI e trabalhar com autenticação, banco de dados e relacionamentos entre entidades.

Pretendo continuar evoluindo o projeto conforme avanço nos estudos, adicionando novas funcionalidades e, futuramente, possivelmente desenvolvendo uma interface para consumir a API.

## Como executar

### 1. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto, utilizando o `.env.example` como modelo.

```env
SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Criar os itens iniciais do cardápio

```bash
python seed.py
```

### 4. Executar a API

```bash
python -m uvicorn main:app --reload
```

A API estará disponível em:

```text
http://127.0.0.1:8000
```

### 5. Acessar a documentação

A documentação interativa do FastAPI pode ser acessada pelo Swagger:

```text
http://127.0.0.1:8000/docs
```

A partir da documentação, é possível testar as rotas e funcionalidades da API.
