from flask_jwt_extended import create_access_token
from app.repositories.usuario_repository import UsuarioRepository
from app.models.usuario import PerfilUsuario

class AuthService:
    def __init__(self):
        self.usuario_repository = UsuarioRepository()
    
    def registrar_usuario(self, nome: str, email: str, senha: str) -> dict:
        if self.usuario_repository.get_by_email(email):
            raise ValueError("Email já cadastrado")
        
        usuario = self.usuario_repository.create(
            nome=nome,
            email=email,
            senha=senha,
            perfil=PerfilUsuario.CLIENTE
        )
        
        return {
            'message': 'Usuário registrado com sucesso',
            'usuario': usuario.to_dict()
        }
    
    def autenticar_usuario(self, email: str, senha: str) -> dict:
        if not self.usuario_repository.verificar_senha(email, senha):
            raise ValueError("Credenciais inválidas")
        
        usuario = self.usuario_repository.get_by_email(email)
        access_token = create_access_token(identity={
            'id': usuario.id,
            'email': usuario.email,
            'perfil': usuario.perfil.value
        })
        
        return {
            'access_token': access_token,
            'usuario': usuario.to_dict()
        }
    
    def get_usuario_atual(self, usuario_id: int) -> dict:
        usuario = self.usuario_repository.get_by_id(usuario_id)
        if not usuario:
            raise ValueError("Usuário não encontrado")
        return usuario.to_dict() 