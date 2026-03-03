from task_management.interactors.dtos import ListViewDTO
from task_management.interactors.storage_interfaces import \
    ListStorageInterface, ViewStorageInterface

from task_management.mixins import ListValidationMixin


class GetListViewsInteractor:

    def __init__(self, list_storage: ListStorageInterface,
                 view_storage: ViewStorageInterface):
        self.list_storage = list_storage
        self.view_storage = view_storage

    @property
    def list_mixin(self) -> ListValidationMixin:
        return ListValidationMixin(list_storage=self.list_storage)

    def get_list_views(self, list_id: str) -> list[ListViewDTO]:
        self.list_mixin.check_list_not_deleted(list_id=list_id)

        return self.view_storage.get_list_views(list_id=list_id)
