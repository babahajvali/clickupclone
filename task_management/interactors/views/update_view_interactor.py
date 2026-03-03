from typing import Optional

from task_management.exceptions.custom_exceptions import NothingToUpdateView
from task_management.interactors.dtos import ViewDTO
from task_management.interactors.storage_interfaces import ViewStorageInterface
from task_management.mixins import ViewValidationMixin


class UpdateViewInteractor:

    def __init__(self, view_storage: ViewStorageInterface):
        self.view_storage = view_storage

    @property
    def view_mixin(self) -> ViewValidationMixin:
        return ViewValidationMixin(view_storage=self.view_storage, )

    def update_view(self, view_id: str, name: Optional[str],
                    description: Optional[str]) -> ViewDTO:

        self._check_update_view_field_properties(
            view_id=view_id, name=name, description=description)
        self.view_mixin.check_view_exist(view_id=view_id)

        return self.view_storage.update_view(
            view_id=view_id, name=name, description=description)

    def _check_update_view_field_properties(
            self, view_id: str, name: Optional[str],
            description: Optional[str]):

        is_description_provided = description is not None
        is_name_provided = name is not None
        has_no_update_field_properties = any([
            is_description_provided,
            is_name_provided,
        ])

        if not has_no_update_field_properties:
            raise NothingToUpdateView(view_id=view_id)
        if is_name_provided:
            self.view_mixin.check_view_name_not_empty(name=name)
