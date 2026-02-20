from abc import ABC, abstractmethod
from typing import Optional

from task_management.interactors.dtos import CreateFieldDTO, FieldDTO, \
    UpdateFieldValueDTO, TaskFieldValueDTO, TaskFieldValuesDTO, \
    CreateFieldValueDTO, UpdateFieldDTO


class FieldStorageInterface(ABC):

    @abstractmethod
    def create_field(
            self, create_field_data: CreateFieldDTO, order: int) -> FieldDTO:
        pass

    @abstractmethod
    def is_field_name_exists(
            self, field_name: str, template_id: str,
            exclude_field_id: Optional[str]) -> bool:
        pass

    @abstractmethod
    def get_field_by_id(self, field_id: str) -> FieldDTO:
        pass

    @abstractmethod
    def update_field(
            self, field_id: str, update_field_data: UpdateFieldDTO) \
            -> FieldDTO:
        pass

    @abstractmethod
    def is_field_exists(self, field_id: str) -> bool:
        pass

    @abstractmethod
    def check_field_name_except_this_field(
            self, field_id: str, field_name: str, template_id: str) -> bool:
        pass

    @abstractmethod
    def get_field_by_name(
            self, field_name: str, template_id: str) -> FieldDTO:
        pass

    @abstractmethod
    def get_active_fields_for_template(self, template_id: str) -> list[
        FieldDTO]:
        pass

    @abstractmethod
    def reorder_fields(self, field_id: str, template_id: str,
                       new_order: int) -> FieldDTO:
        pass

    @abstractmethod
    def template_fields_count(self, template_id: str) -> int:
        pass

    @abstractmethod
    def delete_field(self, field_id: str):
        pass

    @abstractmethod
    def create_bulk_fields(
            self, fields_data: list[CreateFieldDTO]) -> list[FieldDTO]:
        pass

    @abstractmethod
    def set_task_field_value(
            self, field_value_data: UpdateFieldValueDTO) -> TaskFieldValueDTO:
        pass

    @abstractmethod
    def get_field_values_by_task_ids(
            self, task_ids: list[str]) -> list[TaskFieldValuesDTO]:
        pass

    @abstractmethod
    def create_bulk_field_values(
            self, create_bulk_field_values: list[CreateFieldValueDTO]):
        pass

    @abstractmethod
    def get_task_field_value(self, task_id: str, field_id: str) -> bool:
        pass

    @abstractmethod
    def get_workspace_id_from_field_id(self, field_id: str) -> str:
        pass

    @abstractmethod
    def get_next_field_order_in_template(self, template_id: str) -> int:
        pass
