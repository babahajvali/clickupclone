import graphene

from task_management.graphql.mutations.field.exception_handlers import (
    handle_field_exceptions, REORDER_FIELD_EXCEPTIONS)
from task_management.graphql.types.input_types import ReorderFieldInputParams
from task_management.graphql.types.response_types import ReorderFieldResponse
from task_management.graphql.types.types import FieldType
from task_management.interactors.fields.reorder_field_interactor import \
    ReorderFieldInteractor
from task_management.storages import FieldStorage, TemplateStorage, \
    WorkspaceStorage


class ReorderFieldMutation(graphene.Mutation):
    class Arguments:
        params = ReorderFieldInputParams(required=True)

    Output = ReorderFieldResponse

    @staticmethod
    @handle_field_exceptions(REORDER_FIELD_EXCEPTIONS)
    def mutate(root, info, params):
        field_storage = FieldStorage()
        template_storage = TemplateStorage()
        workspace_storage = WorkspaceStorage()

        interactor = ReorderFieldInteractor(
            field_storage=field_storage,
            template_storage=template_storage,
            workspace_storage=workspace_storage,
        )

        field_dto = interactor.reorder_field(
            field_id=params.field_id,
            template_id=params.template_id,
            new_order=params.new_order,
            user_id=info.context.user_id
        )

        return FieldType.from_dto(field_dto)
