import graphene

from task_management.graphql.mutations.field.exception_handlers import (
    handle_field_exceptions, UPDATE_FIELD_EXCEPTIONS)
from task_management.graphql.types.input_types import UpdateFieldInputParams
from task_management.graphql.types.response_types import UpdateFieldResponse
from task_management.graphql.types.types import FieldType
from task_management.interactors.dtos import UpdateFieldDTO
from task_management.interactors.fields.update_field_interactor import \
    UpdateFieldInteractor
from task_management.storages import FieldStorage, WorkspaceStorage


class UpdateFieldMutation(graphene.Mutation):
    class Arguments:
        params = UpdateFieldInputParams(required=True)

    Output = UpdateFieldResponse

    @staticmethod
    @handle_field_exceptions(UPDATE_FIELD_EXCEPTIONS)
    def mutate(root, info, params):
        field_storage = FieldStorage()
        workspace_storage = WorkspaceStorage()

        interactor = UpdateFieldInteractor(
            field_storage=field_storage,
            workspace_storage=workspace_storage,
        )

        update_field_dto = UpdateFieldDTO(
            field_id=params.field_id,
            description=params.description,
            field_name=params.field_name,
            config=params.config,
            is_required=params.is_required
        )

        field_dto = interactor.update_field(
            update_field_dto=update_field_dto,
            user_id=info.context.user_id
        )

        return FieldType.from_dto(field_dto)
