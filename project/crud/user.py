from typing import Optional, List
from sqlalchemy import or_
from sqlalchemy.orm import Session

from project.crud.base import CRUDBase
from project.models import user as user_model
from project.schema import User, CreateUser, UpdateUser


class CRUDUser(CRUDBase[User, CreateUser, UpdateUser]):
    def search(self, db: Session, search_string: Optional[str]) -> List[User]:
        exp = []
        if search_string is not None:
            query_terms = list(filter(lambda x: x != "", [x for x in search_string.split(" ")]))
            # TODO: Improve the search based on a search engine or a search field
            search_fields = [
                user_model.User.name,
                user_model.User.email,
                user_model.User.address
            ]

            exp = [a.like(f"%{b}%") for a in search_fields for b in query_terms]
            exp = [or_(*exp)]
        return self.get_multi(db, filter_expressions=exp)

    def is_duplicated_email(self, db: Session, _user: User):
        count = db.query(self.model).filter(user_model.User.email == _user.email).count()
        return count > 0


user = CRUDUser(user_model.User)
