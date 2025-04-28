from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.pedido_service import PedidoService
from app.models.usuario import PerfilUsuario

bp = Blueprint('pedidos', __name__, url_prefix='/pedidos')
pedido_service = PedidoService()

def verificar_perfil_admin():
    current_user = get_jwt_identity()
    return current_user['perfil'] == PerfilUsuario.ADMIN.value

@bp.route('', methods=['POST'])
@jwt_required()
def criar_pedido():
    data = request.get_json()
    
    if not data or not data.get('cliente_id') or not data.get('itens'):
        return jsonify({'error': 'Cliente e itens são obrigatórios'}), 400
    
    try:
        result = pedido_service.criar_pedido(
            cliente_id=data['cliente_id'],
            itens=data['itens']
        )
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@bp.route('', methods=['GET'])
@jwt_required()
def listar_pedidos():
    try:
        result = pedido_service.listar_pedidos()
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def obter_pedido(id):
    try:
        result = pedido_service.obter_pedido(id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@bp.route('/cliente/<int:cliente_id>', methods=['GET'])
@jwt_required()
def buscar_por_cliente(cliente_id):
    try:
        result = pedido_service.buscar_por_cliente(cliente_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/contar', methods=['GET'])
@jwt_required()
def contar_pedidos():
    try:
        result = pedido_service.contar_pedidos()
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:id>/status', methods=['PUT'])
@jwt_required()
def atualizar_status(id):
    if not verificar_perfil_admin():
        return jsonify({'error': 'Acesso negado'}), 403
    
    data = request.get_json()
    
    if not data or not data.get('status'):
        return jsonify({'error': 'Status é obrigatório'}), 400
    
    try:
        result = pedido_service.atualizar_status(id, data['status'])
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def deletar_pedido(id):
    if not verificar_perfil_admin():
        return jsonify({'error': 'Acesso negado'}), 403
    
    try:
        result = pedido_service.deletar_pedido(id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404 