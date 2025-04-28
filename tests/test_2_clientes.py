import pytest
import requests
import uuid
from conftest import BASE_URL

def test_criar_cliente_sucesso(cliente_token):
    """Testa criação de cliente com sucesso"""
    # Verifica se o token é válido
    response = requests.get(
        f'{BASE_URL}/auth/me',
        headers={'Authorization': f'Bearer {cliente_token}'}
    )
    print(f"\nVerificação do token:")
    print(f"Status: {response.status_code}")
    print(f"Dados do usuário: {response.json()}")
    
    # Gera um email único
    email_unico = f'cliente_{uuid.uuid4().hex[:8]}@test.com'
    
    data = {
        'nome': 'Cliente Teste',
        'email': email_unico,
        'telefone': '11999999999'
    }
    
    print(f"\nDados do cliente a ser criado: {data}")
    print(f"Token do cliente: {cliente_token}")
    
    response = requests.post(
        f'{BASE_URL}/clientes',
        headers={
            'Authorization': f'Bearer {cliente_token}',
            'Content-Type': 'application/json'
        },
        json=data
    )
    
    print(f"Status code: {response.status_code}")
    print(f"Resposta: {response.json()}")
    
    assert response.status_code == 201
    cliente = response.json()
    assert 'id' in cliente
    assert cliente['nome'] == 'Cliente Teste'
    assert cliente['email'] == email_unico
    assert cliente['telefone'] == '11999999999'

def test_criar_cliente_email_duplicado(cliente_token):
    """Testa criação de cliente com email duplicado"""
    # Primeiro cria um cliente com sucesso
    email_teste = f'cliente_{uuid.uuid4().hex[:8]}@test.com'
    
    # Cria o primeiro cliente
    data = {
        'nome': 'Cliente Teste',
        'email': email_teste,
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
    
    assert response.status_code == 201, "Falha ao criar o primeiro cliente"
    
    # Tenta criar outro cliente com o mesmo email
    print(f"\nTentando criar cliente duplicado com email: {email_teste}")
    
    response = requests.post(
        f'{BASE_URL}/clientes',
        headers={
            'Authorization': f'Bearer {cliente_token}',
            'Content-Type': 'application/json'
        },
        json=data
    )
    
    print(f"Status code: {response.status_code}")
    print(f"Resposta: {response.json()}")
    
    assert response.status_code == 400
    assert 'error' in response.json()

def test_listar_clientes(admin_token, cliente_exemplo):
    """Testa listagem de clientes"""
    response = requests.get(
        f'{BASE_URL}/clientes',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    
    assert response.status_code == 200
    clientes = response.json()
    assert len(clientes) > 0
    assert any(c['id'] == cliente_exemplo['id'] for c in clientes)

def test_obter_cliente(cliente_token, cliente_exemplo):
    """Testa obtenção de cliente específico"""
    response = requests.get(
        f'{BASE_URL}/clientes/{cliente_exemplo["id"]}',
        headers={'Authorization': f'Bearer {cliente_token}'}
    )
    
    assert response.status_code == 200
    cliente = response.json()
    assert cliente['id'] == cliente_exemplo['id']
    assert cliente['nome'] == cliente_exemplo['nome']

def test_atualizar_cliente(cliente_token, cliente_exemplo):
    """Testa atualização de cliente"""
    data = {
        'nome': 'Cliente Atualizado',
        'telefone': '11988888888'
    }
    
    response = requests.put(
        f'{BASE_URL}/clientes/{cliente_exemplo["id"]}',
        headers={'Authorization': f'Bearer {cliente_token}'},
        json=data
    )
    
    assert response.status_code == 200
    cliente = response.json()
    assert cliente['nome'] == 'Cliente Atualizado'
    assert cliente['telefone'] == '11988888888'

def test_deletar_cliente(admin_token, cliente_exemplo):
    """Testa deleção de cliente"""
    response = requests.delete(
        f'{BASE_URL}/clientes/{cliente_exemplo["id"]}',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    
    assert response.status_code == 204
    
    # Verifica se o cliente foi realmente deletado
    response = requests.get(
        f'{BASE_URL}/clientes/{cliente_exemplo["id"]}',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 404

def test_buscar_cliente_por_nome(admin_token, cliente_exemplo):
    """Testa busca de cliente por nome"""
    response = requests.get(
        f'{BASE_URL}/clientes/nome/{cliente_exemplo["nome"]}',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    
    assert response.status_code == 200
    clientes = response.json()
    assert len(clientes) > 0
    assert any(c['nome'] == cliente_exemplo['nome'] for c in clientes) 