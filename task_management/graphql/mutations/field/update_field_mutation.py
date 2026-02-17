import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import FieldNotFoundType, \
    TemplateNotFoundType, FieldNameAlreadyExistsType, \
    ModificationNotAllowedType, InvalidFieldConfigType, \
    InvalidFieldDefaultValueType
from task_management.graphql.types.input_types import UpdateFieldInputParams
from task_management.graphql.types.response_types import UpdateFieldResponse
from task_management.graphql.types.types import FieldType
from task_management.interactors.field.field_interactor import \
    FieldInteractor
from task_management.interactors.dtos import UpdateFieldDTO
from task_management.storages import FieldStorage, TemplateStorage, \
    WorkspaceStorage

class UpdateFieldMutation(graphene.Mutation):
    class Arguments:
        params = UpdateFieldInputParams(required=True)

    Output = UpdateFieldResponse

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
            update_field_data = UpdateFieldDTO(
                field_id=params.field_id,
                description=params.description if params.description else None,
                field_name=params.field_name if params.field_name else None,
                config=params.config if params.config else None,
                is_required=params.is_required if params.is_required is not None else None
            )

            result = interactor.update_field(
                update_field_data=update_field_data,
                user_id=info.context.user_id
            )

            return FieldType(
                field_id=result.field_id,
                field_type=result.field_type.value,
                description=result.description,
                template_id=result.template_id,
                field_name=result.field_name,
                order=result.order,
                config=result.config,
                is_active=result.is_active,
                is_required=result.is_required,
                created_by=result.created_by
            )

        except custom_exceptions.FieldNotFoundException as e:
            return FieldNotFoundType(field_id=e.field_id)

        except custom_exceptions.TemplateNotFoundException as e:
            return TemplateNotFoundType(template_id=e.template_id)

        except custom_exceptions.FieldNameAlreadyExistsException as e:
            return FieldNameAlreadyExistsType(field_name=e.field_name)

        except custom_exceptions.ModificationNotAllowedException as e:
            return ModificationNotAllowedType(user_id=e.user_id)

        except custom_exceptions.InvalidFieldConfigException as e:
            return InvalidFieldConfigType(
                field_type=e.field_type,
                invalid_keys=e.invalid_keys,
                message=e.message
            )

        except custom_exceptions.InvalidFieldDefaultValueException as e:
            return InvalidFieldDefaultValueType(
                field_type=e.field_type,
                default_value=e.default_value,
                message=e.message
            )
