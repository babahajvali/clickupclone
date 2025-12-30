from dataclasses import dataclass
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


@dataclass
class CreateTemplateDTO:
    name: str
    description: str
    list_id: str
    is_default: bool
    created_by: str


@dataclass
class UpdateTemplateDTO:
    template_id: str
    name: str
    list_id: str
    description: str
    is_default: bool
    created_by: str

@dataclass
class TemplateDTO:
    template_id: str
    name: str
    list_id: str
    description: str
    is_default: bool
    created_by: str


DEFAULT_FIELDS = [
            {
                "field_type": FieldTypeEnum.Text,
                "field_name": "Title",
                "description": "Task title",
                "order": 1,
                "config": {"max_length": 255},
                "is_required": True
            },
            {
                "field_type": FieldTypeEnum.User,
                "field_name": "Assignee",
                "order": 2
            },
            {
                "field_type": FieldTypeEnum.Date,
                "field_name": "Due Date",
                "order": 3
            },
            {
                "field_type": FieldTypeEnum.Dropdown,
                "field_name": "Priority",
                "order": 4,
                "config": {
                    "options": ["Low", "Medium", "High"]
                }
            },
            {
                "field_type": FieldTypeEnum.Dropdown,
                "field_name": "Status",
                "order": 5,
                "config": {
                    "options": ["Todo", "In Progress", "Done"],
                    "default": "Todo"
                }
            }
        ]


@dataclass
class CreateTaskDTO:
    title: str
    description: str
    list_id: str
    created_by: str
    is_active: bool


@dataclass
class UpdateTaskDTO:
    task_id: str
    title: str
    description: str
    list_id: str
    created_by: str
    is_active: bool

@dataclass
class TaskDTO:
    task_id: str
    title: str
    description: str
    list_id: str
    created_by: str
    is_active: bool

@dataclass
class TaskAssigneeDTO:
    assignee_id: str
    assignee_name: str
    task_id: str
    assigned_by: str
    is_active: bool

@dataclass
class RemoveTaskAssigneeDTO:
    task_id: str
    assignee_id: str
    removed_by: str
    is_active: bool
