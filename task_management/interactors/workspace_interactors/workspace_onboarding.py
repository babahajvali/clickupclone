from task_management.exceptions.enums import Role
from task_management.interactors.dtos import CreateListDTO, CreateSpaceDTO
from task_management.interactors.list_interactors.list_interactors import \
    ListInteractor
from task_management.interactors.space_interactors.space_interactors import \
    SpaceInteractor
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
from task_management.interactors.workspace_interactors.workspace_member_interactors import \
    WorkspaceMemberInteractor


class WorkspaceOnboardingHandler:
    def __init__(self,space_storage: SpaceStorageInterface,
                 user_storage: UserStorageInterface,
                 space_permission_storage: SpacePermissionStorageInterface,
                 workspace_storage: WorkspaceStorageInterface,
                 workspace_member_storage: WorkspaceMemberStorageInterface,
                 list_storage: ListStorageInterface,
                 template_storage: TemplateStorageInterface,
                 field_storage: FieldStorageInterface,
                 folder_storage: FolderStorageInterface,
                 list_permission_storage: ListPermissionStorageInterface,
                 folder_permission_storage: FolderPermissionStorageInterface):
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


    def create_space(self, user_id: str, workspace_id: str):

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

        space_data = space_interactor.create_space(space_input_data)

        return self._create_list(space_id=space_data.space_id,
                                 user_id=user_id, )

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

    def change_permissions_for_user_in_transfer(self, workspace_id: str, user_id: str, new_user_id: str):
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