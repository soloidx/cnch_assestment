from sqlalchemy import Column, String, Integer

from sqlalchemy.orm import relationship

from project.models.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    image = Column(String)
