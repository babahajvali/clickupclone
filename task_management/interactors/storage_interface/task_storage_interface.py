from abc import ABC, abstractmethod

from task_management.interactors.dtos import CreateTaskDTO, UpdateTaskDTO, \
    TaskDTO, FilterDTO


class TaskStorageInterface(ABC):

    @abstractmethod
    def check_task_exist(self, task_id: str) -> bool:
        pass

    @abstractmethod
    def create_task(self, task_data: CreateTaskDTO) -> TaskDTO:
        pass

    @abstractmethod
    def update_task(self, update_task_data: UpdateTaskDTO) -> TaskDTO:
        pass

    @abstractmethod
    def get_task_by_id(self, task_id: str) -> TaskDTO:
        pass

    @abstractmethod
    def get_list_tasks(self, list_id: str) -> list[TaskDTO]:
        pass

    @abstractmethod
    def remove_task(self, task_id: str) -> TaskDTO:
        pass

    @abstractmethod
    def check_task_order_exist(self, order: int, list_id: str) -> bool:
        pass

    @abstractmethod
    def task_filter_data(self, filter_data: FilterDTO):
        pass

    @abstractmethod
    def get_template_fields_by_list(self, list_id: str):
        pass

    @abstractmethod
    def get_tasks_count(self, list_id: str):
        pass

    @abstractmethod
    def reorder_tasks(self, list_id: str, order: int, task_id: str):
        pass

    @abstractmethod
    def get_list_task_ids(self, list_id: str)-> list[str]:
        pass
