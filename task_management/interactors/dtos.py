from dataclasses import dataclass

from typing import Optional

from task_management.exceptions.enums import ViewTypeEnum, FieldTypeEnum, \
    GenderEnum, RoleEnum, PermissionsEnum


@dataclass
class UserDTO:
    user_id: str
    full_name: str
    username: str
    gender: str
    email: str
    password: str
    phone_number: str
    is_active: bool
    image_url: str


@dataclass
class CreateUserDTO:
    username: str
    full_name: str
    email: str
    password: str
    phone_number: str
    gender: GenderEnum
    image_url: str

@dataclass
class AccountDTO:
    id: int
    user_id: str
    username: str
    is_active: bool


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


@dataclass
class UserTasksDTO:
    user_id: str
    tasks: list[TaskDTO]


@dataclass
class CreateListDTO:
    name: str
    description: str
    space_id: str
    order: int
    is_active: bool
    created_by: str
    is_private: bool
    folder_id: Optional[str] = None


@dataclass
class UpdateListDTO:
    list_id: str
    name: str
    description: str
    space_id: str
    is_active: bool
    order: int
    is_private: bool
    created_by: str
    folder_id: Optional[str] = None


@dataclass
class ListDTO:
    list_id: str
    name: str
    description: str
    space_id: str
    is_active: bool
    order: int
    is_private: bool
    created_by: str
    folder_id: Optional[str] = None


@dataclass
class CreateViewDTO:
    name: str
    description: str
    view_type: ViewTypeEnum
    created_by: str


@dataclass
class UpdateViewDTO:
    view_id: str
    name: str
    description: str
    view_type: ViewTypeEnum
    created_by: str


@dataclass
class ViewDTO:
    view_id: str
    name: str
    description: str
    view_type: ViewTypeEnum
    created_by: str


@dataclass
class CreateFolderDTO:
    name: str
    description: str
    space_id: str
    order: int
    is_active: bool
    created_by: str
    is_private: bool


@dataclass
class UpdateFolderDTO:
    folder_id: str
    name: str
    description: str
    space_id: str
    order: int
    is_active: bool
    created_by: str
    is_private: bool


@dataclass
class FolderDTO:
    folder_id: str
    name: str
    description: str
    space_id: str
    order: int
    is_active: bool
    created_by: str
    is_private: bool


@dataclass
class ListViewDTO:
    id: int
    list_id: str
    view_id: str
    applied_by: str
    is_active: bool


@dataclass
class RemoveListViewDTO:
    id: int
    list_id: str
    view_id: str
    removed_by: str
    is_active: bool


@dataclass
class CreateSpaceDTO:
    name: str
    description: str
    workspace_id: str
    order: int
    is_active: bool
    is_private: bool
    created_by: str


@dataclass
class SpaceDTO:
    space_id: str
    name: str
    description: str
    workspace_id: str
    order: int
    is_active: bool
    is_private: bool
    created_by: str


@dataclass
class WorkspaceDTO:
    workspace_id: str
    name: str
    description: str
    owner_id: str
    is_active: bool


@dataclass
class CreateWorkspaceDTO:
    name: str
    description: str
    owner_id: str


@dataclass
class AddMemberToWorkspaceDTO:
    workspace_id: str
    user_id: str
    role: RoleEnum
    is_active: bool
    added_by: str


@dataclass
class WorkspaceMemberDTO:
    id: int
    workspace_id: str
    user_id: str
    role: RoleEnum
    is_active: bool
    added_by: str

@dataclass
class CreateUserSpacePermissionDTO:
    space_id: str
    user_id: str
    permission_type: PermissionsEnum
    is_active: bool
    added_by: str

@dataclass
class UserSpacePermissionDTO:
    id: int
    space_id: str
    permission_type: PermissionsEnum
    user_id: str
    is_active: bool
    added_by: str

@dataclass
class CreateUserFolderPermissionDTO:
    folder_id: str
    user_id: str
    permission_type: PermissionsEnum
    is_active: bool
    added_by: str

@dataclass
class UserFolderPermissionDTO:
    id: int
    folder_id: str
    permission_type: PermissionsEnum
    user_id: str
    is_active: bool
    added_by: str

@dataclass
class CreateUserListPermissionDTO:
    list_id: str
    permission_type: PermissionsEnum
    user_id: str
    is_active: bool
    added_by: str

@dataclass
class UserListPermissionDTO:
    id: int
    list_id: str
    permission_type: PermissionsEnum
    user_id: str
    is_active: bool
    added_by: str