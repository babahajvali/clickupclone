from task_management.interactors.dtos import WorkspaceDTO, CreateWorkspaceDTO, \
    UpdateWorkspaceDTO
from task_management.interactors.storage_interfaces.workspace_storage_interface import \
    WorkspaceStorageInterface
from task_management.models import Workspace, User, Account


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

    def get_workspace(self, workspace_id: str) -> WorkspaceDTO | None:
        try:
            workspace_data = Workspace.objects.get(workspace_id=workspace_id)

            return self._workspace_dto(data=workspace_data)
        except Workspace.DoesNotExist:
            return None

    def create_workspace(self,
                         workspace_data: CreateWorkspaceDTO) -> WorkspaceDTO:
        created_by = User.objects.get(user_id=workspace_data.user_id)
        account = Account.objects.get(account_id=workspace_data.account_id)

        workspace_data = Workspace.objects.create(
            name=workspace_data.name, description=workspace_data.description,
            created_by=created_by, account=account)

        return self._workspace_dto(data=workspace_data)

    def update_workspace(self,
                         workspace_data: UpdateWorkspaceDTO) -> WorkspaceDTO:
        workspace_obj = Workspace.objects.get(
            workspace_id=workspace_data.workspace_id)
        if workspace_data.name:
            workspace_obj.name = workspace_data.name

        if workspace_data.description:
            workspace_obj.description = workspace_data.description

        workspace_obj.save()

        return self._workspace_dto(data=workspace_obj)

    def validate_user_is_workspace_owner(self, user_id: str,
                                         workspace_id: str) -> bool:
        workspace_data = Workspace.objects.filter(workspace_id=workspace_id,
                                     created_by_id=user_id).exists()
        return workspace_data

    def delete_workspace(self, workspace_id: str) -> WorkspaceDTO:
        workspace_data = Workspace.objects.get(workspace_id=workspace_id)
        workspace_data.is_active = False
        workspace_data.save()

        return self._workspace_dto(data=workspace_data)

    def transfer_workspace(self, workspace_id: str,
                           new_user_id: str) -> WorkspaceDTO:
        # change the owner id with new_user_id
        new_owner = User.objects.get(user_id=new_user_id)
        workspace_data = Workspace.objects.get(workspace_id=workspace_id)
        workspace_data.created_by = new_owner
        workspace_data.save()

        return self._workspace_dto(data=workspace_data)

    def get_workspaces_by_account(self, account_id: str) -> list[WorkspaceDTO]:
        account_workspaces = Workspace.objects.filter(account_id=account_id,
                                                      is_active=True)

        return [self._workspace_dto(data=workspace_data) for workspace_data in
                account_workspaces]

