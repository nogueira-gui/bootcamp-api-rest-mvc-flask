from app import db
from passlib.hash import pbkdf2_sha256
from enum import Enum

class PerfilUsuario(Enum):
    ADMIN = "ADMIN"
    CLIENTE = "CLIENTE"

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)
    perfil = db.Column(db.Enum(PerfilUsuario), default=PerfilUsuario.CLIENTE)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=True)
    
    def __init__(self, nome, email, senha, perfil=PerfilUsuario.CLIENTE, cliente_id=None):
        self.nome = nome
        self.email = email
        self.set_senha(senha)
        self.perfil = perfil
        self.cliente_id = cliente_id
    
    def set_senha(self, senha):
        self.senha_hash = pbkdf2_sha256.hash(senha)
    
    def verificar_senha(self, senha):
        return pbkdf2_sha256.verify(senha, self.senha_hash)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'perfil': self.perfil.value,
            'cliente_id': self.cliente_id
        } 