import requests
import json

API_URL = "http://localhost:5000"
IMAGEM_PATH = "images\Mago Negro.png"
NOME_PRODUTO = "Mago Negro"
DESCRICAO = "Um poderoso mago das trevas"
PRECO = 99.99
ESTOQUE = 10

login_data = {
    "email": "yami@example.com",
    "senha": "yami123"
}

print("Fazendo login...")
try:
    login_response = requests.post(f"{API_URL}/auth/login", json=login_data)
    login_response.raise_for_status()
    
    token = login_response.json().get('access_token')
    
    if not token:
        print("Erro: Token não encontrado na resposta")
        exit(1)
except requests.exceptions.RequestException as e:
    print(f"Erro ao fazer login: {str(e)}")
    print("Verifique se a API está rodando e acessível em http://localhost:5000")
    exit(1)
except json.JSONDecodeError as e:
    print(f"Erro ao decodificar resposta JSON: {str(e)}")
    print(f"Resposta recebida: {login_response.text}")
    exit(1)

print("Criando produto...")
try:
    files = {
        'imagem': open(IMAGEM_PATH, 'rb')
    }

    data = {
        'nome': NOME_PRODUTO,
        'descricao': DESCRICAO,
        'preco': PRECO,
        'quantidade_estoque': ESTOQUE
    }

    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.post(
        f"{API_URL}/produtos",
        headers=headers,
        data=data,
        files=files
    )
    response.raise_for_status()

    print("Produto criado com sucesso!")
    print(f"Resposta: {response.json()}")
except requests.exceptions.RequestException as e:
    print(f"Erro ao criar produto: {str(e)}")
    exit(1)
except FileNotFoundError:
    print(f"Erro: Arquivo de imagem não encontrado em {IMAGEM_PATH}")
    exit(1)
except Exception as e:
    print(f"Erro inesperado: {str(e)}")
    exit(1) 