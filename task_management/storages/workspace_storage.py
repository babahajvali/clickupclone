from typing import Optional

from task_management.exceptions.enums import Role
from task_management.interactors.dtos import WorkspaceDTO, CreateWorkspaceDTO, \
    WorkspaceMemberDTO, CreateWorkspaceMemberDTO
from task_management.interactors.storage_interfaces.workspace_storage_interface import \
    WorkspaceStorageInterface
from task_management.models import Workspace, WorkspaceMember


class WorkspaceStorage(WorkspaceStorageInterface):

    @staticmethod
    def _convert_workspace_to_dto(workspace_obj: Workspace) -> WorkspaceDTO:
        return WorkspaceDTO(
            workspace_id=workspace_obj.workspace_id,
            name=workspace_obj.name,
            description=workspace_obj.description,
            user_id=workspace_obj.created_by_id,
            account_id=workspace_obj.account_id,
            is_deleted=workspace_obj.is_deleted,
        )

    @staticmethod
    def _convert_workspace_member_to_dto(
            workspace_member_obj: WorkspaceMember) -> WorkspaceMemberDTO:
        role = Role(workspace_member_obj.role)
        return WorkspaceMemberDTO(
            id=workspace_member_obj.pk,
            workspace_id=workspace_member_obj.workspace_id,
            user_id=workspace_member_obj.user_id,
            role=role,
            added_by=workspace_member_obj.added_by_id,
            is_active=workspace_member_obj.is_active,
        )

    def get_workspace(self, workspace_id: str) -> WorkspaceDTO | None:
        workspace_obj = Workspace.objects.filter(
            workspace_id=workspace_id).first()

        if workspace_obj is None:
            return None

        return self._convert_workspace_to_dto(workspace_obj=workspace_obj)

    def create_workspace(
            self, create_workspace_dto: CreateWorkspaceDTO) -> WorkspaceDTO:

        workspace_obj = Workspace.objects.create(
            name=create_workspace_dto.name,
            description=create_workspace_dto.description,
            created_by_id=create_workspace_dto.user_id,
            account_id=create_workspace_dto.account_id)

        return self._convert_workspace_to_dto(
            workspace_obj=workspace_obj)

    def update_workspace(
            self, workspace_id: str, name: Optional[str],
            description: Optional[str]) -> WorkspaceDTO:

        workspace_properties = {}

        is_name_provided = name is not None
        if is_name_provided:
            workspace_properties['name'] = name

        is_descriptor_provided = description is not None
        if is_descriptor_provided:
            workspace_properties['description'] = description

        Workspace.objects.filter(workspace_id=workspace_id).update(
            **workspace_properties)

        return self.get_workspace(workspace_id=workspace_id)

    def validate_user_is_workspace_owner(
            self, user_id: str, workspace_id: str) -> bool:

        return Workspace.objects.filter(
            workspace_id=workspace_id, created_by_id=user_id).exists()

    def delete_workspace(self, workspace_id: str) -> WorkspaceDTO:

        Workspace.objects.filter(workspace_id=workspace_id).update(
            is_deleted=True)

        return self.get_workspace(workspace_id=workspace_id)

    def transfer_workspace(
            self, workspace_id: str, new_user_id: str) -> WorkspaceDTO:

        Workspace.objects.filter(workspace_id=workspace_id).update(
            created_by_id=new_user_id)

        return self.get_workspace(workspace_id=workspace_id)

    def get_account_workspaces(
            self, account_id: str) -> list[WorkspaceDTO]:

        workspace_objs = Workspace.objects.filter(
            account_id=account_id, is_deleted=False)

        return [self._convert_workspace_to_dto(workspace_obj=workspace_obj)
                for workspace_obj in workspace_objs]

    def get_active_workspaces(
            self, workspace_ids: list[str]) -> list[WorkspaceDTO]:

        workspace_objs = Workspace.objects.filter(
            workspace_id__in=workspace_ids, is_deleted=False)

        return [self._convert_workspace_to_dto(workspace_obj=workspace_obj)
                for workspace_obj in workspace_objs]

    def create_workspace_member(
            self, workspace_member_dto: CreateWorkspaceMemberDTO) \
            -> WorkspaceMemberDTO:

        workspace_member_dto = WorkspaceMember.objects.create(
            workspace_id=workspace_member_dto.workspace_id,
            user_id=workspace_member_dto.user_id,
            added_by_id=workspace_member_dto.added_by,
            role=workspace_member_dto.role.value)

        return self._convert_workspace_member_to_dto(
            workspace_member_obj=workspace_member_dto)

    def get_workspace_member(
            self, workspace_id: str, user_id: str) \
            -> WorkspaceMemberDTO | None:

        workspace_member_dto = WorkspaceMember.objects.filter(
            workspace_id=workspace_id, user_id=user_id).first()

        if not workspace_member_dto:
            return None

        return self._convert_workspace_member_to_dto(
            workspace_member_obj=workspace_member_dto)

    def get_workspace_member_by_id(
            self, workspace_member_id: int) -> WorkspaceMemberDTO:
        workspace_member_dto = WorkspaceMember.objects.get(
            pk=workspace_member_id)

        return self._convert_workspace_member_to_dto(
            workspace_member_obj=workspace_member_dto)

    def remove_member_from_workspace(
            self, workspace_member_id: int) -> WorkspaceMemberDTO:

        WorkspaceMember.objects.filter(pk=workspace_member_id).update(
            is_active=False)

        return self.get_workspace_member_by_id(
            workspace_member_id=workspace_member_id)

    def update_workspace_member_role(
            self, workspace_id: str, user_id: str, role: str) \
            -> WorkspaceMemberDTO:

        WorkspaceMember.objects.filter(
            workspace_id=workspace_id, user_id=user_id).update(role=role)

        return self.get_workspace_member(
            workspace_id=workspace_id, user_id=user_id)

    def get_workspace_members(
            self, workspace_id: str) -> list[WorkspaceMemberDTO]:

        workspace_member_objs = WorkspaceMember.objects.filter(
            workspace_id=workspace_id, is_active=True)

        return [
            self._convert_workspace_member_to_dto(
                workspace_member_obj=workspace_member_obj)
            for workspace_member_obj in workspace_member_objs]

    def get_active_user_workspaces(
            self, user_id: str) -> list[WorkspaceMemberDTO]:

        workspace_member_objs = WorkspaceMember.objects.filter(
            user_id=user_id, is_active=True).distinct()

        return [
            self._convert_workspace_member_to_dto(
                workspace_member_obj=workspace_member_obj)
            for workspace_member_obj in workspace_member_objs]

    def deactivate_workspace_members(
            self, member_ids: list[int]) -> list[WorkspaceMemberDTO]:

        WorkspaceMember.objects.filter(pk__in=member_ids).update(
            is_active=False)

        return [self.get_workspace_member_by_id(
            workspace_member_id=workspace_member_id) for workspace_member_id in
            member_ids]

    def get_workspaces(self, workspace_ids: list[str]) -> list[WorkspaceDTO]:

        workspaces_objs = Workspace.objects.filter(
            workspace_id__in=workspace_ids, is_deleted=False)

        return [self._convert_workspace_to_dto(workspace_obj=workspace_obj)
                for workspace_obj in workspaces_objs]
