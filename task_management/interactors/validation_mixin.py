from task_management.exceptions.custom_exceptions import UserNotFoundException, \
    TemplateNotFoundException, UnexpectedFieldTypeFoundException, \
    FieldNameAlreadyExistsException, FieldOrderAlreadyExistsException, \
    NotAccessToCreationException, FieldNotFoundException, \
    InvalidFieldConfigException, InvalidFieldDefaultValueException, \
    AlreadyExistedTemplateNameException, \
    DefaultTemplateAlreadyExistedException, ListNotFoundException
from task_management.interactors.dtos import FieldTypeEnum, PermissionsEnum
from task_management.interactors.storage_interface.field_storage_interface import \
    FieldStorageInterface
from task_management.interactors.storage_interface.list_storage_interface import \
    ListStorageInterface
from task_management.interactors.storage_interface.permission_storage_interface import \
    PermissionStorageInterface
from task_management.interactors.storage_interface.template_storage_interface import \
    TemplateStorageInterface
from task_management.interactors.storage_interface.user_storage_interface import \
    UserStorageInterface

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
    def check_user_exist(user_id: str, user_storage: UserStorageInterface):
        is_exist = user_storage.check_user_exist(user_id=user_id)

        if not is_exist:
            raise UserNotFoundException(user_id=user_id)

    @staticmethod
    def check_template_exist(template_id: str,
                             template_storage: TemplateStorageInterface):
        is_exist = template_storage.check_template_exist(
            template_id=template_id)

        if not is_exist:
            raise TemplateNotFoundException(template_id=template_id)

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
                                              permission_storage: PermissionStorageInterface):

        user_permissions = permission_storage.get_user_access_permissions(
            user_id=user_id)

        if user_permissions == PermissionsEnum.GUEST:
            raise NotAccessToCreationException(user_id=user_id)

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
    def check_user_has_access_to_create_template(user_id: str,
                                                 permission_storage: PermissionStorageInterface):
        user_permissions = permission_storage.get_user_access_permissions(
            user_id=user_id)

        if user_permissions == PermissionsEnum.GUEST.value:
            raise NotAccessToCreationException(user_id=user_id)

    @staticmethod
    def check_default_template_exists(template_name: str,
                                      template_storage: TemplateStorageInterface):
        is_exist = template_storage.check_default_template_exist()

        if is_exist:
            raise DefaultTemplateAlreadyExistedException(
                template_name=template_name)

    @staticmethod
    def check_list_exists(list_id: str, list_storage: ListStorageInterface):
        is_exist = list_storage.check_list_exist(list_id=list_id)

        if not is_exist:
            raise ListNotFoundException(list_id=list_id)

    @staticmethod
    def check_template_name_exist(template_name: str, template_id: str,
                                  template_storage: TemplateStorageInterface):
        is_exist = template_storage.check_template_name_exist_except_this_template(
            template_name=template_name, template_id=template_id)

        if is_exist:
            raise AlreadyExistedTemplateNameException(
                template_name=template_name)
