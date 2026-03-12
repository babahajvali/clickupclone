import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import FieldNotFoundType, \
    ModificationNotAllowedType, ResourceLockedType, UserNotWorkspaceMemberType
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
    def mutate(root, info, params):
        field_storage = FieldStorage()
        workspace_storage = WorkspaceStorage()

        interactor = DeleteFieldInteractor(
            field_storage=field_storage,
            workspace_storage=workspace_storage,
        )

        try:
            field_dto = interactor.delete_field(
                field_id=params.field_id,
                user_id=info.context.user_id
            )

            return FieldType(
                field_id=field_dto.field_id,
                field_type=field_dto.field_type.value,
                description=field_dto.description,
                template_id=field_dto.template_id,
                field_name=field_dto.field_name,
                is_deleted=field_dto.is_deleted,
                order=field_dto.order,
                config=field_dto.config,
                is_required=field_dto.is_required,
                created_by=field_dto.created_by
            )

        except custom_exceptions.FieldNotFound as e:
            return FieldNotFoundType(field_id=e.field_id)

        except custom_exceptions.ModificationNotAllowed as e:
            return ModificationNotAllowedType(user_id=e.user_id)

        except custom_exceptions.ResourceLockedException as e:
            return ResourceLockedType(message=e.message)

        except custom_exceptions.UserNotWorkspaceMember as e:
            return UserNotWorkspaceMemberType(user_id=e.user_id)
