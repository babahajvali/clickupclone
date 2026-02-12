from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import UserNotFoundType, \
    InactiveUserType
from task_management.graphql.types.types import GetUserTaskType, TaskType
from task_management.interactors.task.task_assignee_interactor import \
    TaskAssigneeInteractor
from task_management.storages.list_storage import ListStorage
from task_management.storages.space_storage import SpaceStorage
from task_management.storages.task_assignee_storage import TaskAssigneeStorage
from task_management.storages.task_storage import TaskStorage
from task_management.storages.user_storage import UserStorage
from task_management.storages.workspace_storage import WorkspaceStorage


def get_user_tasks_resolver(root, info,params):
    user_id = params.user_id

    user_storage = UserStorage()
    task_storage = TaskStorage()
    task_assignee_storage = TaskAssigneeStorage()
    list_storage = ListStorage()
    space_storage = SpaceStorage()
    workspace_storage = WorkspaceStorage()

    interactor = TaskAssigneeInteractor(
        user_storage=user_storage,
        task_storage=task_storage,
        task_assignee_storage=task_assignee_storage,
        list_storage=list_storage,
        space_storage=space_storage,
        workspace_storage=workspace_storage,
    )

    try:
        result = interactor.get_user_assigned_tasks(user_id=user_id)

        return GetUserTaskType(
            user_id=result.user_id,
            tasks=[
                TaskType(
                    task_id=task.task_id,
                    title=task.title,
                    description=task.description,
                    list_id=task.list_id,
                    order=task.order,
                    created_by=task.created_by,
                    is_delete=task.is_deleted,
                )
                for task in result.tasks
            ]
        )
    except custom_exceptions.UserNotFoundException as e:
        return UserNotFoundType(user_id=e.user_id)
    except custom_exceptions.InactiveUserException as e:
        return InactiveUserType(user_id=e.user_id)
