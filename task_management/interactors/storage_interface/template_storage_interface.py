from abc import ABC, abstractmethod


class TemplateStorageInterface(ABC):

    @abstractmethod
    def check_template_exist(self, template_id: str) -> bool:
        pass