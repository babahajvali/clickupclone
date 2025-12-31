from task_management.interactors.dtos import CreateFolderDTO, FolderDTO, \
    UpdateFolderDTO
from task_management.interactors.storage_interface.folder_storage_interface import \
    FolderStorageInterface
from task_management.interactors.storage_interface.permission_storage_interface import \
    PermissionStorageInterface
from task_management.interactors.storage_interface.space_storage_interface import \
    SpaceStorageInterface
from task_management.interactors.validation_mixin import ValidationMixin


class FolderInteractor(ValidationMixin):

    def __init__(self, folder_storage: FolderStorageInterface,
                 permission_storage: PermissionStorageInterface,
                 space_storage: SpaceStorageInterface):
        self.folder_storage = folder_storage
        self.space_storage = space_storage
        self.permission_storage = permission_storage

    def create_folder(self, create_folder_data: CreateFolderDTO) -> FolderDTO:
        self.check_user_has_access_to_folder_modification(
            user_id=create_folder_data.created_by,
            permission_storage=self.permission_storage)
        self.validate_space_exist_and_status(space_storage=self.space_storage,
                                             space_id=create_folder_data.space_id)
        self.validate_folder_order(order=create_folder_data.order,
                                   space_id=create_folder_data.space_id,
                                   folder_storage=self.folder_storage)

        return self.folder_storage.create_folder(create_folder_data)

    def update_folder(self, update_folder_data: UpdateFolderDTO) -> FolderDTO:
        self.validate_folder_exist_and_status(
            folder_id=update_folder_data.folder_id,
            folder_storage=self.folder_storage)
        self.validate_space_exist_and_status(space_storage=self.space_storage,
                                             space_id=update_folder_data.space_id)
        self.check_user_has_access_to_folder_modification(
            user_id=update_folder_data.created_by,
            permission_storage=self.permission_storage)
        self.validate_folder_order(order=update_folder_data.order,
                                   space_id=update_folder_data.space_id,
                                   folder_storage=self.folder_storage)

        return self.folder_storage.update_folder(update_folder_data)

    def remove_folder(self, folder_id: str, user_id: str) -> FolderDTO:
        self.validate_folder_exist_and_status(
            folder_id=folder_id,
            folder_storage=self.folder_storage)
        self.check_user_has_access_to_folder_modification(user_id=user_id,
                                                          permission_storage=self.permission_storage)

        return self.folder_storage.remove_folder(folder_id)

    def make_folder_private(self, folder_id: str, user_id: str) -> FolderDTO:
        self.validate_folder_exist_and_status(folder_id=folder_id,
                                              folder_storage=self.folder_storage)
        self.check_user_has_access_to_folder_modification(user_id=user_id,
                                                          permission_storage=self.permission_storage)

        return self.folder_storage.set_folder_private(folder_id=folder_id)

    def make_folder_public(self, folder_id: str, user_id: str) -> FolderDTO:
        self.validate_folder_exist_and_status(folder_id=folder_id,
                                              folder_storage=self.folder_storage)
        self.check_user_has_access_to_folder_modification(user_id=user_id,
                                                          permission_storage=self.permission_storage)

        return self.folder_storage.set_folder_public(folder_id=folder_id)

    def get_space_folders(self, space_id: str) -> list[FolderDTO]:
        self.validate_space_exist_and_status(space_id=space_id,
                                             space_storage=self.space_storage)

        return self.folder_storage.get_space_folders(space_id=space_id)
