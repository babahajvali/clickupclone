from task_management.constants.field_constants import FIELD_TYPE_RULES
from task_management.exceptions.custom_exceptions import \
    UnsupportedFieldTypeException, FieldNameAlreadyExistsException, \
    InvalidFieldDefaultValueException, InvalidFieldConfigException, \
    FieldNotFoundException, InactiveFieldException
from task_management.exceptions.enums import FieldTypes
from task_management.interactors.storage_interfaces import \
    FieldStorageInterface


class FieldValidationMixin:

    def __init__(self, field_storage: FieldStorageInterface, **kwargs):
        self.field_storage = field_storage
        super().__init__(**kwargs)

    @staticmethod
    def check_field_type(field_type: str):
        field_types = FieldTypes.get_values()

        if field_type not in field_types:
            raise UnsupportedFieldTypeException(field_type=field_type)

    def validate_field_name_not_exists(self, field_name: str,
                                       template_id: str):
        is_exist = self.field_storage.is_field_name_exists(
            field_name=field_name, template_id=template_id)

        if is_exist:
            raise FieldNameAlreadyExistsException(field_name=field_name)

    def validate_field_is_active(self, field_id: str):
        field_data = self.field_storage.get_field_by_id(field_id=field_id)

        if not field_data:
            raise FieldNotFoundException(field_id=field_id)

        if not field_data.is_active:
            raise InactiveFieldException(field_id=field_id)


    def check_field_name_in_db_except_current_field(
            self, field_id: str, field_name: str, template_id: str):

        try:
            field_data = self.field_storage.get_field_by_name(
                field_name=field_name, template_id=template_id)

            if field_data.field_id != field_id:
                raise FieldNameAlreadyExistsException(field_name=field_name)
        except FieldNotFoundException:
            raise FieldNotFoundException(field_id=field_id)

    @staticmethod
    def validate_field_config(field_type: str, config: dict):
        default_value = config.get("default")

        rules = FIELD_TYPE_RULES[field_type]

        allowed_keys = rules["config_keys"]
        invalid_keys = set(config.keys()) - allowed_keys

        if invalid_keys:
            raise InvalidFieldConfigException(
                field_type=field_type,
                invalid_keys=list(invalid_keys)
            )

        if field_type == FieldTypes.DROPDOWN.value:
            if "options" not in config or not config["options"]:
                raise InvalidFieldConfigException(
                    field_type=field_type,
                    message="Dropdown must have non-empty options"
                )

        if default_value is not None:
            if field_type == FieldTypes.DROPDOWN.value:
                if default_value not in config.get("options", []):
                    raise InvalidFieldDefaultValueException(
                        field_type=field_type,
                        message="Default value must be one of dropdown options"
                    )

        if field_type == FieldTypes.NUMBER.value and default_value is not None:
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

        if field_type == FieldTypes.TEXT.value and default_value is not None:
            max_length = config.get("max_length")

            if max_length is not None and len(default_value) > max_length:
                raise InvalidFieldDefaultValueException(
                    field_type=field_type,
                    message=f"Default value length {len(default_value)} exceeds max_length {max_length}"
                )
