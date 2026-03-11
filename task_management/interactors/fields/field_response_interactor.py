from task_management.exceptions.enums import FieldType
from task_management.interactors.dtos import (
    TaskFieldValueDTO,
    UpdateFieldValueDTO,
)
from task_management.interactors.fields.validators.field_config_validator import \
    FieldConfigValidator
from task_management.interactors.storage_interfaces import (
    FieldStorageInterface,
    TaskStorageInterface,
    WorkspaceStorageInterface,
)
from task_management.mixins import (
    FieldValidationMixin,
    WorkspaceValidationMixin,
    TaskValidationMixin,
)


class FieldResponseInteractor(
    FieldValidationMixin, TaskValidationMixin, WorkspaceValidationMixin):
    """
    Field Response Interactor set or update the task field value

    Handle the task field value operation.
    This interactor check the business logic and permission validation
     before set the task field value.

    Key Responsibility:
     - Create or update the task field value with validations

    Dependencies:
        - FieldStorageInterface
        - TaskStorageInterface
        - WorkspaceStorageInterface

    """

    def __init__(
            self, field_storage: FieldStorageInterface,
            task_storage: TaskStorageInterface,
            workspace_storage: WorkspaceStorageInterface):
        super().__init__(
            field_storage=field_storage,
            task_storage=task_storage,
            workspace_storage=workspace_storage)
        self.field_storage = field_storage
        self.task_storage = task_storage
        self.workspace_storage = workspace_storage

    def set_task_field_response(
            self, update_field_value_dto: UpdateFieldValueDTO, user_id: str
    ) -> TaskFieldValueDTO:
        """Set or update a task's value for a specific custom field."""
        self.check_task_not_deleted(task_id=update_field_value_dto.task_id)
        self.check_field_not_deleted(field_id=update_field_value_dto.field_id)
        self._check_user_has_edit_access_for_field(
            field_id=update_field_value_dto.field_id, user_id=user_id
        )
        field_dto = self.field_storage.get_fields(
            field_ids=[update_field_value_dto.field_id]
        )[0]
        self._check_field_value_by_type(
            config=field_dto.config,
            value=update_field_value_dto.value,
            field_type=field_dto.field_type.value
        )

        return self.field_storage.update_or_create_task_field_value(
            field_value_dto=update_field_value_dto, user_id=user_id
        )

    def _check_user_has_edit_access_for_field(
            self, field_id: str, user_id: str):
        workspace_id = self.field_storage.get_workspace_id_from_field_id(
            field_id=field_id)

        self.check_user_has_edit_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id
        )

    @staticmethod
    def _check_field_value_by_type(field_type: str, value: str, config: dict):
        handler = FieldConfigValidator.get_value_validation_handler(
            field_type=FieldType(field_type)
        )
        if handler:
            handler(value=value, config=config)
