from app.repositories.base_repository import BaseRepository
from app.models.pedido import Pedido, ItemPedido
from app.models.produto import Produto
from app import db
from typing import List, Dict

class PedidoRepository(BaseRepository):
    def __init__(self):
        super().__init__(Pedido)
    
    def criar_pedido_com_itens(self, cliente_id: int, itens: List[Dict]) -> Pedido:
        pedido = self.create(cliente_id=cliente_id)
        
        for item in itens:
            produto = Produto.query.get(item['produto_id'])
            if not produto or produto.quantidade_estoque < item['quantidade']:
                raise ValueError(f"Produto {item['produto_id']} não disponível em estoque")
            
            item_pedido = ItemPedido(
                pedido=pedido,
                produto_id=produto.id,
                quantidade=item['quantidade'],
                preco_unitario=produto.preco
            )
            
            produto.quantidade_estoque -= item['quantidade']
            db.session.add(item_pedido)
        
        pedido.calcular_total()
        db.session.commit()
        return pedido
    
    def buscar_por_cliente(self, cliente_id: int) -> List[Pedido]:
        return self.filter_by(cliente_id=cliente_id)
    
    def contar_total(self) -> int:
        return self.model_class.query.count()
    
    def atualizar_status(self, pedido_id: int, status: str) -> Pedido:
        pedido = self.get_by_id(pedido_id)
        if pedido:
            pedido.status = status
            db.session.commit()
        return pedido
    
    def delete(self, pedido: Pedido) -> None:
        for item in pedido.itens:
            db.session.delete(item)
        
        db.session.delete(pedido)
        db.session.commit() 