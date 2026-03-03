import pytest

from task_management.exceptions.custom_exceptions import (
    DropdownOptionsEmpty,
    InvalidFieldDefaultValue,
    UnexpectedFieldConfigKeys,
    DropdownOptionNotAllowed,
    EmptyFieldConfig
)
from task_management.exceptions.enums import FieldConfig
from task_management.interactors.fields.validators.dropdown_validator import \
    DropdownField


class TestDropdownField:

    def setup_method(self):
        self.dropdown = DropdownField()

    def test_empty_config(self):
        with pytest.raises(EmptyFieldConfig):
            self.dropdown.check_dropdown_config_data({})

    def test_invalid_keys(self):
        config = {
            "wrong_key": "value"
        }

        with pytest.raises(UnexpectedFieldConfigKeys):
            self.dropdown.check_dropdown_config_data(config)

    def test_options_missing(self):
        config = {
            FieldConfig.DEFAULT.value: "A"
        }

        with pytest.raises(DropdownOptionsEmpty):
            self.dropdown.check_dropdown_config_data(config)

    def test_options_empty_list(self):
        config = {
            FieldConfig.OPTIONS.value: []
        }

        with pytest.raises(DropdownOptionsEmpty):
            self.dropdown.check_dropdown_config_data(config)

    def test_invalid_default_value(self):
        config = {
            FieldConfig.OPTIONS.value: ["A", "B"],
            FieldConfig.DEFAULT.value: "C"
        }

        with pytest.raises(InvalidFieldDefaultValue):
            self.dropdown.check_dropdown_config_data(config)

    def test_valid_config(self):
        config = {
            FieldConfig.OPTIONS.value: ["A", "B"],
            FieldConfig.DEFAULT.value: "A"
        }

        self.dropdown.check_dropdown_config_data(config)

    def test_invalid_dropdown_value(self):
        config = {
            FieldConfig.OPTIONS.value: ["A", "B"]
        }

        with pytest.raises(DropdownOptionNotAllowed):
            DropdownField.check_dropdown_field_value("C", config)

    def test_valid_dropdown_value(self):
        config = {
            FieldConfig.OPTIONS.value: ["A", "B"]
        }

        DropdownField.check_dropdown_field_value("A", config)
