from task_management.exceptions.enums import FieldTypeEnum

FIELD_TYPE_RULES = {
    FieldTypeEnum.TEXT.value: {
        "config_keys": {"max_length", "default"},
        "default_type": str,
        "default_required": False,
    },
    FieldTypeEnum.USER.value: {
        "config_keys": {"multiple", "allow_groups"},
        "default_type": str,
        "default_required": False,
    },
    FieldTypeEnum.NUMBER.value: {
        "config_keys": {"min", "max", "default"},
        "default_type": (int, float),
        "default_required": False,
    },
    FieldTypeEnum.DROPDOWN.value: {
        "config_keys": {"options", "default"},
        "default_type": str,
        "default_required": False,
    },
    FieldTypeEnum.DATE.value: {
        "config_keys": set("default"),
        "default_type": str,
        "default_required": False,
    },
    FieldTypeEnum.CHECKBOX.value: {
        "config_keys": set("default"),
        "default_type": bool,
        "default_required": False,
    },
    FieldTypeEnum.EMAIL.value: {
        "config_keys": set("default"),
        "default_type": str,
        "default_required": False,
    },
}


FIXED_FIELDS = [
    {
        "field_type": FieldTypeEnum.DATE.value,
        "field_name": "Due Date",
        "description": "Due date for complete task",
    },
    {
        "field_type": FieldTypeEnum.DROPDOWN.value,
        "field_name": "Priority",
        "config": {
            "options": ["Low", "Medium", "High"],
            "default": "Medium"
        }
    },
    {
        "field_type": FieldTypeEnum.DROPDOWN.value,
        "field_name": "Status",
        "config": {
            "options": ["Todo", "In Progress", "Done"],
            "default": "Todo"
        }
    }
]
