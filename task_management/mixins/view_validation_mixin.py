from task_management.exceptions.custom_exceptions import ViewNotFound, \
    EmptyViewName
from task_management.exceptions.enums import ViewType
from task_management.interactors.storage_interfaces import ViewStorageInterface


class ViewValidationMixin:

    def __init__(self, view_storage: ViewStorageInterface, **kwargs):
        self.view_storage = view_storage
        super().__init__(**kwargs)

    def check_view_exist(self, view_type: str):
        existed_views = ViewType.get_values()

        if view_type not in existed_views:
            raise ViewNotFound(view_type=view_type)

    @staticmethod
    def check_view_name_not_empty(name: str):

        is_name_empty = not name or not name.strip()
        if is_name_empty:
            raise EmptyViewName(view_name=name)
