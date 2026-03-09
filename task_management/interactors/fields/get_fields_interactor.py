from typing import List

from task_management.exceptions.custom_exceptions import InvalidFieldIdsFound
from task_management.interactors.dtos import FieldDTO
from task_management.interactors.storage_interfaces import \
    FieldStorageInterface


class GetFieldsInteractor:
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

    def get_fields(self, field_ids: List[str]) -> List[FieldDTO]:
        self._check_field_ids_exists(field_ids=field_ids)

        return self.field_storage.get_fields(field_ids=field_ids)

    def _check_field_ids_exists(self, field_ids: List[str]):
        existed_field_ids = self.field_storage.get_existing_field_ids(
            field_ids=field_ids)

        invalid_field_ids = [field_id for field_id in field_ids if
                             field_id not in existed_field_ids]

        if invalid_field_ids:
            raise InvalidFieldIdsFound(field_ids=invalid_field_ids)
