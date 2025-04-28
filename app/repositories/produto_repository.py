from app.repositories.base_repository import BaseRepository
from app.models.produto import Produto
from sqlalchemy import or_

class ProdutoRepository(BaseRepository):
    def __init__(self):
        super().__init__(Produto)
    
    def buscar_por_nome(self, nome: str) -> list[Produto]:
        return self.model_class.query.filter(
            or_(
                Produto.nome.ilike(f'%{nome}%'),
                Produto.descricao.ilike(f'%{nome}%')
            )
        ).all()
    
    def contar_total(self) -> int:
        return self.model_class.query.count()
    
    def verificar_estoque(self, produto_id: int, quantidade: int) -> bool:
        produto = self.get_by_id(produto_id)
        return produto and produto.quantidade_estoque >= quantidade 