from app.repositories.cliente_repository import ClienteRepository
from typing import List, Dict, Optional

class ClienteService:
    def __init__(self):
        self.cliente_repository = ClienteRepository()
    
    def criar_cliente(self, nome: str, email: str, telefone: Optional[str] = None, endereco: Optional[str] = None, usuario_id: int = None) -> Dict:
        if self.cliente_repository.first(usuario_id=usuario_id):
            raise ValueError("Cliente já cadastrado")
            
        if self.cliente_repository.first(email=email):
            raise ValueError("Email já cadastrado")
        
        cliente = self.cliente_repository.create(
            nome=nome,
            email=email,
            telefone=telefone,
            endereco=endereco,
            usuario_id=usuario_id
        )
        
        return cliente.to_dict()
    
    def listar_clientes(self) -> List[Dict]:
        clientes = self.cliente_repository.get_all()
        return [cliente.to_dict() for cliente in clientes]
    
    def obter_cliente(self, id: int) -> Dict:
        cliente = self.cliente_repository.get_by_id(id)
        if not cliente:
            raise ValueError("Cliente não encontrado")
        return cliente.to_dict()
    
    def buscar_por_nome(self, nome: str) -> List[Dict]:
        clientes = self.cliente_repository.buscar_por_nome(nome)
        return [cliente.to_dict() for cliente in clientes]
    
    def contar_clientes(self) -> Dict:
        total = self.cliente_repository.contar_total()
        return {'total': total}
    
    def atualizar_cliente(self, id: int, **kwargs) -> Dict:
        cliente = self.cliente_repository.get_by_id(id)
        if not cliente:
            raise ValueError("Cliente não encontrado")
        
        if 'email' in kwargs and kwargs['email'] != cliente.email:
            if self.cliente_repository.first(email=kwargs['email']):
                raise ValueError("Email já cadastrado")
        
        cliente = self.cliente_repository.update(cliente, **kwargs)
        return cliente.to_dict()
    
    def deletar_cliente(self, id: int) -> Dict:
        cliente = self.cliente_repository.get_by_id(id)
        if not cliente:
            raise ValueError("Cliente não encontrado")
        
        self.cliente_repository.delete(cliente)
        return {'message': 'Cliente deletado com sucesso'} 