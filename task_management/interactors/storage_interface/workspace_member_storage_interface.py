from abc import ABC, abstractmethod

from task_management.exceptions.enums import RoleEnum
from task_management.interactors.dtos import WorkspaceMemberDTO, \
    AddMemberToWorkspaceDTO


class WorkspaceMemberStorageInterface(ABC):

    @abstractmethod
    def add_member_to_workspace(self,
                                workspace_member_data: AddMemberToWorkspaceDTO) -> WorkspaceMemberDTO:
        pass

    @abstractmethod
    def get_workspace_member(self, workspace_id: str,
                             user_id: str) -> WorkspaceMemberDTO:
        pass

    @abstractmethod
    def remove_member_from_workspace(self, workspace_id: str,
                                     user_id: str) -> WorkspaceMemberDTO:
        # set the workspace_member is_active is false
        pass

    @abstractmethod
    def update_the_member_role(self, workspace_id: str, user_id: str,
                               role: RoleEnum) -> WorkspaceMemberDTO:
        # change the member role
        pass

    @abstractmethod
    def get_workspace_members(self, workspace_id: str) -> list[WorkspaceMemberDTO]:
        pass
