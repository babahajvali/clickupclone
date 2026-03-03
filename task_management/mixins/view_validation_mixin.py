from task_management.exceptions.custom_exceptions import ViewNotFound, \
    ViewTypeNotFound, EmptyViewName
from task_management.exceptions.enums import ViewTypes
from task_management.interactors.storage_interfaces import ViewStorageInterface


class ViewValidationMixin:

    def __init__(self, view_storage: ViewStorageInterface):
        self.view_storage = view_storage

    def check_view_exist(self, view_id: str):
        is_exists = self.view_storage.check_view_exists(view_id=view_id)

        if not is_exists:
            raise ViewNotFound(view_id=view_id)

    @staticmethod
    def check_view_type(view_type: str):
        view_types = ViewTypes.get_values()
        is_view_type_invalid = view_type not in view_types

        if is_view_type_invalid:
            raise ViewTypeNotFound(view_type=view_type)

    @staticmethod
    def check_view_name_not_empty(name: str):

        is_name_empty = not name or not name.strip()
        if is_name_empty:
            raise EmptyViewName(view_name=name)
