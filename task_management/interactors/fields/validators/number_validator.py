from typing import Dict

from task_management.constants.field_constants import FIELD_TYPE_KEYS
from task_management.exceptions.custom_exceptions import \
    UnexpectedFieldConfigKeys, NumberDefaultValueBelowMinimum, \
    NumberDefaultValueAboveMaximum, MaxValueLessThanMinValue, \
    NumberValueBelowMinimum, InvalidNumberFieldValue, NumberValueExceedsMaximum
from task_management.exceptions.enums import FieldConfig, FieldType


class NumberField:

    def check_number_config(self, config: Dict):

        self._validate_unexpected_config_keys(config=config)

        min_val = config.get(FieldConfig.MIN.value)
        max_val = config.get(FieldConfig.MAX.value)

        self._validate_max_not_less_than_min(max_val=max_val, min_val=min_val)

        self._validate_default_value_within_range(
            config=config, max_val=max_val, min_val=min_val)

    def _validate_default_value_within_range(
            self, config: Dict, max_val: int | None, min_val: int | None):
        default_value = config.get(FieldConfig.DEFAULT.value)
        is_default_value_provided = default_value is not None
        if not is_default_value_provided:
            return

        self._validate_default_value_not_below_minimum(default_value, min_val)
        self._validate_default_value_not_above_maximum(default_value, max_val)

    @staticmethod
    def _validate_default_value_not_below_minimum(
            default_value: int, min_val: int | None):
        is_below_minimum = min_val is not None and default_value < min_val
        if is_below_minimum:
            raise NumberDefaultValueBelowMinimum(
                message=f"Default value {default_value} is less "
                        f"than minimum {min_val}")

    @staticmethod
    def _validate_default_value_not_above_maximum(
            default_value: int, max_val: int | None):
        is_above_maximum = max_val is not None and default_value > max_val
        if is_above_maximum:
            raise NumberDefaultValueAboveMaximum(
                message=f"Default value {default_value} is greater "
                        f"than maximum {max_val}")

    @staticmethod
    def _validate_max_not_less_than_min(
            max_val: int | None, min_val: int | None):
        is_min_max_both_provided = min_val is not None and max_val is not None
        if not is_min_max_both_provided:
            return

        is_max_less_than_min = max_val < min_val
        if is_max_less_than_min:
            raise MaxValueLessThanMinValue(
                field_type=FieldType.NUMBER.value,
                message=f"max {max_val} must be greater than or equal to min {min_val}")

    @staticmethod
    def _validate_unexpected_config_keys(config: Dict):
        allowed_keys = FIELD_TYPE_KEYS[FieldType.NUMBER.value][
            FieldConfig.CONFIG_KEYS.value]
        invalid_keys = set(config.keys()) - allowed_keys
        if invalid_keys:
            raise UnexpectedFieldConfigKeys(
                field_type=FieldType.NUMBER.value,
                invalid_keys=list(invalid_keys))

    def check_number_value_within_range(self, value: str, config: Dict):
        numeric_value = self._validate_number_value_is_numeric(value)
        self._validate_number_value_not_below_minimum(numeric_value, config)
        self._validate_number_value_not_exceeds_maximum(numeric_value, config)

    @staticmethod
    def _validate_number_value_is_numeric(value: str) -> float:
        try:
            return float(value)
        except (ValueError, TypeError):
            raise InvalidNumberFieldValue(
                message="Number fields value must be a valid number")

    @staticmethod
    def _validate_number_value_not_below_minimum(
            numeric_value: float, config: Dict):
        min_value = config.get(FieldConfig.MIN.value)
        if min_value is not None and numeric_value < min_value:
            raise NumberValueBelowMinimum(
                message=f"Number must be at least {min_value}")

    @staticmethod
    def _validate_number_value_not_exceeds_maximum(
            numeric_value: float, config: Dict):
        max_value = config.get(FieldConfig.MAX.value)
        if max_value is not None and numeric_value > max_value:
            raise NumberValueExceedsMaximum(
                message=f"Number must not exceed {max_value}")
