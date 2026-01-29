from task_management.constants.field_constants import FIELD_TYPE_RULES
from task_management.exceptions.custom_exceptions import UserNotFoundException, \
    TemplateNotFoundException, UnsupportedFieldTypeException, \
    FieldNameAlreadyExistsException, ModificationNotAllowedException, \
    InvalidFieldConfigException, InvalidFieldDefaultValueException, \
    TemplateNameAlreadyExistsException, \
    ListNotFoundException, TaskNotFoundException, \
    DeletedTaskException, InactiveListException, \
    SpaceNotFoundException, InactiveSpaceException, \
    FolderNotFoundException, InactiveFolderException, \
    ViewTypeNotFoundException, ViewNotFoundException, \
    WorkspaceNotFoundException, InactiveWorkspaceException, \
    InactiveUserException, UserNotWorkspaceOwnerException, \
    InactiveWorkspaceMemberException, AccountNotFoundException, \
    InactiveAccountException, UnexpectedRoleException, \
    UnsupportedVisibilityTypeException, FieldNotFoundException
from task_management.exceptions.enums import PermissionsEnum, FieldTypeEnum, \
    ViewTypeEnum, Role, Visibility
from task_management.interactors.storage_interface.account_storage_interface import \
    AccountStorageInterface
from task_management.interactors.storage_interface.account_member_storage_interface import \
    AccountMemberStorageInterface
from task_management.interactors.storage_interface.field_storage_interface import \
    FieldStorageInterface
from task_management.interactors.storage_interface.folder_permission_storage_interface import \
    FolderPermissionStorageInterface
from task_management.interactors.storage_interface.folder_storage_interface import \
    FolderStorageInterface
from task_management.interactors.storage_interface.list_permission_storage_interface import \
    ListPermissionStorageInterface
from task_management.interactors.storage_interface.list_storage_interface import \
    ListStorageInterface
from task_management.interactors.storage_interface.space_permission_storage_interface import \
    SpacePermissionStorageInterface
from task_management.interactors.storage_interface.space_storage_interface import \
    SpaceStorageInterface
from task_management.interactors.storage_interface.task_storage_interface import \
    TaskStorageInterface
from task_management.interactors.storage_interface.template_storage_interface import \
    TemplateStorageInterface
from task_management.interactors.storage_interface.user_storage_interface import \
    UserStorageInterface
from task_management.interactors.storage_interface.view_storage_interface import \
    ViewStorageInterface
from task_management.interactors.storage_interface.workspace_member_storage_interface import \
    WorkspaceMemberStorageInterface
from task_management.interactors.storage_interface.workspace_storage_interface import \
    WorkspaceStorageInterface


class ValidationMixin:

    @staticmethod
    def validate_user_is_active(user_id: str,
                                user_storage: UserStorageInterface):
        user_data = user_storage.get_user_data(user_id=user_id)

        if not user_data:
            raise UserNotFoundException(user_id=user_id)

        if not user_data.is_active:
            raise InactiveUserException(user_id=user_id)

    def get_template_list_id(self, template_id: str,
                             template_storage: TemplateStorageInterface):
        return self.get_template(template_id, template_storage).list_id

    @staticmethod
    def get_template(template_id: str, storage: TemplateStorageInterface):
        template = storage.get_template_by_id(template_id)

        if not template:
            raise TemplateNotFoundException(template_id)

        return template

    @staticmethod
    def validate_field_type(field_type: str):

        field_types = [x.value for x in FieldTypeEnum]

        if field_type not in field_types:
            raise UnsupportedFieldTypeException(field_type=field_type)

    @staticmethod
    def validate_field_name_not_exists(field_name: str, template_id: str,
                                       field_storage: FieldStorageInterface):
        is_exist = field_storage.is_field_name_exists(field_name=field_name,
                                                      template_id=template_id)

        if is_exist:
            raise FieldNameAlreadyExistsException(field_name=field_name)

    @staticmethod
    def validate_template_name_not_exists(template_name: str,
                                          template_storage: TemplateStorageInterface):

        is_exist = template_storage.is_template_name_exist(
            template_name=template_name)

        if is_exist:
            raise TemplateNameAlreadyExistsException(
                template_name=template_name)

    @staticmethod
    def validate_field_name_unique(field_id: str, field_name: str,
                                   template_id: str,
                                   field_storage: FieldStorageInterface):

        is_field_name_exist = field_storage.check_field_name_except_this_field(
            field_id=field_id, field_name=field_name, template_id=template_id)

        if is_field_name_exist:
            raise FieldNameAlreadyExistsException(field_name=field_name)

    @staticmethod
    def validate_field_config(field_type: str, config: dict):

        default_value = config.get("default")

        if field_type not in FIELD_TYPE_RULES:
            raise UnsupportedFieldTypeException(
                field_type=field_type
            )

        rules = FIELD_TYPE_RULES[field_type]

        allowed_keys = rules["config_keys"]
        invalid_keys = set(config.keys()) - allowed_keys

        if invalid_keys:
            raise InvalidFieldConfigException(
                field_type=field_type,
                invalid_keys=list(invalid_keys)
            )

        if field_type == FieldTypeEnum.DROPDOWN.value:
            if "options" not in config or not config["options"]:
                raise InvalidFieldConfigException(
                    field_type=field_type,
                    message="Dropdown must have non-empty options"
                )

        if default_value is not None:
            if field_type == FieldTypeEnum.DROPDOWN.value:
                if default_value not in config.get("options", []):
                    raise InvalidFieldDefaultValueException(
                        field_type=field_type,
                        message="Default value must be one of dropdown options"
                    )

        if field_type == FieldTypeEnum.NUMBER.value and default_value is not None:
            min_val = config.get("min")
            max_val = config.get("max")

            if min_val is not None and default_value < min_val:
                raise InvalidFieldDefaultValueException(
                    field_type=field_type,
                    message=f"Default value {default_value} is less than minimum {min_val}"
                )

            if max_val is not None and default_value > max_val:
                raise InvalidFieldDefaultValueException(
                    field_type=field_type,
                    message=f"Default value {default_value} is greater than maximum {max_val}"
                )

        if field_type == FieldTypeEnum.TEXT.value and default_value is not None:
            max_length = config.get("max_length")

            if max_length is not None and len(default_value) > max_length:
                raise InvalidFieldDefaultValueException(
                    field_type=field_type,
                    message=f"Default value length {len(default_value)} exceeds max_length {max_length}"
                )

    @staticmethod
    def validate_list_is_active(list_id: str,
                                list_storage: ListStorageInterface):
        list_data = list_storage.get_list(list_id=list_id)

        if not list_data:
            raise ListNotFoundException(list_id=list_id)

        if not list_data.is_active:
            raise InactiveListException(list_id=list_id)

    @staticmethod
    def validate_user_has_access_to_list(user_id: str, list_id: str,
                                         permission_storage: ListPermissionStorageInterface):
        user_permissions = permission_storage.get_user_permission_for_list(
            user_id=user_id, list_id=list_id)

        if not user_permissions.permission_type == PermissionsEnum.FULL_EDIT.value:
            raise ModificationNotAllowedException(user_id=user_id)

    @staticmethod
    def get_active_task_list_id(task_id: str,
                                task_storage: TaskStorageInterface) -> str:

        task_data = task_storage.get_task_by_id(task_id=task_id)

        if not task_data:
            raise TaskNotFoundException(task_id=task_id)

        if task_data.is_deleted:
            raise DeletedTaskException(task_id=task_id)

        return task_data.list_id

    @staticmethod
    def validate_space_is_active(space_id: str,
                                 space_storage: SpaceStorageInterface):

        space_data = space_storage.get_space(space_id=space_id)

        if not space_data:
            raise SpaceNotFoundException(space_id=space_id)

        if not space_data.is_active:
            raise InactiveSpaceException(space_id=space_id)

    @staticmethod
    def validate_folder_is_active(folder_id: str,
                                  folder_storage: FolderStorageInterface):
        folder_data = folder_storage.get_folder(folder_id=folder_id)

        if not folder_data:
            raise FolderNotFoundException(folder_id=folder_id)

        if not folder_data.is_active:
            raise InactiveFolderException(folder_id=folder_id)

    @staticmethod
    def validate_user_has_access_to_folder(user_id: str,
                                           folder_id: str,
                                           permission_storage: FolderPermissionStorageInterface):

        user_permission = permission_storage.get_user_permission_for_folder(
            user_id=user_id, folder_id=folder_id)

        if not user_permission.permission_type == PermissionsEnum.FULL_EDIT.value:
            raise ModificationNotAllowedException(user_id=user_id)

    @staticmethod
    def check_view_type(view_type: str):
        view_types = [x.value for x in ViewTypeEnum]

        if view_type not in view_types:
            raise ViewTypeNotFoundException(view_type=view_type)

    @staticmethod
    def validate_view_exist(view_id: str, view_storage: ViewStorageInterface):
        view_data = view_storage.get_view(view_id=view_id)

        if not view_data:
            raise ViewNotFoundException(view_id=view_id)

    @staticmethod
    def validate_user_has_access_to_space(user_id: str, space_id: str,
                                          permission_storage: SpacePermissionStorageInterface):

        user_permissions = permission_storage.get_user_permission_for_space(
            user_id=user_id, space_id=space_id)

        if not user_permissions.permission_type == PermissionsEnum.FULL_EDIT.value:
            raise ModificationNotAllowedException(user_id=user_id)

    @staticmethod
    def validate_workspace_is_active(workspace_id: str,
                                     workspace_storage: WorkspaceStorageInterface):
        workspace_data = workspace_storage.get_workspace(
            workspace_id=workspace_id)

        if not workspace_data:
            raise WorkspaceNotFoundException(workspace_id=workspace_id)

        if not workspace_data.is_active:
            raise InactiveWorkspaceException(workspace_id=workspace_id)

    @staticmethod
    def _validate_visibility_type(visibility: str):
        existed_visibilities = [each.value for each in Visibility]

        if visibility not in existed_visibilities:
            raise UnsupportedVisibilityTypeException(
                visibility_type=visibility)

    @staticmethod
    def validate_user_is_workspace_owner(user_id: str, workspace_id: str,
                                         workspace_storage: WorkspaceStorageInterface):
        is_owner = workspace_storage.validate_user_is_workspace_owner(
            workspace_id=workspace_id, user_id=user_id)

        if not is_owner:
            raise UserNotWorkspaceOwnerException(user_id=user_id)

    @staticmethod
    def validate_user_can_modify_workspace(
            user_id: str,
            workspace_id: str,
            workspace_storage: WorkspaceStorageInterface,
            workspace_member_storage: WorkspaceMemberStorageInterface
    ):
        workspace_data = workspace_storage.get_workspace(
            workspace_id=workspace_id
        )

        if not workspace_data:
            raise WorkspaceNotFoundException(workspace_id=workspace_id)

        if not workspace_data.is_active:
            raise InactiveWorkspaceException(workspace_id=workspace_id)

        if str(workspace_data.user_id) == str(user_id):
            return

        member_permission = workspace_member_storage.get_workspace_member(
            workspace_id=workspace_id,
            user_id=user_id
        )

        if not member_permission or member_permission.role == Role.GUEST.value:
            raise ModificationNotAllowedException(user_id=user_id)

    @staticmethod
    def validate_workspace_member_is_active(workspace_member_id: int,
                                            workspace_member_storage: WorkspaceMemberStorageInterface):
        workspace_member_data = workspace_member_storage.get_workspace_member_by_id(
            workspace_member_id=workspace_member_id)

        if not workspace_member_data.is_active:
            raise InactiveWorkspaceMemberException(
                workspace_member_id=workspace_member_id)

    @staticmethod
    def validate_account_is_active(account_id: str,
                                   account_storage: AccountStorageInterface):
        account_data = account_storage.get_account_by_id(account_id=account_id)

        if not account_data:
            raise AccountNotFoundException(account_id=account_id)

        if not account_data.is_active:
            raise InactiveAccountException(account_id=account_id)

    @staticmethod
    def validate_user_access_for_account(user_id: str, account_id: str,
                                         account_member_storage: AccountMemberStorageInterface):
        account_user_data = account_member_storage.get_user_permission_for_account(
            user_id=user_id, account_id=account_id)
        if account_user_data.role == Role.GUEST.value:
            raise ModificationNotAllowedException(user_id=user_id)

    @staticmethod
    def validate_user_access_for_workspace(user_id: str, workspace_id: str,
                                           workspace_member_storage: WorkspaceMemberStorageInterface):
        workspace_user_data = workspace_member_storage.get_workspace_member(
            user_id=user_id, workspace_id=workspace_id)

        if workspace_user_data.role == Role.GUEST.value:
            raise ModificationNotAllowedException(user_id=user_id)

    @staticmethod
    def validate_role(role: str):
        existed_roles = [x.value for x in Role]
        if role not in existed_roles:
            raise UnexpectedRoleException(role=role)

    @staticmethod
    def validate_field(field_id: str, field_storage: FieldStorageInterface):
        is_exist = field_storage.is_field_exists(field_id=field_id)

        if not is_exist:
            raise FieldNotFoundException(field_id=field_id)
