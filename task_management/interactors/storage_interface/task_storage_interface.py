from abc import ABC, abstractmethod

from task_management.interactors.dtos import CreateTaskDTO, UpdateTaskDTO, \
    TaskDTO, FilterDTO


class TaskStorageInterface(ABC):

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
    def task_filter_data(self, filter_data: FilterDTO):
        pass

    @abstractmethod
    def get_tasks_count(self, list_id: str):
        pass

    @abstractmethod
    def reorder_tasks(self, list_id: str, order: int, task_id: str):
        pass

