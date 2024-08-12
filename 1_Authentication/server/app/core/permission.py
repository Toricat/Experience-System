# from enum import Enum
# from typing import Optional

# class UserRole(Enum):
#     USER = "user"
#     MANAGER = "manager"
#     ADMIN = "admin"

# class Permission:
#     def __init__(self, role: UserRole):
#         self.role = role

#     def can_read_item(self, item_user_id: int, current_user_id: int) -> bool:
#         if self.role == UserRole.ADMIN:
#             return True  
#         elif self.role == UserRole.MANAGER:
#             return True  
#         elif self.role == UserRole.USER:
#             return item_user_id == current_user_id  
#         return False

#     def can_read_user(self, user_id: int, current_user_id: int) -> bool:
#         if self.role == UserRole.ADMIN:
#             return True 
#         elif self.role == UserRole.MANAGER:
#             return False  # Managers cannot read user details
#         elif self.role == UserRole.USER:
#             return user_id == current_user_id  # Users can only read their own details
#         return False
from typing import List

class Permission:
    def __init__(self, name: str):
        self.name = name


create = Permission("create")
read_own = Permission("read_own")
read_all = Permission("read_all")
update_own = Permission("update_own")
update_all = Permission("update_all")
delete_own = Permission("delete_own")
delete_all = Permission("delete_all")

class Role:
    def __init__(self, name: str, permissions: List[Permission]):
        self.name = name
        self.permissions = permissions

    def has_permission(self, permission: Permission) -> bool:
        return permission in self.permissions
    
user_role = Role(
    name="user",
    permissions=[read_own, update_own, create]
)

manager_role = Role(
    name="manager",
    permissions=[create,read_own, read_all, update_own, update_all]
)

admin_role = Role(
    name="admin",
    permissions=[create,read_own, read_all, update_own, update_all, delete_own, delete_all]
)


