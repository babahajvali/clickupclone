from task_management.exceptions.enums import FieldType
from task_management.interactors.fields.validators.dropdown_validator import \
    DropdownField
from task_management.interactors.fields.validators.number_validator import \
    NumberField
from task_management.interactors.fields.validators.text_validator import \
    TextField


class FieldValueValidator:

    @staticmethod
    def validate_field_value(field_type: str, value: str, config: dict):
        validation_handlers = {
            FieldType.TEXT.value: TextField.validate_text_field,
            FieldType.NUMBER.value: NumberField.validate_number_field,
            FieldType.DROPDOWN.value: DropdownField.validate_dropdown_field,
        }

        handler = validation_handlers.get(field_type)
        if handler:
            handler(value=value, config=config)
