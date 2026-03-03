from task_management.exceptions.custom_exceptions import ViewNotFound, \
    EmptyViewName
from task_management.interactors.storage_interfaces import ViewStorageInterface


class ViewValidationMixin:

    def __init__(self, view_storage: ViewStorageInterface):
        self.view_storage = view_storage

    def check_view_exist(self, view_id: str):
        is_exists = self.view_storage.check_view_exists(view_id=view_id)

        if not is_exists:
            raise ViewNotFound(view_id=view_id)

    @staticmethod
    def check_view_name_not_empty(name: str):

        is_name_empty = not name or not name.strip()
        if is_name_empty:
            raise EmptyViewName(view_name=name)
