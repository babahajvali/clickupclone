from typing import Any, Dict

from task_management.exceptions.enums import FieldType
from task_management.interactors.fields.validators.dropdown_validator import (
    DropdownValidator,
)
from task_management.interactors.fields.validators.number_validator import (
    NumberValidator,
)
from task_management.interactors.fields.validators.text_validator import (
    TextValidator,
)


class FieldConfigValidator:

    @staticmethod
    def check_field_config(field_type: FieldType, config: Dict[str, Any]) -> None:
        validation_handlers = {
            FieldType.DROPDOWN: DropdownValidator().validate_config,
            FieldType.TEXT: TextValidator().validate_config,
            FieldType.NUMBER: NumberValidator().validate_config,
        }

        handler = validation_handlers.get(field_type)
        if handler:
            handler(config=config)
