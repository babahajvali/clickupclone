from typing import Optional

from task_management.exceptions.custom_exceptions import EmptyNameException
from task_management.interactors.dtos import CreateViewDTO, ViewDTO
from task_management.interactors.storage_interfaces import \
    ViewStorageInterface, ListStorageInterface

from task_management.mixins import ViewValidationMixin


class ViewInteractor(ViewValidationMixin):

    def __init__(self, view_storage: ViewStorageInterface,
                 list_storage: ListStorageInterface):
        super().__init__(view_storage=view_storage)
        self.view_storage = view_storage
        self.list_storage = list_storage

    def create_view(self, create_view_data: CreateViewDTO) -> ViewDTO:

        self._validate_view_name_not_empty(name=create_view_data.name)
        self.check_view_type(view_type=create_view_data.view_type.value)

        return self.view_storage.create_view(create_view_data)

    def update_view(self, view_id: str, name: Optional[str],
                    description: Optional[str]) -> ViewDTO:
        self.validate_view_exist(view_id=view_id)

        is_name_provided = name is not None
        is_description_provided = description is not None
        fields_to_update = {}

        if is_name_provided:
            self._validate_view_name_not_empty(name=name)
            fields_to_update['name'] = name

        if is_description_provided:
            fields_to_update['description'] = description

        if not fields_to_update:
            raise EmptyNameException(name=name)
        return self.view_storage.update_view(view_id=view_id,
                                             update_fields=fields_to_update)

    def get_views(self):
        return self.view_storage.get_all_views()

    @staticmethod
    def _validate_view_name_not_empty(name: str):

        if not name or not name.strip():
            raise EmptyNameException(name=name)
