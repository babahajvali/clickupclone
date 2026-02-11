from django.db import transaction

from task_management.exceptions.enums import Role
from task_management.interactors.dtos import CreateListDTO, CreateSpaceDTO
from task_management.interactors.list_interactors.list_interactors import \
    ListInteractor
from task_management.interactors.space_interactors.space_interactors import \
    SpaceInteractor
from task_management.interactors.storage_interfaces import \
    SpaceStorageInterface, UserStorageInterface, \
    SpacePermissionStorageInterface, WorkspaceStorageInterface, \
    WorkspaceMemberStorageInterface, ListStorageInterface, \
    TemplateStorageInterface, FieldStorageInterface, FolderStorageInterface, \
    ListPermissionStorageInterface, FolderPermissionStorageInterface, \
    AccountStorageInterface
from task_management.interactors.workspace.workspace import \
    Workspace
from task_management.interactors.workspace.workspace_member_interactors import \
    WorkspaceMemberInteractor


class WorkspaceOnboardingHandler:
    def __init__(self, space_storage: SpaceStorageInterface,
                 user_storage: UserStorageInterface,
                 space_permission_storage: SpacePermissionStorageInterface,
                 workspace_storage: WorkspaceStorageInterface,
                 workspace_member_storage: WorkspaceMemberStorageInterface,
                 list_storage: ListStorageInterface,
                 template_storage: TemplateStorageInterface,
                 field_storage: FieldStorageInterface,
                 folder_storage: FolderStorageInterface,
                 list_permission_storage: ListPermissionStorageInterface,
                 folder_permission_storage: FolderPermissionStorageInterface,
                 account_storage: AccountStorageInterface):
        self.workspace_storage = workspace_storage
        self.user_storage = user_storage
        self.workspace_member_storage = workspace_member_storage
        self.space_storage = space_storage
        self.space_permission_storage = space_permission_storage
        self.folder_storage = folder_storage
        self.folder_permission_storage = folder_permission_storage
        self.list_storage = list_storage
        self.list_permission_storage = list_permission_storage
        self.template_storage = template_storage
        self.field_storage = field_storage
        self.account_storage = account_storage

    @transaction.atomic
    def handle(self, user_id: str, workspace_id: str):
        space_data = self._create_space(workspace_id=workspace_id,
                                        user_id=user_id)

        return self._create_list(space_id=space_data.space_id, user_id=user_id)

    def _create_space(self, user_id: str, workspace_id: str):
        space_interactor = SpaceInteractor(
            space_storage=self.space_storage,
            space_permission_storage=self.space_permission_storage,
            workspace_storage=self.workspace_storage,
            workspace_member_storage=self.workspace_member_storage,
        )

        space_input_data = CreateSpaceDTO(
            name=f"Space",
            description=f"Default space",
            created_by=user_id,
            workspace_id=workspace_id,
            is_private=False
        )
        return space_interactor.create_space(space_input_data)

    def _create_list(self, space_id: str, user_id: str):
        list_interactor = ListInteractor(
            list_storage=self.list_storage,
            template_storage=self.template_storage,
            list_permission_storage=self.list_permission_storage,
            folder_storage=self.folder_storage,
            space_storage=self.space_storage,
            field_storage=self.field_storage,
            workspace_member_storage=self.workspace_member_storage
        )

        list_input_data = CreateListDTO(
            name=f"List 1",
            description=f"Default list",
            created_by=user_id,
            space_id=space_id,
            is_private=False,
            folder_id=None
        )

        return list_interactor.create_list(list_input_data)

    def transfer_the_workspace(self, workspace_id: str, current_user_id: str,
                               new_user_id: str):
        workspace_interactor = Workspace(
            workspace_storage=self.workspace_storage,
            workspace_member_storage=self.workspace_member_storage,
            account_storage=self.account_storage,
            user_storage=self.user_storage
        )

        workspace_interactor.transfer_workspace(
            workspace_id=workspace_id, user_id=current_user_id,
            new_user_id=new_user_id)

        return self.change_permissions_for_user_in_transfer(
            workspace_id=workspace_id, user_id=current_user_id,
            new_user_id=new_user_id, )

    def change_permissions_for_user_in_transfer(
            self, workspace_id: str, user_id: str, new_user_id: str):
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
