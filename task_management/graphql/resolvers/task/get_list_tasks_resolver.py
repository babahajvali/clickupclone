from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import ListNotFoundType, \
    InactiveListType
from task_management.graphql.types.types import TaskType, TasksType
from task_management.interactors.task_interactors.task_interactor import \
    TaskInteractor

from task_management.storages.task_storage import TaskStorage
from task_management.storages.list_storage import ListStorage
from task_management.storages.list_permission_storage import ListPermissionStorage
from task_management.storages.field_storage import FieldStorage
from task_management.storages.field_value_storage import FieldValueStorage


def get_list_tasks_resolver(root, info, params):
    list_id = params.list_id

    task_storage = TaskStorage()
    list_storage = ListStorage()
    permission_storage = ListPermissionStorage()
    field_storage = FieldStorage()
    field_value_storage = FieldValueStorage()

    interactor = TaskInteractor(
        task_storage=task_storage,
        list_storage=list_storage,
        permission_storage=permission_storage,
        field_storage=field_storage,
        field_value_storage=field_value_storage
    )

    try:
        tasks_data = interactor.get_list_tasks(list_id=list_id)

        tasks_output = [
            TaskType(
                task_id=str(task.task_id),
                title=task.title,
                description=task.description,
                list_id=str(task.list_id),
                order=task.order,
                created_by=str(task.created_by),
                is_delete=task.is_deleted
            ) for task in tasks_data
        ]

        return TasksType(tasks=tasks_output)

    except custom_exceptions.ListNotFoundException as e:
        return ListNotFoundType(list_id=e.list_id)

    except custom_exceptions.InactiveListException as e:
        return InactiveListType(list_id=e.list_id)
