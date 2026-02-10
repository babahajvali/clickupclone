import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import TaskNotFoundType, \
    DeletedTaskType, ModificationNotAllowedType, InvalidOrderType
from task_management.graphql.types.input_types import ReorderTaskInputParams
from task_management.graphql.types.response_types import ReorderTaskResponse
from task_management.graphql.types.types import TaskType
from task_management.interactors.task_interactors.task_interactor import \
    TaskInteractor
from task_management.storages.field_value_storage import FieldValueStorage
from task_management.storages.space_storage import SpaceStorage
from task_management.storages.task_storage import TaskStorage
from task_management.storages.list_storage import ListStorage
from task_management.storages.field_storage import FieldStorage
from task_management.storages.workspace_member import WorkspaceMemberStorage


class ReorderTaskMutation(graphene.Mutation):
    class Arguments:
        params = ReorderTaskInputParams(required=True)

    Output = ReorderTaskResponse

    @staticmethod
    def mutate(root, info, params):
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
                is_delete=result.is_deleted
            )

        except custom_exceptions.TaskNotFoundException as e:
            return TaskNotFoundType(task_id=e.task_id)

        except custom_exceptions.DeletedTaskException as e:
            return DeletedTaskType(task_id=e.task_id)

        except custom_exceptions.ModificationNotAllowedException as e:
            return ModificationNotAllowedType(user_id=e.user_id)

        except custom_exceptions.InvalidOrderException as e:
            return InvalidOrderType(order=e.order)
