import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import \
    ModificationNotAllowedType, InvalidFieldValue
from task_management.graphql.types.input_types import SetFieldValuesInputParams
from task_management.graphql.types.response_types import \
    SetTaskFieldValueResponse
from task_management.graphql.types.types import FieldValueType
from task_management.interactors.dtos import UpdateFieldValueDTO
from task_management.interactors.field_interactors.field_value_interactor import \
    FieldValueInteractor
from task_management.storages.field_storage import FieldStorage
from task_management.storages.field_value_storage import FieldValueStorage
from task_management.storages.list_storage import ListStorage
from task_management.storages.space_storage import SpaceStorage
from task_management.storages.task_storage import TaskStorage
from task_management.storages.workspace_member import WorkspaceMemberStorage


class SetFieldValueMutation(graphene.Mutation):
    class Arguments:
        params = SetFieldValuesInputParams(required=True)

    Output = SetTaskFieldValueResponse

    @staticmethod
    def mutate(root, info, params):
        field_storage = FieldStorage()
        field_value_storage = FieldValueStorage()
        task_storage = TaskStorage()
        workspace_member_storage = WorkspaceMemberStorage()
        space_storage = SpaceStorage()
        list_storage = ListStorage()

        interactor = FieldValueInteractor(
            field_storage=field_storage,
            field_value_storage=field_value_storage,
            task_storage=task_storage,
            workspace_member_storage=workspace_member_storage,
            space_storage=space_storage,
            list_storage=list_storage,
        )

        update_data = UpdateFieldValueDTO(
            task_id=params.task_id,
            field_id=params.field_id,
            value=params.value,
        )

        try:
            result = interactor.set_task_field_value(
                set_value_data=update_data, user_id=info.context.user_id)

            return FieldValueType(
                id=result.id,
                task_id=result.task_id,
                field_id=result.field_id,
                value=result.value
            )

        except custom_exceptions.ModificationNotAllowedException as exc:
            return ModificationNotAllowedType(user_id=exc.user_id)

        except custom_exceptions.InvalidFieldValueException as e:
            return InvalidFieldValue(message=e.message)
