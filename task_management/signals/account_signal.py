from task_management.interactors.dtos import CreateWorkspaceDTO
from task_management.signal_services.default_space_list_creation_service import \
    DefaultSpaceListCreationService
from task_management.signal_services.default_workspace_creation_service import \
    CreateDefaultWorkspaceService


def create_default_workspace_space_lists(sender, instance, created, **kwargs):
    account = instance
    if created:
        workspace_input_data = CreateWorkspaceDTO(
            name=f"{account.name}'s Workspace",
            description=f"Default workspace",
            user_id=account.owner_id,
            account_id=account.account_id
        )

        CreateDefaultWorkspaceService.create_default_workspace(
            workspace_input=workspace_input_data)


def create_default_space_list(sender, instance, created, **kwargs):
    if created:
        workspace = instance

        DefaultSpaceListCreationService.create_default_space_list(
            workspace_id=workspace.workspace_id, user_id=workspace.owner_id)
