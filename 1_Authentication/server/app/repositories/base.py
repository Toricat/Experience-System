from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, delete, select, func, asc, desc,or_, and_
from sqlalchemy.orm import joinedload, selectinload,aliased
from typing import Callable, Type, Generic, TypeVar, List, Any, Dict, Optional, Tuple
import operator
from pydantic import BaseModel


Entity = TypeVar("Entity")
ModelSchemaType = TypeVar('ModelSchemaType',bound=BaseModel) 

class BaseRepository(Generic[Entity, ModelSchemaType]):
    def __init__(self,  entity_type: Type[Entity], schema_type: Type[ModelSchemaType])-> None:
        self.entity_type = entity_type
        self.schema_type = schema_type

    async def get(self, session: AsyncSession, filters: Optional[Dict[str, Any]] = None,
                    columns: Optional[List[str]] = None, order_by: Optional[List[str]] = None,
                    joins: Optional[List[Tuple[str, str]]] = None) -> Optional[ModelSchemaType]:
            if columns:
                query = select(*[getattr(self.entity_type, col) for col in columns if hasattr(self.entity_type, col)])
            else:
                query = select(self.entity_type)

            # Handle joins
            if joins:
                for join_type, onclause in joins:
                    attribute = getattr(self.entity_type, onclause)
                    if join_type.lower() == 'joined':
                        query = query.options(joinedload(attribute))
                    elif join_type.lower() == 'select':
                        query = query.options(selectinload(attribute))

            # Apply filters
            if filters:
                for key, value in (filters or {}).items():
                    field, op = self._parse_field_operator(key)
                    query = query.where(op(getattr(self.entity_type, field), value))

            # Apply order by
            if order_by:
                for order in order_by:
                    desc_indicator = '-' if order.startswith('-') else ''
                    field_clean = order.lstrip('-+')
                    column = getattr(self.entity_type, field_clean)
                    query = query.order_by(desc(column) if desc_indicator else asc(column))
                    
            # Execute the query
            result = await session.execute(query)
            # Execute query and return result
            if columns:
                # Return a dictionary and convert to model instance if needed
                entity_data = result.mappings().first()
                return self.schema_type(**entity_data) if entity_data else None
            else:
                # Return the entity directly
                return result.scalars().first()
    async def get_all(self,session: AsyncSession, filters: Optional[Dict[str, Any]] = None,
                      columns: Optional[List[str]] = None,
                      order_by: Optional[List[str]] = None,
                      group_by: Optional[List[str]] = None,
                      having: Optional[Dict[str, Any]] = None,
                      joins: Optional[List[Tuple[str, str]]] = None,
                      limit: Optional[int] = None,
                      offset: Optional[int] = None) -> List[ModelSchemaType]:
        if columns:
                entity_alias = aliased(self.entity_type)
                attributes = [getattr(entity_alias, col) for col in columns]
                query = select(*attributes)
        else:
            query = select(self.entity_type)
        if joins:
            for join_type, onclause in joins:
                attribute = getattr(self.entity_type, onclause)
                if join_type.lower() == 'joined':
                    query = query.options(joinedload(attribute))
                elif join_type.lower() == 'select':
                    query = query.options(selectinload(attribute))

        if filters:
            for key, value in (filters or {}).items():
                field, op = self._parse_field_operator(key)
                query = query.where(op(getattr(self.entity_type, field), value))

        if group_by:
            query = query.group_by(*[getattr(self.entity_type, gb) for gb in group_by])

        if having:
            for condition, value in having.items():
                query = query.having(func.count(getattr(self.entity_type, condition)) > value)

        if order_by:
            for field in order_by:
                desc_indicator = '-' if field.startswith('-') else ''
                field_clean = field.lstrip('-+')
                query = query.order_by(desc(getattr(self.entity_type, field_clean)) if desc_indicator else asc(getattr(self.entity_type, field_clean)))
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        result = await session.execute(query)
        entity  = result.scalars().all()
        return [self.schema_type.model_validate(entity) for entity in entity ]

    async def create(self,session: AsyncSession,data: Dict[str, Any]) -> Optional[ModelSchemaType]:
        entity = self.entity_type(**data)
        session.add(entity)
        await session.commit()
        await session.refresh(entity)
        return  entity 

    async def update(self,session: AsyncSession, filters: Dict[str, Any], data: Dict[str, Any]) -> Optional[ModelSchemaType]:
        query = update(self.entity_type).where(*[getattr(self.entity_type, key) == value for key, value in filters.items()]).values(**data)
        # .returning(self.entity_type)
        await session.execute(query)
        # result.fetchone()
        await session.commit()
        return None

    async def delete(self,session: AsyncSession, filters: Dict[str, Any]) -> Optional[ModelSchemaType]:
        query = delete(self.entity_type).where(*[getattr(self.entity_type, key) == value for key, value in filters.items()])
        await session.execute(query)
        await session.commit()
        return None

    def _parse_field_operator(self, key: str) -> Tuple[str, Callable]:
        if '__' in key:
            field, op_name = key.split('__', 1)
            op = {
                'eq': operator.eq,
                'ne': operator.ne,
                'lt': operator.lt,
                'gt': operator.gt,
                'le': operator.le,
                'ge': operator.ge,
                
            }.get(op_name, operator.eq)
            return field, op
        return key, operator.eq
