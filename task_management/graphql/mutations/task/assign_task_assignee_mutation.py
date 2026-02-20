import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import UserNotFoundType, \
    TaskNotFoundType, DeletedTaskType, InactiveUserType, \
    ModificationNotAllowedType
from task_management.graphql.types.input_types import \
    CreateTaskAssigneeInputParams
from task_management.graphql.types.response_types import \
    CreateTaskAssigneeResponse
from task_management.graphql.types.types import TaskAssigneeType
from task_management.interactors.task.task_assignee_interactor import \
    TaskAssigneeInteractor
from task_management.storages import UserStorage, TaskStorage, WorkspaceStorage


class AssignTaskAssigneeMutation(graphene.Mutation):
    class Arguments:
        params = CreateTaskAssigneeInputParams(required=True)

    Output = CreateTaskAssigneeResponse

    @staticmethod
    def mutate(root, info, params):
        user_storage = UserStorage()
        task_storage = TaskStorage()
        workspace_storage = WorkspaceStorage()

        interactor = TaskAssigneeInteractor(
            user_storage=user_storage,
            task_storage=task_storage,
            workspace_storage=workspace_storage
        )

        try:
            result = interactor.assign_task_assignee(
                task_id=params.task_id, user_id=params.user_id,
                assigned_by=info.context.user_id)

            return TaskAssigneeType(
                assign_id=result.assign_id,
                user_id=result.user_id,
                task_id=result.task_id,
                is_active=result.is_active,
                assigned_by=result.assigned_by
            )

        except custom_exceptions.UserNotFound as e:
            return UserNotFoundType(user_id=e.user_id)
        except custom_exceptions.TaskNotFound as e:
            return TaskNotFoundType(task_id=e.task_id)
        except custom_exceptions.DeletedTaskFound as e:
            return DeletedTaskType(task_id=e.task_id)
        except custom_exceptions.InactiveUser as e:
            return InactiveUserType(user_id=e.user_id)
        except custom_exceptions.ModificationNotAllowed as e:
            return ModificationNotAllowedType(user_id=e.user_id)
