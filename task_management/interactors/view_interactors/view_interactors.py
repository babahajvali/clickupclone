from task_management.interactors.dtos import CreateViewDTO, ViewDTO, \
    UpdateViewDTO
from task_management.interactors.storage_interface.permission_storage_interface import \
    PermissionStorageInterface
from task_management.interactors.storage_interface.view_storage_interface import \
    ViewStorageInterface
from task_management.interactors.validation_mixin import ValidationMixin


class ViewInteractor(ValidationMixin):

    def __init__(self, view_storage: ViewStorageInterface,
                 permission_storage: PermissionStorageInterface):
        self.view_storage = view_storage
        self.permission_storage = permission_storage

    def create_view(self, create_view_data: CreateViewDTO) -> ViewDTO:
        self.check_user_has_access_to_list_modification(
            user_id=create_view_data.created_by,
            permission_storage=self.permission_storage)
        return self.view_storage.create_view(create_view_data)

    def update_view(self, update_view_data: UpdateViewDTO) -> ViewDTO:
        self.check_user_has_access_to_list_modification(
            user_id=update_view_data.created_by,
            permission_storage=self.permission_storage)
        return self.view_storage.update_view(update_view_data)

    