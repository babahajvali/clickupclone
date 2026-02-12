from task_management.exceptions.custom_exceptions import ListNotFoundException, \
    InactiveListException
from task_management.interactors.storage_interfaces import ListStorageInterface


class ListValidationMixin:

    def __init__(self, list_storage: ListStorageInterface, **kwargs):
        self.list_storage = list_storage
        super().__init__(**kwargs)

    def validate_list_is_active(self, list_id: str):
        list_data = self.list_storage.get_list(list_id=list_id)

        if not list_data:
            raise ListNotFoundException(list_id=list_id)

        if not list_data.is_active:
            raise InactiveListException(list_id=list_id)
