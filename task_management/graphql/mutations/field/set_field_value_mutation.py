import graphene

from task_management.exceptions import custom_exceptions
from task_management.exceptions.custom_exceptions import DeletedFieldException
from task_management.graphql.types.error_types import \
    ModificationNotAllowedType, InvalidFieldValue, TaskNotFoundType, \
    DeletedTaskType, FieldNotFoundType, DeletedFieldType, \
    UserNotWorkspaceMemberType
from task_management.graphql.types.input_types import SetFieldValuesInputParams
from task_management.graphql.types.response_types import \
    SetTaskFieldValueResponse
from task_management.graphql.types.types import FieldValueType
from task_management.interactors.dtos import UpdateFieldValueDTO
from task_management.interactors.fields.field_value_interactor import \
    FieldResponseInteractor
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
            result = interactor.set_task_field_response(
                set_value_data=update_data, user_id=info.context.user_id)

            return FieldValueType(
                id=result.id,
                task_id=result.task_id,
                field_id=result.field_id,
                value=result.value
            )

        except custom_exceptions.TaskNotFound as e:
            return TaskNotFoundType(task_id=e.task_id)

        except custom_exceptions.DeletedTaskFound as e:
            return DeletedTaskType(task_id=e.task_id)

        except custom_exceptions.FieldNotFound as e:
            return FieldNotFoundType(field_id=e.field_id)

        except custom_exceptions.DeletedFieldException as e:
            return DeletedFieldType(field_id=e.field_id)

        except custom_exceptions.UserNotWorkspaceMember as e:
            return UserNotWorkspaceMemberType(user_id=e.user_id)

        except custom_exceptions.ModificationNotAllowed as exc:
            return ModificationNotAllowedType(user_id=exc.user_id)

        except custom_exceptions.InvalidFieldValue as e:
            return InvalidFieldValue(message=e.message)
