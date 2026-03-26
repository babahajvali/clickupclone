import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import \
    ModificationNotAllowedType, InvalidFieldValue, TaskNotFoundType, \
    DeletedTaskType, FieldNotFoundType, DeletedFieldType, \
    UserNotWorkspaceMemberType, TextValueExceedsMaxLengthType, \
    InvalidNumberFieldValueType, NumberValueBelowMinimumType, \
    NumberValueExceedsMaximumType, DropdownOptionNotAllowedType
from task_management.graphql.types.input_types import SetFieldValuesInputParams
from task_management.graphql.types.response_types import \
    SetTaskFieldValueResponse
from task_management.graphql.types.types import FieldValueType
from task_management.interactors.dtos import UpdateFieldValueDTO
from task_management.interactors.fields.field_response_interactor import \
    FieldResponseInteractor
from task_management.realtime import broadcast_task_field_value_updated
from task_management.storages import FieldStorage, TaskStorage, \
    WorkspaceStorage


class SetFieldValueMutation(graphene.Mutation):
    class Arguments:
        params = SetFieldValuesInputParams(required=True)

    Output = SetTaskFieldValueResponse

    @staticmethod
    def mutate(root, info, params):
        field_storage = FieldStorage()
        task_storage = TaskStorage()
        workspace_storage = WorkspaceStorage()

        interactor = FieldResponseInteractor(
            field_storage=field_storage,
            task_storage=task_storage,
            workspace_storage=workspace_storage
        )

        update_data = UpdateFieldValueDTO(
            task_id=params.task_id,
            field_id=params.field_id,
            value=params.value,
        )

        try:
            task_field_value_dto = interactor.set_task_field_response(
                update_field_value_dto=update_data,
                user_id=info.context.user_id,
            )
            task_data = task_storage.get_task(task_id=params.task_id)

            if task_data is not None:
                broadcast_task_field_value_updated(
                    task_id=str(task_data.task_id),
                    list_id=str(task_data.list_id),
                    field_value_id=task_field_value_dto.id,
                    field_id=str(task_field_value_dto.field_id),
                    value=task_field_value_dto.value,
                    updated_by=str(info.context.user_id),
                )

            return FieldValueType(
                id=task_field_value_dto.id,
                task_id=task_field_value_dto.task_id,
                field_id=task_field_value_dto.field_id,
                value=task_field_value_dto.value
            )

        except custom_exceptions.TaskNotFound as e:
            return TaskNotFoundType(task_id=e.task_id)

        except custom_exceptions.TaskIsDeleted as e:
            return DeletedTaskType(task_id=e.task_id)

        except custom_exceptions.FieldNotFound as e:
            return FieldNotFoundType(field_id=e.field_id)

        except custom_exceptions.FieldIsDeleted as e:
            return DeletedFieldType(field_id=e.field_id)

        except custom_exceptions.UserNotWorkspaceMember as e:
            return UserNotWorkspaceMemberType(user_id=e.user_id)

        except custom_exceptions.ModificationNotAllowed as exc:
            return ModificationNotAllowedType(user_id=exc.user_id)

        except custom_exceptions.InvalidFieldValue as e:
            return InvalidFieldValue(message=e.message)

        except custom_exceptions.TextValueExceedsMaxLength as e:
            return TextValueExceedsMaxLengthType(message=e.message)

        except custom_exceptions.InvalidNumberFieldValue as e:
            return InvalidNumberFieldValueType(message=e.message)

        except custom_exceptions.NumberValueBelowMinimum as e:
            return NumberValueBelowMinimumType(message=e.message)

        except custom_exceptions.NumberValueExceedsMaximum as e:
            return NumberValueExceedsMaximumType(message=e.message)

        except custom_exceptions.DropdownOptionNotAllowed as e:
            return DropdownOptionNotAllowedType(message=e.message)
