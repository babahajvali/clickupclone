from typing import Any, Dict

from task_management.exceptions.enums import FieldType
from task_management.interactors.fields.validators.dropdown_validator import \
    DropdownValidator
from task_management.interactors.fields.validators.number_validator import \
    NumberValidator
from task_management.interactors.fields.validators.text_validator import \
    TextValidator


class FieldConfigValidator:

    def check_field_config(
            self, field_type: FieldType, config: Dict[str, Any]) -> None:
        handler = self.get_config_validation_handler(
            field_type=field_type
        )
        if handler:
            handler(config=config)

    @staticmethod
    def get_config_validation_handler(field_type: FieldType):
        validation_handlers = {
            FieldType.DROPDOWN: DropdownValidator().validate_config,
            FieldType.TEXT: TextValidator().validate_config,
            FieldType.NUMBER: NumberValidator().validate_config,
        }
        return validation_handlers.get(field_type)

    @staticmethod
    def get_value_validation_handler(field_type: FieldType):
        validation_handlers = {
            FieldType.TEXT: TextValidator().validate_value,
            FieldType.NUMBER: NumberValidator().validate_value,
            FieldType.DROPDOWN: DropdownValidator().validate_value,
        }
        return validation_handlers.get(field_type)
