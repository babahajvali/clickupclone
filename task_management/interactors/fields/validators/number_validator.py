from typing import Any, Dict

from task_management.constants.field_constants import FIELD_TYPE_KEYS
from task_management.exceptions.custom_exceptions import (
    InvalidNumberFieldValue,
    MaxValueLessThanMinValue,
    NumberValueBelowMinimum,
    NumberValueExceedsMaximum,
    UnexpectedFieldConfigKeys,
)
from task_management.exceptions.enums import FieldConfig, FieldType


class NumberValidator:

    def validate_config(self, config: Dict[str, Any]) -> None:
        self._validate_unexpected_config_keys(config)

        min_val = config.get(FieldConfig.MIN.value)
        max_val = config.get(FieldConfig.MAX.value)

        self._validate_max_not_less_than_min(min_val, max_val)
        self._validate_default_value(config, min_val, max_val)

    def _validate_default_value(
        self, config: Dict[str, Any], min_val: Any, max_val: Any
    ) -> None:
        default_value = config.get(FieldConfig.DEFAULT.value)

        if default_value is None:
            return

        self._validate_not_below_min(default_value, min_val)
        self._validate_not_above_max(default_value, max_val)

    @staticmethod
    def _validate_max_not_less_than_min(min_val: Any, max_val: Any) -> None:
        if min_val is None or max_val is None:
            return

        if max_val < min_val:
            raise MaxValueLessThanMinValue(
                field_type=FieldType.NUMBER.value,
                message=f"max {max_val} must be >= min {min_val}",
            )

    def validate_value(self, value: str, config: Dict[str, Any]) -> None:
        numeric_value = self._parse_numeric_value(value)

        min_val = config.get(FieldConfig.MIN.value)
        max_val = config.get(FieldConfig.MAX.value)

        self._validate_not_below_min(numeric_value, min_val)
        self._validate_not_above_max(numeric_value, max_val)

    @staticmethod
    def _parse_numeric_value(value: str) -> float:
        try:
            return float(value)
        except (ValueError, TypeError):
            raise InvalidNumberFieldValue(
                message="Number fields value must be a valid number"
            )

    @staticmethod
    def _validate_not_below_min(value: Any, min_val: Any) -> None:
        if min_val is not None and value < min_val:
            raise NumberValueBelowMinimum(
                message=f"Number must be at least {min_val}"
            )

    @staticmethod
    def _validate_not_above_max(value: Any, max_val: Any) -> None:
        if max_val is not None and value > max_val:
            raise NumberValueExceedsMaximum(
                message=f"Number must not exceed {max_val}"
            )

    @staticmethod
    def _validate_unexpected_config_keys(config: Dict[str, Any]) -> None:
        allowed_keys = FIELD_TYPE_KEYS[FieldType.NUMBER.value][
            FieldConfig.CONFIG_KEYS.value
        ]
        invalid_keys = set(config.keys()) - allowed_keys
        if invalid_keys:
            raise UnexpectedFieldConfigKeys(
                field_type=FieldType.NUMBER.value,
                invalid_keys=list(invalid_keys),
            )
