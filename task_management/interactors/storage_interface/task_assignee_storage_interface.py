from abc import ABC, abstractmethod

from task_management.interactors.dtos import TaskAssigneeDTO, \
    RemoveTaskAssigneeDTO, UserTasksDTO


class TaskAssigneeStorageInterface(ABC):

    @abstractmethod
    def assign_task_assignee(self, task_id: str, user_id: str, assigned_by: str) -> TaskAssigneeDTO:
        pass

    @abstractmethod
    def remove_task_assignee(self, assign_id: str,removed_by: str) -> RemoveTaskAssigneeDTO:
        pass

    @abstractmethod
    def get_task_assignee(self, assign_id: str)-> TaskAssigneeDTO:
        pass

    @abstractmethod
    def get_task_assignees(self, task_id: str) -> list[TaskAssigneeDTO]:
        pass

    @abstractmethod
    def get_user_assigned_tasks(self,user_id: str) -> list[UserTasksDTO]:
        # get tasks only active tasks
        pass

    @abstractmethod
    def get_user_today_tasks(self,user_id: str) -> list[UserTasksDTO]:
        # get today active tasks
        pass