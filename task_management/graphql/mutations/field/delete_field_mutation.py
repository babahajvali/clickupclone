import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import FieldNotFoundType, \
    TemplateNotFoundType, ModificationNotAllowedType
from task_management.graphql.types.input_types import DeleteFieldInputParams
from task_management.graphql.types.response_types import DeleteFieldResponse
from task_management.graphql.types.types import FieldType
from task_management.interactors.field_interactors.field_interactors import \
    FieldInteractor
from task_management.storages.field_storage import FieldStorage
from task_management.storages.list_storage import ListStorage
from task_management.storages.space_storage import SpaceStorage
from task_management.storages.template_storage import TemplateStorage
from task_management.storages.list_permission_storage import ListPermissionStorage
from task_management.storages.workspace_member import WorkspaceMemberStorage


class DeleteFieldMutation(graphene.Mutation):
    class Arguments:
        params = DeleteFieldInputParams(required=True)

    Output = DeleteFieldResponse

    @staticmethod
    def mutate(root, info, params):
        field_storage = FieldStorage()
        template_storage = TemplateStorage()
        list_storage = ListStorage()
        workspace_member_storage = WorkspaceMemberStorage()
        space_storage = SpaceStorage()

        interactor = FieldInteractor(
            field_storage=field_storage,
            template_storage=template_storage,
            list_storage=list_storage,
            workspace_member_storage=workspace_member_storage,
            space_storage=space_storage,
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

        except custom_exceptions.FieldNotFoundException as e:
            return FieldNotFoundType(field_id=e.field_id)

        except custom_exceptions.TemplateNotFoundException as e:
            return TemplateNotFoundType(template_id=e.template_id)

        except custom_exceptions.ModificationNotAllowedException as e:
            return ModificationNotAllowedType(user_id=e.user_id)