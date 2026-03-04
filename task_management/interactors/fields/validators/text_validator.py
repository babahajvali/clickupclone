from typing import Dict

from task_management.constants.field_constants import FIELD_TYPE_KEYS
from task_management.exceptions.custom_exceptions import \
    UnexpectedFieldConfigKeys, TextDefaultValueExceedsMaxLength, \
    TextValueExceedsMaxLength
from task_management.exceptions.enums import FieldConfig, FieldType


class TextField:

    def check_text_config(self, config: dict):

        self._validate_config_keys(config=config)
        self._validate_default_value(config=config)

    @staticmethod
    def _validate_default_value(config: Dict):
        default_value = config.get(FieldConfig.DEFAULT.value)
        is_default_value_provided = default_value is not None
        if not is_default_value_provided:
            return

        max_length = config.get(FieldConfig.MAX_LENGTH.value)
        is_exceeds_max_length = max_length is not None and len(
            default_value) > max_length
        if is_exceeds_max_length:
            raise TextDefaultValueExceedsMaxLength(
                message=f"Default value length {len(default_value)}"
                        f" exceeds max_length {max_length}")

    @staticmethod
    def _validate_config_keys(config: Dict):
        allowed_keys = FIELD_TYPE_KEYS[FieldType.TEXT.value][
            FieldConfig.CONFIG_KEYS.value]
        invalid_keys = set(config.keys()) - allowed_keys
        if invalid_keys:
            raise UnexpectedFieldConfigKeys(
                field_type=FieldType.TEXT.value,
                invalid_keys=list(invalid_keys))

    @staticmethod
    def check_text_field_value(value: str, config: Dict):
        """Validate text fields value against max_length constraint."""
        max_length = config.get(FieldConfig.MAX_LENGTH.value)
        if max_length and len(value) > max_length:
            raise TextValueExceedsMaxLength(
                message=f"Text exceeds maximum length of {max_length} "
                        f"characters")
