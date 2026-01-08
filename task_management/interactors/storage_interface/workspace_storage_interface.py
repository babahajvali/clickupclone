from abc import ABC, abstractmethod

from task_management.interactors.dtos import CreateWorkspaceDTO, WorkspaceDTO, \
    UpdateWorkspaceDTO


class WorkspaceStorageInterface(ABC):

    @abstractmethod
    def get_workspace(self,workspace_id: str)-> WorkspaceDTO:
        pass

    @abstractmethod
    def create_workspace(self,workspace_data: CreateWorkspaceDTO)-> WorkspaceDTO:
        pass

    @abstractmethod
    def update_workspace(self,workspace_data: UpdateWorkspaceDTO)-> WorkspaceDTO:
        pass

    @abstractmethod
    def ensure_user_is_workspace_owner(self, user_id: str, workspace_id: str):
        pass

    @abstractmethod
    def remove_workspace(self,workspace_id: str,user_id: str) -> WorkspaceDTO:
        pass

    @abstractmethod
    def transfer_workspace(self, workspace_id: str, new_user_id: str)-> WorkspaceDTO:
        # change the owner id with new_user_id
        pass

    @abstractmethod
    def get_workspaces_by_account(self,account_id: str) -> list[WorkspaceDTO]:
        pass



