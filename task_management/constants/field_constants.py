from task_management.exceptions.enums import FieldType, FieldConfig

FIELD_TYPE_KEYS = {
    FieldType.TEXT.value: {
        FieldConfig.CONFIG_KEYS.value: {FieldConfig.MAX_LENGTH.value,
                                        FieldConfig.DEFAULT.value},
    },
    FieldType.NUMBER.value: {
        FieldConfig.CONFIG_KEYS.value: {
            FieldConfig.MIN.value, FieldConfig.MAX.value,
            FieldConfig.DEFAULT.value},
    },
    FieldType.DROPDOWN.value: {
        FieldConfig.CONFIG_KEYS.value: {FieldConfig.OPTIONS.value,
                                        FieldConfig.DEFAULT.value},
    },
}

FIXED_FIELDS = [
    {
        "field_type": FieldType.DATE.value,
        "field_name": "Due Date",
        "description": "Due date for complete tasks",
    },
    {
        "field_type": FieldType.DROPDOWN.value,
        "field_name": "Priority",
        "description": "Priority for complete tasks",
        "config": {
            "options": ["Low", "Medium", "High", "Urgent"],
            "default": "Medium"
        }
    },
    {
        "field_type": FieldType.DROPDOWN.value,
        "field_name": "Status",
        "description": "Status for complete tasks",
        "config": {
            "options": ["Todo", "In Progress", "Complete"],
            "default": "Todo"
        }
    }
]
