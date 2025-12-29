from dataclasses import dataclass
from enum import Enum


class FieldTypeEnum(Enum):
    Dropdown = "dropdown"
    Text = "text"
    Number = "number"
    Date = "date"
    Checkbox = "checkbox"
    email = "email"


class PermissionsEnum(Enum):
    ADMIN = "admin"
    MEMBER = "member"
    GUEST = "guest"


@dataclass
class CreateFieldDTO:
    field_type: FieldTypeEnum
    field_name: str
    description: str
    template_id: str
    order: int
    config: dict
    is_required: bool
    created_by: str


@dataclass
class UpdateFieldDTO:
    field_id: str
    field_type: FieldTypeEnum
    description: str
    template_id: str
    field_type: FieldTypeEnum
    field_name: str
    description: str
    template_id: str
    order: int
    config: dict
    is_required: bool
    created_by: str


@dataclass
class FieldDTO:
    field_id: str
    field_type: FieldTypeEnum
    description: str
    template_id: str
    field_name: str
    order: int
    config: dict
    is_required: bool
    created_by: str