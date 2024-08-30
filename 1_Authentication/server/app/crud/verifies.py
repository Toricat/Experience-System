from crud.base import CRUDBase
from models.verify import Verify
from schemas.verifies import VerifyInDB, VerifyUpdate

CRUDVerify = CRUDBase[Verify, VerifyInDB, VerifyUpdate]
crud_verify = CRUDVerify(Verify)

