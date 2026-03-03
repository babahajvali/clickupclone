import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import FieldNotFoundType, \
    FieldNameAlreadyExistsType, \
    ModificationNotAllowedType, InvalidFieldConfigType, \
    InvalidFieldDefaultValueType, NothingToUpdateFieldType, DeletedFieldType, \
    EmptyFieldNameType, MissingFieldConfigType, DropdownOptionsMissingType, \
    UserNotWorkspaceMemberType, TextDefaultValueExceedsMaxLengthType, \
    NumberDefaultValueBelowMinimumType, NumberDefaultValueAboveMaximumType, \
    DropdownDefaultValueNotInOptionsType, MaxValueLessThanMinValueType
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
    def mutate(root, info, params):
        field_storage = FieldStorage()
        workspace_storage = WorkspaceStorage()

        interactor = UpdateFieldInteractor(
            field_storage=field_storage,
            workspace_storage=workspace_storage,
        )

        try:
            update_field_data = UpdateFieldDTO(
                field_id=params.field_id,
                description=params.description,
                field_name=params.field_name,
                config=params.config,
                is_required=params.is_required
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
                is_deleted=result.is_deleted,
                is_required=result.is_required,
                created_by=result.created_by
            )

        except custom_exceptions.FieldNotFound as e:
            return FieldNotFoundType(field_id=e.field_id)

        except custom_exceptions.DeletedFieldException as e:
            return DeletedFieldType(field_id=e.field_id)

        except custom_exceptions.FieldNameAlreadyExists as e:
            return FieldNameAlreadyExistsType(field_name=e.field_name)

        except custom_exceptions.EmptyFieldName as e:
            return EmptyFieldNameType(field_name=e.field_name)

        except custom_exceptions.EmptyFieldConfig as e:
            return MissingFieldConfigType(field_type=e.field_type)

        except custom_exceptions.DropdownOptionsEmpty as e:
            return DropdownOptionsMissingType(field_type=e.field_type)

        except custom_exceptions.UserNotWorkspaceMember as e:
            return UserNotWorkspaceMemberType(user_id=e.user_id)

        except custom_exceptions.ModificationNotAllowed as e:
            return ModificationNotAllowedType(user_id=e.user_id)

        except custom_exceptions.UnexpectedFieldConfigKeys as e:
            return InvalidFieldConfigType(
                field_type=e.field_type,
                invalid_keys=e.invalid_keys,
                message=e.message
            )

        except custom_exceptions.InvalidFieldDefaultValue as e:
            return InvalidFieldDefaultValueType(
                field_type=e.field_type,
                default_value=e.default_value,
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

        except custom_exceptions.NothingToUpdateField as e:
            return NothingToUpdateFieldType(field_id=e.field_id)

        except custom_exceptions.MaxValueLessThanMinValue as e:
            return MaxValueLessThanMinValueType(
                field_type=e.field_type,
                message=e.message,
            )
