from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.auth_service import AuthService

bp = Blueprint('auth', __name__, url_prefix='/auth')
auth_service = AuthService()

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('senha'):
        return jsonify({'error': 'Email e senha são obrigatórios'}), 400
    
    try:
        result = auth_service.registrar_usuario(
            nome=data.get('nome', ''),
            email=data['email'],
            senha=data['senha']
        )
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('senha'):
        return jsonify({'error': 'Email e senha são obrigatórios'}), 400
    
    try:
        result = auth_service.autenticar_usuario(
            email=data['email'],
            senha=data['senha']
        )
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

@bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user = get_jwt_identity()
    
    try:
        result = auth_service.get_usuario_atual(current_user['id'])
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404 