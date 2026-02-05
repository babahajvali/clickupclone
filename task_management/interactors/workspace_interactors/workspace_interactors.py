from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.exceptions.enums import Role
from task_management.interactors.dtos import CreateWorkspaceDTO, WorkspaceDTO, \
    UpdateWorkspaceDTO, AddMemberToWorkspaceDTO, CreateListDTO, CreateSpaceDTO
from task_management.interactors.list_interactors.list_interactors import \
    ListInteractor
from task_management.interactors.space_interactors.space_interactors import \
    SpaceInteractor
from task_management.interactors.storage_interface.account_storage_interface import \
    AccountStorageInterface
from task_management.interactors.storage_interface.field_storage_interface import \
    FieldStorageInterface
from task_management.interactors.storage_interface.folder_permission_storage_interface import \
    FolderPermissionStorageInterface
from task_management.interactors.storage_interface.folder_storage_interface import \
    FolderStorageInterface
from task_management.interactors.storage_interface.list_permission_storage_interface import \
    ListPermissionStorageInterface
from task_management.interactors.storage_interface.list_storage_interface import \
    ListStorageInterface
from task_management.interactors.storage_interface.space_permission_storage_interface import \
    SpacePermissionStorageInterface
from task_management.interactors.storage_interface.space_storage_interface import \
    SpaceStorageInterface
from task_management.interactors.storage_interface.template_storage_interface import \
    TemplateStorageInterface
from task_management.interactors.storage_interface.user_storage_interface import \
    UserStorageInterface
from task_management.interactors.storage_interface.workspace_member_storage_interface import \
    WorkspaceMemberStorageInterface
from task_management.interactors.storage_interface.workspace_storage_interface import \
    WorkspaceStorageInterface
from task_management.interactors.validation_mixin import ValidationMixin
from task_management.interactors.workspace_interactors.workspace_member_interactors import \
    WorkspaceMemberInteractor


class WorkspaceInteractor(ValidationMixin):
    def __init__(self, workspace_storage: WorkspaceStorageInterface,
                 user_storage: UserStorageInterface,
                 account_storage: AccountStorageInterface,
                 workspace_member_storage: WorkspaceMemberStorageInterface,
                 space_storage: SpaceStorageInterface,
                 space_permission_storage: SpacePermissionStorageInterface,
                 folder_storage: FolderStorageInterface,
                 folder_permission_storage: FolderPermissionStorageInterface,
                 list_storage: ListStorageInterface,
                 list_permission_storage: ListPermissionStorageInterface,
                 template_storage: TemplateStorageInterface,
                 field_storage: FieldStorageInterface):
        self.workspace_storage = workspace_storage
        self.user_storage = user_storage
        self.account_storage = account_storage
        self.workspace_member_storage = workspace_member_storage
        self.space_storage = space_storage
        self.space_permission_storage = space_permission_storage
        self.folder_storage = folder_storage
        self.folder_permission_storage = folder_permission_storage
        self.list_storage = list_storage
        self.list_permission_storage = list_permission_storage
        self.template_storage = template_storage
        self.field_storage = field_storage

    @invalidate_interactor_cache(cache_name="user_workspaces")
    def create_workspace(self, create_workspace_data: CreateWorkspaceDTO) \
            -> WorkspaceDTO:
        self.validate_user_is_active(create_workspace_data.user_id,
                                     user_storage=self.user_storage)
        self.validate_account_is_active(create_workspace_data.account_id,
                                        account_storage=self.account_storage)
        self.validate_user_is_account_owner(
            create_workspace_data.user_id,
            account_id=create_workspace_data.account_id,
            account_storage=self.account_storage)

        result = self.workspace_storage.create_workspace(
            workspace_data=create_workspace_data)

        create_workspace_member = AddMemberToWorkspaceDTO(
            workspace_id=result.workspace_id,
            user_id=create_workspace_data.user_id,
            role=Role.OWNER,
            added_by=create_workspace_data.user_id,
        )
        self.workspace_member_storage.add_member_to_workspace(
            create_workspace_member)

        self._create_space(workspace_id=result.workspace_id,
                           user_id=result.user_id)

        return result

    @invalidate_interactor_cache(cache_name="workspace_users")
    def update_workspace(self, update_workspace_data: UpdateWorkspaceDTO,
                         user_id: str) -> WorkspaceDTO:
        self.validate_workspace_is_active(
            update_workspace_data.workspace_id,
            workspace_storage=self.workspace_storage)
        self.validate_user_access_for_workspace(
            user_id=user_id, workspace_id=update_workspace_data.workspace_id,
            workspace_member_storage=self.workspace_member_storage)

        return self.workspace_storage.update_workspace(
            workspace_data=update_workspace_data)

    @invalidate_interactor_cache(cache_name="user_workspaces")
    def delete_workspace(self, workspace_id: str,
                         user_id: str) -> WorkspaceDTO:
        self.validate_user_is_workspace_owner(
            user_id=user_id, workspace_id=workspace_id,
            workspace_storage=self.workspace_storage)
        self.validate_workspace_is_active(
            workspace_id, workspace_storage=self.workspace_storage)
        return self.workspace_storage.delete_workspace(
            workspace_id=workspace_id)

    @invalidate_interactor_cache(cache_name="user_workspaces")
    def transfer_workspace(self, workspace_id: str, user_id: str,
                           new_user_id: str) -> WorkspaceDTO:
        self.validate_user_is_workspace_owner(user_id=user_id,
                                              workspace_id=workspace_id,
                                              workspace_storage=self.workspace_storage)
        self.validate_user_is_active(user_id=new_user_id,
                                     user_storage=self.user_storage)
        result = self.workspace_storage.transfer_workspace(
            workspace_id=workspace_id, new_user_id=new_user_id)

        workspace_member_interactor = WorkspaceMemberInteractor(
            workspace_member_storage=self.workspace_member_storage,
            user_storage=self.user_storage,
            workspace_storage=self.workspace_storage,
            list_storage=self.list_storage,
            list_permission_storage=self.list_permission_storage,
            folder_storage=self.folder_storage,
            folder_permission_storage=self.folder_permission_storage,
            space_storage=self.space_storage,
            space_permission_storage=self.space_permission_storage,
        )
        workspace_member_interactor.change_member_role(
            workspace_id=workspace_id, user_id=new_user_id,
            role=Role.OWNER.value,
            changed_by=new_user_id)

        workspace_member_interactor.change_member_role(
            workspace_id=workspace_id, user_id=user_id, role=Role.MEMBER.value,
            changed_by=new_user_id)


        return result

    def get_workspace(self, workspace_id: str) -> WorkspaceDTO:
        self.validate_workspace_is_active(workspace_id,
                                          workspace_storage=self.workspace_storage)

        return self.workspace_storage.get_workspace(workspace_id=workspace_id)

    def account_workspaces(self, account_id: str) -> list[WorkspaceDTO]:
        self.validate_account_is_active(account_id,
                                        account_storage=self.account_storage)

        return self.workspace_storage.get_workspaces_by_account(
            account_id=account_id)

    def _create_space(self, user_id: str, workspace_id: str):
        space_interactor = SpaceInteractor(
            space_storage=self.space_storage,
            permission_storage=self.space_permission_storage,
            list_storage=self.list_storage,
            workspace_storage=self.workspace_storage,
            workspace_member_storage=self.workspace_member_storage,
        )

        space_input_data = CreateSpaceDTO(
            name="Space",
            description="Default space",
            created_by=user_id,
            workspace_id=workspace_id,
            is_private=False
        )

        space_data = space_interactor.create_space(space_input_data)

        return self._create_list(space_id=space_data.space_id,
                                 user_id=user_id, )

    def _create_list(self, space_id: str, user_id: str):
        list_interactor = ListInteractor(
            list_storage=self.list_storage,
            template_storage=self.template_storage,
            list_permission_storage=self.list_permission_storage,
            folder_storage=self.folder_storage,
            folder_permission_storage=self.folder_permission_storage,
            space_storage=self.space_storage,
            space_permission_storage=self.space_permission_storage,
            field_storage=self.field_storage,
        )

        list_input_data = CreateListDTO(
            name="List 1",
            description="Default list",
            created_by=user_id,
            space_id=space_id,
            is_private=False,
            folder_id=None
        )

        return list_interactor.create_list(list_input_data)
