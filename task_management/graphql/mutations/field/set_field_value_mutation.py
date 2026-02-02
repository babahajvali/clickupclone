import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import \
    ModificationNotAllowedType
from task_management.graphql.types.input_types import SetFieldValuesInputParams
from task_management.graphql.types.response_types import \
    SetTaskFieldValueResponse
from task_management.graphql.types.types import FieldValueType
from task_management.interactors.dtos import UpdateFieldValueDTO
from task_management.interactors.field_interactors.field_value_interactor import \
    FieldValueInteractor
from task_management.storages.field_storage import FieldStorage
from task_management.storages.field_value_storage import FieldValueStorage
from task_management.storages.list_permission_storage import \
    ListPermissionStorage
from task_management.storages.task_storage import TaskStorage


class SetFieldValueMutation(graphene.Mutation):
    class Arguments:
        params = SetFieldValuesInputParams(required=True)

    Output = SetTaskFieldValueResponse

    @staticmethod
    def mutate(root, info, params):
        field_storage = FieldStorage()
        field_value_storage = FieldValueStorage()
        permission_storage = ListPermissionStorage()
        task_storage = TaskStorage()

        interactor = FieldValueInteractor(
            field_storage=field_storage,
            permission_storage=permission_storage,
            field_value_storage=field_value_storage,
            task_storage=task_storage,
        )

        update_data = UpdateFieldValueDTO(
            task_id=params.task_id,
            field_id=params.field_id,
            value=params.value,
        )

        try:
            result = interactor.set_task_field_value(
                set_value_data=update_data, user_id=info.context.user_id)

            return FieldValueType(
                id=result.id,
                task_id=result.task_id,
                field_id=result.field_id,
                value=result.value
            )

        except custom_exceptions.ModificationNotAllowedException as exc:
            return ModificationNotAllowedType(user_id=exc.user_id)
