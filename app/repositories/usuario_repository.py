from app.repositories.base_repository import BaseRepository
from app.models.usuario import Usuario

class UsuarioRepository(BaseRepository):
    def __init__(self):
        super().__init__(Usuario)
    
    def get_by_email(self, email: str) -> Usuario:
        return self.first(email=email)
    
    def verificar_senha(self, email: str, senha: str) -> bool:
        usuario = self.get_by_email(email)
        if usuario:
            return usuario.verificar_senha(senha)
        return False 