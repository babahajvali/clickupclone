from enum import Enum

class FieldTypeEnum(Enum):
    Dropdown = "dropdown"
    User = "user"
    Text = "text"
    Number = "number"
    Date = "date"
    Checkbox = "checkbox"
    email = "email"


class PermissionsEnum(Enum):
    ADMIN = "admin"
    MEMBER = "member"
    GUEST = "guest"

class ViewTypeEnum(Enum):
    Table = "table"
    Calendar = "calendar"
    Board = "board"
    Dashboard = "dashboard"
