from task_management.interactors.dtos import FieldDTO
from task_management.interactors.storage_interfaces import \
    FieldStorageInterface
from task_management.mixins import FieldValidationMixin


class GetFieldInteractor:
    """
    Get Field Interactor get the custom field by field id

    Handle the get field operation
    This interactor check the business rules and input validation
     before get the custom field

    Key Responsibility:
     - Get the custom field

    Dependencies:
        - FieldStorageInterface
    """

    def __init__(self, field_storage: FieldStorageInterface):
        self.field_storage = field_storage

    @property
    def field_mixin(self) -> FieldValidationMixin:
        return FieldValidationMixin(field_storage=self.field_storage)

    def get_field(self, field_id: str) -> FieldDTO:
        """Fetch a single field by id."""
        self.field_mixin.check_field_exists(field_id=field_id)

        return self.field_storage.get_field(field_id=field_id)
