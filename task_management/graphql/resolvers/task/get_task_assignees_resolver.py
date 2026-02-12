from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import TaskNotFoundType, \
    DeletedTaskType
from task_management.graphql.types.types import TaskAssigneeType, \
    TaskAssigneesType
from task_management.interactors.task.task_assignee_interactor import \
    TaskAssigneeInteractor
from task_management.storages.list_storage import ListStorage
from task_management.storages.space_storage import SpaceStorage
from task_management.storages.task_assignee_storage import TaskAssigneeStorage
from task_management.storages.task_storage import TaskStorage
from task_management.storages.user_storage import UserStorage
from task_management.storages.workspace_storage import WorkspaceStorage


def get_task_assignees_resolver(root,info,params):
    task_id = params.task_id

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
        workspace_storage=workspace_storage
    )

    try:
        assignees_data = interactor.get_task_assignees(task_id=task_id)

        result = [ TaskAssigneeType(
            assign_id=each.assign_id,
            user_id=each.user_id,
            task_id=each.task_id,
            is_active=each.is_active,
            assigned_by=each.assigned_by
        ) for each in assignees_data]

        return TaskAssigneesType(assignees=result)
    except custom_exceptions.TaskNotFoundException as e:
        return TaskNotFoundType(task_id=e.task_id)
    except custom_exceptions.DeletedTaskException as e:
        return DeletedTaskType(task_id=e.task_id)