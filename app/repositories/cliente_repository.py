from app.repositories.base_repository import BaseRepository
from app.models.cliente import Cliente
from sqlalchemy import or_

class ClienteRepository(BaseRepository):
    def __init__(self):
        super().__init__(Cliente)
    
    def buscar_por_nome(self, nome: str) -> list[Cliente]:
        return self.model_class.query.filter(
            or_(
                Cliente.nome.ilike(f'%{nome}%'),
                Cliente.email.ilike(f'%{nome}%')
            )
        ).all()
    
    def contar_total(self) -> int:
        return self.model_class.query.count() 