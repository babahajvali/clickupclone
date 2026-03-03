from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import TaskNotFoundType, \
    DeletedTaskType
from task_management.graphql.types.types import TaskAssigneeType, \
    TaskAssigneesType
from task_management.interactors.tasks.get_task_assignees_interactor import \
    GetTaskAssigneesInteractor
from task_management.storages import TaskStorage


def get_task_assignees_resolver(root, info, params):
    task_id = params.task_id

    task_storage = TaskStorage()

    interactor = GetTaskAssigneesInteractor(
        task_storage=task_storage,
    )

    try:
        assignees_data = interactor.get_task_assignees(task_id=task_id)

        result = [TaskAssigneeType(
            assign_id=each.assign_id,
            user_id=each.user_id,
            task_id=each.task_id,
            is_active=each.is_active,
            assigned_by=each.assigned_by
        ) for each in assignees_data]

        return TaskAssigneesType(assignees=result)
    except custom_exceptions.TaskNotFound as e:
        return TaskNotFoundType(task_id=e.task_id)
    except custom_exceptions.DeletedTaskFound as e:
        return DeletedTaskType(task_id=e.task_id)
