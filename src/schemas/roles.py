from enum import Enum

class RoleEnum(str, Enum):
    USER = "user"
    ADVANCED = "moderator"
    ADMIN = "admin"