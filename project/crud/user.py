from project.crud.base import CRUDBase
from project.models import user as user_model
from project.schema import User, CreateUser, UpdateUser


class CRUDUser(CRUDBase[User, CreateUser, UpdateUser]):
    pass


user = CRUDUser(user_model.User)
