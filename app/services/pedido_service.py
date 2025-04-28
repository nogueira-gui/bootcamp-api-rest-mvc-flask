from app.repositories.pedido_repository import PedidoRepository
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.produto_repository import ProdutoRepository
from typing import List, Dict

class PedidoService:
    def __init__(self):
        self.pedido_repository = PedidoRepository()
        self.cliente_repository = ClienteRepository()
        self.produto_repository = ProdutoRepository()
    
    def criar_pedido(self, cliente_id: int, itens: List[Dict]) -> Dict:
        if not self.cliente_repository.get_by_id(cliente_id):
            raise ValueError("Cliente não encontrado")
        
        for item in itens:
            if not self.produto_repository.verificar_estoque(item['produto_id'], item['quantidade']):
                raise ValueError(f"Produto {item['produto_id']} não disponível em estoque")
        
        pedido = self.pedido_repository.criar_pedido_com_itens(cliente_id, itens)
        return pedido.to_dict()
    
    def listar_pedidos(self) -> List[Dict]:
        pedidos = self.pedido_repository.get_all()
        return [pedido.to_dict() for pedido in pedidos]
    
    def obter_pedido(self, id: int) -> Dict:
        pedido = self.pedido_repository.get_by_id(id)
        if not pedido:
            raise ValueError("Pedido não encontrado")
        return pedido.to_dict()
    
    def buscar_por_cliente(self, cliente_id: int) -> List[Dict]:
        if not self.cliente_repository.get_by_id(cliente_id):
            raise ValueError("Cliente não encontrado")
        
        pedidos = self.pedido_repository.buscar_por_cliente(cliente_id)
        return [pedido.to_dict() for pedido in pedidos]
    
    def contar_pedidos(self) -> Dict:
        total = self.pedido_repository.contar_total()
        return {'total': total}
    
    def atualizar_status(self, id: int, status: str) -> Dict:
        pedido = self.pedido_repository.get_by_id(id)
        if not pedido:
            raise ValueError("Pedido não encontrado")
        
        pedido = self.pedido_repository.atualizar_status(id, status)
        return pedido.to_dict()
    
    def deletar_pedido(self, id: int) -> Dict:
        pedido = self.pedido_repository.get_by_id(id)
        if not pedido:
            raise ValueError("Pedido não encontrado")
        
        self.pedido_repository.delete(pedido)
        return {'message': 'Pedido deletado com sucesso'} 