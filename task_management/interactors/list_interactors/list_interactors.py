from task_management.interactors.dtos import CreateListDTO, ListDTO, \
    UpdateListDTO
from task_management.interactors.storage_interface.folder_storage_interface import \
    FolderStorageInterface
from task_management.interactors.storage_interface.list_storage_interface import \
    ListStorageInterface
from task_management.interactors.storage_interface.permission_storage_interface import \
    PermissionStorageInterface
from task_management.interactors.storage_interface.space_storage_interface import \
    SpaceStorageInterface
from task_management.interactors.storage_interface.task_storage_interface import \
    TaskStorageInterface
from task_management.interactors.validation_mixin import ValidationMixin


class ListInteractor(ValidationMixin):

    def __init__(self, list_storage: ListStorageInterface,
                 task_storage: TaskStorageInterface,
                 folder_storage: FolderStorageInterface,
                 space_storage: SpaceStorageInterface,
                 permission_storage: PermissionStorageInterface):
        self.list_storage = list_storage
        self.task_storage = task_storage
        self.folder_storage = folder_storage
        self.space_storage = space_storage
        self.permission_storage = permission_storage

    def create_list(self, create_list_data: CreateListDTO) -> ListDTO:
        self.check_user_has_access_to_list_modification(
            user_id=create_list_data.created_by,
            permission_storage=self.permission_storage)
        self.validate_space_exist_and_status(
            space_id=create_list_data.space_id,
            space_storage=self.space_storage)
        self.validate_list_order(order=create_list_data.order,list_storage=self.list_storage)

        if create_list_data.folder_id is not None:
            self.validate_folder_exist_and_status(
                folder_id=create_list_data.folder_id,
                folder_storage=self.folder_storage)

        return self.list_storage.crate_list(create_list_data=create_list_data)

    def update_list(self, update_list_data: UpdateListDTO) -> ListDTO:
        self.check_list_exists_and_status(list_id=update_list_data.list_id,
                                          list_storage=self.list_storage)
        self.check_user_has_access_to_list_modification(
            user_id=update_list_data.created_by,
            permission_storage=self.permission_storage)
        self.validate_space_exist_and_status(
            space_id=update_list_data.space_id,
            space_storage=self.space_storage)
        self.validate_list_order(order=update_list_data.order,
                                 list_storage=self.list_storage)

        if update_list_data.folder_id is not None:
            self.validate_folder_exist_and_status(
                folder_id=update_list_data.folder_id,
                folder_storage=self.folder_storage)

        return self.list_storage.update_list(update_list_data=update_list_data)

    def get_folder_lists(self, folder_id: str) -> list[ListDTO]:
        self.validate_folder_exist_and_status(folder_id=folder_id,folder_storage=self.folder_storage)

        return self.list_storage.get_folder_lists(folder_id=folder_id)

    def get_space_lists(self, space_id: str) -> list[ListDTO]:
        self.validate_space_exist_and_status(space_id=space_id,space_storage=self.space_storage)


        return self.list_storage.get_space_lists(space_id=space_id)
    def remove_list(self, list_id: str, user_id: str):
        self.check_user_has_access_to_list_modification(user_id=user_id, permission_storage=self.permission_storage)
        self.check_list_exists_and_status(list_id=list_id, list_storage=self.list_storage)

        return self.list_storage.remove_list(list_id=list_id)

    def set_list_private(self, list_id: str, user_id: str):
        self.check_user_has_access_to_list_modification(user_id=user_id, permission_storage=self.permission_storage)
        self.check_list_exists_and_status(list_id=list_id, list_storage=self.list_storage)

        return self.list_storage.make_list_private(list_id=list_id)

    def set_list_public(self, list_id: str, user_id: str):
        self.check_user_has_access_to_list_modification(user_id=user_id,
                                                        permission_storage=self.permission_storage)
        self.check_list_exists_and_status(list_id=list_id,
                                          list_storage=self.list_storage)

        return self.list_storage.make_list_public(list_id=list_id)




