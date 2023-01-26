from sqlalchemy.orm import Session

from project.crud.base import CRUDBase
from project.models import user as user_model
from project.schema import User, CreateUser, UpdateUser


class CRUDUser(CRUDBase[User, CreateUser, UpdateUser]):
    def is_duplicated_email(self, db: Session, user: User):
        count = db.query(self.model).filter(user_model.User.email == user.email).count()
        return count > 0


user = CRUDUser(user_model.User)
