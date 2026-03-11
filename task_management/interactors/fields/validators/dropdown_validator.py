from typing import Any, Dict

from task_management.constants.field_constants import FIELD_TYPE_KEYS
from task_management.exceptions.custom_exceptions import (
    DuplicateDropdownOptions,
    DropdownDefaultValueNotInOptions,
    DropdownOptionNotAllowed,
    DropdownOptionsEmpty,
    EmptyDropdownConfig,
    EmptyDropdownOptions,
    UnexpectedFieldConfigKeys,
)
from task_management.exceptions.enums import FieldConfig, FieldType


class DropdownValidator:

    def validate_config(self, config: Dict[str, Any]) -> None:
        self._check_config_not_empty(config)
        self._validate_unexpected_config_keys(config)
        options = self._validate_options_not_empty(config)
        self._validate_options_are_unique(options)
        self._validate_empty_options(options)
        self._validate_default_value_in_options(config, options)

    @staticmethod
    def _validate_default_value_in_options(
            config: Dict[str, Any], options: list[Any]
    ) -> None:
        default_value = config.get(FieldConfig.DEFAULT.value)
        if default_value is None:
            return

        if default_value not in options:
            raise DropdownDefaultValueNotInOptions(
                message="Default value must be one of dropdown options"
            )

    @staticmethod
    def _validate_options_not_empty(config: Dict[str, Any]) -> list[Any]:
        options = config.get(FieldConfig.OPTIONS.value)

        if not options:
            raise DropdownOptionsEmpty(
                message="Dropdown options must not be empty"
            )

        return options

    @staticmethod
    def _validate_options_are_unique(options: list[Any]) -> None:
        unique_options = [str(option).strip() for option in options]
        if len(unique_options) != len(set(unique_options)):
            raise DuplicateDropdownOptions(
                message="Dropdown options must be unique"
            )

    @staticmethod
    def _validate_empty_options(options: list[Any]) -> None:
        empty_options = [
            option for option in options if str(option).strip() == ""
        ]
        if empty_options:
            raise EmptyDropdownOptions(
                message="Dropdown options must not contain empty values"
            )

    @staticmethod
    def _validate_unexpected_config_keys(config: Dict[str, Any]) -> None:
        allowed_keys = FIELD_TYPE_KEYS[FieldType.DROPDOWN.value][
            FieldConfig.CONFIG_KEYS.value
        ]
        invalid_keys = set(config.keys()) - allowed_keys
        if invalid_keys:
            raise UnexpectedFieldConfigKeys(
                field_type=FieldType.DROPDOWN.value,
                invalid_keys=list(invalid_keys),
            )

    @staticmethod
    def validate_value(value: str, config: Dict[str, Any]) -> None:
        options = config.get(FieldConfig.OPTIONS.value, [])

        if value not in options:
            raise DropdownOptionNotAllowed(
                message=(
                    "Invalid option. "
                    f"Option must be one of: {', '.join(options)}"
                )
            )

    @staticmethod
    def _check_config_not_empty(config: Dict[str, Any]) -> None:
        if not config:
            raise EmptyDropdownConfig(field_type=FieldType.DROPDOWN.value)
