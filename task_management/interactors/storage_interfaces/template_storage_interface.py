from abc import ABC, abstractmethod
from typing import Optional

from task_management.interactors.dtos import TemplateDTO, CreateTemplateDTO


class TemplateStorageInterface(ABC):

    @abstractmethod
    def get_template(self, template_id: str) -> TemplateDTO:
        pass

    @abstractmethod
    def create_template(self, template_data: CreateTemplateDTO) -> TemplateDTO:
        pass

    @abstractmethod
    def validate_template_exists(self, template_id: str) -> bool:
        pass

    @abstractmethod
    def update_template(
            self, template_id: str, name: Optional[str],
            description: Optional[str]) -> TemplateDTO:
        pass

    @abstractmethod
    def get_workspace_id_from_template_id(self, template_id: str) -> str:
        pass
