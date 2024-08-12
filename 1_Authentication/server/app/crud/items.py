from crud.base import CRUDBase
from models.items import Item
from schemas.items import  ItemInDB, ItemUpdate

CRUDItem = CRUDBase[Item, ItemInDB, ItemUpdate]
crud_item = CRUDItem(Item)