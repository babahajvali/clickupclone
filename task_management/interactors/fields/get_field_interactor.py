from task_management.interactors.dtos import FieldDTO
from task_management.interactors.storage_interfaces import \
    FieldStorageInterface
from task_management.mixins import FieldValidationMixin


class GetFieldInteractor:
    """Field Management Business Logic Interactor.
    
    Handles Get Filed .
    This interactor enforces business rules and validates user permissions
     before performing any fields operations.

    Key Responsibilities:
        - Get Field

    
    Dependencies:
        - FieldStorageInterface: Field data persistence

    Attributes:
        field_storage (FieldStorageInterface): Storage for fields operations
    """

    def __init__(self, field_storage: FieldStorageInterface):
        self.field_storage = field_storage

    @property
    def field_mixin(self) -> FieldValidationMixin:
        return FieldValidationMixin(field_storage=self.field_storage)

    def get_field(self, field_id: str) -> FieldDTO:
        self.field_mixin.get_field_if_exists(field_id=field_id)

        return self.field_storage.get_field(field_id=field_id)
