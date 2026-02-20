import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import InactiveListType, \
    ListNotFoundType, ModificationNotAllowedType
from task_management.graphql.types.input_types import CreateTaskInputParams
from task_management.graphql.types.response_types import CreateTaskResponse
from task_management.graphql.types.types import TaskType
from task_management.interactors.dtos import CreateTaskDTO
from task_management.interactors.task.task_creation_handler import \
    TaskCreationHandler
from task_management.storages import ListStorage, TaskStorage, \
    WorkspaceStorage, FieldStorage


class CreateTaskMutation(graphene.Mutation):
    class Arguments:
        params = CreateTaskInputParams(required=True)

    Output = CreateTaskResponse

    @staticmethod
    def mutate(root, info, params):
        create_task_dto = CreateTaskDTO(
            title=params.title,
            description=params.description,
            list_id=params.list_id,
            created_by=info.context.user_id
        )

        list_storage = ListStorage()
        task_storage = TaskStorage()
        workspace_storage = WorkspaceStorage()
        field_storage = FieldStorage()

        handler = TaskCreationHandler(
            list_storage=list_storage,
            task_storage=task_storage,
            workspace_storage=workspace_storage,
            field_storage=field_storage
        )

        try:
            result = handler.handle_task(create_task_dto)

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
