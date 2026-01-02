from abc import ABC, abstractmethod

from task_management.interactors.dtos import CreateWorkspaceDTO, WorkspaceDTO


class WorkspaceStorageInterface(ABC):

    @abstractmethod
    def get_workspace(self,workspace_id: str)-> WorkspaceDTO:
        pass

    @abstractmethod
    def create_workspace(self,workspace_data: CreateWorkspaceDTO)-> WorkspaceDTO:
        pass

    @abstractmethod
    def update_workspace(self,workspace_data: WorkspaceDTO)-> WorkspaceDTO:
        pass

    @abstractmethod
    def validate_workspace_owner(self,user_id: str, workspace_id: str):
        pass

    @abstractmethod
    def remove_workspace(self,workspace_id: str,user_id: str) -> WorkspaceDTO:
        pass

    @abstractmethod
    def transfer_workspace(self, workspace_id: str, new_user_id: str)-> WorkspaceDTO:
        # change the owner id with new_user_id
        pass



