from task_management.exceptions.enums import PermissionsEnum
from task_management.interactors.dtos import UserFolderPermissionDTO, \
    CreateUserFolderPermissionDTO
from task_management.interactors.storage_interface.folder_permission_storage_interface import \
    FolderPermissionStorageInterface
from task_management.models import FolderPermission, Folder, User


class FolderPermissionStorage(FolderPermissionStorageInterface):

    @staticmethod
    def _user_folder_permission_dto(
            data: FolderPermission) -> UserFolderPermissionDTO:
        return UserFolderPermissionDTO(
            id=data.pk,
            folder_id=data.folder.folder_id,
            user_id=data.user.user_id,
            permission_type=data.permission_type,
            is_active=data.is_active,
            added_by=data.added_by.user_id,
        )

    def get_user_permission_for_folder(
            self, user_id: str,
            folder_id: str) -> UserFolderPermissionDTO | None:
        try:
            user_folder_permission = FolderPermission.objects.get(
                user_id=user_id,
                folder_id=folder_id)

            return self._user_folder_permission_dto(
                data=user_folder_permission)
        except FolderPermission.DoesNotExist:
            return None

    def update_user_permission_for_folder(self, user_id: str, folder_id: str,
                                          permission_type: PermissionsEnum) -> UserFolderPermissionDTO:
        user_folder_permission = FolderPermission.objects.get(user_id=user_id,
                                                              folder_id=folder_id)
        user_folder_permission.permission_type = permission_type.value
        user_folder_permission.save()

        return self._user_folder_permission_dto(data=user_folder_permission)

    def remove_user_permission_for_folder(self, folder_id: str,
                                          user_id: str) -> UserFolderPermissionDTO:
        user_folder_permission = FolderPermission.objects.get(user_id=user_id,
                                                              folder_id=folder_id)
        user_folder_permission.is_active = False
        user_folder_permission.save()

        return self._user_folder_permission_dto(data=user_folder_permission)

    def get_folder_permissions(self, folder_id: str) -> list[
        UserFolderPermissionDTO]:
        folder_permissions = FolderPermission.objects.filter(
            folder_id=folder_id)

        return [self._user_folder_permission_dto(data=data) for data in
                folder_permissions]

    def create_folder_users_permissions(self,
                                        users_permission_data: list[
                                            CreateUserFolderPermissionDTO]) -> \
            list[UserFolderPermissionDTO]:
        folder_ids = list(
            set(perm.folder_id for perm in users_permission_data))
        user_ids = list(set(perm.user_id for perm in users_permission_data))
        added_by_ids = list(
            set(perm.added_by for perm in users_permission_data))

        folders = {str(f.folder_id): f for f in
                   Folder.objects.filter(folder_id__in=folder_ids)}
        users = {str(u.user_id): u for u in
                 User.objects.filter(user_id__in=user_ids)}
        added_by_users = {str(u.user_id): u for u in
                          User.objects.filter(user_id__in=added_by_ids)}

        permissions_to_create = []
        for perm_data in users_permission_data:
            folder = folders.get(str(perm_data.folder_id))
            user = users.get(str(perm_data.user_id))
            added_by_user = added_by_users.get(str(perm_data.added_by))
            permissions_to_create.append(
                FolderPermission(
                    folder=folder,
                    user=user,
                    permission_type=perm_data.permission_type.value,
                    added_by=added_by_user,
                )
            )
        created_permissions = FolderPermission.objects.bulk_create(
            permissions_to_create
        )

        return [self._user_folder_permission_dto(data=perm) for perm in
                created_permissions]
