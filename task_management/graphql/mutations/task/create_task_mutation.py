import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import InactiveListType, \
    ListNotFoundType, ModificationNotAllowedType
from task_management.graphql.types.input_types import CreateTaskInputParams
from task_management.graphql.types.response_types import CreateTaskResponse
from task_management.graphql.types.types import TaskType
from task_management.interactors.dtos import CreateTaskDTO
from task_management.interactors.task_interactors.task_interactor import \
    TaskInteractor
from task_management.storages.field_storage import FieldStorage
from task_management.storages.field_value_storage import FieldValueStorage
from task_management.storages.list_storage import ListStorage
from task_management.storages.space_storage import SpaceStorage
from task_management.storages.task_storage import TaskStorage
from task_management.storages.workspace_member import WorkspaceMemberStorage


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
        workspace_member_storage = WorkspaceMemberStorage()
        field_storage = FieldStorage()
        field_value_storage = FieldValueStorage()
        space_storage = SpaceStorage()

        interactor = TaskInteractor(
            list_storage=list_storage,
            task_storage=task_storage,
            workspace_member_storage=workspace_member_storage,
            field_storage=field_storage,
            field_value_storage=field_value_storage,
            space_storage=space_storage,
        )

        try:
            result = interactor.create_task(create_task_dto)

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
