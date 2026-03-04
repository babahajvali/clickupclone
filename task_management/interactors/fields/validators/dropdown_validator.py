from typing import Any

from task_management.constants.field_constants import FIELD_TYPE_KEYS
from task_management.exceptions.custom_exceptions import EmptyFieldConfig, \
    DropdownOptionsEmpty, UnexpectedFieldConfigKeys, \
    DropdownOptionNotAllowed, DropdownDefaultValueNotInOptions
from task_management.exceptions.enums import FieldConfig, FieldType


class DropdownField:

    def check_dropdown_config(self, config: dict):
        self._check_config_not_empty(
            config=config, field_type=FieldType.DROPDOWN.value)

        self._validate_unexpected_config_keys(config)
        options = self._validate_options_not_empty(config=config)

        self._validate_default_value_in_options(config=config, options=options)

    @staticmethod
    def _validate_default_value_in_options(config: dict, options: Any | None):
        default_value = config.get(FieldConfig.DEFAULT.value)
        is_default_value_provided = default_value is not None
        if not is_default_value_provided:
            return

        is_invalid_default = default_value not in options
        if is_invalid_default:
            raise DropdownDefaultValueNotInOptions(
                message="Default value must be one of dropdown options")

    @staticmethod
    def _validate_options_not_empty(config: dict) -> Any | None:
        options = config.get(FieldConfig.OPTIONS.value)

        is_options_empty = not options
        if is_options_empty:
            raise DropdownOptionsEmpty(
                field_type=FieldType.DROPDOWN.value)
        return options

    @staticmethod
    def _validate_unexpected_config_keys(config: dict):
        allowed_keys = FIELD_TYPE_KEYS[FieldType.DROPDOWN.value][
            FieldConfig.CONFIG_KEYS.value]
        invalid_keys = set(config.keys()) - allowed_keys
        if invalid_keys:
            raise UnexpectedFieldConfigKeys(
                field_type=FieldType.DROPDOWN.value,
                invalid_keys=list(invalid_keys))

    @staticmethod
    def check_dropdown_value_in_options(value: str, config: dict):

        options = config.get(FieldConfig.OPTIONS.value, [])

        if value not in options:
            raise DropdownOptionNotAllowed(
                message=f"Invalid option. "
                        f"Option must be one of: {', '.join(options)}")

    @staticmethod
    def _check_config_not_empty(config: dict, field_type: str):

        is_empty_config = not config
        if is_empty_config:
            raise EmptyFieldConfig(
                field_type=field_type)
