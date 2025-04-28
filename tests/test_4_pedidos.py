import pytest
import requests
from conftest import BASE_URL

@pytest.fixture
def pedido_exemplo(admin_token, cliente_exemplo, produto_exemplo):
    """Cria um pedido de exemplo via API"""
    response = requests.post(
        f'{BASE_URL}/pedidos',
        headers={'Authorization': f'Bearer {admin_token}'},
        json={
            'cliente_id': cliente_exemplo['id'],
            'itens': [
                {
                    'produto_id': produto_exemplo['id'],
                    'quantidade': 2
                }
            ]
        }
    )
    
    if response.status_code != 201:
        raise Exception(f"Erro ao criar pedido de exemplo: {response.json()}")
        
    return response.json()

def test_criar_pedido_sucesso(cliente_token, cliente_exemplo, produto_exemplo):
    """Testa criação de pedido com sucesso"""
    print("\n=== Iniciando teste de criação de pedido ===")
    print(f"Cliente exemplo: {cliente_exemplo}")
    print(f"Produto exemplo: {produto_exemplo}")
    
    # Verifica se o cliente existe
    print("\nVerificando cliente...")
    response = requests.get(
        f'{BASE_URL}/clientes/{cliente_exemplo["id"]}',
        headers={'Authorization': f'Bearer {cliente_token}'}
    )
    print(f"Resposta da verificação do cliente: {response.status_code} - {response.json()}")
    assert response.status_code == 200, f"Cliente não encontrado: {response.json()}"
    
    # Verifica se o produto existe e tem estoque
    print("\nVerificando produto...")
    response = requests.get(
        f'{BASE_URL}/produtos/{produto_exemplo["id"]}',
        headers={'Authorization': f'Bearer {cliente_token}'}
    )
    print(f"Resposta da verificação do produto: {response.status_code} - {response.json()}")
    assert response.status_code == 200, f"Produto não encontrado: {response.json()}"
    produto = response.json()
    assert produto['quantidade_estoque'] >= 2, f"Produto sem estoque suficiente: {produto}"
    
    # Cria o pedido
    pedido_data = {
        'cliente_id': cliente_exemplo['id'],
        'itens': [
            {
                'produto_id': produto_exemplo['id'],
                'quantidade': 2
            }
        ]
    }
    
    print("\nDados do pedido a ser criado:")
    print(f"pedido_data: {pedido_data}")
    print(f"Headers: Authorization: Bearer {cliente_token}")
    
    print("\nEnviando requisição de criação do pedido...")
    response = requests.post(
        f'{BASE_URL}/pedidos',
        headers={
            'Authorization': f'Bearer {cliente_token}',
            'Content-Type': 'application/json'
        },
        json=pedido_data
    )
    
    print(f"\nResposta da criação do pedido:")
    print(f"Status Code: {response.status_code}")
    print(f"Resposta: {response.json()}")
    
    assert response.status_code == 201, f"Erro ao criar pedido: {response.json()}"
    pedido = response.json()
    
    print("\nVerificando dados do pedido criado:")
    print(f"Pedido completo: {pedido}")
    
    assert 'id' in pedido, f"Pedido sem ID: {pedido}"
    assert pedido['cliente_id'] == cliente_exemplo['id'], f"Cliente ID incorreto: {pedido}"
    assert len(pedido['itens']) == 1, f"Número incorreto de itens: {pedido}"
    assert pedido['itens'][0]['produto_id'] == produto_exemplo['id'], f"Produto ID incorreto: {pedido}"
    assert pedido['itens'][0]['quantidade'] == 2, f"Quantidade incorreta: {pedido}"
    assert pedido['status'] == 'PENDENTE', f"Status incorreto: {pedido}"
    
    print("\n=== Teste concluído com sucesso ===")

def test_criar_pedido_sem_autenticacao(cliente_exemplo, produto_exemplo):
    """Testa criação de pedido sem autenticação"""
    response = requests.post(
        f'{BASE_URL}/pedidos',
        json={
            'cliente_id': cliente_exemplo['id'],
            'itens': [
                {
                    'produto_id': produto_exemplo['id'],
                    'quantidade': 2
                }
            ]
        }
    )
    
    assert response.status_code == 401

def test_criar_pedido_sem_estoque(admin_token, cliente_exemplo, produto_exemplo):
    """Testa criação de pedido sem estoque suficiente"""
    # Atualiza o estoque do produto para 0
    response = requests.put(
        f'{BASE_URL}/produtos/{produto_exemplo["id"]}',
        headers={'Authorization': f'Bearer {admin_token}'},
        data={
            'quantidade_estoque': '0'
        }
    )
    
    response = requests.post(
        f'{BASE_URL}/pedidos',
        headers={'Authorization': f'Bearer {admin_token}'},
        json={
            'cliente_id': cliente_exemplo['id'],
            'itens': [
                {
                    'produto_id': produto_exemplo['id'],
                    'quantidade': 2
                }
            ]
        }
    )
    
    assert response.status_code == 400
    assert 'error' in response.json()

def test_listar_pedidos(admin_token, pedido_exemplo):
    """Testa listagem de pedidos"""
    response = requests.get(
        f'{BASE_URL}/pedidos',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    
    assert response.status_code == 200
    pedidos = response.json()
    assert len(pedidos) > 0
    assert any(p['id'] == pedido_exemplo['id'] for p in pedidos)

def test_obter_pedido(cliente_token, pedido_exemplo):
    """Testa obtenção de pedido específico"""
    response = requests.get(
        f'{BASE_URL}/pedidos/{pedido_exemplo["id"]}',
        headers={'Authorization': f'Bearer {cliente_token}'}
    )
    
    assert response.status_code == 200
    pedido = response.json()
    assert pedido['id'] == pedido_exemplo['id']
    assert pedido['cliente_id'] == pedido_exemplo['cliente_id']
    assert len(pedido['itens']) == len(pedido_exemplo['itens'])
    assert pedido['status'] == 'PENDENTE'

def test_buscar_pedidos_por_cliente(admin_token, pedido_exemplo):
    """Testa busca de pedidos por cliente"""
    response = requests.get(
        f'{BASE_URL}/pedidos/cliente/{pedido_exemplo["cliente_id"]}',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    
    assert response.status_code == 200
    pedidos = response.json()
    assert len(pedidos) > 0
    assert any(p['id'] == pedido_exemplo['id'] for p in pedidos)

def test_atualizar_status_pedido(admin_token, pedido_exemplo):
    """Testa atualização de status do pedido"""
    response = requests.put(
        f'{BASE_URL}/pedidos/{pedido_exemplo["id"]}/status',
        headers={'Authorization': f'Bearer {admin_token}'},
        json={
            'status': 'EM_PREPARO'
        }
    )
    
    assert response.status_code == 200
    pedido = response.json()
    assert pedido['status'] == 'EM_PREPARO'

def test_atualizar_status_pedido_sem_permissao(cliente_token, pedido_exemplo):
    """Testa atualização de status do pedido sem permissão"""
    response = requests.put(
        f'{BASE_URL}/pedidos/{pedido_exemplo["id"]}/status',
        headers={'Authorization': f'Bearer {cliente_token}'},
        json={
            'status': 'EM_PREPARO'
        }
    )
    
    assert response.status_code == 403
    assert 'error' in response.json()

def test_deletar_pedido(admin_token, pedido_exemplo):
    """Testa deleção de pedido"""
    response = requests.delete(
        f'{BASE_URL}/pedidos/{pedido_exemplo["id"]}',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    
    assert response.status_code == 200
    assert response.json()['message'] == 'Pedido deletado com sucesso'
    
    # Verifica se o pedido foi realmente deletado
    response = requests.get(
        f'{BASE_URL}/pedidos/{pedido_exemplo["id"]}',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 404 