from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import UserNotFoundType, \
    InactiveUserType
from task_management.graphql.types.types import GetUserTaskType, TaskType
from task_management.interactors.tasks.get_user_tasks_interactor import \
    GetUserTasksInteractor
from task_management.storages import UserStorage, TaskStorage


def get_user_tasks_resolver(root, info, params):
    user_id = params.user_id

    user_storage = UserStorage()
    task_storage = TaskStorage()

    interactor = GetUserTasksInteractor(
        user_storage=user_storage,
        task_storage=task_storage,
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
                    is_deleted=task.is_deleted,
                )
                for task in result.tasks
            ]
        )
    except custom_exceptions.UserNotFound as e:
        return UserNotFoundType(user_id=e.user_id)

    except custom_exceptions.InactiveUser as e:
        return InactiveUserType(user_id=e.user_id)
