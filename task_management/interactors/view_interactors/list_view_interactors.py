from task_management.exceptions.custom_exceptions import \
    ListViewNotFoundException
from task_management.interactors.dtos import ListViewDTO, RemoveListViewDTO
from task_management.interactors.storage_interface.list_storage_interface import \
    ListStorageInterface
from task_management.interactors.storage_interface.list_views_storage_interface import \
    ListViewsStorageInterface
from task_management.interactors.storage_interface.list_permission_storage_interface import \
    ListPermissionStorageInterface
from task_management.interactors.storage_interface.view_storage_interface import \
    ViewStorageInterface
from task_management.interactors.validation_mixin import ValidationMixin


class ListViewInteractor(ValidationMixin):

    def __init__(self, list_view_storage: ListViewsStorageInterface,
                 list_storage: ListStorageInterface,
                 view_storage: ViewStorageInterface,
                 permission_storage: ListPermissionStorageInterface):
        self.list_view_storage = list_view_storage
        self.list_storage = list_storage
        self.view_storage = view_storage
        self.permission_storage = permission_storage

    def apply_view_for_list(self, view_id: str, list_id: str,
                            user_id: str) -> ListViewDTO:
        self.validate_user_has_access_to_list(user_id=user_id,
                                              list_id=list_id,
                                              permission_storage=self.permission_storage)
        self.validate_view_exist(view_id=view_id,
                                 view_storage=self.view_storage)
        self.validate_list_is_active(list_id=list_id,
                                     list_storage=self.list_storage)

        return self.list_view_storage.apply_view_for_list(view_id=view_id,
                                                          list_id=list_id,
                                                          user_id=user_id)

    def remove_view_for_list(self, view_id: str, list_id: str,
                             user_id: str) -> RemoveListViewDTO:
        self.validate_user_has_access_to_list(user_id=user_id,
                                              list_id=list_id,
                                              permission_storage=self.permission_storage)
        self.validate_view_exist(view_id=view_id,
                                 view_storage=self.view_storage)
        self.validate_list_is_active(list_id=list_id,
                                     list_storage=self.list_storage)

        return self.list_view_storage.remove_view_for_list(view_id=view_id,
                                                           list_id=list_id)

    def get_list_views(self, list_id: str) -> list[ListViewDTO]:
        self.validate_list_is_active(list_id=list_id,
                                     list_storage=self.list_storage)

        return self.list_view_storage.get_list_views(list_id=list_id)

    def _validate_list_view_exist(self, list_id: str, view_id: str):
        is_exist = self.list_view_storage.is_list_view_exist(list_id=list_id,
                                                             view_id=view_id)

        if not is_exist:
            raise ListViewNotFoundException(view_id=view_id, list_id=list_id)
