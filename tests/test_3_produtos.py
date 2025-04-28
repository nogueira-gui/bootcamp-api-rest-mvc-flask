import pytest
import requests
from conftest import BASE_URL

def test_criar_produto_sucesso(admin_token):
    """Testa criação de produto com sucesso"""
    data = {
        'nome': 'Produto Teste',
        'descricao': 'Descrição do produto teste',
        'preco': '10.99',
        'quantidade_estoque': '100'
    }
    
    response = requests.post(
        f'{BASE_URL}/produtos',
        headers={'Authorization': f'Bearer {admin_token}'},
        data=data
    )
    
    assert response.status_code == 201
    produto = response.json()
    assert 'id' in produto
    assert produto['nome'] == 'Produto Teste'
    assert produto['preco'] == 10.99
    assert produto['quantidade_estoque'] == 100

def test_criar_produto_sem_autenticacao():
    """Testa criação de produto sem autenticação"""
    data = {
        'nome': 'Produto Teste',
        'descricao': 'Descrição do produto teste',
        'preco': '10.99',
        'quantidade_estoque': '100'
    }
    
    response = requests.post(
        f'{BASE_URL}/produtos',
        data=data
    )
    
    assert response.status_code == 401

def test_criar_produto_sem_permissao(cliente_token):
    """Testa criação de produto sem permissão"""
    response = requests.post(
        f'{BASE_URL}/produtos',
        headers={'Authorization': f'Bearer {cliente_token}'},
        json={
            'nome': 'Produto Teste',
            'descricao': 'Descrição do produto teste',
            'preco': 10.99,
            'quantidade_estoque': 100
        }
    )
    
    assert response.status_code == 403
    assert 'error' in response.json()

def test_criar_produto_sem_nome(admin_token):
    data = {
        'descricao': 'Descrição do produto teste',
        'preco': '10.99',
        'quantidade_estoque': '100'
    }
    
    response = requests.post(
        f'{BASE_URL}/produtos',
        headers={'Authorization': f'Bearer {admin_token}'},
        data=data
    )
    
    assert response.status_code == 400
    assert 'error' in response.json()

def test_criar_produto_sem_preco(admin_token):
    data = {
        'nome': 'Produto Teste',
        'descricao': 'Descrição do produto teste',
        'quantidade_estoque': '100'
    }
    
    response = requests.post(
        f'{BASE_URL}/produtos',
        headers={'Authorization': f'Bearer {admin_token}'},
        data=data
    )
    
    assert response.status_code == 400
    assert 'error' in response.json()

def test_listar_produtos(admin_token, produto_exemplo):
    """Testa listagem de produtos"""
    response = requests.get(
        f'{BASE_URL}/produtos',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    
    assert response.status_code == 200
    produtos = response.json()
    assert len(produtos) > 0
    assert any(p['id'] == produto_exemplo['id'] for p in produtos)

def test_obter_produto(admin_token, produto_exemplo):
    """Testa obtenção de produto específico"""
    response = requests.get(
        f'{BASE_URL}/produtos/{produto_exemplo["id"]}',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    
    assert response.status_code == 200
    produto = response.json()
    assert produto['id'] == produto_exemplo['id']
    assert produto['nome'] == produto_exemplo['nome']

def test_atualizar_produto(admin_token, produto_exemplo):
    """Testa atualização de produto"""
    data = {
        'nome': 'Produto Atualizado',
        'descricao': 'Nova descrição',
        'preco': '15.99',
        'quantidade_estoque': '50'
    }
    
    response = requests.put(
        f'{BASE_URL}/produtos/{produto_exemplo["id"]}',
        headers={'Authorization': f'Bearer {admin_token}'},
        data=data
    )
    
    assert response.status_code == 200
    produto = response.json()
    assert produto['nome'] == 'Produto Atualizado'
    assert produto['preco'] == 15.99
    assert produto['quantidade_estoque'] == 50

def test_deletar_produto(admin_token, produto_exemplo):
    """Testa deleção de produto"""
    response = requests.delete(
        f'{BASE_URL}/produtos/{produto_exemplo["id"]}',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    
    assert response.status_code == 200
    assert response.json()['message'] == 'Produto deletado com sucesso'
    
    # Verifica se o produto foi realmente deletado
    response = requests.get(
        f'{BASE_URL}/produtos/{produto_exemplo["id"]}',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 404

def test_buscar_produto_por_nome(admin_token, produto_exemplo):
    """Testa busca de produto por nome"""
    response = requests.get(
        f'{BASE_URL}/produtos/nome/{produto_exemplo["nome"]}',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    
    assert response.status_code == 200
    produtos = response.json()
    assert len(produtos) > 0
    assert any(p['nome'] == produto_exemplo['nome'] for p in produtos)

def test_atualizar_estoque_produto(admin_token, produto_exemplo):
    """Testa atualização do estoque de um produto"""

    response = requests.get(
        f'{BASE_URL}/produtos/{produto_exemplo["id"]}',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    estoque_atual = response.json()['quantidade_estoque']
    
    novo_estoque = estoque_atual + 10
    data = {
        'quantidade_estoque': novo_estoque
    }
    
    response = requests.put(
        f'{BASE_URL}/produtos/{produto_exemplo["id"]}',
        headers={
            'Authorization': f'Bearer {admin_token}',
            'Content-Type': 'application/json'
        },
        json=data
    )
    
    assert response.status_code == 200
    produto = response.json()
    assert produto['quantidade_estoque'] == novo_estoque
    
    response = requests.get(
        f'{BASE_URL}/produtos/{produto_exemplo["id"]}',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    produto = response.json()
    assert produto['quantidade_estoque'] == novo_estoque

def test_atualizar_estoque_produto_negativo(admin_token, produto_exemplo):
    """Testa tentativa de atualizar estoque com valor negativo"""
    data = {
        'quantidade_estoque': -10
    }
    
    response = requests.put(
        f'{BASE_URL}/produtos/{produto_exemplo["id"]}',
        headers={
            'Authorization': f'Bearer {admin_token}',
            'Content-Type': 'application/json'
        },
        json=data
    )
    
    assert response.status_code == 400
    assert 'error' in response.json() 