from abc import abstractmethod

from task_management.exceptions.custom_exceptions import UserNotFoundException, \
    TemplateNotFoundException, UnexpectedFieldTypeFoundException, \
    FieldNameAlreadyExistsException, FieldOrderAlreadyExistsException, \
    NotAccessToModificationException, FieldNotFoundException, \
    InvalidFieldConfigException, InvalidFieldDefaultValueException, \
    AlreadyExistedTemplateNameException, \
    DefaultTemplateAlreadyExistedException, ListNotFoundException, \
    TaskNotFoundException, TaskAssigneeNotFoundException, \
    InactiveTaskFoundException, InactiveListFoundException, \
    SpaceNotFoundException, InactiveSpaceFoundException, \
    FolderNotFoundException, InactiveFolderFoundException, \
    FolderOrderAlreadyExistedException, \
    FolderListOrderAlreadyExistedException, \
    SpaceListOrderAlreadyExistedException, ViewTypeNotFoundException, \
    ViewNotFoundException, SpaceOrderAlreadyExistedException, \
    WorkspaceNotFoundException, InactiveWorkspaceFoundException, \
    InactiveUserFoundException, UserNotWorkspaceOwnerException
from task_management.exceptions.enums import PermissionsEnum, FieldTypeEnum, \
    ViewTypeEnum, RoleEnum
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
from task_management.interactors.storage_interface.task_assignee_storage_interface import \
    TaskAssigneeStorageInterface
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

FIELD_TYPE_RULES = {
    FieldTypeEnum.Text: {
        "config_keys": {"max_length"},
        "default_type": str,
        "default_required": False,
    },
    FieldTypeEnum.Number: {
        "config_keys": {"min", "max"},
        "default_type": (int, float),
        "default_required": False,
    },
    FieldTypeEnum.Dropdown: {
        "config_keys": {"options"},
        "default_type": str,
        "default_required": False,
    },
    FieldTypeEnum.Date: {
        "config_keys": set(),
        "default_type": str,
        "default_required": False,
    },
    FieldTypeEnum.Checkbox: {
        "config_keys": set(),
        "default_type": bool,
        "default_required": False,
    },
    FieldTypeEnum.email: {
        "config_keys": set(),
        "default_type": str,
        "default_required": False,
    },
}


class ValidationMixin:

    @staticmethod
    def validate_user_exist_and_status(user_id: str,
                                       user_storage: UserStorageInterface):
        user_data = user_storage.get_user_data(user_id=user_id)

        if not user_data:
            raise UserNotFoundException(user_id=user_id)

        if not user_data.is_active:
            raise InactiveUserFoundException(user_id=user_id)

    @staticmethod
    def check_template_exist(template_id: str,
                             template_storage: TemplateStorageInterface):
        template_data = template_storage.get_template_exist(
            template_id=template_id)

        if not template_data:
            raise TemplateNotFoundException(template_id=template_id)

        return template_data.list_id

    @staticmethod
    def check_field_type(field_type: str):

        field_types = [x.value for x in FieldTypeEnum]

        if field_type not in field_types:
            raise UnexpectedFieldTypeFoundException(field_type=field_type)

    @staticmethod
    def check_already_existed_field_name(field_name: str, template_id: str,
                                         field_storage: FieldStorageInterface):
        is_exist = field_storage.check_field_name_exist(field_name=field_name,
                                                        template_id=template_id)

        if is_exist:
            raise FieldNameAlreadyExistsException(field_name=field_name)

    @staticmethod
    def check_field_name_exist(field_id: str, field_name: str,
                               template_id: str,
                               field_storage: FieldStorageInterface):

        is_field_name_exist = field_storage.check_field_name_except_this_field(
            field_id=field_id, field_name=field_name, template_id=template_id)

        if is_field_name_exist:
            raise FieldNameAlreadyExistsException(field_name=field_name)

    @staticmethod
    def check_field_order_is_valid(field_order: int, template_id: str,
                                   field_storage: FieldStorageInterface):

        is_exist = field_storage.check_field_order_exist(
            field_order=field_order, template_id=template_id)

        if is_exist:
            raise FieldOrderAlreadyExistsException(field_order=field_order)

    @staticmethod
    def check_user_has_access_to_create_field(user_id: str,
                                              permission_storage: SpacePermissionStorageInterface):

        user_permissions = permission_storage.get_user_access_permissions(
            user_id=user_id)

        if user_permissions == PermissionsEnum.VIEW:
            raise NotAccessToModificationException(user_id=user_id)

    @staticmethod
    def validate_field(field_id: str, template_id: str,
                       field_storage: FieldStorageInterface):
        is_exist = field_storage.check_field_exist(field_id=field_id,
                                                   template_id=template_id)

        if not is_exist:
            raise FieldNotFoundException(field_id=field_id)

    @staticmethod
    def validate_field_config_and_default(field_type: FieldTypeEnum,
                                          config: dict):

        if isinstance(field_type, FieldTypeEnum):
            field_type_value = field_type
        else:
            try:
                field_type_value = FieldTypeEnum(field_type)
            except ValueError:
                raise UnexpectedFieldTypeFoundException(
                    field_type=field_type.value)

        default_value = config.get("default")

        if field_type_value not in FIELD_TYPE_RULES:
            raise UnexpectedFieldTypeFoundException(
                field_type=field_type_value.value
            )

        rules = FIELD_TYPE_RULES[field_type_value]

        allowed_keys = rules["config_keys"]
        invalid_keys = set(config.keys()) - allowed_keys

        if invalid_keys:
            raise InvalidFieldConfigException(
                field_type=field_type.value,
                invalid_keys=list(invalid_keys)
            )

        if field_type == FieldTypeEnum.Dropdown:
            if "options" not in config or not config["options"]:
                raise InvalidFieldConfigException(
                    field_type=field_type.value,
                    message="Dropdown must have non-empty options"
                )

        if default_value is not None:
            expected_type = rules["default_type"]

            if not isinstance(default_value, expected_type):
                raise InvalidFieldDefaultValueException(
                    field_type=field_type.value,
                    default_value=default_value
                )

            if field_type == FieldTypeEnum.Dropdown:
                if default_value not in config.get("options", []):
                    raise InvalidFieldDefaultValueException(
                        field_type=field_type.value,
                        message="Default value must be one of dropdown options"
                    )

        if field_type_value == FieldTypeEnum.Number and default_value is not None:
            min_val = config.get("min")
            max_val = config.get("max")

            if min_val is not None and default_value < min_val:
                raise InvalidFieldDefaultValueException(
                    field_type=field_type_value.value,
                    message=f"Default value {default_value} is less than minimum {min_val}"
                )

            if max_val is not None and default_value > max_val:
                raise InvalidFieldDefaultValueException(
                    field_type=field_type_value.value,
                    message=f"Default value {default_value} is greater than maximum {max_val}"
                )

        if field_type_value == FieldTypeEnum.Text and default_value is not None:
            max_length = config.get("max_length")

            if max_length is not None and len(default_value) > max_length:
                raise InvalidFieldDefaultValueException(
                    field_type=field_type_value.value,
                    message=f"Default value length {len(default_value)} exceeds max_length {max_length}"
                )

    @staticmethod
    def check_already_existed_template_name(template_name: str,
                                            template_storage: TemplateStorageInterface):

        is_exist = template_storage.check_template_name_exist(
            template_name=template_name)

        if is_exist:
            raise AlreadyExistedTemplateNameException(
                template_name=template_name)


    @staticmethod
    def check_default_template_exists(template_name: str,
                                      template_storage: TemplateStorageInterface):
        is_exist = template_storage.check_default_template_exist()

        if is_exist:
            raise DefaultTemplateAlreadyExistedException(
                template_name=template_name)

    @staticmethod
    def check_list_exists_and_status(list_id: str,
                                     list_storage: ListStorageInterface):
        list_data = list_storage.get_list(list_id=list_id)

        if not list_data:
            raise ListNotFoundException(list_id=list_id)

        if not list_data.is_active:
            raise InactiveListFoundException(list_id=list_id)

    @staticmethod
    def check_template_name_exist(template_name: str, template_id: str,
                                  template_storage: TemplateStorageInterface):
        is_exist = template_storage.check_template_name_exist_except_this_template(
            template_name=template_name, template_id=template_id)

        if is_exist:
            raise AlreadyExistedTemplateNameException(
                template_name=template_name)

    @staticmethod
    def check_user_has_access_to_create_task(user_id: str,
                                             permission_storage: SpacePermissionStorageInterface):
        user_permissions = permission_storage.get_user_access_permissions(
            user_id=user_id)

        if user_permissions == PermissionsEnum.VIEW.value:
            raise NotAccessToModificationException(user_id=user_id)

    @staticmethod
    def check_user_has_access_to_list_modification(user_id: str, list_id: str,
                                                   permission_storage: ListPermissionStorageInterface):
        user_permissions = permission_storage.get_user_permission_for_list(
            user_id=user_id, list_id=list_id)

        if user_permissions == PermissionsEnum.VIEW.value:
            raise NotAccessToModificationException(user_id=user_id)

    @staticmethod
    def validate_task_exists(task_id: str, task_storage: TaskStorageInterface)-> str:

        task_data = task_storage.get_task_by_id(task_id=task_id)

        if not task_data:
            raise TaskNotFoundException(task_id=task_id)

        if not task_data.is_active:
            raise InactiveTaskFoundException(task_id=task_id)

        return task_data.list_id

    @staticmethod
    def check_task_assignee_exists(assign_id: str,
                                   task_assignee_storage: TaskAssigneeStorageInterface):
        is_exist = task_assignee_storage.check_task_assignee_exist(
            assign_id=assign_id)

        if not is_exist:
            raise TaskAssigneeNotFoundException(assign_id=assign_id)

    @staticmethod
    def validate_space_exist_and_status(space_id: str,
                                        space_storage: SpaceStorageInterface):

        space_data = space_storage.get_space(space_id=space_id)

        if not space_data:
            raise SpaceNotFoundException(space_id=space_id)

        if not space_data.is_active:
            raise InactiveSpaceFoundException(space_id=space_id)

    @staticmethod
    def validate_folder_exist_and_status(folder_id: str,
                                         folder_storage: FolderStorageInterface):
        folder_data = folder_storage.get_folder(folder_id=folder_id)

        if not folder_data:
            raise FolderNotFoundException(folder_id=folder_id)

        if not folder_data.is_active:
            raise InactiveFolderFoundException(folder_id=folder_id)

    @staticmethod
    def validate_list_order_in_folder(order: int, folder_id: str,
                                      list_storage: ListStorageInterface):
        is_order_exist = list_storage.check_list_order_exist_in_folder(
            order=order, folder_id=folder_id)

        if is_order_exist:
            raise FolderListOrderAlreadyExistedException(folder_id=folder_id)

    @staticmethod
    def validate_list_order_in_space(order: int, space_id: str,
                                     list_storage: ListStorageInterface):
        is_order_exist = list_storage.check_list_order_exist_in_space(
            order=order, space_id=space_id)

        if is_order_exist:
            raise SpaceListOrderAlreadyExistedException(space_id=space_id)

    @staticmethod
    def check_user_has_access_to_folder_modification(user_id: str,
                                                     folder_id: str,
                                                     permission_storage: FolderPermissionStorageInterface):

        user_permissions = permission_storage.get_user_permission_for_folder(
            user_id=user_id, folder_id=folder_id)

        if user_permissions == PermissionsEnum.VIEW.value:
            raise NotAccessToModificationException(user_id=user_id)

    @staticmethod
    def validate_folder_order(order: int, space_id: str,
                              folder_storage: FolderStorageInterface):
        is_order_exist = folder_storage.check_order_exist(order=order,
                                                          space_id=space_id)

        if is_order_exist:
            raise FolderOrderAlreadyExistedException(space_id=space_id)

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
    def check_user_has_access_to_space_modification(user_id: str,
                                                    space_id: str,
                                                    permission_storage: SpacePermissionStorageInterface):

        user_permissions = permission_storage.get_user_permission_for_space(
            user_id=user_id, space_id=space_id)

        if user_permissions == PermissionsEnum.VIEW.value:
            raise NotAccessToModificationException(user_id=user_id)

    @staticmethod
    def check_space_order_exist(workspace_id: str, order: int,
                                space_storage: SpaceStorageInterface):
        is_space_order_exist = space_storage.check_space_order_exist(
            order=order, workspace_id=workspace_id)

        if is_space_order_exist:
            raise SpaceOrderAlreadyExistedException(workspace_id=workspace_id)

    @staticmethod
    def validate_workspace_exist_and_status(workspace_id: str,
                                            workspace_storage: WorkspaceStorageInterface):
        workspace_data = workspace_storage.get_workspace(
            workspace_id=workspace_id)

        if not workspace_data:
            raise WorkspaceNotFoundException(workspace_id=workspace_id)

        if not workspace_data.is_active:
            raise InactiveWorkspaceFoundException(workspace_id=workspace_id)

    @staticmethod
    def check_user_owner_of_workspace(user_id: str, workspace_id: str,
                                      workspace_storage: WorkspaceStorageInterface):
        is_owner = workspace_storage.validate_workspace_owner(
            workspace_id=workspace_id, user_id=user_id)

        if not is_owner:
            raise UserNotWorkspaceOwnerException(user_id=user_id)

    @staticmethod
    def validate_user_owner_or_editor_access(
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
            raise InactiveWorkspaceFoundException(workspace_id=workspace_id)

        if workspace_data.owner_id == user_id:
            return

        member_permission = workspace_member_storage.get_workspace_member(
            workspace_id=workspace_id,
            user_id=user_id
        )

        if not member_permission or member_permission.role == RoleEnum.GUEST.value:
            raise NotAccessToModificationException(user_id=user_id)
