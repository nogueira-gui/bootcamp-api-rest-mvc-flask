# 📦 API RESTful - Desafio Final - Bootcamp Arquiteto(a) de Software

Este projeto é uma API RESTful desenvolvida com **Flask (Python)** seguindo o padrão arquitetural **MVC**. A API permite operações CRUD em um domínio escolhido (Usuario, Clientes, Produtos e Pedidos) e está estruturada para ser executada com **Docker** e **Docker Compose**. Também inclui autenticação e autorização via tokens JWT.

---

## 📚 Sumário

- [🔧 Tecnologias](#-tecnologias)  
- [📁 Estrutura de Pastas](#-estrutura-de-pastas)  
- [🚀 Como Executar](#-como-executar)  
- [🔐 Autenticação e Autorização](#-autenticação-e-autorização)  
- [📌 Endpoints da API](#-endpoints-da-api)  
- [🗂️ Diagrama Arquitetural](#-diagrama-arquitetural)  
- [📄 Licença](#-licença)  

---

## 🔧 Tecnologias

- Python 3.11+  
- Flask  
- Flask-JWT-Extended  
- SQLAlchemy  
- PostgreSQL  
- Docker e Docker Compose  

## 🏗️ Padrões de Projeto

O projeto utiliza diversos padrões de projeto para garantir uma arquitetura limpa e manutenível. Os padrões mais importantes são:

### Padrões Fundamentais

#### 1. MVC (Model-View-Controller)
- **Propósito**: Separação clara de responsabilidades
- **Implementação**: 
  - `models/`: Entidades de domínio (Produto, Cliente, Pedido)
  - `controllers/`: Tratamento de requisições HTTP
  - `views/`: Rotas da API REST
- **Benefícios**: Código organizado, manutenível e escalável

#### 2. Repository Pattern
- **Propósito**: Abstrair o acesso ao banco de dados
- **Implementação**: Classes em `repositories/` (ProdutoRepository, ClienteRepository)
- **Benefícios**: 
  - Troca de banco de dados sem afetar a lógica de negócio
  - Centralização das operações de persistência
  - Facilita testes unitários

#### 3. Service Layer
- **Propósito**: Conter a lógica de negócio
- **Implementação**: Classes em `services/` (ProdutoService, ClienteService)
- **Benefícios**:
  - Separação clara entre regras de negócio e controladores
  - Código mais organizado e testável
  - Reutilização de lógica entre diferentes endpoints

#### 4. Dependency Injection
- **Propósito**: Reduzir acoplamento entre componentes
- **Implementação**: Injeção de serviços nos controladores
- **Benefícios**:
  - Facilita testes unitários
  - Código mais flexível e manutenível
  - Melhor organização das dependências

### Outros Padrões Utilizados

#### Padrões de Criação
- **Factory Method**: Criação de repositórios
- **Singleton**: Instanciação única de serviços

#### Padrões Estruturais
- **Facade**: Interface simplificada para serviços complexos (ex: S3)
- **Decorator**: Autenticação e autorização
- **Data Transfer Object (DTO)**: Transferência de dados entre camadas

#### Padrões Comportamentais
- **Strategy**: Diferentes estratégias de autenticação
- **Observer**: Reação a eventos do banco de dados
- **Template Method**: Operações CRUD base

## 📸 Armazenamento de Imagens (S3)

A API utiliza o Amazon S3 para armazenamento de imagens de produtos. Para desenvolvimento local, utilizamos o LocalStack para simular o ambiente AWS.

### Configuração do S3

Para configurar o S3, são necessárias as seguintes variáveis de ambiente:
```bash
AWS_ACCESS_KEY_ID=test
AWS_SECRET_ACCESS_KEY=test
AWS_DEFAULT_REGION=us-east-1
S3_BUCKET_NAME=produtos-imagens
S3_ENDPOINT_URL=http://localstack:4566
```

### Funcionalidades do Serviço S3

- Upload de imagens com validação de formato (JPG, JPEG, PNG)
- Limite de tamanho de arquivo (5MB)
- Geração automática de nomes únicos para evitar conflitos
- Exclusão automática de imagens antigas ao atualizar produtos
- URLs públicas para acesso às imagens

### Simulação Local com LocalStack

O projeto utiliza o LocalStack para simular o ambiente AWS localmente. O LocalStack é configurado no `docker-compose.yml`:

```yaml
localstack:
  image: localstack/localstack:latest
  ports:
    - "4566:4566"
  environment:
    - SERVICES=s3
    - DEBUG=1
    - DATA_DIR=/tmp/localstack/data
  volumes:
    - ./localstack:/tmp/localstack
```

Para usar o S3 localmente:

1. O bucket é criado automaticamente na inicialização do LocalStack
2. As URLs das imagens são geradas com o endpoint local: `http://localhost:4566/<bucket>/<chave>`
3. O serviço S3 é integrado automaticamente ao gerenciamento de produtos

### Integração com Produtos

O serviço S3 é integrado automaticamente ao gerenciamento de produtos, permitindo:
1. Upload de imagens ao criar/atualizar produtos
2. Exclusão automática de imagens ao deletar produtos
3. Validação de formatos e tamanhos de arquivo

---

## 📁 Estrutura de Pastas

```bash
.
├── app/
│   ├── controllers/    # Controladores: tratam as requisições HTTP
│   ├── models/         # Modelos: definem as entidades de domínio
│   ├── services/       # Serviços: lógica de negócio
│   ├── repositories/   # Repositórios: abstração de acesso ao banco
│   ├── auth/           # Módulo de autenticação e autorização
│   ├── config/         # Configurações da aplicação
│   └── __init__.py     # Inicialização da aplicação Flask
├── tests/              # Testes automatizados (unitários e integração)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt    # Dependências Python
├── README.md           # Documentação do projeto
└── .env.example        # Variáveis de ambiente
```

---

## 🚀 Como Executar

```bash
# 1. Clone o repositório
git clone https://github.com/nogueira-gui/bootcamp-api-rest-mvc-flask.git

# 2. Entre na pasta do projeto
cd bootcamp-api-rest-mvc-flask

# 3. Suba o ambiente com Docker Compose
docker-compose up --build

# 4. Acesse a API
http://localhost:5000
```

### 🧪 Instalação de Dependências para Testes

Para executar os testes localmente (sem Docker), siga os passos abaixo:

```bash
# 1. Crie um ambiente virtual Python (recomendado)
python -m venv venv

# 2. Ative o ambiente virtual
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate

# 4. Instale as dependências
pip install -r requirements.txt

# 5. Execute os testes
pytest
```

---

## 🔐 Autenticação e Autorização

A API utiliza **JWT (JSON Web Tokens)** para autenticação. Algumas rotas são protegidas e exigem um token válido no header:

```
Authorization: Bearer <seu_token_jwt>
```

- **POST /auth/login**: autentica o usuário e retorna um token JWT.  
- **POST /auth/register**: registra novo usuário.

Cada usuário possui um perfil (por exemplo, **ADMIN** ou **USER**), e certas rotas só podem ser acessadas por perfis específicos.

---

## 📌 Endpoints da API

### 🧾 Autenticação

| Método | Rota            | Descrição                           | Protegida |
|--------|-----------------|-------------------------------------|-----------|
| POST   | `/auth/login`   | Autentica usuário e gera token JWT  | ❌        |
| POST   | `/auth/register`| Registra novo usuário               | ❌        |
| GET    | `/auth/me`      | Retorna dados do usuário logado     | ✅        |

---

### 👤 Clientes

| Método | Rota                       | Descrição                             | Protegida    |
|--------|----------------------------|---------------------------------------|--------------|
| POST   | `/clientes`                | Criar novo cliente                    | ✅ (USER)    |
| GET    | `/clientes`                | Listar todos os clientes              | ✅ (USER)    |
| GET    | `/clientes/{id}`           | Obter cliente por ID                  | ✅ (USER)    |
| GET    | `/clientes/nome/{nome}`    | Buscar clientes por nome              | ✅ (USER)    |
| GET    | `/clientes/contar`         | Retornar total de clientes            | ✅ (USER)    |
| PUT    | `/clientes/{id}`           | Atualizar cliente                     | ✅ (USER)    |
| DELETE | `/clientes/{id}`           | Remover cliente                       | ✅ (ADMIN)   |

---

### 📦 Produtos

| Método | Rota                       | Descrição                             | Protegida    |
|--------|----------------------------|---------------------------------------|--------------|
| POST   | `/produtos`                | Criar novo produto                    | ✅ (ADMIN)   |
| GET    | `/produtos`                | Listar todos os produtos              | ✅ (USER)    |
| GET    | `/produtos/{id}`           | Obter produto por ID                  | ✅ (USER)    |
| GET    | `/produtos/nome/{nome}`    | Buscar produtos por nome              | ✅ (USER)    |
| GET    | `/produtos/contar`         | Retornar total de produtos            | ✅ (USER)    |
| PUT    | `/produtos/{id}`           | Atualizar produto                     | ✅ (ADMIN)   |
| DELETE | `/produtos/{id}`           | Remover produto                       | ✅ (ADMIN)   |

---

### 🛒 Pedidos

| Método | Rota                       | Descrição                             | Protegida    |
|--------|----------------------------|---------------------------------------|--------------|
| POST   | `/pedidos`                 | Criar novo pedido                     | ✅ (USER)    |
| GET    | `/pedidos`                 | Listar todos os pedidos               | ✅ (USER)    |
| GET    | `/pedidos/{id}`            | Obter pedido por ID                   | ✅ (USER)    |
| GET    | `/pedidos/cliente/{id}`    | Buscar pedidos por cliente            | ✅ (USER)    |
| GET    | `/pedidos/contar`          | Retornar total de pedidos             | ✅ (USER)    |
| PUT    | `/pedidos/{id}/status`     | Atualizar status do pedido            | ✅ (ADMIN)   |
| DELETE | `/pedidos/{id}`            | Remover pedido                        | ✅ (ADMIN)   |

---

## 🗂️ Diagrama Arquitetural

> Insira aqui a imagem do diagrama UML/C4 (por exemplo, gerado no draw.io).

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License**.