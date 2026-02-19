from task_management.exceptions.enums import FieldTypes

FIELD_TYPE_RULES = {
    FieldTypes.TEXT.value: {
        "config_keys": {"max_length", "default"},
    },
    FieldTypes.NUMBER.value: {
        "config_keys": {"min", "max", "default"},
    },
    FieldTypes.DROPDOWN.value: {
        "config_keys": {"options", "default"},
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
            "options": ["Low", "Medium", "High","Urgent"],
            "default": "Medium"
        }
    },
    {
        "field_type": FieldTypes.DROPDOWN.value,
        "field_name": "Status",
        "description": "Status for complete task",
        "config": {
            "options": ["Todo", "In Progress", "Complete"],
            "default": "Todo"
        }
    }
]
