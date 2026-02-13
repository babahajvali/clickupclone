import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import InactiveListType, \
    ListNotFoundType, ModificationNotAllowedType, TaskNotFoundType, \
    DeletedTaskType
from task_management.graphql.types.input_types import UpdateTaskInputParams
from task_management.graphql.types.response_types import UpdateTaskResponse
from task_management.graphql.types.types import TaskType
from task_management.interactors.task.task_interactor import TaskInteractor
from task_management.storages.list_storage import ListStorage
from task_management.storages.space_storage import SpaceStorage
from task_management.storages.task_storage import TaskStorage
from task_management.storages.workspace_storage import WorkspaceStorage


class UpdateTaskMutation(graphene.Mutation):
    class Arguments:
        params = UpdateTaskInputParams(required=True)

    Output = UpdateTaskResponse

    @staticmethod
    def mutate(root, info, params):
        list_storage = ListStorage()
        task_storage = TaskStorage()
        space_storage = SpaceStorage()
        workspace_storage = WorkspaceStorage()

        interactor = TaskInteractor(
            list_storage=list_storage,
            task_storage=task_storage,
            space_storage=space_storage,
            workspace_storage=workspace_storage,
        )
        try:
            result = interactor.update_task(
                task_id=params.task_id, name=params.name,
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
        except custom_exceptions.InactiveListException as e:
            return InactiveListType(list_id=e.list_id)
        except custom_exceptions.ListNotFoundException as e:
            return ListNotFoundType(list_id=e.list_id)
        except custom_exceptions.ModificationNotAllowedException as e:
            return ModificationNotAllowedType(user_id=e.user_id)
        except custom_exceptions.TaskNotFoundException as e:
            return TaskNotFoundType(task_id=e.task_id)
        except custom_exceptions.DeletedTaskException as e:
            return DeletedTaskType(task_id=e.task_id)
