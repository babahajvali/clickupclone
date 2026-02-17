import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import TaskNotFoundType, \
    DeletedTaskType, ModificationNotAllowedType
from task_management.graphql.types.input_types import DeleteTaskInputParams
from task_management.graphql.types.response_types import DeleteTaskResponse
from task_management.graphql.types.types import TaskType
from task_management.interactors.task.task_interactor import \
    TaskInteractor
from task_management.storages import ListStorage, TaskStorage, WorkspaceStorage


class DeleteTaskMutation(graphene.Mutation):
    class Arguments:
        params = DeleteTaskInputParams(required=True)

    Output = DeleteTaskResponse

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
            result = interactor.delete_task(
                task_id=params.task_id,
                user_id=info.context.user_id
            )

            return TaskType(
                task_id=result.task_id,
                title=result.title,
                description=result.description,
                list_id=result.list_id,
                order=result.order,
                created_by=result.created_by,
                is_delete=result.is_deleted
            )


        except custom_exceptions.TaskNotFoundException as e:
            return TaskNotFoundType(task_id=e.task_id)

        except custom_exceptions.DeletedTaskException as e:
            return DeletedTaskType(task_id=e.task_id)

        except custom_exceptions.ModificationNotAllowedException as e:
            return ModificationNotAllowedType(user_id=e.user_id)
