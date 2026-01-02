from task_management.interactors.dtos import CreateWorkspaceDTO, WorkspaceDTO
from task_management.interactors.storage_interface.user_storage_interface import \
    UserStorageInterface
from task_management.interactors.storage_interface.workspace_storage_interface import \
    WorkspaceStorageInterface
from task_management.interactors.validation_mixin import ValidationMixin


class WorkspaceInteractor(ValidationMixin):
    def __init__(self, workspace_storage: WorkspaceStorageInterface,
                 user_storage: UserStorageInterface):
        self.workspace_storage = workspace_storage
        self.user_storage = user_storage

    def create_workspace(self, create_workspace_data: CreateWorkspaceDTO) \
            -> WorkspaceDTO:
        self.validate_user_exist_and_status(create_workspace_data.owner_id,
                                            user_storage=self.user_storage)

        return self.workspace_storage.create_workspace(
            workspace_data=create_workspace_data)

    def update_workspace(self,
                         update_workspace_data: WorkspaceDTO) -> WorkspaceDTO:
        self.validate_user_exist_and_status(update_workspace_data.owner_id,
                                            user_storage=self.user_storage)
        self.validate_workspace_exist_and_status(
            update_workspace_data.workspace_id,
            workspace_storage=self.workspace_storage)

        return self.workspace_storage.update_workspace(
            workspace_data=update_workspace_data)

    def delete_workspace(self, workspace_id: str,
                         user_id: str) -> WorkspaceDTO:
        self.validate_user_exist_and_status(user_id,
                                            user_storage=self.user_storage)
        self.check_user_owner_of_workspace(user_id=user_id,
                                           workspace_id=workspace_id,
                                           workspace_storage=self.workspace_storage)

        return self.workspace_storage.remove_workspace(user_id=user_id,
                                                       workspace_id=workspace_id)

    def transfer_workspace(self, workspace_id: str, user_id: str,
                           new_user_id: str) -> WorkspaceDTO:
        self.validate_user_exist_and_status(user_id=user_id,
                                            user_storage=self.user_storage)
        self.check_user_owner_of_workspace(user_id=user_id,
                                           workspace_id=workspace_id,
                                           workspace_storage=self.workspace_storage)
        self.validate_user_exist_and_status(user_id=new_user_id,
                                            user_storage=self.user_storage)

        return self.workspace_storage.transfer_workspace(
            workspace_id=workspace_id, new_user_id=new_user_id)
