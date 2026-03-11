import pytest

from task_management.exceptions.custom_exceptions import (
    DuplicateDropdownOptions,
    DropdownOptionsEmpty,
    UnexpectedFieldConfigKeys,
    DropdownOptionNotAllowed,
    EmptyDropdownConfig,
    DropdownDefaultValueNotInOptions,
)
from task_management.exceptions.enums import FieldConfig
from task_management.interactors.fields.validators.dropdown_validator import \
    DropdownValidator


class TestDropdownField:

    def setup_method(self):
        self.dropdown = DropdownValidator()

    def test_empty_config(self):
        with pytest.raises(EmptyDropdownConfig):
            self.dropdown.validate_config({})

    def test_invalid_keys(self):
        config = {
            "wrong_key": "value"
        }

        with pytest.raises(UnexpectedFieldConfigKeys):
            self.dropdown.validate_config(config)

    def test_options_missing(self):
        config = {
            FieldConfig.DEFAULT.value: "A"
        }

        with pytest.raises(DropdownOptionsEmpty):
            self.dropdown.validate_config(config)

    def test_options_empty_list(self):
        config = {
            FieldConfig.OPTIONS.value: []
        }

        with pytest.raises(DropdownOptionsEmpty):
            self.dropdown.validate_config(config)

    def test_invalid_default_value(self):
        config = {
            FieldConfig.OPTIONS.value: ["A", "B"],
            FieldConfig.DEFAULT.value: "C"
        }

        with pytest.raises(DropdownDefaultValueNotInOptions):
            self.dropdown.validate_config(config)

    def test_duplicate_options(self):
        config = {
            FieldConfig.OPTIONS.value: ["A", "A"],
            FieldConfig.DEFAULT.value: "A"
        }

        with pytest.raises(DuplicateDropdownOptions):
            self.dropdown.validate_config(config)

    def test_valid_config(self):
        config = {
            FieldConfig.OPTIONS.value: ["A", "B"],
            FieldConfig.DEFAULT.value: "A"
        }

        self.dropdown.validate_config(config)

    def test_invalid_dropdown_value(self):
        config = {
            FieldConfig.OPTIONS.value: ["A", "B"]
        }

        with pytest.raises(DropdownOptionNotAllowed):
            self.dropdown.validate_value("C", config)

    def test_valid_dropdown_value(self):
        config = {
            FieldConfig.OPTIONS.value: ["A", "B"]
        }

        self.dropdown.validate_value("A", config)
