from meicobaseapi.infrastructure.Roles.roles_repository import RolesRepository

class RolesService:

    def __init__(self):
        self.repo = RolesRepository()


    def get_all_roles(self):
        try:
            return self.repo.get_all()
        except Exception as e:
            raise e
    

    def get_role_by_name(self, name):
        try:
            return self.repo.get_by_name(name)
        except Exception as e:
            raise e


    def create_role(self, data):
        try:
            return self.repo.create(data)
        except Exception as e:
            raise e


    def update_role(self, usuario, auth_user, data):
        try:
            return self.repo.update(usuario.id, auth_user, data)
        except Exception as e:
            raise e


    def delete_role(self, user_id):
        try:
            return self.repo.delete(user_id)
        except Exception as e:
            raise e
    

    def get_role_by_id(self, user_id):
        try:
            return self.repo.get_by_id(user_id)
        except Exception as e:
            raise e