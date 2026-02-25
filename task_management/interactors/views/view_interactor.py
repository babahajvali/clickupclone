from typing import Optional

from task_management.exceptions.custom_exceptions import EmptyViewName, \
    NothingToUpdateView
from task_management.interactors.dtos import CreateViewDTO, ViewDTO
from task_management.interactors.storage_interfaces import \
    ViewStorageInterface, ListStorageInterface

from task_management.mixins import ViewValidationMixin


class ViewInteractor:

    def __init__(self, view_storage: ViewStorageInterface,
                 list_storage: ListStorageInterface):
        self.view_storage = view_storage
        self.list_storage = list_storage

    @property
    def view_mixin(self) -> ViewValidationMixin:
        return ViewValidationMixin(view_storage=self.view_storage, )

    def create_view(self, create_view_data: CreateViewDTO) -> ViewDTO:

        self._check_view_name_not_empty(name=create_view_data.name)
        self.view_mixin.check_view_type(
            view_type=create_view_data.view_type.value)

        return self.view_storage.create_view(create_view_data)

    def update_view(self, view_id: str, name: Optional[str],
                    description: Optional[str]) -> ViewDTO:

        self.view_mixin.check_view_exist(view_id=view_id)

        self._check_update_view_field_properties(
            view_id=view_id, name=name, description=description)

        return self.view_storage.update_view(
            view_id=view_id, name=name, description=description)

    def get_all_views(self):
        return self.view_storage.get_all_views()

    def get_view(self, view_id: str) -> ViewDTO:
        self.view_mixin.check_view_exist(view_id=view_id)

        return self.view_storage.get_view(view_id)

    @staticmethod
    def _check_view_name_not_empty(name: str):

        is_name_empty = not name or not name.strip()
        if is_name_empty:
            raise EmptyViewName(view_name=name)

    def _check_update_view_field_properties(
            self, view_id: str, name: Optional[str],
            description: Optional[str]):

        field_properties_to_update = {}

        is_name_provided = name is not None
        if is_name_provided:
            self._check_view_name_not_empty(name=name)
            field_properties_to_update['name'] = name
        is_description_provided = description is not None
        if is_description_provided:
            field_properties_to_update['description'] = description

        if not field_properties_to_update:
            raise NothingToUpdateView(view_id=view_id)
