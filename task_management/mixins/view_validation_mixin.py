from task_management.exceptions.custom_exceptions import ViewNotFound, \
    EmptyViewName, ListViewNotFound
from task_management.exceptions.enums import ViewType
from task_management.interactors.storage_interfaces import \
    ListViewStorageInterface


class ViewValidationMixin:

    def __init__(self, view_storage: ListViewStorageInterface, **kwargs):
        self.view_storage = view_storage
        super().__init__(**kwargs)

    @staticmethod
    def check_view_type(view_type: str):
        existed_views = ViewType.get_values()

        if view_type not in existed_views:
            raise ViewNotFound(view_type=view_type)

    @staticmethod
    def check_list_view_name_not_empty(name: str):

        is_name_empty = not name or not name.strip()
        if is_name_empty:
            raise EmptyViewName(view_name=name)

    def check_list_view_exist(self, list_view_id: int) -> None:
        list_view_dto = self.view_storage.is_list_view_exist(
            list_view_id=list_view_id)

        if not list_view_dto:
            raise ListViewNotFound(list_view_id=list_view_id)
