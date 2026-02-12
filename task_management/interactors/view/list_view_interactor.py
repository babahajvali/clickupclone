from task_management.exceptions.custom_exceptions import \
    ListViewNotFoundException
from task_management.interactors.dtos import ListViewDTO, RemoveListViewDTO
from task_management.interactors.storage_interfaces import \
    ListViewsStorageInterface, ListStorageInterface, ViewStorageInterface, \
    WorkspaceStorageInterface, SpaceStorageInterface

from task_management.mixins import WorkspaceValidationMixin, \
    ListValidationMixin, ViewValidationMixin


class ListViewInteractor(WorkspaceValidationMixin, ListValidationMixin,
                         ViewValidationMixin):

    def __init__(self, list_view_storage: ListViewsStorageInterface,
                 list_storage: ListStorageInterface,
                 view_storage: ViewStorageInterface,
                 workspace_storage: WorkspaceStorageInterface,
                 space_storage: SpaceStorageInterface):
        super().__init__(workspace_storage=workspace_storage,
                         view_storage=view_storage, list_storage=list_storage)
        self.list_view_storage = list_view_storage
        self.list_storage = list_storage
        self.view_storage = view_storage
        self.workspace_storage = workspace_storage
        self.space_storage = space_storage

    def apply_view_for_list(self, view_id: str, list_id: str,
                            user_id: str) -> ListViewDTO:
        list_view_data = self.list_view_storage.get_list_view(list_id=list_id,
                                                              view_id=view_id)
        if list_view_data:
            return list_view_data

        self._validate_user_has_access_to_list(user_id=user_id,
                                               list_id=list_id, )
        self.validate_view_exist(view_id=view_id)
        self.validate_list_is_active(list_id=list_id)

        return self.list_view_storage.apply_view_for_list(view_id=view_id,
                                                          list_id=list_id,
                                                          user_id=user_id)

    def remove_view_for_list(self, view_id: str, list_id: str,
                             user_id: str) -> RemoveListViewDTO:
        self._validate_user_has_access_to_list(user_id=user_id,
                                               list_id=list_id)
        self.validate_view_exist(view_id=view_id)
        self.validate_list_is_active(list_id=list_id)
        self._validate_list_view_exist(list_id=list_id, view_id=view_id)

        return self.list_view_storage.remove_view_for_list(view_id=view_id,
                                                           list_id=list_id)

    def get_list_views(self, list_id: str) -> list[ListViewDTO]:
        self.validate_list_is_active(list_id=list_id)

        return self.list_view_storage.get_list_views(list_id=list_id)

    def _validate_list_view_exist(self, list_id: str, view_id: str):
        is_exist = self.list_view_storage.is_list_view_exist(list_id=list_id,
                                                             view_id=view_id)

        if is_exist:
            raise ListViewNotFoundException(view_id=view_id, list_id=list_id)

    def _validate_user_has_access_to_list(self, list_id: str, user_id: str):
        space_id = self.list_storage.get_list_space_id(list_id=list_id)
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)

        self.validate_user_has_access_to_workspace(workspace_id=workspace_id,user_id=user_id)
