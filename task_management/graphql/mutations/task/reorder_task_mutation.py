import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import TaskNotFoundType, \
    DeletedTaskType, ModificationNotAllowedType, InvalidOrderType, \
    UserNotWorkspaceMemberType
from task_management.graphql.types.input_types import ReorderTaskInputParams
from task_management.graphql.types.response_types import ReorderTaskResponse
from task_management.graphql.types.types import TaskType
from task_management.interactors.tasks.reorder_task_interactor import \
    ReorderTaskInteractor
from task_management.storages import TaskStorage, WorkspaceStorage


class ReorderTaskMutation(graphene.Mutation):
    class Arguments:
        params = ReorderTaskInputParams(required=True)

    Output = ReorderTaskResponse

    @staticmethod
    def mutate(root, info, params):
        task_storage = TaskStorage()
        workspace_storage = WorkspaceStorage()

        interactor = ReorderTaskInteractor(
            task_storage=task_storage,
            workspace_storage=workspace_storage
        )

        try:
            result = interactor.reorder_task(
                task_id=params.task_id,
                order=params.order,
                user_id=info.context.user_id
            )

            return TaskType(
                task_id=result.task_id,
                title=result.title,
                description=result.description,
                list_id=result.list_id,
                order=result.order,
                created_by=result.created_by,
                is_deleted=result.is_deleted
            )

        except custom_exceptions.TaskNotFound as e:
            return TaskNotFoundType(task_id=e.task_id)

        except custom_exceptions.DeletedTaskFound as e:
            return DeletedTaskType(task_id=e.task_id)

        except custom_exceptions.ModificationNotAllowed as e:
            return ModificationNotAllowedType(user_id=e.user_id)

        except custom_exceptions.InvalidOrder as e:
            return InvalidOrderType(order=e.order)

        except custom_exceptions.UserNotWorkspaceMember as e:
            return UserNotWorkspaceMemberType(user_id=e.user_id)
