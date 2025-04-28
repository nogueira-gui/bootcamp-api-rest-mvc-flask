import pytest
import requests
import uuid
from conftest import BASE_URL

def test_registro_usuario_sucesso():
    """Testa registro de usuário com sucesso"""
    email = f"test_{uuid.uuid4().hex[:8]}@test.com"
    response = requests.post(f'{BASE_URL}/auth/register', json={
        'email': email,
        'senha': 'test123',
        'perfil': 'CLIENTE'
    })
    
    assert response.status_code == 201
    assert 'usuario' in response.json()
    assert 'id' in response.json()['usuario']
    assert response.json()['usuario']['email'] == email

def test_registro_usuario_email_existente(usuario_aleatorio):
    """Testa registro de usuário com email já existente"""
    response = requests.post(f'{BASE_URL}/auth/register', json={
        'email': usuario_aleatorio['email'],
        'senha': 'test123',
        'perfil': 'CLIENTE'
    })
    
    assert response.status_code == 400
    assert 'error' in response.json()

def test_login_sucesso(usuario_aleatorio):
    """Testa login com credenciais válidas"""
    response = requests.post(f'{BASE_URL}/auth/login', json={
        'email': usuario_aleatorio['email'],
        'senha': usuario_aleatorio['senha']
    })
    
    assert response.status_code == 200
    assert 'access_token' in response.json()

def test_login_credenciais_invalidas():
    """Testa login com credenciais inválidas"""
    response = requests.post(f'{BASE_URL}/auth/login', json={
        'email': 'inexistente@test.com',
        'senha': 'senhaerrada'
    })
    
    assert response.status_code == 401
    assert 'error' in response.json()

def test_login_dados_invalidos():
    """Testa login com dados inválidos"""
    response = requests.post(f'{BASE_URL}/auth/login', json={
        'email': 'emailinvalido',
        'senha': ''
    })
    
    assert response.status_code == 400
    assert 'error' in response.json()

def test_rota_protegida_sem_token():
    """Testa acesso a rota protegida sem token"""
    response = requests.get(f'{BASE_URL}/produtos')
    
    assert response.status_code == 401
    assert 'msg' in response.json()

def test_rota_protegida_token_invalido():
    """Testa acesso a rota protegida com token inválido"""
    response = requests.get(
        f'{BASE_URL}/produtos',
        headers={'Authorization': 'Bearer tokeninvalido'}
    )
    
    assert response.status_code == 422
    assert 'msg' in response.json()

def test_rota_protegida_token_valido(admin_token):
    """Testa acesso a rota protegida com token válido"""
    response = requests.get(
        f'{BASE_URL}/produtos',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    
    assert response.status_code == 200 