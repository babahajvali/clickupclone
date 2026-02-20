from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import InactiveListType, \
    ListNotFoundType
from task_management.graphql.types.types import TaskAssigneeType, \
    TaskAssigneesType
from task_management.interactors.tasks.task_assignee_interactor import \
    TaskAssigneeInteractor
from task_management.storages import UserStorage, TaskStorage, WorkspaceStorage


def get_list_task_assignees_resolver(root,info, params):
    list_id = params.list_id

    user_storage = UserStorage()
    task_storage = TaskStorage()
    workspace_storage = WorkspaceStorage()

    interactor = TaskAssigneeInteractor(
        user_storage=user_storage,
        task_storage=task_storage,
        workspace_storage=workspace_storage
    )

    try:
        assignees_data = interactor.get_assignees_for_list_tasks(list_id=list_id)

        result = [TaskAssigneeType(
            assign_id=each.assign_id,
            user_id=each.user_id,
            task_id=each.task_id,
            is_active=each.is_active,
            assigned_by=each.assigned_by
        ) for each in assignees_data]

        return TaskAssigneesType(assignees=result)
    except custom_exceptions.InactiveList as e:
        return InactiveListType(list_id=e.list_id)
    except custom_exceptions.ListNotFound as e:
        return ListNotFoundType(list_id=e.list_id)