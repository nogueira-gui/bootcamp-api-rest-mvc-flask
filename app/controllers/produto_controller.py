from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.produto_service import ProdutoService
from app.services.s3_service import S3Service
from app.models.usuario import PerfilUsuario
import os
from botocore.exceptions import ClientError

bp = Blueprint('produtos', __name__, url_prefix='/produtos')
produto_service = ProdutoService()
s3_service = S3Service()

def verificar_perfil_admin():
    current_user = get_jwt_identity()
    return current_user['perfil'] == PerfilUsuario.ADMIN.value

@bp.route('', methods=['POST'])
@jwt_required()
def criar_produto():
    if not verificar_perfil_admin():
        return jsonify({'error': 'Acesso negado'}), 403
    
    imagem_url = None
    if 'imagem' in request.files:
        try:
            imagem_url = s3_service.upload_imagem(request.files['imagem'])
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
    
    data = request.form.to_dict()
    
    if not data or not data.get('nome') or not data.get('preco'):
        return jsonify({'error': 'Nome e preço são obrigatórios'}), 400
    
    try:
        result = produto_service.criar_produto(
            nome=data['nome'],
            descricao=data.get('descricao', ''),
            preco=float(data['preco']),
            quantidade_estoque=int(data.get('quantidade_estoque', 0)),
            imagem_url=imagem_url
        )
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@bp.route('', methods=['GET'])
@jwt_required()
def listar_produtos():
    try:
        result = produto_service.listar_produtos()
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def obter_produto(id):
    try:
        result = produto_service.obter_produto(id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@bp.route('/nome/<string:nome>', methods=['GET'])
@jwt_required()
def buscar_por_nome(nome):
    try:
        result = produto_service.buscar_por_nome(nome)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/contar', methods=['GET'])
@jwt_required()
def contar_produtos():
    try:
        result = produto_service.contar_produtos()
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_produto(id):
    if not verificar_perfil_admin():
        return jsonify({'error': 'Acesso negado'}), 403
    
    imagem_url = None
    if 'imagem' in request.files:
        try:
            print(f"Recebendo nova imagem: {request.files['imagem']}")  # Log para debug
            imagem_url = s3_service.upload_imagem(request.files['imagem'])
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
    
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()
    
    try:
        if imagem_url:
            data['imagem_url'] = imagem_url
        
        if 'preco' in data:
            data['preco'] = float(data['preco'])
        if 'quantidade_estoque' in data:
            data['quantidade_estoque'] = int(data['quantidade_estoque'])
        
        result = produto_service.atualizar_produto(id, **data)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def deletar_produto(id):
    if not verificar_perfil_admin():
        return jsonify({'error': 'Acesso negado'}), 403
    
    try:
        result = produto_service.deletar_produto(id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    
@bp.route('/imagem/<string:filename>', methods=['GET'])
@jwt_required()
def buscar_imagem(filename):
    try:
        print(f"Tentando buscar imagem: {filename}")  # Log para debug
        
        if not filename:
            return jsonify({'error': 'Nome do arquivo não fornecido'}), 400
            
        try:
            s3_service.s3_client.head_object(
                Bucket=s3_service.bucket_name,
                Key=filename
            )
        except ClientError as e:
            print(f"Erro ao verificar arquivo no S3: {str(e)}")  # Log para debug
            return jsonify({'error': f'Arquivo não encontrado: {filename}'}), 404
            
        temp_path = s3_service.download_imagem(filename)
        
        ext = filename.split('.')[-1].lower()
        mime_type = f'image/{ext}'
        
        with open(temp_path, 'rb') as f:
            content = f.read()
        
        os.remove(temp_path)
        
        return content, 200, {'Content-Type': mime_type}
    except ValueError as e:
        print(f"Erro ao processar imagem: {str(e)}")  # Log para debug
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")  # Log para debug
        return jsonify({'error': f'Erro ao processar imagem: {str(e)}'}), 500
