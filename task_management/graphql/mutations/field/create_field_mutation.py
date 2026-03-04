import graphene

from task_management.exceptions import custom_exceptions
from task_management.exceptions.enums import FieldType as FieldTypeEnum
from task_management.graphql.types.error_types import TemplateNotFoundType, \
    UnsupportedFieldTypeType, FieldNameAlreadyExistsType, \
    ModificationNotAllowedType, InvalidFieldConfigType, \
    EmptyFieldNameType, MissingFieldConfigType, \
    DropdownOptionsMissingType, TextDefaultValueExceedsMaxLengthType, \
    NumberDefaultValueBelowMinimumType, NumberDefaultValueAboveMaximumType, \
    DropdownDefaultValueNotInOptionsType, MaxValueLessThanMinValueType
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
    def mutate(root, info, params):
        field_storage = FieldStorage()
        template_storage = TemplateStorage()
        workspace_storage = WorkspaceStorage()

        interactor = CreateFieldInteractor(
            field_storage=field_storage,
            template_storage=template_storage,
            workspace_storage=workspace_storage,
        )

        try:
            field_type = FieldTypeEnum(params.field_type)
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
                is_deleted=result.is_deleted,
                order=result.order,
                config=result.config,
                is_required=result.is_required,
                created_by=result.created_by
            )

        except custom_exceptions.TemplateNotFound as e:
            return TemplateNotFoundType(template_id=e.template_id)

        except custom_exceptions.UnsupportedFieldType as e:
            return UnsupportedFieldTypeType(field_type=e.field_type)

        except custom_exceptions.FieldNameAlreadyExists as e:
            return FieldNameAlreadyExistsType(field_name=e.field_name)

        except custom_exceptions.ModificationNotAllowed as e:
            return ModificationNotAllowedType(user_id=e.user_id)

        except custom_exceptions.UnexpectedFieldConfigKeys as e:
            return InvalidFieldConfigType(
                field_type=e.field_type,
                invalid_keys=e.invalid_keys,
                message=e.message
            )

        except custom_exceptions.TextDefaultValueExceedsMaxLength as e:
            return TextDefaultValueExceedsMaxLengthType(message=e.message)

        except custom_exceptions.NumberDefaultValueBelowMinimum as e:
            return NumberDefaultValueBelowMinimumType(message=e.message)

        except custom_exceptions.NumberDefaultValueAboveMaximum as e:
            return NumberDefaultValueAboveMaximumType(message=e.message)

        except custom_exceptions.DropdownDefaultValueNotInOptions as e:
            return DropdownDefaultValueNotInOptionsType(message=e.message)

        except custom_exceptions.EmptyFieldName as e:
            return EmptyFieldNameType(field_name=e.field_name)

        except custom_exceptions.EmptyFieldConfig as e:
            return MissingFieldConfigType(field_type=e.field_type)

        except custom_exceptions.DropdownOptionsEmpty as e:
            return DropdownOptionsMissingType(field_type=e.field_type)

        except custom_exceptions.MaxValueLessThanMinValue as e:
            return MaxValueLessThanMinValueType(
                field_type=e.field_type,
                message=e.message,
            )
