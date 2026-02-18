from abc import ABC, abstractmethod

from task_management.interactors.dtos import TemplateDTO, CreateTemplateDTO, \
    UpdateTemplateDTO, FieldDTO


class TemplateStorageInterface(ABC):

    @abstractmethod
    def get_template_by_id(self, template_id: str) -> TemplateDTO:
        pass

    @abstractmethod
    def create_template(self, template_data: CreateTemplateDTO) -> TemplateDTO:
        pass

    @abstractmethod
    def validate_template_exists(self, template_id: str) -> bool:
        pass

    @abstractmethod
    def check_template_name_exist_except_this_template(
            self, template_name: str, template_id: str) -> bool:
        pass

    @abstractmethod
    def update_template(self, template_id: str,
                        field_properties: dict) -> TemplateDTO:
        pass

    @abstractmethod
    def get_template_list_id(self, template_id: str) -> str:
        pass

    @abstractmethod
    def get_workspace_id_from_template_id(self, template_id: str) -> str:
        pass
