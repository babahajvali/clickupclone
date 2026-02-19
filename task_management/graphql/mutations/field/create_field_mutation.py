import graphene

from task_management.exceptions import custom_exceptions
from task_management.exceptions.enums import FieldTypes
from task_management.graphql.types.error_types import TemplateNotFoundType, \
    UnsupportedFieldTypeType, FieldNameAlreadyExistsType, \
    ModificationNotAllowedType, InvalidFieldConfigType, \
    InvalidFieldDefaultValueType
from task_management.graphql.types.input_types import CreateFieldInputParams
from task_management.graphql.types.response_types import CreateFieldResponse
from task_management.graphql.types.types import FieldType
from task_management.interactors.field.field_interactor import \
    FieldInteractor
from task_management.interactors.dtos import CreateFieldDTO
from task_management.storages import FieldStorage, TemplateStorage, \
    WorkspaceStorage


class CreateFieldMutation(graphene.Mutation):
    class Arguments:
        params = CreateFieldInputParams(required=True)

    Output = CreateFieldResponse

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
            field_type = FieldTypes(params.field_type)
            create_field_data = CreateFieldDTO(
                field_type=field_type,
                field_name=params.field_name,
                description=params.description,
                template_id=params.template_id,
                config=params.config,
                is_required=params.is_required,
                created_by_user_id=info.context.user_id
            )

            result = interactor.create_field(
                field_data=create_field_data)

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

        except custom_exceptions.TemplateNotFoundException as e:
            return TemplateNotFoundType(template_id=e.template_id)

        except custom_exceptions.UnsupportedFieldTypeException as e:
            return UnsupportedFieldTypeType(field_type=e.field_type)

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
