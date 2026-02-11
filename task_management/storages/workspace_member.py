from task_management.exceptions.enums import Role
from task_management.interactors.dtos import AddMemberToWorkspaceDTO, \
    WorkspaceMemberDTO
from task_management.interactors.storage_interfaces.workspace_member_storage_interface import \
    WorkspaceMemberStorageInterface
from task_management.models import Workspace, User, WorkspaceMember


class WorkspaceMemberStorage(WorkspaceMemberStorageInterface):

    @staticmethod
    def _workspace_member_dto(data: WorkspaceMember) -> WorkspaceMemberDTO:
        role = Role(data.role)
        return WorkspaceMemberDTO(
            id=data.pk,
            workspace_id=data.workspace.workspace_id,
            user_id=data.user.user_id,
            role=role,
            added_by=data.added_by.user_id,
            is_active=data.is_active,
        )

    def add_member_to_workspace(self,
                                workspace_member_data: AddMemberToWorkspaceDTO) -> WorkspaceMemberDTO:
        workspace = Workspace.objects.get(
            workspace_id=workspace_member_data.workspace_id)
        user = User.objects.get(user_id=workspace_member_data.user_id)
        added_by = User.objects.get(user_id=workspace_member_data.added_by)

        workspace_member_data = WorkspaceMember.objects.create(
            workspace=workspace, user=user, added_by=added_by,
            role=workspace_member_data.role.value)

        return self._workspace_member_dto(data=workspace_member_data)

    def get_workspace_member(self, workspace_id: str,
                             user_id: str) -> WorkspaceMemberDTO | None:
        try:
            workspace_member_data = WorkspaceMember.objects.get(
                workspace_id=workspace_id, user_id=user_id)

            return self._workspace_member_dto(data=workspace_member_data)
        except WorkspaceMember.DoesNotExist:
            return None

    def get_workspace_member_by_id(self,
                                   workspace_member_id: int) -> WorkspaceMemberDTO:
        workspace_member_data = WorkspaceMember.objects.get(
            pk=workspace_member_id)

        return self._workspace_member_dto(data=workspace_member_data)

    def remove_member_from_workspace(
            self, workspace_member_id: int) -> WorkspaceMemberDTO:
        # set the workspace_member is_active is false
        workspace_member_data = WorkspaceMember.objects.get(
            pk=workspace_member_id)
        workspace_member_data.is_active = False
        workspace_member_data.save()

        return self._workspace_member_dto(data=workspace_member_data)

    def update_the_member_role(self, workspace_id: str, user_id: str,
                               role: str) -> WorkspaceMemberDTO:
        workspace_member_data = WorkspaceMember.objects.get(
            workspace_id=workspace_id, user_id=user_id)
        workspace_member_data.role = role
        workspace_member_data.save()

        return self._workspace_member_dto(data=workspace_member_data)

    def get_workspace_members(self, workspace_id: str) -> list[
        WorkspaceMemberDTO]:
        workspace_members = WorkspaceMember.objects.filter(
            workspace_id=workspace_id, is_active=True)

        return [self._workspace_member_dto(data=each) for each in
                workspace_members]

    def get_user_workspaces(self, user_id: str) -> list[WorkspaceMemberDTO]:

        user_workspaces = WorkspaceMember.objects.filter(
            user_id=user_id,is_active=True).distinct()

        return [self._workspace_member_dto(data=each) for each in
                user_workspaces]

    def re_add_member_to_workspace(
            self, workspace_member_data: AddMemberToWorkspaceDTO) -> \
            WorkspaceMemberDTO:

        workspace_member = WorkspaceMember.objects.create(
            workspace_id=workspace_member_data.workspace_id,
            user_id=workspace_member_data.user_id)
        added_by = User.objects.get(user_id=workspace_member_data.added_by)

        workspace_member.is_active = True
        workspace_member.added_by = added_by
        workspace_member.save()

        return self._workspace_member_dto(data=workspace_member)
