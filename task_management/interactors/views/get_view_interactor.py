from task_management.interactors.dtos import ViewDTO
from task_management.interactors.storage_interfaces import \
    ViewStorageInterface
from task_management.mixins import ViewValidationMixin


class GetViewInteractor(ViewValidationMixin):

    def __init__(self, view_storage: ViewStorageInterface):
        super().__init__(view_storage=view_storage)
        self.view_storage = view_storage

    def get_view(self, view_id: str) -> ViewDTO:
        self.check_view_exist(view_id=view_id)

        return self.view_storage.get_view(view_id)
