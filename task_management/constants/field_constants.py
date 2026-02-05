from task_management.exceptions.enums import FieldTypes

FIELD_TYPE_RULES = {
    FieldTypes.TEXT.value: {
        "config_keys": {"max_length", "default"},
        "default_type": str,
    },
    FieldTypes.USER.value: {
        "config_keys": {"multiple", "allow_groups"},
    },
    FieldTypes.NUMBER.value: {
        "config_keys": {"min", "max", "default"},
        "default_type": (int, float),
    },
    FieldTypes.DROPDOWN.value: {
        "config_keys": {"options", "default"},
    },
    FieldTypes.DATE.value: {
        "config_keys": set("default"),
    },
    FieldTypes.CHECKBOX.value: {
        "config_keys": set("default"),
    },
    FieldTypes.EMAIL.value: {
        "config_keys": set("default"),
    },
}

FIXED_FIELDS = [
    {
        "field_type": FieldTypes.DATE.value,
        "field_name": "Due Date",
        "description": "Due date for complete task",
    },
    {
        "field_type": FieldTypes.DROPDOWN.value,
        "field_name": "Priority",
        "description": "Priority for complete task",
        "config": {
            "options": ["Low", "Medium", "High"],
            "default": "Medium"
        }
    },
    {
        "field_type": FieldTypes.DROPDOWN.value,
        "field_name": "Status",
        "description": "Status for complete task",
        "config": {
            "options": ["Todo", "In Progress", "Done"],
            "default": "Todo"
        }
    }
]
