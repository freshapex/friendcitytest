from sqlalchemy.ext.declarative import declarative_base,as_declarative,declared_attr

from typing import Any

Base = declarative_base()

# @as_declarative()
# class Base:
#     id:Any
#     __name__:str

#     @declared_attr
#     def __tablename__(cls) -> str:
#         return cls.__name__.lower()
         