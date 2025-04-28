import pytest
import requests
import uuid
import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app

load_dotenv()

BASE_URL = os.getenv('API_URL', 'http://localhost:5000')

@pytest.fixture
def app():
    """Cria uma instância da aplicação para testes"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/test_db')
    return app

@pytest.fixture
def admin_token():
    """Obtém token do admin padrão"""
    response = requests.post(f'{BASE_URL}/auth/login', json={
        'email': 'yami@example.com',
        'senha': os.getenv('ADMIN_PASSWORD', 'yami123')
    })
    return response.json()['access_token']

@pytest.fixture
def usuario_aleatorio():
    """Cria um usuário aleatório via API e retorna seus dados"""
    email = f"test_{uuid.uuid4().hex[:8]}@test.com"
    senha = "test123"
    
    response = requests.post(f'{BASE_URL}/auth/register', json={
        'email': email,
        'senha': senha,
        'perfil': 'CLIENTE'
    })
    
    return {
        'email': email,
        'senha': senha,
        'id': response.json()['usuario']['id']
    }

@pytest.fixture
def cliente_token(usuario_aleatorio):
    """Obtém token do usuário aleatório"""
    response = requests.post(f'{BASE_URL}/auth/login', json={
        'email': usuario_aleatorio['email'],
        'senha': usuario_aleatorio['senha']
    })
    return response.json()['access_token']

@pytest.fixture
def produto_exemplo(admin_token):
    """Cria um produto de exemplo via API"""
    data = {
        'nome': 'Produto Teste',
        'descricao': 'Descrição do produto teste',
        'preco': '99.99',
        'quantidade_estoque': '10'
    }
    
    response = requests.post(
        f'{BASE_URL}/produtos',
        headers={'Authorization': f'Bearer {admin_token}'},
        data=data
    )
    
    if response.status_code != 201:
        raise Exception(f"Erro ao criar produto de exemplo: {response.json()}")
        
    return response.json()

@pytest.fixture
def cliente_exemplo(cliente_token):
    """Cria um cliente de exemplo via API"""
    
    data = {
        'nome': 'Cliente Teste',
        'email': f'cliente_{uuid.uuid4().hex[:8]}@test.com',
        'telefone': '11999999999'
    }
    
    response = requests.post(
        f'{BASE_URL}/clientes',
        headers={
            'Authorization': f'Bearer {cliente_token}',
            'Content-Type': 'application/json'
        },
        json=data
    )
    
    if response.status_code != 201:
        raise Exception(f"Erro ao criar cliente de exemplo: {response.json()}")
        
    return response.json() 