from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import InactiveListType, \
    ListNotFoundType
from task_management.graphql.types.types import TaskAssigneeType, \
    TaskAssigneesType
from task_management.interactors.task_interactors.task_assignee_interactor import \
    TaskAssigneeInteractor
from task_management.storages.list_permission_storage import \
    ListPermissionStorage
from task_management.storages.list_storage import ListStorage
from task_management.storages.task_assignee_storage import TaskAssigneeStorage
from task_management.storages.task_storage import TaskStorage
from task_management.storages.user_storage import UserStorage


def get_list_task_assignees_resolver(root,info, params):
    list_id = params.list_id

    user_storage = UserStorage()
    task_storage = TaskStorage()
    list_permission_storage = ListPermissionStorage()
    task_assignee_storage = TaskAssigneeStorage()
    list_storage = ListStorage()

    interactor = TaskAssigneeInteractor(
        user_storage=user_storage,
        task_storage=task_storage,
        permission_storage=list_permission_storage,
        task_assignee_storage=task_assignee_storage,
        list_storage=list_storage,
    )

    try:
        assignees_data = interactor.get_list_task_assignees(list_id=list_id)

        result = [TaskAssigneeType(
            assign_id=each.assign_id,
            user_id=each.user_id,
            task_id=each.task_id,
            is_active=each.is_active,
            assigned_by=each.assigned_by
        ) for each in assignees_data]

        return TaskAssigneesType(assignees=result)
    except custom_exceptions.InactiveListException as e:
        return InactiveListType(list_id=e.list_id)
    except custom_exceptions.ListNotFoundException as e:
        return ListNotFoundType(list_id=e.list_id)