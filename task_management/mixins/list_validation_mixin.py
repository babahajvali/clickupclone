from task_management.exceptions.custom_exceptions import ListNotFound, \
    DeletedListFound
from task_management.interactors.storage_interfaces import ListStorageInterface


class ListValidationMixin:

    def __init__(self, list_storage: ListStorageInterface):
        self.list_storage = list_storage

    def check_list_is_active(self, list_id: str):
        list_data = self.list_storage.get_list(list_id=list_id)

        is_list_not_found = not list_data
        if is_list_not_found:
            raise ListNotFound(list_id=list_id)

        is_list_delete = list_data.is_deleted
        if is_list_delete:
            raise DeletedListFound(list_id=list_id)

    def check_list_is_exists(self, list_id: str):

        is_list_exists = self.list_storage.is_list_exists(list_id=list_id)

        is_list_not_exists = not is_list_exists
        if is_list_not_exists:
            raise ListNotFound(list_id=list_id)
