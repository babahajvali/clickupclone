import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import FieldNotFoundType, \
    TemplateNotFoundType, ModificationNotAllowedType
from task_management.graphql.types.input_types import DeleteFieldInputParams
from task_management.graphql.types.response_types import DeleteFieldResponse
from task_management.graphql.types.types import FieldType
from task_management.interactors.field.field_interactor import \
    FieldInteractor
from task_management.storages import FieldStorage, TemplateStorage, \
    WorkspaceStorage


class DeleteFieldMutation(graphene.Mutation):
    class Arguments:
        params = DeleteFieldInputParams(required=True)

    Output = DeleteFieldResponse

    @staticmethod
    def mutate(root, info, params):
        field_storage = FieldStorage()
        template_storage = TemplateStorage()
        workspace_storage = WorkspaceStorage()

        interactor = FieldInteractor(
            field_storage=field_storage,
            template_storage=template_storage,
            workspace_storage=workspace_storage,
        )

        try:
            result = interactor.delete_field(
                field_id=params.field_id,
                user_id=info.context.user_id
            )

            return FieldType(
                field_id=result.field_id,
                field_type=result.field_type.value,
                description=result.description,
                template_id=result.template_id,
                field_name=result.field_name,
                is_active=result.is_active,
                order=result.order,
                config=result.config,
                is_required=result.is_required,
                created_by=result.created_by
            )

        except custom_exceptions.FieldNotFound as e:
            return FieldNotFoundType(field_id=e.field_id)

        except custom_exceptions.TemplateNotFound as e:
            return TemplateNotFoundType(template_id=e.template_id)

        except custom_exceptions.ModificationNotAllowed as e:
            return ModificationNotAllowedType(user_id=e.user_id)