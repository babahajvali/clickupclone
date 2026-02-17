from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import TaskNotFoundType, \
    DeletedTaskType
from task_management.graphql.types.types import TaskType
from task_management.interactors.task.task_interactor import \
    TaskInteractor
from task_management.storages import ListStorage, TaskStorage, WorkspaceStorage


def get_task_resolver(root, info, params):
    task_id = params.task_id

    list_storage = ListStorage()
    task_storage = TaskStorage()
    workspace_storage = WorkspaceStorage()

    interactor = TaskInteractor(
        list_storage=list_storage,
        task_storage=task_storage,
        workspace_storage=workspace_storage,
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
            is_delete=task_data.is_deleted
        )

        return task_output

    except custom_exceptions.TaskNotFoundException as e:
        return TaskNotFoundType(task_id=e.task_id)

    except custom_exceptions.DeletedTaskException as e:
        return DeletedTaskType(task_id=e.task_id)
