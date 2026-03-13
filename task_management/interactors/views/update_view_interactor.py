from task_management.exceptions.custom_exceptions import NothingToUpdateView
from task_management.interactors.dtos import ViewDTO, UpdateViewDTO
from task_management.interactors.storage_interfaces import ViewStorageInterface
from task_management.mixins import ViewValidationMixin


class UpdateViewInteractor(ViewValidationMixin):

    def __init__(self, view_storage: ViewStorageInterface):
        super().__init__(view_storage=view_storage)
        self.view_storage = view_storage

    def update_view(self, update_view_dto: UpdateViewDTO) -> ViewDTO:
        self._check_update_view_properties(
            update_view_dto=update_view_dto)
        self.check_view_exist(view_id=update_view_dto.view_id)

        return self.view_storage.update_view(
            view_id=update_view_dto.view_id,
            name=update_view_dto.name,
            description=update_view_dto.description,
        )

    def _check_update_view_properties(
            self, update_view_dto: UpdateViewDTO) -> None:
        is_description_provided = update_view_dto.description is not None
        is_name_provided = update_view_dto.name is not None
        has_no_update_view_properties = not (
                is_description_provided or is_name_provided)

        if has_no_update_view_properties:
            raise NothingToUpdateView(view_id=update_view_dto.view_id)
        if is_name_provided:
            self.check_view_name_not_empty(name=update_view_dto.name)
