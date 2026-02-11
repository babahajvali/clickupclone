from task_management.exceptions.enums import Role
from task_management.interactors.workspace_interactors.workspace_member_interactors import \
    WorkspaceMemberInteractor
from task_management.storages.folder_permission_storage import \
    FolderPermissionStorage
from task_management.storages.folder_storage import FolderStorage
from task_management.storages.list_permission_storage import \
    ListPermissionStorage
from task_management.storages.list_storage import ListStorage
from task_management.storages.space_permission_storage import \
    SpacePermissionStorage
from task_management.storages.space_storage import SpaceStorage
from task_management.storages.user_storage import UserStorage
from task_management.storages.workspace_member import WorkspaceMemberStorage
from task_management.storages.workspace_storage import WorkspaceStorage


class WorkspaceTransferService:

    @staticmethod
    def change_permissions_for_user_in_transfer(workspace_id: str, user_id: str, new_user_id: str):
        workspace_member_interactor = WorkspaceMemberInteractor(
            workspace_member_storage=WorkspaceMemberStorage(),
            user_storage=UserStorage(),
            workspace_storage=WorkspaceStorage(),
            list_storage=ListStorage(),
            list_permission_storage=ListPermissionStorage(),
            folder_storage=FolderStorage(),
            folder_permission_storage=FolderPermissionStorage(),
            space_storage=SpaceStorage(),
            space_permission_storage=SpacePermissionStorage(),
        )
        workspace_member_interactor.change_member_role(
            workspace_id=workspace_id, user_id=new_user_id,
            role=Role.OWNER.value,
            changed_by=new_user_id)

        workspace_member_interactor.change_member_role(
            workspace_id=workspace_id, user_id=user_id, role=Role.MEMBER.value,
            changed_by=new_user_id)