from task_management.exceptions.custom_exceptions import ViewTypeNotFound
from task_management.exceptions.enums import ViewType
from task_management.interactors.dtos import CreateViewDTO, ViewDTO
from task_management.interactors.storage_interfaces import ViewStorageInterface
from task_management.mixins import ViewValidationMixin


class CreateViewInteractor:

    def __init__(self, view_storage: ViewStorageInterface):
        self.view_storage = view_storage

    @property
    def view_mixin(self) -> ViewValidationMixin:
        return ViewValidationMixin(view_storage=self.view_storage, )

    def create_view(self, create_view_data: CreateViewDTO) -> ViewDTO:
        self.view_mixin.check_view_name_not_empty(name=create_view_data.name)
        self.check_view_type(
            view_type=create_view_data.view_type.value)

        return self.view_storage.create_view(create_view_data)

    @staticmethod
    def check_view_type(view_type: str):
        view_types = ViewType.get_values()
        is_view_type_invalid = view_type not in view_types

        if is_view_type_invalid:
            raise ViewTypeNotFound(view_type=view_type)
