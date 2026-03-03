import pytest

from task_management.exceptions.custom_exceptions import (
    UnexpectedFieldConfigKeys,
    MaxValueLessThanMinValue,
    NumberDefaultValueBelowMinimum,
    NumberDefaultValueAboveMaximum,
    InvalidNumberFieldValue,
    NumberValueBelowMinimum,
    NumberValueExceedsMaximum,
)
from task_management.exceptions.enums import FieldConfig
from task_management.interactors.fields.validators.number_validator import \
    NumberField


class TestNumberField:

    def setup_method(self):
        self.number_field = NumberField()

    def test_invalid_config_keys(self):
        config = {
            "wrong_key": 10
        }

        with pytest.raises(UnexpectedFieldConfigKeys):
            self.number_field.check_number_config(config)

    def test_max_less_than_min(self):
        config = {
            FieldConfig.MIN.value: 10,
            FieldConfig.MAX.value: 5
        }

        with pytest.raises(MaxValueLessThanMinValue):
            self.number_field.check_number_config(config)

    def test_default_less_than_min(self):
        config = {
            FieldConfig.MIN.value: 5,
            FieldConfig.MAX.value: 20,
            FieldConfig.DEFAULT.value: 2
        }

        with pytest.raises(NumberDefaultValueBelowMinimum):
            self.number_field.check_number_config(config)

    def test_default_greater_than_max(self):
        config = {
            FieldConfig.MIN.value: 5,
            FieldConfig.MAX.value: 20,
            FieldConfig.DEFAULT.value: 25
        }

        with pytest.raises(NumberDefaultValueAboveMaximum):
            self.number_field.check_number_config(config)

    def test_default_value_exact_min(self):
        config = {
            FieldConfig.MIN.value: 5,
            FieldConfig.MAX.value: 20,
            FieldConfig.DEFAULT.value: 5
        }

        self.number_field.check_number_config(config)

    def test_valid_number_config(self):
        config = {
            FieldConfig.MIN.value: 5,
            FieldConfig.MAX.value: 20,
            FieldConfig.DEFAULT.value: 10
        }

        self.number_field.check_number_config(config)

    def test_invalid_number_value_not_numeric(self):
        config = {}

        with pytest.raises(InvalidNumberFieldValue):
            NumberField.check_number_field_value("abc", config)

    def test_number_below_min(self):
        config = {
            FieldConfig.MIN.value: 10
        }

        with pytest.raises(NumberValueBelowMinimum):
            NumberField.check_number_field_value("5", config)

    def test_number_above_max(self):
        config = {
            FieldConfig.MAX.value: 100
        }

        with pytest.raises(NumberValueExceedsMaximum):
            NumberField.check_number_field_value("150", config)

    def test_valid_number_value(self):
        config = {
            FieldConfig.MIN.value: 5,
            FieldConfig.MAX.value: 20
        }

        NumberField.check_number_field_value("10", config)
