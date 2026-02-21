from task_management.exceptions.enums import Role
from task_management.interactors.dtos import WorkspaceDTO, CreateWorkspaceDTO, \
    WorkspaceMemberDTO, AddMemberToWorkspaceDTO
from task_management.interactors.storage_interfaces.workspace_storage_interface import \
    WorkspaceStorageInterface
from task_management.models import Workspace, WorkspaceMember


class WorkspaceStorage(WorkspaceStorageInterface):

    @staticmethod
    def _workspace_dto(data: Workspace) -> WorkspaceDTO:
        return WorkspaceDTO(
            workspace_id=data.workspace_id,
            name=data.name,
            description=data.description,
            user_id=data.created_by.user_id,
            account_id=data.account.account_id,
            is_active=data.is_active,
        )

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

    def get_workspace(self, workspace_id: str) -> WorkspaceDTO | None:
        try:
            workspace_data = Workspace.objects.get(workspace_id=workspace_id)

            return self._workspace_dto(data=workspace_data)
        except Workspace.DoesNotExist:
            return None

    def create_workspace(self,
                         workspace_data: CreateWorkspaceDTO) -> WorkspaceDTO:

        workspace_data = Workspace.objects.create(
            name=workspace_data.name, description=workspace_data.description,
            created_by_id=workspace_data.user_id,
            account_id=workspace_data.account_id)

        return self._workspace_dto(data=workspace_data)

    def update_workspace(
            self, workspace_id: str, field_properties: dict) -> WorkspaceDTO:

        Workspace.objects.filter(workspace_id=workspace_id).update(
            **field_properties)
        workspace_obj = Workspace.objects.get(workspace_id=workspace_id)

        return self._workspace_dto(data=workspace_obj)

    def validate_user_is_workspace_owner(
            self, user_id: str, workspace_id: str) -> bool:

        workspace_data = Workspace.objects.filter(workspace_id=workspace_id,
                                                  created_by_id=user_id).exists()
        return workspace_data

    def delete_workspace(self, workspace_id: str) -> WorkspaceDTO:
        workspace_data = Workspace.objects.get(workspace_id=workspace_id)
        workspace_data.is_delete = False
        workspace_data.save(update_fields=["is_active"])

        return self._workspace_dto(data=workspace_data)

    def transfer_workspace(
            self, workspace_id: str, new_user_id: str) -> WorkspaceDTO:

        workspace_data = Workspace.objects.get(workspace_id=workspace_id)
        workspace_data.created_by = new_user_id
        workspace_data.save(update_fields=["created_by"])

        return self._workspace_dto(data=workspace_data)

    def get_active_account_workspaces(
            self, account_id: str) -> list[WorkspaceDTO]:

        account_workspaces = Workspace.objects.filter(account_id=account_id,
                                                      is_active=True)

        return [self._workspace_dto(data=workspace_data) for workspace_data in
                account_workspaces]

    def get_active_workspaces(
            self, workspace_ids: list[str]) -> list[WorkspaceDTO]:

        workspaces_data = Workspace.objects.filter(
            workspace_id__in=workspace_ids, is_active=True)

        return [self._workspace_dto(data=each) for each in workspaces_data]

    def add_member_to_workspace(
            self, workspace_member_data: AddMemberToWorkspaceDTO) \
            -> WorkspaceMemberDTO:

        workspace_member_data = WorkspaceMember.objects.create(
            workspace_id=workspace_member_data.workspace_id,
            user_id=workspace_member_data.user_id,
            added_by_id=workspace_member_data.added_by,
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

        workspace_member_data = WorkspaceMember.objects.get(
            pk=workspace_member_id)
        workspace_member_data.is_delete = False
        workspace_member_data.save(update_fields=["is_active"])

        return self._workspace_member_dto(data=workspace_member_data)

    def update_the_member_role(
            self, workspace_id: str, user_id: str, role: str) \
            -> WorkspaceMemberDTO:

        workspace_member_data = WorkspaceMember.objects.get(
            workspace_id=workspace_id, user_id=user_id)
        workspace_member_data.role = role
        workspace_member_data.save(update_fields=["role"])

        return self._workspace_member_dto(data=workspace_member_data)

    def get_workspace_members(
            self, workspace_id: str) -> list[WorkspaceMemberDTO]:

        workspace_members = WorkspaceMember.objects.filter(
            workspace_id=workspace_id, is_active=True)

        return [self._workspace_member_dto(data=each) for each in
                workspace_members]

    def get_active_user_workspaces(
            self, user_id: str) -> list[WorkspaceMemberDTO]:

        user_workspaces = WorkspaceMember.objects.filter(
            user_id=user_id, is_active=True).distinct()

        return [self._workspace_member_dto(data=each) for each in
                user_workspaces]

    def re_add_member_to_workspace(
            self, workspace_member_data: AddMemberToWorkspaceDTO) -> \
            WorkspaceMemberDTO:

        workspace_member = WorkspaceMember.objects.create(
            workspace_id=workspace_member_data.workspace_id,
            user_id=workspace_member_data.user_id)

        workspace_member.is_delete = True
        workspace_member.added_by = workspace_member_data.added_by
        workspace_member.save(update_fields=["is_active", "added_by"])

        return self._workspace_member_dto(data=workspace_member)

    def deactivate_workspace_members(
            self, member_ids: list[int]) -> list[WorkspaceMemberDTO]:

        WorkspaceMember.objects.filter(pk__in=member_ids).update(
            is_active=False)
        workspace_members = WorkspaceMember.objects.filter(pk__in=member_ids)

        return [self._workspace_member_dto(data=each) for each in
                workspace_members]

    def get_workspaces(self, workspace_ids: list[str]) -> list[WorkspaceDTO]:

        workspaces_data = Workspace.objects.filter(
            workspace_id__in=workspace_ids)

        return [self._workspace_dto(data=each) for each in workspaces_data]
