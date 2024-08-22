from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel
from sqlalchemy import select, update as sqlalchemy_update, delete as sqlalchemy_delete
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]) -> None:
        self._model = model

    async def create(
        self, session: AsyncSession, obj_in: CreateSchemaType
    ) -> ModelType:
        obj_in_data = dict(obj_in)
        db_obj = self._model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        return db_obj

    async def get(self, session: AsyncSession, *args, **kwargs) -> Optional[ModelType]:
        result = await session.execute(
            select(self._model)
            .filter(*args)
            .filter_by(**kwargs)
        )
        return result.scalars().first()

    async def get_multi(
        self, session: AsyncSession, *args, offset: int = 0, limit: int = 100, **kwargs
    ) -> List[ModelType]:
        result = await session.execute(
            select(self._model)
            .filter(*args)
            .filter_by(**kwargs)
            .offset(offset)
            .limit(limit)
        )
        return result.scalars().all()

    async def update(
        self,
        session: AsyncSession,
        *args: Any,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
        **kwargs: Any
    ) -> Optional[ModelType]:
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.dict(exclude_unset=True)
        
        result = await session.execute( 
            sqlalchemy_update(self._model)
            .where(*args, **kwargs)
            .values(**update_data)
            .returning(self._model))
        await session.commit()

        return result.scalars().first()

    async def delete(
        self, session: AsyncSession, *args: Any, **kwargs: Any
    ) -> Optional[ModelType]:
  
        result = await session.execute( 
            sqlalchemy_delete(self._model)
            .where(*args, **kwargs)
            .returning(self._model))
        
        await session.commit()
        return result.scalars().first()
