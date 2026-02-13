from task_management.exceptions.custom_exceptions import ViewNotFoundException, \
    ViewTypeNotFoundException
from task_management.exceptions.enums import ViewTypes
from task_management.interactors.storage_interfaces import ViewStorageInterface


class ViewValidationMixin:

    def __init__(self, view_storage: ViewStorageInterface, **kwargs):
        self.view_storage = view_storage
        super().__init__(**kwargs)


    def validate_view_exist(self, view_id: str):
        is_exists = self.view_storage.check_view_exists(view_id=view_id)

        if not is_exists:
            raise ViewNotFoundException(view_id=view_id)

    @staticmethod
    def check_view_type(view_type: str):
        view_types = ViewTypes.get_values()

        if view_type not in view_types:
            raise ViewTypeNotFoundException(view_type=view_type)
