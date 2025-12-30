from abc import ABC, abstractmethod

from task_management.interactors.dtos import CreateTaskDTO, UpdateTaskDTO, \
    TaskDTO


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