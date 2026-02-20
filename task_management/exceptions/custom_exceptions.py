class UserNotFound(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id


class EmptyName(Exception):
    def __init__(self, name: str):
        self.name = name


class InactiveUser(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id


class TemplateNotFound(Exception):
    def __init__(self, template_id: str):
        self.template_id = template_id


class UnsupportedFieldType(Exception):
    def __init__(self, field_type: str):
        self.field_type = field_type


class FieldNameAlreadyExists(Exception):
    def __init__(self, field_name: str):
        self.field_name = field_name


class InactiveField(Exception):
    def __init__(self, field_id: str):
        self.field_id = field_id


class ModificationNotAllowed(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id


class FieldNotFound(Exception):
    def __init__(self, field_id: str):
        self.field_id = field_id


class InvalidFieldConfig(Exception):
    def __init__(
            self,
            field_type: str,
            invalid_keys: list | None = None,
            message: str | None = None
    ):
        self.field_type = field_type
        self.invalid_keys = invalid_keys

        if message:
            self.message = message
        elif invalid_keys:
            self.message = (
                f"Invalid config keys {invalid_keys} "
                f"for field type '{field_type}'."
            )
        else:
            self.message = f"Invalid config for field type '{field_type}'."

    def __str__(self):
        return self.message


class DropdownOptionsMissing(Exception):
    def __init__(self, field_type: str):
        self.field_type = field_type


class InvalidFieldDefaultValue(Exception):
    def __init__(
            self, field_type: str, default_value=None,
            message: str | None = None):

        self.field_type = field_type
        self.default_value = default_value

        if message:
            self.message = message
        else:
            self.message = (
                f"Invalid default value '{default_value}' "
                f"for field type '{field_type}'."
            )

    def __str__(self):
        return self.message


class ListNotFound(Exception):
    def __init__(self, list_id: str):
        self.list_id = list_id


class UserListPermissionNotFound(Exception):
    def __init__(self, user_id: str, list_id: str):
        self.user_id = user_id
        self.list_id = list_id


class InactiveUserListPermission(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id


class UserHaveAlreadyListPermission(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id


class TaskNotFound(Exception):
    def __init__(self, task_id: str):
        self.task_id = task_id


class TaskAssigneeNotFound(Exception):
    def __init__(self, assign_id: str):
        self.assign_id = assign_id


class InActiveTaskAssigneeFound(Exception):
    def __init__(self, assign_id: str):
        self.assign_id = assign_id


class DeletedTaskFound(Exception):
    def __init__(self, task_id: str):
        self.task_id = task_id


class InactiveList(Exception):
    def __init__(self, list_id: str):
        self.list_id = list_id


class SpaceNotFound(Exception):
    def __init__(self, space_id: str):
        self.space_id = space_id


class InactiveSpace(Exception):
    def __init__(self, space_id: str):
        self.space_id = space_id


class FolderNotFound(Exception):
    def __init__(self, folder_id: str):
        self.folder_id = folder_id


class InactiveFolder(Exception):
    def __init__(self, folder_id: str):
        self.folder_id = folder_id


class ViewTypeNotFound(Exception):
    def __init__(self, view_type: str):
        self.view_type = view_type


class ViewNotFound(Exception):
    def __init__(self, view_id: str):
        self.view_id = view_id


class WorkspaceNotFound(Exception):
    def __init__(self, workspace_id: str):
        self.workspace_id = workspace_id


class InvalidWorkspaceIdsFound(Exception):
    def __init__(self, workspace_ids: list[str]):
        self.workspace_ids = workspace_ids


class InactiveWorkspace(Exception):
    def __init__(self, workspace_id: str):
        self.workspace_id = workspace_id


class UserNotWorkspaceOwner(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id


class UnsupportedVisibilityType(Exception):
    def __init__(self, visibility_type: str):
        self.visibility_type = visibility_type


class UnexpectedRole(Exception):
    def __init__(self, role: str):
        self.role = role


class UnexpectedPermission(Exception):
    def __init__(self, permission: str):
        self.permission = permission


class EmailNotFound(Exception):
    def __init__(self, email: str):
        self.email = email


class IncorrectPassword(Exception):
    def __init__(self, password: str):
        self.password = password


class UsernameAlreadyExists(Exception):
    def __init__(self, username: str):
        self.username = username


class EmailAlreadyExists(Exception):
    def __init__(self, email: str):
        self.email = email


class PhoneNumberAlreadyExists(Exception):
    def __init__(self, phone_number: str):
        self.phone_number = phone_number


class UsernameNotFound(Exception):
    def __init__(self, username: str):
        self.username = username


class InvalidOffset(Exception):
    def __init__(self, offset: int):
        self.offset = offset


class InvalidLimit(Exception):
    def __init__(self, limit: int):
        self.limit = limit


class InvalidOrder(Exception):
    def __init__(self, order: int):
        self.order = order


class UserNotWorkspaceMember(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id


class WorkspaceMemberIdNotFound(Exception):
    def __init__(self, workspace_member_id: int):
        self.workspace_member_id = workspace_member_id


class InactiveWorkspaceMember(Exception):
    def __init__(self, workspace_member_id: int):
        self.workspace_member_id = workspace_member_id


class WorkspaceMemberNotFound(Exception):
    def __init__(self, workspace_id: str, user_id: str):
        self.workspace_id = workspace_id
        self.user_id = user_id


class AccountNameAlreadyExists(Exception):
    def __init__(self, name: str):
        self.name = name


class NothingToUpdateAccount(Exception):
    def __init__(self, account_id: str):
        self.account_id = account_id


class NothingToUpdateWorkspace(Exception):
    def __init__(self, workspace_id: str):
        self.workspace_id = workspace_id


class NothingToUpdateField(Exception):
    def __init__(self, field_id: str):
        self.field_id = field_id


class NothingToUpdateTemplate(Exception):
    def __init__(self, template_id: str):
        self.template_id = template_id


class NothingToUpdateList(Exception):
    def __init__(self, list_id: str):
        self.list_id = list_id


class NothingToUpdateFolderException(Exception):
    def __init__(self, folder_id: str):
        self.folder_id = folder_id


class NothingToUpdateSpace(Exception):
    def __init__(self, space_id: str):
        self.space_id = space_id


class NothingToUpdateTask(Exception):
    def __init__(self, task_id: str):
        self.task_id = task_id


class NothingToUpdateView(Exception):
    def __init__(self, view_id: str):
        self.view_id = view_id


class AccountNotFound(Exception):
    def __init__(self, account_id: str):
        self.account_id = account_id


class InvalidAccountIds(Exception):
    def __init__(self, account_ids: list[str]):
        self.account_ids = account_ids


class InactiveAccountIds(Exception):
    def __init__(self, account_ids: list[str]):
        self.account_ids = account_ids


class InactiveAccount(Exception):
    def __init__(self, account_id: str):
        self.account_id = account_id


class UserNotAccountOwner(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id


class UserDoesNotHaveAccountPermission(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id


class ListViewNotFound(Exception):
    def __init__(self, list_id: str, view_id: str):
        self.list_id = list_id
        self.view_id = view_id


class AccountMemberNotFound(Exception):
    def __init__(self, account_member_id: int):
        self.account_member_id = account_member_id


class InvalidResetToken(Exception):
    def __init__(self, token: str):
        self.token = token

    def __str__(self):
        return f"Invalid or expired reset token: {self.token}"


class ResetTokenExpired(Exception):
    def __init__(self, token: str):
        self.token = token

    def __str__(self):
        return f"Invalid or expired reset token: {self.token}"


class MissingFieldConfig(Exception):
    def __init__(self, field_type: str):
        self.field_type = field_type


class InvalidFieldValue(Exception):
    def __init__(self, message: str):
        self.message = message
