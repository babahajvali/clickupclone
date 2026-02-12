from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import ListNotFoundType, \
    InactiveListType
from task_management.graphql.types.types import TaskType, TasksType
from task_management.interactors.task.task_interactor import \
    TaskInteractor
from task_management.storages.space_storage import SpaceStorage

from task_management.storages.task_storage import TaskStorage
from task_management.storages.list_storage import ListStorage
from task_management.storages.workspace_storage import WorkspaceStorage


def get_list_tasks_resolver(root, info, params):
    list_id = params.list_id

    list_storage = ListStorage()
    task_storage = TaskStorage()
    space_storage = SpaceStorage()
    workspace_storage = WorkspaceStorage()

    interactor = TaskInteractor(
        list_storage=list_storage,
        task_storage=task_storage,
        space_storage=space_storage,
        workspace_storage=workspace_storage,
    )

    try:
        tasks_data = interactor.get_list_tasks(list_id=list_id)

        tasks_output = [
            TaskType(
                task_id=task.task_id,
                title=task.title,
                description=task.description,
                list_id=task.list_id,
                order=task.order,
                created_by=task.created_by,
                is_delete=task.is_deleted
            ) for task in tasks_data
        ]

        return TasksType(tasks=tasks_output)

    except custom_exceptions.ListNotFoundException as e:
        return ListNotFoundType(list_id=e.list_id)

    except custom_exceptions.InactiveListException as e:
        return InactiveListType(list_id=e.list_id)
