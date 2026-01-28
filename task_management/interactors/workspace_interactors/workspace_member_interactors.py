from task_management.exceptions.enums import PermissionsEnum, Role
from task_management.interactors.dtos import AddMemberToWorkspaceDTO, \
    WorkspaceMemberDTO, CreateUserSpacePermissionDTO, \
    CreateUserFolderPermissionDTO, CreateUserListPermissionDTO
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
from task_management.interactors.storage_interface.user_storage_interface import \
    UserStorageInterface
from task_management.interactors.storage_interface.workspace_member_storage_interface import \
    WorkspaceMemberStorageInterface
from task_management.interactors.storage_interface.workspace_storage_interface import \
    WorkspaceStorageInterface
from task_management.interactors.validation_mixin import ValidationMixin
from task_management.decorators.caching_decorators import interactor_cache, \
    invalidate_interactor_cache


class WorkspaceMemberInteractor(ValidationMixin):

    def __init__(self,
                 workspace_member_storage: WorkspaceMemberStorageInterface,
                 workspace_storage: WorkspaceStorageInterface,
                 user_storage: UserStorageInterface,
                 space_permission_storage: SpacePermissionStorageInterface,
                 folder_permission_storage: FolderPermissionStorageInterface,
                 list_permission_storage: ListPermissionStorageInterface,
                 space_storage: SpaceStorageInterface,
                 folder_storage: FolderStorageInterface,
                 list_storage: ListStorageInterface):
        self.workspace_member_storage = workspace_member_storage
        self.workspace_storage = workspace_storage
        self.user_storage = user_storage
        self.space_permission_storage = space_permission_storage
        self.folder_permission_storage = folder_permission_storage
        self.list_permission_storage = list_permission_storage
        self.space_storage = space_storage
        self.folder_storage = folder_storage
        self.list_storage = list_storage

    @invalidate_interactor_cache(cache_name="user_workspaces")
    def add_member_to_workspace(self,
                                workspace_member_data: AddMemberToWorkspaceDTO) -> WorkspaceMemberDTO:
        existed_member = self.workspace_member_storage.get_workspace_member(
            workspace_id=workspace_member_data.workspace_id,
            user_id=workspace_member_data.user_id)
        if existed_member:
            if not existed_member.is_active:
                existed_member = self.workspace_member_storage.re_add_member_to_workspace(
                    workspace_member_data=workspace_member_data)
            return existed_member
        self.validate_workspace_is_active(
            workspace_id=workspace_member_data.workspace_id,
            workspace_storage=self.workspace_storage)
        self.validate_user_is_active(
            user_id=workspace_member_data.user_id,
            user_storage=self.user_storage)
        self.validate_role(role=workspace_member_data.role.value)

        self.validate_user_can_modify_workspace(
            user_id=workspace_member_data.added_by,
            workspace_id=workspace_member_data.workspace_id,
            workspace_storage=self.workspace_storage,
            workspace_member_storage=self.workspace_member_storage)

        workspace_member = self.workspace_member_storage.add_member_to_workspace(
            workspace_member_data=workspace_member_data)

        self.add_permissions_for_workspace_spaces(
            workspace_id=workspace_member_data.workspace_id,
            user_id=workspace_member_data.user_id,
            role=workspace_member_data.role.value,
            added_by=workspace_member_data.added_by
        )

        return workspace_member

    @invalidate_interactor_cache(cache_name="user_workspaces")
    def remove_member_from_workspace(self, workspace_member_id: int,
                                     removed_by: str) -> WorkspaceMemberDTO:
        self.validate_workspace_member_is_active(
            workspace_member_id=workspace_member_id,
            workspace_member_storage=self.workspace_member_storage)
        workspace_member_data = self.workspace_member_storage.get_workspace_member_by_id(
            workspace_member_id=workspace_member_id)
        self.validate_user_can_modify_workspace(
            user_id=removed_by,
            workspace_id=workspace_member_data.workspace_id,
            workspace_storage=self.workspace_storage,
            workspace_member_storage=self.workspace_member_storage)

        workspace_member = self.workspace_member_storage.remove_member_from_workspace(
            workspace_member_id=workspace_member_id)

        self.remove_permissions_for_workspace_spaces(
            workspace_id=workspace_member_data.workspace_id,
            user_id=workspace_member_data.user_id
        )

        return workspace_member

    @invalidate_interactor_cache(cache_name="user_workspaces")
    def change_member_role(
            self, workspace_id: str, user_id: str, role: str,
            changed_by: str) -> WorkspaceMemberDTO:
        self.validate_workspace_is_active(workspace_id=workspace_id,
                                          workspace_storage=self.workspace_storage)
        self.validate_user_is_active(user_id=user_id,
                                     user_storage=self.user_storage)
        self.validate_user_can_modify_workspace(user_id=changed_by,
                                                workspace_id=workspace_id,
                                                workspace_storage=self.workspace_storage,
                                                workspace_member_storage=self.workspace_member_storage)
        self.validate_role(role=role)

        workspace_member = self.workspace_member_storage.update_the_member_role(
            workspace_id=workspace_id, user_id=user_id, role=role)

        self.update_permissions_for_workspace_spaces(
            workspace_id=workspace_id,
            user_id=user_id,
            role=role
        )

        return workspace_member

    def add_permissions_for_workspace_spaces(self, workspace_id: str,
                                             user_id: str,
                                             role: str, added_by: str):
        self.validate_workspace_is_active(workspace_id=workspace_id,
                                          workspace_storage=self.workspace_storage)

        workspace_spaces = self.space_storage.get_workspace_spaces(
            workspace_id=workspace_id)
        space_ids = [each.space_id for each in workspace_spaces]
        user_spaces_permission = []

        for each in workspace_spaces:
            permission_type = self._get_permission_type_by_role(role)
            space_permission = CreateUserSpacePermissionDTO(
                user_id=user_id,
                space_id=each.space_id,
                permission_type=permission_type,
                added_by=added_by
            )
            user_spaces_permission.append(space_permission)

        if user_spaces_permission:
            self.space_permission_storage.create_user_space_permissions(
                permission_data=user_spaces_permission)

        self.add_permissions_space_folders(
            space_ids=space_ids,
            user_id=user_id,
            role=role,
            added_by=added_by
        )

    def add_permissions_space_folders(self, space_ids: list[str], user_id: str,
                                      role: str, added_by: str):
        space_folders = self.folder_storage.get_space_folders(
            space_ids=space_ids)

        folder_permissions = []

        for each in space_folders:
            permission_type = self._get_permission_type_by_role(role)

            folder_permission = CreateUserFolderPermissionDTO(
                user_id=user_id,
                folder_id=each.folder_id,
                permission_type=permission_type,
                added_by=added_by
            )
            folder_permissions.append(folder_permission)

        if folder_permissions:
            self.folder_permission_storage.create_folder_users_permissions(
                users_permission_data=folder_permissions)

        self.add_permissions_for_lists(
            space_ids=space_ids,
            user_id=user_id,
            role=role,
            added_by=added_by
        )

    def add_permissions_for_lists(self, space_ids: list[str],
                                  user_id: str, role: str, added_by: str):
        space_lists = self.list_storage.get_space_lists(space_ids=space_ids)

        list_permissions = []
        permission_type = self._get_permission_type_by_role(role)

        for each_list in space_lists:
            list_permission = CreateUserListPermissionDTO(
                user_id=user_id,
                list_id=each_list.list_id,
                permission_type=permission_type,
                added_by=added_by
            )
            list_permissions.append(list_permission)

        if list_permissions:
            self.list_permission_storage.create_list_users_permissions(
                user_permissions=list_permissions)

    def remove_permissions_for_workspace_spaces(self, workspace_id: str,
                                                user_id: str):
        workspace_spaces = self.space_storage.get_workspace_spaces(
            workspace_id=workspace_id)
        space_ids = [each.space_id for each in workspace_spaces]

        for space_id in space_ids:
            self.space_permission_storage.remove_user_permission_for_space(
                user_id=user_id,
                space_id=space_id
            )

        self.remove_permissions_space_folders(
            space_ids=space_ids,
            user_id=user_id
        )

    def remove_permissions_space_folders(self, space_ids: list[str],
                                         user_id: str):
        space_folders = self.folder_storage.get_space_folders(
            space_ids=space_ids)

        for folder in space_folders:
            self.folder_permission_storage.remove_user_permission_for_folder(
                folder_id=folder.folder_id,
                user_id=user_id
            )

        self.remove_permissions_for_lists(
            space_ids=space_ids,
            user_id=user_id
        )

    def remove_permissions_for_lists(self, space_ids: list[str], user_id: str):

        space_lists = self.list_storage.get_space_lists(space_ids=space_ids)

        for each_list in space_lists:
            self.list_permission_storage.remove_user_permission_for_list(
                list_id=each_list.list_id,
                user_id=user_id
            )

    def update_permissions_for_workspace_spaces(self, workspace_id: str,
                                                user_id: str, role: str):
        workspace_spaces = self.space_storage.get_workspace_spaces(
            workspace_id=workspace_id)
        space_ids = [each.space_id for each in workspace_spaces]

        permission_type = self._get_permission_type_by_role(role)

        for space_id in space_ids:
            self.space_permission_storage.update_user_permission_for_space(
                user_id=user_id,
                space_id=space_id,
                permission_type=permission_type
            )

        self.update_permissions_space_folders(
            space_ids=space_ids,
            user_id=user_id,
            role=role
        )

    def update_permissions_space_folders(self, space_ids: list[str],
                                         user_id: str, role: str):
        space_folders = self.folder_storage.get_space_folders(
            space_ids=space_ids)

        permission_type = self._get_permission_type_by_role(role)

        for folder in space_folders:
            self.folder_permission_storage.update_user_permission_for_folder(
                user_id=user_id,
                folder_id=folder.folder_id,
                permission_type=permission_type
            )

        self.update_permissions_for_lists(
            space_ids=space_ids,
            user_id=user_id,
            role=role
        )

    def update_permissions_for_lists(self, space_ids: list[str],
                                     user_id: str, role: str):
        space_lists = self.list_storage.get_space_lists(space_ids=space_ids)

        permission_type = self._get_permission_type_by_role(role)

        for each_list in space_lists:
            self.list_permission_storage.update_user_permission_for_list(
                list_id=each_list.list_id,
                user_id=user_id,
                permission_type=permission_type
            )

    @interactor_cache(cache_name="user_workspaces", timeout=5 * 60)
    def get_user_workspaces(self, user_id: str) -> list[WorkspaceMemberDTO]:

        return self.workspace_member_storage.get_user_workspaces(
            user_id=user_id)

    @staticmethod
    def _get_permission_type_by_role(role: str) -> PermissionsEnum:
        if role == Role.GUEST.value:
            return PermissionsEnum.VIEW
        else:
            return PermissionsEnum.FULL_EDIT
