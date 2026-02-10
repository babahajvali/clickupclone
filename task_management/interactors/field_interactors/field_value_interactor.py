from task_management.exceptions.custom_exceptions import \
    InvalidFieldValueException
from task_management.exceptions.enums import FieldTypes
from task_management.interactors.dtos import TaskFieldValueDTO, \
    UpdateFieldValueDTO, CreateFieldValueDTO
from task_management.interactors.storage_interface.field_storage_interface import \
    FieldStorageInterface
from task_management.interactors.storage_interface.list_storage_interface import \
    ListStorageInterface
from task_management.interactors.storage_interface.space_storage_interface import \
    SpaceStorageInterface
from task_management.interactors.storage_interface.task_field_values_storage_interface import \
    FieldValueStorageInterface
from task_management.interactors.storage_interface.task_storage_interface import \
    TaskStorageInterface
from task_management.interactors.storage_interface.workspace_member_storage_interface import \
    WorkspaceMemberStorageInterface
from task_management.interactors.validation_mixin import ValidationMixin


class FieldValueInteractor(ValidationMixin):

    def __init__(self, field_value_storage: FieldValueStorageInterface,
                 field_storage: FieldStorageInterface,
                 task_storage: TaskStorageInterface,
                 workspace_member_storage: WorkspaceMemberStorageInterface,
                 space_storage: SpaceStorageInterface,
                 list_storage: ListStorageInterface,):
        self.field_value_storage = field_value_storage
        self.field_storage = field_storage
        self.task_storage = task_storage
        self.workspace_member_storage = workspace_member_storage
        self.space_storage = space_storage
        self.list_storage = list_storage

    def set_task_field_value(self, set_value_data: UpdateFieldValueDTO,
                             user_id: str) -> TaskFieldValueDTO:
        self.validate_field(field_id=set_value_data.field_id,
                            field_storage=self.field_storage)
        self._validate_field_value(field_id=set_value_data.field_id,
                                   value=set_value_data.value)
        list_id = self.get_active_task_list_id(task_id=set_value_data.task_id,
                                               task_storage=self.task_storage)
        space_id = self.list_storage.get_list_space_id(list_id=list_id)
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.validate_user_has_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id,
            workspace_member_storage=self.workspace_member_storage)
        task_field_value_data = self.field_value_storage.check_task_field_value(
            task_id=set_value_data.task_id, field_id=set_value_data.field_id)

        if not task_field_value_data:
            create_field_value = CreateFieldValueDTO(
                task_id=set_value_data.task_id,
                field_id=set_value_data.field_id,
                value=set_value_data.value,
                created_by=user_id
            )
            return self.field_value_storage.create_bulk_field_values(
                create_bulk_field_values=[create_field_value])[0]

        return self.field_value_storage.set_task_field_value(
            field_value_data=set_value_data)

    def _validate_field_value(self, field_id: str, value: str):
        field_data = self.field_storage.get_field_by_id(field_id=field_id)
        config = field_data.config or {}

        if field_data.field_type == FieldTypes.TEXT:
            self._validate_text_field(value, config)

        elif field_data.field_type == FieldTypes.NUMBER:
            self._validate_number_field(value, config)

        elif field_data.field_type == FieldTypes.DROPDOWN:
            self._validate_dropdown_field(value, config)

    @staticmethod
    def _validate_text_field(value: str, config: dict):

        max_length = config.get("max_length")
        if max_length and len(value) > max_length:
            raise InvalidFieldValueException(
                message=f"Text exceeds maximum length of {max_length} characters")

    @staticmethod
    def _validate_number_field(value, config: dict):
        try:
            numeric_value = float(value)
        except (ValueError, TypeError):
            raise InvalidFieldValueException(
                message="Number field value must be a valid number")

        min_value = config.get("min")
        if min_value is not None and numeric_value < min_value:
            raise InvalidFieldValueException(
                message=f"Number must be at least {min_value}")

        max_value = config.get("max")
        if max_value is not None and numeric_value > max_value:
            raise InvalidFieldValueException(
                message=f"Number must not exceed {max_value}")

    @staticmethod
    def _validate_dropdown_field(value: str, config: dict):
        options = config.get("options", [])

        if value not in options:
            raise InvalidFieldValueException(
                message=f"Invalid option. Option must be one of: {', '.join(options)}")
