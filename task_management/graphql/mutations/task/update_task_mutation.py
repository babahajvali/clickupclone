import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import InactiveListType, \
    ListNotFoundType, ModificationNotAllowedType, TaskNotFoundType, \
    DeletedTaskType
from task_management.graphql.types.input_types import UpdateTaskInputParams
from task_management.graphql.types.response_types import UpdateTaskResponse
from task_management.graphql.types.types import TaskType
from task_management.interactors.tasks.task_interactor import TaskInteractor
from task_management.storages import ListStorage, TaskStorage, WorkspaceStorage


class UpdateTaskMutation(graphene.Mutation):
    class Arguments:
        params = UpdateTaskInputParams(required=True)

    Output = UpdateTaskResponse

    @staticmethod
    def mutate(root, info, params):
        list_storage = ListStorage()
        task_storage = TaskStorage()
        workspace_storage = WorkspaceStorage()

        interactor = TaskInteractor(
            list_storage=list_storage,
            task_storage=task_storage,
            workspace_storage=workspace_storage,
        )
        try:
            result = interactor.update_task(
                task_id=params.task_id, title=params.title,
                user_id=info.context.user_id,description=params.description)

            return TaskType(
                task_id=result.task_id,
                title=result.title,
                description=result.description,
                order=result.order,
                list_id=result.list_id,
                is_delete=result.is_deleted,
                created_by=result.created_by
            )
        except custom_exceptions.InactiveList as e:
            return InactiveListType(list_id=e.list_id)
        except custom_exceptions.ListNotFound as e:
            return ListNotFoundType(list_id=e.list_id)
        except custom_exceptions.ModificationNotAllowed as e:
            return ModificationNotAllowedType(user_id=e.user_id)
        except custom_exceptions.TaskNotFound as e:
            return TaskNotFoundType(task_id=e.task_id)
        except custom_exceptions.DeletedTaskFound as e:
            return DeletedTaskType(task_id=e.task_id)
