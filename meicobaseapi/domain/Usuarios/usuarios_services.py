from meicobaseapi.infrastructure.Usuarios.usuarios_repository import UsuariosRepository

class UsuariosService:
    def __init__(self):
        self.repo = UsuariosRepository()

    def get_all_users(self):
        try:
            return self.repo.get_all()
        except Exception as e:
            return e
    
    def get_user_by_email(self, email):
        try:
            return self.repo.get_by_email(email)
        except Exception as e:
            return e

    def create_user(self, data):
        try:
            return self.repo.create(data)
        except Exception as e:
            return e

    def update_user(self, usuario, auth_user, data):
        try:
            return self.repo.update(usuario.id, auth_user, data)
        except Exception as e:
            return e

    def delete_user(self, user_id):
        try:
            return self.repo.delete(user_id)
        except Exception as e:
            return e
    
    def get_user_by_id(self, user_id):
        try:
            return self.repo.get_by_id(user_id)
        except Exception as e:
            raise e