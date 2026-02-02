from abc import ABC, abstractmethod

from task_management.interactors.dtos import CreateFieldDTO, FieldDTO, \
    UpdateFieldDTO


class FieldStorageInterface(ABC):

    @abstractmethod
    def create_field(self, create_field_data: CreateFieldDTO) -> FieldDTO:
        pass

    @abstractmethod
    def is_field_name_exists(self, field_name: str, template_id: str) -> bool:
        pass

    @abstractmethod
    def get_field_by_id(self,field_id: str)->FieldDTO:
        pass

    @abstractmethod
    def update_field(self, update_field_data: UpdateFieldDTO) -> FieldDTO:
        pass

    @abstractmethod
    def is_field_exists(self, field_id: str) -> bool:
        pass

    @abstractmethod
    def check_field_name_except_this_field(self,field_id: str , field_name: str, template_id: str) -> bool:
        pass

    @abstractmethod
    def get_fields_for_template(self, template_id: str) -> list[FieldDTO]:
        pass

    @abstractmethod
    def reorder_fields(self, field_id: str, template_id: str,new_order: int) -> FieldDTO:
        pass

    @abstractmethod
    def template_fields_count(self,template_id: str) -> int:
        pass

    @abstractmethod
    def delete_field(self, field_id: str):
        pass

    @abstractmethod
    def create_bulk_fields(self, fields_data: list[CreateFieldDTO]) -> list[FieldDTO]:
        pass


