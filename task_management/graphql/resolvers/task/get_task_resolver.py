from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import TaskNotFoundType, \
    DeletedTaskType
from task_management.graphql.types.types import TaskType
from task_management.interactors.tasks.get_task_interactor import \
    GetTaskInteractor
from task_management.storages import TaskStorage


def get_task_resolver(root, info, params):
    task_id = params.task_id

    task_storage = TaskStorage()

    interactor = GetTaskInteractor(
        task_storage=task_storage,
    )

    try:
        task_data = interactor.get_task(task_id=task_id)

        task_output = TaskType(
            task_id=task_data.task_id,
            title=task_data.title,
            description=task_data.description,
            list_id=task_data.list_id,
            order=task_data.order,
            created_by=task_data.created_by,
            is_deleted=task_data.is_deleted
        )

        return task_output

    except custom_exceptions.TaskNotFound as e:
        return TaskNotFoundType(task_id=e.task_id)

    except custom_exceptions.DeletedTaskFound as e:
        return DeletedTaskType(task_id=e.task_id)
