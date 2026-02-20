from task_management.constants.field_constants import FIELD_TYPE_KEYS
from task_management.exceptions.custom_exceptions import \
    InvalidFieldConfig, InvalidFieldDefaultValue, \
    InvalidFieldValue
from task_management.exceptions.enums import FieldConfig, FieldType


class NumberField:

    @staticmethod
    def check_number_config(config: dict):

        allowed_keys = FIELD_TYPE_KEYS[FieldType.NUMBER.value][
            FieldConfig.CONFIG_KEYS.value]
        invalid_keys = set(config.keys()) - allowed_keys
        if invalid_keys:
            raise InvalidFieldConfig(
                field_type=FieldType.NUMBER.value,
                invalid_keys=list(invalid_keys))

        min_val = config.get(FieldConfig.MIN.value)
        max_val = config.get(FieldConfig.MAX.value)

        is_min_max_both_provided = min_val is not None and max_val is not None
        if not is_min_max_both_provided:
            return

        is_max_less_than_min = max_val < min_val
        if is_max_less_than_min:
            raise InvalidFieldConfig(
                field_type=FieldType.NUMBER.value,
                message=f"max {max_val} must be greater than or equal to min {min_val}")

        default_value = config.get(FieldConfig.DEFAULT.value)
        is_default_value_provided = default_value is not None
        if not is_default_value_provided:
            return

        is_below_minimum = min_val is not None and default_value < min_val
        if is_below_minimum:
            raise InvalidFieldDefaultValue(
                field_type=FieldType.NUMBER.value,
                message=f"Default value {default_value} is less than minimum {min_val}")

        is_above_maximum = max_val is not None and default_value > max_val
        if is_above_maximum:
            raise InvalidFieldDefaultValue(
                field_type=FieldType.NUMBER.value,
                message=f"Default value {default_value} is greater than maximum {max_val}")

    @staticmethod
    def validate_number_field(value, config: dict):
        try:
            numeric_value = float(value)
        except (ValueError, TypeError):
            raise InvalidFieldValue(
                message="Number field value must be a valid number")

        min_value = config.get(FieldConfig.MIN.value)
        if min_value is not None and numeric_value < min_value:
            raise InvalidFieldValue(
                message=f"Number must be at least {min_value}")

        max_value = config.get(FieldConfig.MAX.value)
        if max_value is not None and numeric_value > max_value:
            raise InvalidFieldValue(
                message=f"Number must not exceed {max_value}")
