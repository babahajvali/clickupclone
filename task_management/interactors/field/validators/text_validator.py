from task_management.constants.field_constants import FIELD_TYPE_KEYS
from task_management.exceptions.custom_exceptions import \
    InvalidFieldDefaultValue, InvalidFieldValue, \
    InvalidFieldConfig
from task_management.exceptions.enums import FieldConfig, FieldType


class TextField:

    @staticmethod
    def check_text_config(config: dict):

        allowed_keys = FIELD_TYPE_KEYS[FieldType.TEXT.value][
            FieldConfig.CONFIG_KEYS.value]
        invalid_keys = set(config.keys()) - allowed_keys
        if invalid_keys:
            raise InvalidFieldConfig(
                field_type=FieldType.TEXT.value,
                invalid_keys=list(invalid_keys))

        default_value = config.get(FieldConfig.DEFAULT.value)
        is_default_value_provided = default_value is not None
        if not is_default_value_provided:
            return

        max_length = config.get(FieldConfig.MAX_LENGTH.value)
        is_exceeds_max_length = max_length is not None and len(
            default_value) > max_length
        if is_exceeds_max_length:
            raise InvalidFieldDefaultValue(
                field_type=FieldType.TEXT.value,
                message=f"Default value length {len(default_value)} exceeds max_length {max_length}")

    @staticmethod
    def validate_text_field(value: str, config: dict):
        """Validate text field value against max_length constraint."""
        max_length = config.get(FieldConfig.MAX_LENGTH.value)
        if max_length and len(value) > max_length:
            raise InvalidFieldValue(
                message=f"Text exceeds maximum length of {max_length} characters")