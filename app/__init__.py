from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
from app.config.swagger_ui import swagger_ui_bp
import os
import time

load_dotenv()

db = SQLAlchemy()
jwt = JWTManager()

def init_db(app):
    """Inicializa o banco de dados e cria as tabelas"""
    max_tentativas = 30
    tentativa = 0
    
    while tentativa < max_tentativas:
        try:
            # Importa todos os modelos para garantir que todas as tabelas sejam criadas
            from app.models.usuario import Usuario, PerfilUsuario
            from app.models.produto import Produto
            from app.models.cliente import Cliente
            from app.models.pedido import Pedido, ItemPedido
            
            # Tenta criar as tabelas
            db.create_all()
            print("✅ Tabelas criadas com sucesso!")
            return True
        except Exception as e:
            tentativa += 1
            print(f"Tentativa {tentativa}/{max_tentativas}: Aguardando PostgreSQL... Erro: {str(e)}")
            time.sleep(1)
    
    print("❌ Não foi possível criar as tabelas após várias tentativas")
    return False

def init_admin_user(app):
    from app.models.usuario import Usuario, PerfilUsuario

    admin = Usuario.query.filter_by(email='yami@example.com').first()
    if not admin:
        admin = Usuario(
            nome='Yami',
            email='yami@example.com',
            senha=os.getenv('ADMIN_PASSWORD', 'yami123'),
            perfil=PerfilUsuario.ADMIN
        )
        db.session.add(admin)
        db.session.commit()
        print("Usuário admin criado com sucesso!")
    else:
        print("Usuário admin já existe!")
    

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'sua-chave-secreta-aqui')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres_user:postgres_password@postgres:5432/app_db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'sua-chave-jwt-aqui')
    
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    db.init_app(app)
    jwt.init_app(app)
    
    # Registra o blueprint do Swagger UI
    app.register_blueprint(swagger_ui_bp)
    
    with app.app_context():
        if not init_db(app):
            raise Exception("Falha ao inicializar o banco de dados")
        init_admin_user(app)

    from app.controllers import auth_controller, cliente_controller, produto_controller, pedido_controller
    
    app.register_blueprint(auth_controller.bp)
    app.register_blueprint(cliente_controller.bp)
    app.register_blueprint(produto_controller.bp)
    app.register_blueprint(pedido_controller.bp)
    
    return app 