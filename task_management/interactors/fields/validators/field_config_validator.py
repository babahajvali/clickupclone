from task_management.exceptions.enums import FieldType
from task_management.interactors.fields.validators.dropdown_validator import \
    DropdownField
from task_management.interactors.fields.validators.number_validator import \
    NumberField
from task_management.interactors.fields.validators.text_validator import \
    TextField


class FieldConfigValidator:

    @staticmethod
    def check_field_config(field_type: FieldType, config: dict):
        validation_handlers = {
            FieldType.DROPDOWN: DropdownField.check_dropdown_config,
            FieldType.TEXT: TextField.check_text_config,
            FieldType.NUMBER: NumberField.check_number_config,
        }

        handler = validation_handlers.get(field_type)
        if handler:
            handler(config=config)
