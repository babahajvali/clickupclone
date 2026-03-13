from task_management.exceptions.custom_exceptions import ViewTypeNotFound
from task_management.exceptions.enums import ViewType
from task_management.interactors.dtos import CreateViewDTO, ViewDTO
from task_management.interactors.storage_interfaces import ViewStorageInterface
from task_management.mixins import ViewValidationMixin


class CreateViewInteractor(ViewValidationMixin):

    def __init__(self, view_storage: ViewStorageInterface):
        super().__init__(view_storage=view_storage)
        self.view_storage = view_storage

    def create_view(self, create_view_dto: CreateViewDTO) -> ViewDTO:
        self.check_view_name_not_empty(name=create_view_dto.name)
        self.check_view_type(
            view_type=create_view_dto.view_type.value)

        return self.view_storage.create_view(create_view_dto)

    @staticmethod
    def check_view_type(view_type: str):
        view_types = ViewType.get_values()
        is_view_type_invalid = view_type not in view_types

        if is_view_type_invalid:
            raise ViewTypeNotFound(view_type=view_type)
