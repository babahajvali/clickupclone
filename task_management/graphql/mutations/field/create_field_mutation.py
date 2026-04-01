import graphene

from task_management.exceptions.enums import FieldType as FieldTypeEnum
from task_management.graphql.mutations.field.exception_handlers import (
    handle_field_exceptions, CREATE_FIELD_EXCEPTIONS)
from task_management.graphql.types.input_types import CreateFieldInputParams
from task_management.graphql.types.response_types import CreateFieldResponse
from task_management.graphql.types.types import FieldType
from task_management.interactors.dtos import CreateFieldDTO
from task_management.interactors.fields.create_field_interactor import \
    CreateFieldInteractor
from task_management.storages import FieldStorage, TemplateStorage, \
    WorkspaceStorage


class CreateFieldMutation(graphene.Mutation):
    class Arguments:
        params = CreateFieldInputParams(required=True)

    Output = CreateFieldResponse

    @staticmethod
    @handle_field_exceptions(CREATE_FIELD_EXCEPTIONS)
    def mutate(root, info, params):
        field_storage = FieldStorage()
        template_storage = TemplateStorage()
        workspace_storage = WorkspaceStorage()

        interactor = CreateFieldInteractor(
            field_storage=field_storage,
            template_storage=template_storage,
            workspace_storage=workspace_storage,
        )

        field_type = FieldTypeEnum(params.field_type)
        create_field_dto = CreateFieldDTO(
            field_type=field_type,
            field_name=params.field_name,
            description=params.description,
            template_id=params.template_id,
            config=params.config,
            is_required=params.is_required,
            created_by_user_id=info.context.user_id
        )

        field_dto = interactor.create_field(
            create_field_dto=create_field_dto)

        return FieldType.from_dto(field_dto)
