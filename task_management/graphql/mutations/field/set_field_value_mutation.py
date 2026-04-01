import graphene

from task_management.graphql.mutations.field.exception_handlers import (
    handle_field_exceptions, SET_FIELD_VALUE_EXCEPTIONS)
from task_management.graphql.types.input_types import SetFieldValuesInputParams
from task_management.graphql.types.response_types import \
    SetTaskFieldValueResponse
from task_management.graphql.types.types import FieldValueType
from task_management.interactors.dtos import UpdateFieldValueDTO
from task_management.interactors.fields.field_response_interactor import \
    FieldResponseInteractor
from task_management.storages import FieldStorage, TaskStorage, \
    WorkspaceStorage


class SetFieldValueMutation(graphene.Mutation):
    class Arguments:
        params = SetFieldValuesInputParams(required=True)

    Output = SetTaskFieldValueResponse

    @staticmethod
    @handle_field_exceptions(SET_FIELD_VALUE_EXCEPTIONS)
    def mutate(root, info, params):
        field_storage = FieldStorage()
        task_storage = TaskStorage()
        workspace_storage = WorkspaceStorage()

        interactor = FieldResponseInteractor(
            field_storage=field_storage,
            task_storage=task_storage,
            workspace_storage=workspace_storage
        )

        update_data = UpdateFieldValueDTO(
            task_id=params.task_id,
            field_id=params.field_id,
            value=params.value,
        )

        task_field_value_dto = interactor.set_task_field_response(
            update_field_value_dto=update_data,
            user_id=info.context.user_id,
        )

        return FieldValueType(
            id=task_field_value_dto.id,
            task_id=task_field_value_dto.task_id,
            field_id=task_field_value_dto.field_id,
            value=task_field_value_dto.value
        )
