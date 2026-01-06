class UserNotFoundException(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id

class InactiveUserFoundException(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id

class TemplateNotFoundException(Exception):
    def __init__(self, template_id: str):
        self.template_id = template_id


class UnSupportedFieldTypeFoundException(Exception):
    def __init__(self, field_type: str):
        self.field_type = field_type


class FieldNameAlreadyExistsException(Exception):
    def __init__(self, field_name: str):
        self.field_name = field_name


class FieldOrderAlreadyExistsException(Exception):
    def __init__(self, field_order: int):
        self.field_order = field_order


class NotAccessToModificationException(Exception):
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


class InvalidFieldDefaultValueException(Exception):
    def __init__(
            self,
            field_type: str,
            default_value=None,
            message: str | None = None
    ):
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


class AlreadyExistedTemplateNameException(Exception):
    def __init__(self, template_name: str):
        self.template_name = template_name


class DefaultTemplateAlreadyExistedException(Exception):
    def __init__(self, template_name: str):
        self.template_name = template_name


class ListNotFoundException(Exception):
    def __init__(self, list_id: str):
        self.list_id = list_id


class FolderListOrderAlreadyExistedException(Exception):
    def __init__(self, folder_id: str):
        self.folder_id = folder_id


class SpaceListOrderAlreadyExistedException(Exception):
    def __init__(self, space_id: str):
        self.space_id = space_id

class FolderOrderAlreadyExistedException(Exception):
    def __init__(self, space_id: str):
        self.space_id = space_id

class TaskNotFoundException(Exception):
    def __init__(self, task_id: str):
        self.task_id = task_id

class TaskAssigneeNotFoundException(Exception):
    def __init__(self, assign_id: str):
        self.assign_id = assign_id
        
class InactiveTaskFoundException(Exception):
    def __init__(self, task_id: str):
        self.task_id = task_id

class InactiveListFoundException(Exception):
    def __init__(self, list_id: str):
        self.list_id = list_id

class SpaceNotFoundException(Exception):
    def __init__(self, space_id: str):
        self.space_id = space_id


class InactiveSpaceFoundException(Exception):
    def __init__(self, space_id: str):
        self.space_id = space_id

class FolderNotFoundException(Exception):
    def __init__(self, folder_id: str):
        self.folder_id = folder_id

class InactiveFolderFoundException(Exception):
    def __init__(self, folder_id: str):
        self.folder_id = folder_id

class ViewTypeNotFoundException(Exception):
    def __init__(self, view_type: str):
        self.view_type = view_type

class ViewNotFoundException(Exception):
    def __init__(self, view_id: str):
        self.view_id = view_id


class SpaceOrderAlreadyExistedException(Exception):
    def __init__(self, workspace_id: str):
        self.workspace_id = workspace_id


class WorkspaceNotFoundException(Exception):
    def __init__(self, workspace_id: str):
        self.workspace_id = workspace_id


class InactiveWorkspaceFoundException(Exception):
    def __init__(self, workspace_id: str):
        self.workspace_id = workspace_id

class UserNotWorkspaceOwnerException(Exception):
    def __init__(self,user_id: str):
        self.user_id = user_id


class UnexpectedRoleFoundException(Exception):
    def __init__(self, role: str):
        self.role = role

class UserDoesNotHaveSpacePermissionException(Exception):
    def __init__(self,user_id: str):
        self.user_id = user_id

class UserDoesNotHaveFolderPermissionException(Exception):
    def __init__(self,user_id: str):
        self.user_id = user_id


class UserDoesNotHaveListPermissionException(Exception):
    def __init__(self,user_id: str):
        self.user_id = user_id

class InactiveUserPermissionException(Exception):
    def __init__(self,user_id: str):
        self.user_id = user_id


class NotExistedEmailFound(Exception):
    def __init__(self,email: str):
        self.email = email

class WrongPasswordFound(Exception):
    def __init__(self, password: str):
        self.password = password

class ExistedUsernameFound(Exception):
    def __init__(self, username: str):
        self.username = username


class ExistedEmailFound(Exception):
    def __init__(self, email: str):
        self.email = email


class ExistedPhoneNumberFound(Exception):
    def __init__(self, phone_number: str):
        self.phone_number = phone_number


class UsernameNotFound(Exception):
    def __init__(self, username: str):
        self.username = username

class TasKOrderAlreadyExistedException(Exception):
    def __init__(self, list_id: str):
        self.list_id = list_id

class InvalidOffsetNumberException(Exception):
    def __init__(self, offset: int):
        self.offset = offset

class InvalidLimitException(Exception):
    def __init__(self, limit: int):
        self.limit = limit

class InvalidOrderException(Exception):
    def __init__(self, order: int):
        self.order = order

class InactiveWorkspaceMemberFoundException(Exception):
    def __init__(self, workspace_member_id: str):
        self.workspace_member_id = workspace_member_id