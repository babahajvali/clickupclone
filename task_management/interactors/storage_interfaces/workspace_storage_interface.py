from abc import ABC, abstractmethod

from task_management.interactors.dtos import CreateWorkspaceDTO, WorkspaceDTO, \
    AddMemberToWorkspaceDTO, WorkspaceMemberDTO


class WorkspaceStorageInterface(ABC):

    @abstractmethod
    def get_workspace(self, workspace_id: str) -> WorkspaceDTO:
        pass

    @abstractmethod
    def create_workspace(self,
                         workspace_data: CreateWorkspaceDTO) -> WorkspaceDTO:
        pass

    @abstractmethod
    def update_workspace(self, workspace_id: str,
                         field_properties: dict) -> WorkspaceDTO:
        pass

    @abstractmethod
    def validate_user_is_workspace_owner(self, user_id: str,
                                         workspace_id: str) -> bool:
        pass

    @abstractmethod
    def delete_workspace(self, workspace_id: str) -> WorkspaceDTO:
        pass

    @abstractmethod
    def transfer_workspace(self, workspace_id: str,
                           new_user_id: str) -> WorkspaceDTO:
        # change the owner id with new_user_id
        pass

    @abstractmethod
    def get_active_account_workspaces(self, account_id: str) -> list[
        WorkspaceDTO]:
        pass

    @abstractmethod
    def get_active_workspaces(self, workspace_ids: list[str]) -> list[
        WorkspaceDTO]:
        pass

    @abstractmethod
    def add_member_to_workspace(self,
                                workspace_member_data: AddMemberToWorkspaceDTO) -> WorkspaceMemberDTO:
        pass

    @abstractmethod
    def get_workspace_member(self, workspace_id: str,
                             user_id: str) -> WorkspaceMemberDTO:
        pass

    @abstractmethod
    def get_workspace_member_by_id(self,
                                   workspace_member_id: int) -> WorkspaceMemberDTO:
        pass

    @abstractmethod
    def remove_member_from_workspace(
            self, workspace_member_id: int) -> WorkspaceMemberDTO:
        # set the workspace_member is_active is false
        pass

    @abstractmethod
    def update_the_member_role(self, workspace_id: str, user_id: str,
                               role: str) -> WorkspaceMemberDTO:
        # change the member role
        pass

    @abstractmethod
    def get_workspace_members(self, workspace_id: str) -> list[
        WorkspaceMemberDTO]:
        pass

    @abstractmethod
    def get_active_user_workspaces(self, user_id: str) -> list[
        WorkspaceMemberDTO]:
        pass

    @abstractmethod
    def re_add_member_to_workspace(
            self, workspace_member_data: AddMemberToWorkspaceDTO) -> \
            WorkspaceMemberDTO:
        pass

    @abstractmethod
    def deactivate_workspace_members(self, member_ids: list[int]) -> list[
        WorkspaceMemberDTO]:
        pass

    @abstractmethod
    def get_workspaces(self, workspace_ids: list[str]) -> list[WorkspaceDTO]:
        pass
