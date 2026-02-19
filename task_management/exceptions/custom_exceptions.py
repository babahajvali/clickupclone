class UserNotFoundException(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id


class EmptyNameException(Exception):
    def __init__(self, name: str):
        self.name = name


class InactiveUserException(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id


class TemplateNotFoundException(Exception):
    def __init__(self, template_id: str):
        self.template_id = template_id


class UnsupportedFieldTypeException(Exception):
    def __init__(self, field_type: str):
        self.field_type = field_type


class FieldNameAlreadyExistsException(Exception):
    def __init__(self, field_name: str):
        self.field_name = field_name


class InactiveFieldException(Exception):
    def __init__(self, field_id: str):
        self.field_id = field_id


class ModificationNotAllowedException(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id


class FieldNotFoundException(Exception):
    def __init__(self, field_id: str):
        self.field_id = field_id


class InvalidFieldConfigException(Exception):
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

        super().__init__(self.message)


class DropdownOptionsMissingException(Exception):
    def __init__(self, field_type: str):
        self.field_type = field_type


class InvalidFieldDefaultValueException(Exception):
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

        super().__init__(self.message)


class TemplateNameAlreadyExistsException(Exception):
    def __init__(self, template_name: str):
        self.template_name = template_name


class ListNotFoundException(Exception):
    def __init__(self, list_id: str):
        self.list_id = list_id


class UserListPermissionNotFoundException(Exception):
    def __init__(self, user_id: str, list_id: str):
        self.user_id = user_id
        self.list_id = list_id


class InactiveUserListPermissionException(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id


class UserHaveAlreadyListPermissionException(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id


class TaskNotFoundException(Exception):
    def __init__(self, task_id: str):
        self.task_id = task_id


class TaskAssigneeNotFoundException(Exception):
    def __init__(self, assign_id: str):
        self.assign_id = assign_id


class InActiveTaskAssigneeFoundException(Exception):
    def __init__(self, assign_id: str):
        self.assign_id = assign_id


class DeletedTaskException(Exception):
    def __init__(self, task_id: str):
        self.task_id = task_id


class InactiveListException(Exception):
    def __init__(self, list_id: str):
        self.list_id = list_id


class SpaceNotFoundException(Exception):
    def __init__(self, space_id: str):
        self.space_id = space_id


class InactiveSpaceException(Exception):
    def __init__(self, space_id: str):
        self.space_id = space_id


class FolderNotFoundException(Exception):
    def __init__(self, folder_id: str):
        self.folder_id = folder_id


class InactiveFolderException(Exception):
    def __init__(self, folder_id: str):
        self.folder_id = folder_id


class ViewTypeNotFoundException(Exception):
    def __init__(self, view_type: str):
        self.view_type = view_type


class ViewNotFoundException(Exception):
    def __init__(self, view_id: str):
        self.view_id = view_id


class WorkspaceNotFoundException(Exception):
    def __init__(self, workspace_id: str):
        self.workspace_id = workspace_id


class InvalidWorkspaceIdsFoundException(Exception):
    def __init__(self, workspace_ids: list[str]):
        self.workspace_ids = workspace_ids


class InactiveWorkspaceException(Exception):
    def __init__(self, workspace_id: str):
        self.workspace_id = workspace_id


class UserNotWorkspaceOwnerException(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id


class UnsupportedVisibilityTypeException(Exception):
    def __init__(self, visibility_type: str):
        self.visibility_type = visibility_type


class UnexpectedRoleException(Exception):
    def __init__(self, role: str):
        self.role = role


class UnexpectedPermissionException(Exception):
    def __init__(self, permission: str):
        self.permission = permission


class EmailNotFoundException(Exception):
    def __init__(self, email: str):
        self.email = email


class IncorrectPasswordException(Exception):
    def __init__(self, password: str):
        self.password = password


class UsernameAlreadyExistsException(Exception):
    def __init__(self, username: str):
        self.username = username


class EmailAlreadyExistsException(Exception):
    def __init__(self, email: str):
        self.email = email


class PhoneNumberAlreadyExistsException(Exception):
    def __init__(self, phone_number: str):
        self.phone_number = phone_number


class UsernameNotFoundException(Exception):
    def __init__(self, username: str):
        self.username = username


class InvalidOffsetException(Exception):
    def __init__(self, offset: int):
        self.offset = offset


class InvalidLimitException(Exception):
    def __init__(self, limit: int):
        self.limit = limit


class InvalidOrderException(Exception):
    def __init__(self, order: int):
        self.order = order


class UserNotWorkspaceMemberException(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id


class WorkspaceMemberNotFoundException(Exception):
    def __init__(self, workspace_member_id: int):
        self.workspace_member_id = workspace_member_id


class InactiveWorkspaceMemberException(Exception):
    def __init__(self, workspace_member_id: int):
        self.workspace_member_id = workspace_member_id


class WorkspaceMemberNotFound(Exception):
    def __init__(self, workspace_id: str, user_id: str):
        self.workspace_id = workspace_id
        self.user_id = user_id


class AccountNameAlreadyExistsException(Exception):
    def __init__(self, name: str):
        self.name = name


class NothingToUpdateAccountException(Exception):
    def __init__(self, account_id: str):
        self.account_id = account_id


class NothingToUpdateWorkspaceException(Exception):
    def __init__(self, workspace_id: str):
        self.workspace_id = workspace_id


class NothingToUpdateFieldException(Exception):
    def __init__(self, field_id: str):
        self.field_id = field_id


class NothingToUpdateTemplateException(Exception):
    def __init__(self, template_id: str):
        self.template_id = template_id


class NothingToUpdateListException(Exception):
    def __init__(self, list_id: str):
        self.list_id = list_id


class NothingToUpdateFolderException(Exception):
    def __init__(self, folder_id: str):
        self.folder_id = folder_id


class NothingToUpdateSpaceException(Exception):
    def __init__(self, space_id: str):
        self.space_id = space_id


class NothingToUpdateTaskException(Exception):
    def __init__(self, task_id: str):
        self.task_id = task_id


class NothingToUpdateViewException(Exception):
    def __init__(self, view_id: str):
        self.view_id = view_id


class AccountNotFoundException(Exception):
    def __init__(self, account_id: str):
        self.account_id = account_id


class InvalidAccountIdsException(Exception):
    def __init__(self, account_ids: list[str]):
        self.account_ids = account_ids


class InactiveAccountIdsException(Exception):
    def __init__(self, account_ids: list[str]):
        self.account_ids = account_ids


class InactiveAccountException(Exception):
    def __init__(self, account_id: str):
        self.account_id = account_id


class UserNotAccountOwnerException(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id


class UserDoesNotHaveAccountPermissionException(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id


class ListViewNotFoundException(Exception):
    def __init__(self, list_id: str, view_id: str):
        self.list_id = list_id
        self.view_id = view_id


class AccountMemberNotFoundException(Exception):
    def __init__(self, account_member_id: int):
        self.account_member_id = account_member_id


class InvalidResetTokenException(Exception):
    def __init__(self, token: str):
        self.token = token
        super().__init__(f"Invalid or expired reset token: {token}")


class ResetTokenExpiredException(Exception):
    def __init__(self, token: str):
        self.token = token
        super().__init__(f"Reset token has expired: {token}")


class MissingFieldConfigException(Exception):
    def __init__(self, field_type: str):
        self.field_type = field_type


class InvalidFieldValueException(Exception):
    def __init__(self, message: str):
        self.message = message
