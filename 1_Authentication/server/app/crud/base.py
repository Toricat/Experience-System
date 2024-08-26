from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel
from sqlalchemy import select, update , delete 
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]) -> None:
        self._model = model

    async def create(
        self, session: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
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

    # async def update(
    #     self,
    #     session: AsyncSession,
    #     *,
    #     obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    #     db_obj: Optional[ModelType] = None,
    #     **kwargs
    # ) -> Optional[ModelType]:
    #     db_obj = db_obj or await self.get(session, **kwargs)
    #     if db_obj is not None:
    #         obj_data = db_obj.dict()
    #         if isinstance(obj_in, dict):
    #             update_data = obj_in
    #         else:
    #             update_data = obj_in.dict(exclude_unset=True)
    #         for field in obj_data:
    #             if field in update_data:
    #                 setattr(db_obj, field, update_data[field])
    #         session.add(db_obj)
    #         await session.commit()
    #         await session.refresh(db_obj)  
    #     return db_obj
    async def update(
        self,
        session: AsyncSession,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
        *args,
        **kwargs
    ) -> Optional[ModelType]:

        update_data = obj_in if isinstance(obj_in, dict) else obj_in.dict(exclude_unset=True, exclude_none=True)
        result = await session.execute(
            update(self._model)
            .filter(*args)
            .filter_by(**kwargs)
            .values(**update_data))
        await session.commit()

        return await self.get(session, *args, **kwargs)

    async def delete(
        self, session: AsyncSession, *args, db_obj: Optional[ModelType] = None, **kwargs
    ) -> ModelType:
        db_obj = db_obj or await self.get(session, *args, **kwargs)
        await session.delete(db_obj)
        await session.commit()
        return db_obj
