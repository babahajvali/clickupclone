import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import TaskNotFoundType, \
    DeletedTaskType, ModificationNotAllowedType, TaskAssigneeNotFoundType
from task_management.graphql.types.input_types import \
    RemoveTaskAssigneeInputParams
from task_management.graphql.types.response_types import \
    RemoveTaskAssigneeResponse
from task_management.graphql.types.types import TaskAssigneeType
from task_management.interactors.task.task_assignee_interactor import \
    TaskAssigneeInteractor
from task_management.storages.list_storage import ListStorage
from task_management.storages.space_storage import SpaceStorage
from task_management.storages.task_assignee_storage import TaskAssigneeStorage
from task_management.storages.task_storage import TaskStorage
from task_management.storages.user_storage import UserStorage
from task_management.storages.workspace_storage import WorkspaceStorage


class RemoveTaskAssigneeMutation(graphene.Mutation):
    class Arguments:
        params = RemoveTaskAssigneeInputParams(required=True)

    Output = RemoveTaskAssigneeResponse

    @staticmethod
    def mutate(root, info, params):
        user_storage = UserStorage()
        task_storage = TaskStorage()
        task_assignee_storage = TaskAssigneeStorage()
        list_storage = ListStorage()
        workspace_storage = WorkspaceStorage()
        space_storage = SpaceStorage()

        interactor = TaskAssigneeInteractor(
            user_storage=user_storage,
            task_storage=task_storage,
            task_assignee_storage=task_assignee_storage,
            list_storage=list_storage,
            space_storage=space_storage,
            workspace_storage=workspace_storage
        )

        try:
            result = interactor.remove_task_assignee(
                assign_id=params.assign_id, user_id=info.context.user_id)

            return TaskAssigneeType(
                assign_id=result.assign_id,
                user_id=result.user_id,
                task_id=result.task_id,
                is_active=result.is_active,
                assigned_by=result.assigned_by
            )

        except custom_exceptions.TaskNotFoundException as e:
            return TaskNotFoundType(task_id=e.task_id)
        except custom_exceptions.DeletedTaskException as e:
            return DeletedTaskType(task_id=e.task_id)
        except custom_exceptions.ModificationNotAllowedException as e:
            return ModificationNotAllowedType(user_id=e.user_id)
        except custom_exceptions.TaskAssigneeNotFoundException as e:
            return TaskAssigneeNotFoundType(assign_id=e.assign_id)
