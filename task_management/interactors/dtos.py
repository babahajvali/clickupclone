from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict

from task_management.exceptions.enums import ViewType, FieldTypes, \
    Gender, Role, Permissions


@dataclass
class UserDTO:
    user_id: str
    full_name: str
    username: str
    password: str
    gender: Gender
    email: str
    phone_number: str
    is_active: bool
    image_url: str


@dataclass
class UpdateUserDTO:
    user_id: str
    full_name: Optional[str]
    username: Optional[str]
    gender: Optional[Gender]
    email: Optional[str]
    phone_number: Optional[str]
    image_url: Optional[str]


@dataclass
class CreateUserDTO:
    username: str
    full_name: str
    email: str
    password: str
    phone_number: str
    gender: Gender
    image_url: str


@dataclass
class CreateFieldDTO:
    field_type: FieldTypes
    field_name: str
    description: str
    template_id: str
    config: Optional[dict]
    is_required: bool
    created_by: str


@dataclass
class UpdateFieldDTO:
    field_id: str
    description: Optional[str]
    field_name: Optional[str]
    config: Optional[dict]
    is_required: Optional[bool]


@dataclass
class FieldDTO:
    field_id: str
    field_type: FieldTypes
    description: str
    template_id: str
    field_name: str
    is_active: bool
    order: int
    config: dict
    is_required: bool
    created_by: str


@dataclass
class CreateTemplateDTO:
    name: str
    description: str
    list_id: str
    created_by: str


@dataclass
class UpdateTemplateDTO:
    template_id: str
    name: Optional[str]
    description: Optional[str]


@dataclass
class TemplateDTO:
    template_id: str
    name: str
    list_id: str
    description: str
    created_by: str


@dataclass
class CreateTaskDTO:
    title: str
    description: str
    list_id: str
    created_by: str


@dataclass
class UpdateTaskDTO:
    task_id: str
    title: str
    description: str


@dataclass
class TaskDTO:
    task_id: str
    title: str
    description: str
    list_id: str
    order: int
    created_by: str
    is_deleted: bool


@dataclass
class TaskAssigneeDTO:
    assign_id: str
    user_id: str
    task_id: str
    assigned_by: str
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
    created_by: str
    is_private: bool
    folder_id: Optional[str] = None


@dataclass
class UpdateListDTO:
    list_id: str
    name: Optional[str]
    description: Optional[str]


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
    view_type: ViewType
    created_by: str


@dataclass
class UpdateViewDTO:
    view_id: str
    name: str
    description: str


@dataclass
class ViewDTO:
    view_id: str
    name: str
    description: str
    view_type: ViewType
    created_by: str


@dataclass
class CreateFolderDTO:
    name: str
    description: str
    space_id: str
    created_by: str
    is_private: bool


@dataclass
class UpdateFolderDTO:
    folder_id: str
    name: Optional[str]
    description: Optional[str]


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
    is_private: bool
    created_by: str


@dataclass
class UpdateSpaceDTO:
    space_id: str
    name: Optional[str]
    description: Optional[str]


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
    user_id: str
    account_id: str
    is_active: bool


@dataclass
class UpdateWorkspaceDTO:
    workspace_id: str
    name: Optional[str]
    description: Optional[str]


@dataclass
class CreateWorkspaceDTO:
    name: str
    description: str
    user_id: str
    account_id: str


@dataclass
class AddMemberToWorkspaceDTO:
    workspace_id: str
    user_id: str
    role: Role
    added_by: str


@dataclass
class WorkspaceMemberDTO:
    id: int
    workspace_id: str
    user_id: str
    role: Role
    is_active: bool
    added_by: str


@dataclass
class CreateUserSpacePermissionDTO:
    space_id: str
    user_id: str
    permission_type: Permissions
    added_by: str


@dataclass
class UserSpacePermissionDTO:
    id: int
    space_id: str
    permission_type: Permissions
    user_id: str
    is_active: bool
    added_by: str


@dataclass
class CreateUserFolderPermissionDTO:
    folder_id: str
    user_id: str
    permission_type: Permissions
    added_by: str


@dataclass
class UserFolderPermissionDTO:
    id: int
    folder_id: str
    permission_type: Permissions
    user_id: str
    is_active: bool
    added_by: str


@dataclass
class CreateUserListPermissionDTO:
    list_id: str
    permission_type: Permissions
    user_id: str
    added_by: str


@dataclass
class UserListPermissionDTO:
    id: int
    list_id: str
    permission_type: Permissions
    user_id: str
    is_active: bool
    added_by: str


@dataclass
class FilterDTO:
    list_id: str
    field_filters: Optional[Dict[str, list[str]]] = None
    assignees: Optional[list[str]] = None
    offset: int = 1
    limit: int = 10


@dataclass
class UpdateFieldValueDTO:
    task_id: str
    field_id: str
    value: str


@dataclass
class CreateFieldValueDTO:
    task_id: str
    field_id: str
    value: str
    created_by: str


@dataclass
class TaskFieldValueDTO:
    id: int
    task_id: str
    field_id: str
    value: str


@dataclass
class FieldValueDTO:
    field_id: str
    value: str


@dataclass
class TaskFieldValuesDTO:
    task_id: str
    values: list[FieldValueDTO]


@dataclass
class CreateAccountDTO:
    name: str
    description: str
    owner_id: str

@dataclass
class UpdateAccountDTO:
    account_id: str
    name: Optional[str]
    description: Optional[str]


@dataclass
class AccountDTO:
    account_id: str
    name: str
    description: str
    owner_id: str
    is_active: bool


@dataclass
class AccountMemberDTO:
    id: int
    user_id: str
    account_id: str
    role: Role
    added_by: str
    is_active: bool


@dataclass
class CreateAccountMemberDTO:
    account_id: str
    user_id: str
    role: Role
    added_by: str | None


@dataclass
class PasswordResetRequestDTO:
    email: str


@dataclass
class PasswordResetDTO:
    token: str
    new_password: str


@dataclass
class PasswordResetTokenDTO:
    user_id: str
    token: str
    is_used: bool
    created_at: datetime
    expires_at: datetime


# task_management/interactors/dtos.py (add these)

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict


@dataclass
class CreateCheckoutSessionDTO:
    user_id: str
    plan_id: str
    success_url: Optional[str] = None
    cancel_url: Optional[str] = None


@dataclass
class CheckoutSessionResponseDTO:
    session_id: str
    checkout_url: str


@dataclass
class PlanDTO:
    plan_id: str
    plan_name: str
    stripe_price_id: str
    price: float
    currency: str
    billing_period: str
    features: Dict
    is_active: bool


@dataclass
class SubscriptionDTO:
    subscription_id: str
    user_id: str
    plan: Optional[PlanDTO]
    stripe_subscription_id: str
    status: str
    current_period_start: datetime
    current_period_end: datetime
    cancel_at_period_end: bool
    canceled_at: Optional[datetime]


@dataclass
class PaymentDTO:
    payment_id: str
    user_id: str
    subscription_id: Optional[str]
    stripe_payment_intent_id: str
    amount: float
    currency: str
    status: str
    payment_method: Optional[str]
    created_at: datetime


@dataclass
class CancelSubscriptionDTO:
    user_id: str
    subscription_id: str


@dataclass
class WebhookEventDTO:
    event_type: str
    event_data: Dict