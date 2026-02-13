from abc import ABC, abstractmethod

from task_management.interactors.dtos import CreateTaskDTO, UpdateTaskDTO, \
    TaskDTO, FilterDTO, TaskAssigneeDTO, UserTasksDTO


class TaskStorageInterface(ABC):

    @abstractmethod
    def create_task(self, task_data: CreateTaskDTO) -> TaskDTO:
        pass

    @abstractmethod
    def update_task(self, task_id: str, update_field: dict) -> TaskDTO:
        pass

    @abstractmethod
    def get_task_by_id(self, task_id: str) -> TaskDTO:
        pass

    @abstractmethod
    def get_task_list_id(self, task_id: str) -> str:
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
    def reorder_tasks(self, list_id: str, new_order: int, task_id: str):
        pass

    @abstractmethod
    def assign_task_assignee(self, task_id: str, user_id: str,
                             assigned_by: str) -> TaskAssigneeDTO:
        pass

    @abstractmethod
    def remove_task_assignee(self, assign_id: str) -> TaskAssigneeDTO:
        pass

    @abstractmethod
    def get_task_assignee(self, assign_id: str) -> TaskAssigneeDTO:
        pass

    @abstractmethod
    def get_task_assignees(self, task_id: str) -> list[TaskAssigneeDTO]:
        pass

    @abstractmethod
    def get_user_assigned_tasks(self, user_id: str) -> UserTasksDTO:
        # get tasks only active tasks
        pass

    @abstractmethod
    def get_user_task_assignee(self,user_id: str, task_id: str,assigned_by: str) -> TaskAssigneeDTO:
        pass

    @abstractmethod
    def reassign_task_assignee(self, assign_id: str)-> TaskAssigneeDTO:
        pass

    @abstractmethod
    def get_assignees_for_list_tasks(self, list_id: str) -> list[TaskAssigneeDTO]:
        pass

