from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.cliente_service import ClienteService
from app.models.usuario import PerfilUsuario

bp = Blueprint('clientes', __name__, url_prefix='/clientes')
cliente_service = ClienteService()

def verificar_perfil_admin():
    current_user = get_jwt_identity()
    return current_user['perfil'] == PerfilUsuario.ADMIN.value

def recuperar_usuario():
    current_user = get_jwt_identity()
    return current_user  

@bp.route('', methods=['POST'])
@jwt_required()
def criar_cliente():
    data = request.get_json()

    if not data or not data.get('nome') or not data.get('email'):
        return jsonify({'error': 'Nome e email são obrigatórios'}), 400

    usuario_logado = recuperar_usuario()
    
    if not usuario_logado or not usuario_logado.get('id'):
        return jsonify({'error': 'Usuário não identificado'}), 401

    if not usuario_logado.get('perfil') == PerfilUsuario.CLIENTE.value:
        return jsonify({'error': 'Apenas clientes podem se cadastrar como cliente'}), 403

    try:
        result = cliente_service.criar_cliente(
            nome=data['nome'],
            email=data['email'],
            telefone=data.get('telefone'),
            endereco=data.get('endereco'),
            usuario_id=usuario_logado.get('id')
        )
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@bp.route('', methods=['GET'])
@jwt_required()
def listar_clientes():
    try:
        result = cliente_service.listar_clientes()
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def obter_cliente(id):
    try:
        result = cliente_service.obter_cliente(id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@bp.route('/nome/<string:nome>', methods=['GET'])
@jwt_required()
def buscar_por_nome(nome):
    try:
        result = cliente_service.buscar_por_nome(nome)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/contar', methods=['GET'])
@jwt_required()
def contar_clientes():
    try:
        result = cliente_service.contar_clientes()
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_cliente(id):
    data = request.get_json()
    
    try:
        result = cliente_service.atualizar_cliente(id, **data)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def deletar_cliente(id):
    if not verificar_perfil_admin():
        return jsonify({'error': 'Acesso negado'}), 403
    
    try:
        cliente_service.deletar_cliente(id)
        return '', 204
    except ValueError as e:
        return jsonify({'error': str(e)}), 404 