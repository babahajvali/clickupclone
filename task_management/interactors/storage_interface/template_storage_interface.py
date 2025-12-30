from abc import ABC, abstractmethod

from task_management.interactors.dtos import TemplateDTO, CreateTemplateDTO


class TemplateStorageInterface(ABC):

    @abstractmethod
    def check_template_exist(self, template_id: str) -> bool:
        pass

    @abstractmethod
    def create_template(self, template_data: CreateTemplateDTO) -> TemplateDTO:
        pass

    @abstractmethod
    def check_template_name_exist(self,template_name: str) -> bool:
        pass

    @abstractmethod
    def check_default_template_exist(self)->bool:
        pass

