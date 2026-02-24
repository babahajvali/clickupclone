from typing import Optional

from task_management.exceptions.custom_exceptions import InvalidOrder, \
    EmptyFolderName, UnsupportedVisibilityType, NothingToUpdateFolderException
from task_management.exceptions.enums import Visibility
from task_management.interactors.storage_interfaces import \
    FolderStorageInterface


class FolderValidator:

    def __init__(self, folder_storage: FolderStorageInterface):
        self.folder_storage = folder_storage

    def check_the_folder_order(self, space_id: str, order: int):
        if order < 1:
            raise InvalidOrder(order=order)
        lists_count = self.folder_storage.get_space_folder_count(
            space_id=space_id)

        if order > lists_count:
            raise InvalidOrder(order=order)

    @staticmethod
    def check_folder_name_not_empty(name: str):

        is_name_empty = name is None or not name.strip()

        if is_name_empty:
            raise EmptyFolderName(folder_name=name)

    @staticmethod
    def check_visibility_type(visibility: str):
        existed_visibilities = [each.value for each in Visibility]

        is_visibility_invalid = visibility not in existed_visibilities
        if is_visibility_invalid:
            raise UnsupportedVisibilityType(
                visibility_type=visibility)

    def check_folder_update_field_properties(
            self, folder_id: str, name: Optional[str],
            description: Optional[str]):

        field_properties_to_update = {}

        is_name_provided = name is not None
        if is_name_provided:
            self.check_folder_name_not_empty(name=name)
            field_properties_to_update['name'] = name

        is_description_provided = description is not None
        if is_description_provided:
            field_properties_to_update['description'] = description

        if not field_properties_to_update:
            raise NothingToUpdateFolderException(folder_id=folder_id)

    def reorder_folder_positions(
            self, space_id: str, old_order: int, new_order: int):


        if new_order > old_order:
            self.folder_storage.shift_folders_down(
                space_id=space_id, old_order=old_order, new_order=new_order
            )
        else:
            self.folder_storage.shift_folders_up(
                space_id=space_id, old_order=old_order, new_order=new_order
            )