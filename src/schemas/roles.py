from enum import Enum

class RoleEnum(str, Enum):
    USER = "user"
    ADVANCED = "advanced"
    ADMIN = "admin"