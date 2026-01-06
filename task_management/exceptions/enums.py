from enum import Enum

class FieldType(Enum):
    DROPDOWN = "dropdown"
    USER = "user"
    TEXT = "text"
    NUMBER = "number"
    DATE = "date"
    CHECKBOX = "checkbox"
    EMAIL = "email"


class Role(Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    GUEST = "guest"

class PermissionsEnum(Enum):
    FULL_EDIT = "full_edit"
    COMMENT = "comment"
    VIEW = "view"

class ViewTypeEnum(Enum):
    TABLE = "table"
    CALENDER = "calendar"
    BOARD = "board"
    DASHBOARD = "dashboard"

class Visibility(Enum):
    PUBLIC = "public"
    PRIVATE = "private"

class PermissionScopeTypeEnum(Enum):
    WORKSPACE = "workspace"
    SPACE ="space"
    FOLDER ="folder"
    LIST ="list"


class GenderEnum(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
