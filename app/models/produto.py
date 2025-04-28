from app import db
from datetime import datetime
from sqlalchemy import CheckConstraint

class Produto(db.Model):
    __tablename__ = 'produtos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    preco = db.Column(db.Float, nullable=False)
    quantidade_estoque = db.Column(db.Integer, default=0)
    imagem_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    __table_args__ = (
        CheckConstraint('quantidade_estoque >= 0', name='check_quantidade_estoque_nao_negativa'),
    )
    
    def __init__(self, nome, descricao, preco, quantidade_estoque=0, imagem_url=None):
        if quantidade_estoque < 0:
            raise ValueError("Quantidade em estoque não pode ser negativa")
            
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.quantidade_estoque = quantidade_estoque
        self.imagem_url = imagem_url
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'preco': self.preco,
            'quantidade_estoque': self.quantidade_estoque,
            'imagem_url': self.imagem_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 