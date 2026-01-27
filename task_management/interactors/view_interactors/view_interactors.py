from task_management.interactors.dtos import CreateViewDTO, ViewDTO, \
    UpdateViewDTO
from task_management.interactors.storage_interface.list_permission_storage_interface import \
    ListPermissionStorageInterface
from task_management.interactors.storage_interface.list_storage_interface import \
    ListStorageInterface
from task_management.interactors.storage_interface.view_storage_interface import \
    ViewStorageInterface
from task_management.interactors.validation_mixin import ValidationMixin


class ViewInteractor(ValidationMixin):

    def __init__(self, view_storage: ViewStorageInterface,
                 permission_storage: ListPermissionStorageInterface,
                 list_storage: ListStorageInterface):
        self.view_storage = view_storage
        self.permission_storage = permission_storage
        self.list_storage = list_storage

    def create_view(self, create_view_data: CreateViewDTO) -> ViewDTO:
        self.check_view_type(view_type=create_view_data.view_type.value)

        return self.view_storage.create_view(create_view_data)

    def update_view(self, update_view_data: UpdateViewDTO) -> ViewDTO:
        self.validate_view_exist(view_id=update_view_data.view_id,
                                 view_storage=self.view_storage)
        return self.view_storage.update_view(update_view_data)

    def get_views(self):
        return self.view_storage.get_all_views()
