from task_management.interactors.dtos import ListDTO
from task_management.interactors.storage_interfaces import ListStorageInterface
from task_management.mixins import ListValidationMixin


class GetListInteractor:

    def __init__(self, list_storage: ListStorageInterface):
        self.list_storage = list_storage

    @property
    def list_mixin(self) -> ListValidationMixin:
        return ListValidationMixin(list_storage=self.list_storage)

    def get_list(self, list_id: str) -> ListDTO:
        self.list_mixin.get_list_if_exists(list_id=list_id)

        return self.list_storage.get_list(list_id=list_id)
