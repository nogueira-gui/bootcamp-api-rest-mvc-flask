from app.repositories.produto_repository import ProdutoRepository
from app.services.s3_service import S3Service
from typing import List, Dict, Optional

class ProdutoService:
    def __init__(self):
        self.produto_repository = ProdutoRepository()
        self.s3_service = S3Service()
    
    def criar_produto(self, nome: str, descricao: str, preco: float, quantidade_estoque: int = 0, imagem_url: Optional[str] = None) -> Dict:
        produto = self.produto_repository.create(
            nome=nome,
            descricao=descricao,
            preco=preco,
            quantidade_estoque=quantidade_estoque,
            imagem_url=imagem_url
        )
        return produto.to_dict()
    
    def listar_produtos(self) -> List[Dict]:
        produtos = self.produto_repository.get_all()
        return [produto.to_dict() for produto in produtos]
    
    def obter_produto(self, id: int) -> Dict:
        produto = self.produto_repository.get_by_id(id)
        if not produto:
            raise ValueError("Produto não encontrado")
        return produto.to_dict()
    
    def buscar_por_nome(self, nome: str) -> List[Dict]:
        produtos = self.produto_repository.buscar_por_nome(nome)
        return [produto.to_dict() for produto in produtos]
    
    def contar_produtos(self) -> Dict:
        total = self.produto_repository.contar_total()
        return {'total': total}
    
    def atualizar_produto(self, id: int, **kwargs) -> Dict:
        produto = self.produto_repository.get_by_id(id)
        if not produto:
            raise ValueError("Produto não encontrado")
        
        if 'quantidade_estoque' in kwargs and kwargs['quantidade_estoque'] < 0:
            raise ValueError("Quantidade em estoque não pode ser negativa")
        
        if 'imagem_url' in kwargs and produto.imagem_url:
            try:
                self.s3_service.delete_file(produto.imagem_url)
            except ValueError:
                pass
        
        produto = self.produto_repository.update(produto, **kwargs)
        return produto.to_dict()
    
    def deletar_produto(self, id: int) -> Dict:
        produto = self.produto_repository.get_by_id(id)
        if not produto:
            raise ValueError("Produto não encontrado")
        
        if produto.imagem_url:
            try:
                self.s3_service.delete_file(produto.imagem_url)
            except ValueError:
                pass
        
        self.produto_repository.delete(produto)
        return {'message': 'Produto deletado com sucesso'}
    
    def verificar_estoque(self, produto_id: int, quantidade: int) -> bool:
        produto = self.produto_repository.get_by_id(produto_id)
        return produto and produto.quantidade_estoque >= quantidade 