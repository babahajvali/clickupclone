import graphene

from django.core.exceptions import ObjectDoesNotExist
from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import TaskNotFoundType, \
    DeletedTaskType, ModificationNotAllowedType
from task_management.graphql.types.input_types import DeleteTaskInputParams
from task_management.graphql.types.response_types import DeleteTaskResponse
from task_management.graphql.types.types import TaskType
from task_management.interactors.task_interactors.task_interactor import \
    TaskInteractor
from task_management.storages.field_value_storage import FieldValueStorage
from task_management.storages.task_storage import TaskStorage
from task_management.storages.list_storage import ListStorage
from task_management.storages.list_permission_storage import ListPermissionStorage
from task_management.storages.field_storage import FieldStorage


class DeleteTaskMutation(graphene.Mutation):
    class Arguments:
        params = DeleteTaskInputParams(required=True)

    Output = DeleteTaskResponse

    @staticmethod
    def mutate(root, info, params):
        task_storage = TaskStorage()
        list_storage = ListStorage()
        permission_storage = ListPermissionStorage()
        field_storage = FieldStorage()
        field_value_storage = FieldValueStorage()

        interactor = TaskInteractor(
            task_storage=task_storage,
            list_storage=list_storage,
            permission_storage=permission_storage,
            field_storage=field_storage,
            field_value_storage=field_value_storage
        )

        try:
            result = interactor.delete_task(
                task_id=params.task_id,
                user_id=params.user_id
            )

            return TaskType(
                task_id=str(result.task_id),
                title=result.title,
                description=result.description,
                list_id=str(result.list_id),
                order=result.order,
                created_by=str(result.created_by),
                is_delete=result.is_deleted
            )


        except custom_exceptions.TaskNotFoundException as e:
            return TaskNotFoundType(task_id=e.task_id)

        except custom_exceptions.DeletedTaskException as e:
            return DeletedTaskType(task_id=e.task_id)

        except custom_exceptions.ModificationNotAllowedException as e:
            return ModificationNotAllowedType(user_id=e.user_id)