from task_management.exceptions.custom_exceptions import ListNotFound, \
    DeletedListFound
from task_management.interactors.dtos import ListDTO
from task_management.interactors.storage_interfaces import ListStorageInterface


class ListValidationMixin:

    def __init__(self, list_storage: ListStorageInterface):
        self.list_storage = list_storage

    def check_list_is_not_deleted(self, list_id: str):
        list_data = self.validate_list_is_exists(list_id=list_id)

        is_list_deleted = list_data.is_deleted
        if is_list_deleted:
            raise DeletedListFound(list_id=list_id)

    def validate_list_is_exists(self, list_id: str) -> ListDTO:

        list_data = self.list_storage.get_list(list_id=list_id)

        is_list_not_found = not list_data
        if is_list_not_found:
            raise ListNotFound(list_id=list_id)

        return list_data
