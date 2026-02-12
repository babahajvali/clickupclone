from task_management.graphql.types.types import TaskFieldValuesType, \
    FieldValuesType, TasksValuesType
from task_management.storages.field_storage import FieldStorage


def get_task_field_values_resolver(root, info,params):
    task_ids = params.task_ids

    storage = FieldStorage()

    values_data = storage.get_field_values_by_task_ids(task_ids)

    result = [
        TaskFieldValuesType(
            task_id=task_data.task_id,
            values=[
                FieldValuesType(
                    field_id=v.field_id,
                    value=v.value
                )
                for v in task_data.values
            ]
        )
        for task_data in values_data
    ]

    return TasksValuesType(task_values=result)

