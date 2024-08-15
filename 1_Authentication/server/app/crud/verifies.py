from crud.base import CRUDBase
from models.verify import Verify
from schemas.verifies import VerifyInDB, VerifyUpdateDB

CRUDVerify = CRUDBase[Verify, VerifyInDB, VerifyUpdateDB]
crud_verify = CRUDVerify(Verify)