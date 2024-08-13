from typing import Any, Dict

from sqlalchemy import inspect, MetaData
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
           return cls.__name__.lower()
    metadata = MetaData()
    def dict(self) -> Dict[str, Any]:
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}