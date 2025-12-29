from abc import ABC, abstractmethod

from task_management.interactors.dtos import CreateFieldDTO, FieldDTO, \
    UpdateFieldDTO


class FieldStorageInterface(ABC):

    @abstractmethod
    def create_field(self, create_field_data: CreateFieldDTO) -> FieldDTO:
        pass

    @abstractmethod
    def check_field_name_exist(self, field_name: str,template_id: str) -> bool:
        pass

    @abstractmethod
    def check_field_order_exist(self, field_order: int, template_id: str) -> bool:
        pass

    @abstractmethod
    def update_field(self, update_field_data: UpdateFieldDTO) -> FieldDTO:
        pass

    @abstractmethod
    def check_field_exist(self,field_id: str, template_id: str) -> bool:
        pass


