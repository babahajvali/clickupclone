import pytest

from task_management.exceptions.custom_exceptions import (
    UnexpectedFieldConfigKeys,
    TextDefaultValueExceedsMaxLength,
    TextValueExceedsMaxLength,
)
from task_management.exceptions.enums import FieldConfig
from task_management.interactors.fields.validators.text_validator import \
    TextField


class TestTextField:

    def setup_method(self):
        self.text_field = TextField()

    def test_invalid_config_keys(self):
        config = {
            "wrong_key": "value"
        }

        with pytest.raises(UnexpectedFieldConfigKeys):
            self.text_field.check_text_config(config)

    def test_default_exceeds_max_length(self):
        config = {
            FieldConfig.MAX_LENGTH.value: 5,
            FieldConfig.DEFAULT.value: "TooLongText"
        }

        with pytest.raises(TextDefaultValueExceedsMaxLength):
            self.text_field.check_text_config(config)

    def test_valid_text_config(self):
        config = {
            FieldConfig.MAX_LENGTH.value: 10,
            FieldConfig.DEFAULT.value: "Hello"
        }

        self.text_field.check_text_config(config)

    def test_default_not_provided(self):
        config = {
            FieldConfig.MAX_LENGTH.value: 5
        }

        self.text_field.check_text_config(config)

    def test_text_value_exceeds_max_length(self):
        config = {
            FieldConfig.MAX_LENGTH.value: 5
        }

        with pytest.raises(TextValueExceedsMaxLength):
            TextField.check_text_field_value("TooLongText", config)

    def test_valid_text_value(self):
        config = {
            FieldConfig.MAX_LENGTH.value: 10
        }

        TextField.check_text_field_value("Hello", config)

    def test_no_max_length_provided(self):
        config = {}

        TextField.check_text_field_value("AnyLengthIsFine", config)
