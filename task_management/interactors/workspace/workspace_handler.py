from django.db import transaction

from task_management.exceptions.enums import Role
from task_management.interactors.dtos import CreateListDTO, CreateSpaceDTO
from task_management.interactors.list.list_creation_handler import \
    ListCreationHandler
from task_management.interactors.space.space_interactor import \
    SpaceInteractor
from task_management.interactors.storage_interfaces import \
    SpaceStorageInterface, UserStorageInterface, \
    WorkspaceStorageInterface, ListStorageInterface, \
    TemplateStorageInterface, FieldStorageInterface, FolderStorageInterface, \
    AccountStorageInterface, ViewStorageInterface
from task_management.interactors.workspace.workspace_interactor import \
    WorkspaceInteractor


class WorkspaceHandler:
    def __init__(self, space_storage: SpaceStorageInterface,
                 user_storage: UserStorageInterface,
                 workspace_storage: WorkspaceStorageInterface,
                 list_storage: ListStorageInterface,
                 template_storage: TemplateStorageInterface,
                 field_storage: FieldStorageInterface,
                 folder_storage: FolderStorageInterface,
                 account_storage: AccountStorageInterface,
                 view_storage: ViewStorageInterface):
        self.workspace_storage = workspace_storage
        self.user_storage = user_storage
        self.space_storage = space_storage
        self.folder_storage = folder_storage
        self.list_storage = list_storage
        self.template_storage = template_storage
        self.field_storage = field_storage
        self.account_storage = account_storage
        self.view_storage = view_storage

    @transaction.atomic
    def handle(self, user_id: str, workspace_id: str):
        space_data = self._create_space(workspace_id=workspace_id,
                                        user_id=user_id)

        self._create_list(space_id=space_data.space_id, user_id=user_id)
        return space_data

    def _create_space(self, user_id: str, workspace_id: str):
        space_interactor = SpaceInteractor(
            space_storage=self.space_storage,
            workspace_storage=self.workspace_storage,
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
        list_handler = ListCreationHandler(
            list_storage=self.list_storage,
            template_storage=self.template_storage,
            folder_storage=self.folder_storage,
            space_storage=self.space_storage,
            field_storage=self.field_storage,
            workspace_storage=self.workspace_storage,
            view_storage=self.view_storage
        )

        list_input_data = CreateListDTO(
            name=f"List 1",
            description=f"Default list",
            created_by=user_id,
            space_id=space_id,
            is_private=False,
            folder_id=None
        )

        return list_handler.handel_list(list_input_data)

    def transfer_the_workspace(self, workspace_id: str, current_user_id: str,
                               new_user_id: str):
        workspace_interactor = WorkspaceInteractor(
            workspace_storage=self.workspace_storage,
            account_storage=self.account_storage,
            user_storage=self.user_storage
        )

        workspace_interactor.transfer_workspace(
            workspace_id=workspace_id, user_id=current_user_id,
            new_user_id=new_user_id)

        return self.change_permissions_for_user_in_transfer(
            workspace_id=workspace_id, user_id=current_user_id,
            new_user_id=new_user_id)

    def change_permissions_for_user_in_transfer(
            self, workspace_id: str, user_id: str, new_user_id: str):
        self.workspace_storage.update_the_member_role(
            workspace_id=workspace_id, user_id=new_user_id,
            role=Role.OWNER.value)

        return self.workspace_storage.update_the_member_role(
            workspace_id=workspace_id, user_id=user_id, role=Role.MEMBER.value)

    def delete_workspace_handle(self, workspace_id: str, user_id: str):
        workspace_interactor = WorkspaceInteractor(
            workspace_storage=self.workspace_storage,
            account_storage=self.account_storage,
            user_storage=self.user_storage
        )
        workspace_data = workspace_interactor.delete_workspace(
            workspace_id=workspace_id, user_id=user_id)
        workspace_members = self.workspace_storage.get_workspace_members(
            workspace_id=workspace_id)

        workspace_member_ids = [obj.id for obj in workspace_members]

        self.workspace_storage.deactivate_workspace_members(
            member_ids=workspace_member_ids)

        return workspace_data