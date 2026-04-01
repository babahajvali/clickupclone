import graphene

from task_management.graphql.mutations.field.exception_handlers import (
    handle_field_exceptions, DELETE_FIELD_EXCEPTIONS)
from task_management.graphql.types.input_types import DeleteFieldInputParams
from task_management.graphql.types.response_types import DeleteFieldResponse
from task_management.graphql.types.types import FieldType
from task_management.interactors.fields.delete_field_interactor import \
    DeleteFieldInteractor
from task_management.storages import FieldStorage, WorkspaceStorage


class DeleteFieldMutation(graphene.Mutation):
    class Arguments:
        params = DeleteFieldInputParams(required=True)

    Output = DeleteFieldResponse

    @staticmethod
    @handle_field_exceptions(DELETE_FIELD_EXCEPTIONS)
    def mutate(root, info, params):
        field_storage = FieldStorage()
        workspace_storage = WorkspaceStorage()

        interactor = DeleteFieldInteractor(
            field_storage=field_storage,
            workspace_storage=workspace_storage,
        )

        field_dto = interactor.delete_field(
            field_id=params.field_id,
            user_id=info.context.user_id
        )

        return FieldType.from_dto(field_dto)
