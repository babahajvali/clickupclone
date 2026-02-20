from task_management.exceptions.custom_exceptions import \
    MissingFieldConfig
from task_management.exceptions.enums import FieldType
from task_management.interactors.field.validators.dropdown_validator import \
    DropdownField
from task_management.interactors.field.validators.text_validator import \
    TextField
from task_management.interactors.field.validators.number_validator import \
    NumberField


class FieldConfigValidator:

    def check_config(self, config: dict, field_type: FieldType):

        mandatory_config_field_types = FieldType.mandatory_config_field_type()

        is_mandatory_config_field_type = (
                field_type.value in mandatory_config_field_types)
        if is_mandatory_config_field_type:
            self.check_mandatory_config_is_not_empty(
                config=config, field_type=field_type.value
            )

        if config:
            self.check_field_config(field_type=field_type, config=config)

    @staticmethod
    def check_field_config(field_type: FieldType, config: dict):

        validation_handlers = {
            FieldType.DROPDOWN: DropdownField.check_dropdown_config_data,
            FieldType.TEXT: TextField.check_text_config,
            FieldType.NUMBER: NumberField.check_number_config,
        }

        handler = validation_handlers.get(field_type)
        if handler:
            handler(config=config)

    @staticmethod
    def check_mandatory_config_is_not_empty(config: dict, field_type: str):

        is_empty_config = not config or config == {}
        if is_empty_config:
            raise MissingFieldConfig(
                field_type=field_type)
