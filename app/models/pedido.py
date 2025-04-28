from app import db
from datetime import datetime

class ItemPedido(db.Model):
    __tablename__ = 'itens_pedido'
    
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)
    
    produto = db.relationship('Produto')
    
    def to_dict(self):
        return {
            'id': self.id,
            'produto_id': self.produto_id,
            'quantidade': self.quantidade,
            'preco_unitario': self.preco_unitario,
            'subtotal': self.quantidade * self.preco_unitario
        }

class Pedido(db.Model):
    __tablename__ = 'pedidos'
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    data_pedido = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='PENDENTE')
    total = db.Column(db.Float, default=0.0)
    
    cliente = db.relationship('Cliente')
    itens = db.relationship('ItemPedido', backref='pedido', lazy=True)
    
    def __init__(self, cliente_id):
        self.cliente_id = cliente_id
    
    def calcular_total(self):
        self.total = sum(item.quantidade * item.preco_unitario for item in self.itens)
    
    def to_dict(self):
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'data_pedido': self.data_pedido.isoformat(),
            'status': self.status,
            'total': self.total,
            'itens': [item.to_dict() for item in self.itens]
        } 