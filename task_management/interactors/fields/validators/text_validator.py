from typing import Any, Dict

from task_management.constants.field_constants import FIELD_TYPE_KEYS
from task_management.exceptions.custom_exceptions import (
    TextDefaultValueExceedsMaxLength,
    TextValueExceedsMaxLength,
    UnexpectedFieldConfigKeys,
)
from task_management.exceptions.enums import FieldConfig, FieldType


class TextValidator:

    def validate_config(self, config: Dict[str, Any]) -> None:
        self._validate_unexpected_config_keys(config)
        self._validate_default_value_not_exceeds_max_length(config)

    @staticmethod
    def _validate_default_value_not_exceeds_max_length(
        config: Dict[str, Any]
    ) -> None:
        default_value = config.get(FieldConfig.DEFAULT.value)
        if default_value is None:
            return

        max_length = config.get(FieldConfig.MAX_LENGTH.value)
        is_exceeds_max_length = (
            max_length is not None and len(default_value) > max_length
        )
        if is_exceeds_max_length:
            raise TextDefaultValueExceedsMaxLength(
                message=(
                    f"Default value length {len(default_value)} "
                    f"exceeds max_length {max_length}"
                )
            )

    @staticmethod
    def _validate_unexpected_config_keys(config: Dict[str, Any]) -> None:
        allowed_keys = FIELD_TYPE_KEYS[FieldType.TEXT.value][
            FieldConfig.CONFIG_KEYS.value
        ]
        invalid_keys = set(config.keys()) - allowed_keys
        if invalid_keys:
            raise UnexpectedFieldConfigKeys(
                field_type=FieldType.TEXT.value,
                invalid_keys=list(invalid_keys),
            )

    @staticmethod
    def validate_value(value: str, config: Dict[str, Any]) -> None:
        """Validate text fields value against max_length constraint."""
        max_length = config.get(FieldConfig.MAX_LENGTH.value)
        if max_length and len(value) > max_length:
            raise TextValueExceedsMaxLength(
                message=(
                    f"Text exceeds maximum length of {max_length} "
                    f"characters"
                )
            )
