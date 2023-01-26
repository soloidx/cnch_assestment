from typing import Generic, TypeVar, Type, Any, Optional, List, Union, Dict

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from project.models import Base

# sqlalchemy model
ModelType = TypeVar("ModelType", bound=Base)
# pydantic create schemas
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(
    Generic[ModelType, CreateSchemaType, UpdateSchemaType]
):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(
        self, db: Session, model_id: Optional[Any], filter_expressions: Optional[List] = None
    ) -> Optional[ModelType]:
        filter_expressions = filter_expressions if filter_expressions is not None else []
        query = db.query(self.model)
        if model_id:
            query = query.filter(self.model.id == model_id)
        for f in filter_expressions:
            query = query.filter(f)
        return query.first()

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        filter_expressions: Optional[List] = None
    ) -> List[ModelType]:
        filter_expressions = filter_expressions if filter_expressions is not None else []
        query = db.query(self.model)
        for f in filter_expressions:
            query = query.filter(f)
        # from sqlalchemy.dialects import sqlite
        # print(str(query.statement.compile(dialect=sqlite.dialect(), compile_kwargs={"literal_binds": True})))
        return query.offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(
        self, db: Session, *, _id: Optional[int], filter_expressions: Optional[List] = None
    ) -> Optional[ModelType]:
        filter_expressions = filter_expressions if filter_expressions is not None else []
        obj = None
        query = db.query(self.model)
        if _id is not None:
            obj = query.get(_id)

        if _id is None and len(filter_expressions) > 0:
            for f in filter_expressions:
                query = query.filter(f)
                obj = query.first()

        if obj is None:
            return
        db.delete(obj)
        db.commit()
        return obj
