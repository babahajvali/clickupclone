from abc import ABC, abstractmethod

from task_management.interactors.dtos import TaskAssigneeDTO, \
    RemoveTaskAssigneeDTO


class TaskAssigneeStorageInterface(ABC):

    @abstractmethod
    def assign_task_assignee(self, task_id: str, user_id: str, assigned_by: str) -> TaskAssigneeDTO:
        pass

    @abstractmethod
    def remove_task_assignee(self, assign_id: str,removed_by: str) -> RemoveTaskAssigneeDTO:
        pass

    @abstractmethod
    def check_tas_assignee_exist(self,assign_id: str)-> bool:
        pass