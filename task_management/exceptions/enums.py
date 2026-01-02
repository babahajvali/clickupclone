from enum import Enum

class FieldTypeEnum(Enum):
    Dropdown = "dropdown"
    User = "user"
    Text = "text"
    Number = "number"
    Date = "date"
    Checkbox = "checkbox"
    email = "email"


class RoleEnum(Enum):
    OWNER = "owner"
    Admin = "admin"
    MEMBER = "member"
    GUEST = "guest"

class PermissionsEnum(Enum):
    FULL_EDIT = "full_edit"
    COMMENT = "comment"
    VIEW = "view"

class ViewTypeEnum(Enum):
    Table = "table"
    Calendar = "calendar"
    Board = "board"
    Dashboard = "dashboard"


class PermissionScopeTypeEnum(Enum):
    WORKSPACE = "workspace"
    SPACE ="space"
    FOLDER ="folder"
    LIST ="list"


class GenderEnum(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
