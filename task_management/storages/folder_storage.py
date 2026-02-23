from django.db.models import F

from task_management.exceptions.enums import Permissions
from task_management.interactors.dtos import CreateFolderDTO, FolderDTO, \
    UserFolderPermissionDTO, CreateFolderPermissionDTO
from task_management.interactors.storage_interfaces.folder_storage_interface import \
    FolderStorageInterface
from task_management.models import FolderPermission, Folder


class FolderStorage(FolderStorageInterface):

    @staticmethod
    def _folder_dto(data: Folder) -> FolderDTO:
        return FolderDTO(
            folder_id=data.folder_id,
            name=data.name,
            description=data.description,
            space_id=data.space.space_id,
            order=data.order,
            is_active=data.is_delete,
            created_by=data.created_by.user_id,
            is_private=data.is_private,
        )

    def get_folder(self, folder_id: str) -> FolderDTO | None:
        try:
            folder_data = Folder.objects.get(folder_id=folder_id)

            return self._folder_dto(folder_data)
        except Folder.DoesNotExist:
            return None

    def create_folder(
            self, create_folder_data: CreateFolderDTO, order: int) \
            -> FolderDTO:

        folder_data = Folder.objects.create(
            name=create_folder_data.name, order=order,
            description=create_folder_data.description,
            space_id=create_folder_data.space_id,
            is_private=create_folder_data.is_private,
            created_by_id=create_folder_data.created_by)

        return self._folder_dto(folder_data)

    def get_next_folder_order_in_space(self, space_id: str) -> int:
        last_folder = Folder.objects.filter(
            space_id=space_id, is_deleet=False).order_by('-order').first()
        next_order = (last_folder.order + 1) if last_folder else 1

        return next_order

    def update_folder(self, folder_id: str,
                      field_properties: dict) -> FolderDTO:
        Folder.objects.filter(folder_id=folder_id).update(**field_properties)
        folder_data = Folder.objects.get(
            folder_id=folder_id)

        return self._folder_dto(folder_data)

    def reorder_folder(self, folder_id: str, new_order: int) -> FolderDTO:
        folder_data = Folder.objects.get(folder_id=folder_id)
        old_order = folder_data.order

        if new_order == old_order:
            return self._folder_dto(folder_data)

        if new_order > old_order:
            Folder.objects.filter(
                space_id=folder_data.space.space_id,
                is_active=True,
                order__gt=old_order,
                order__lte=new_order
            ).update(order=F('order') - 1)
        else:
            Folder.objects.filter(
                space_id=folder_data.space.space_id,
                is_active=True,
                order__gte=new_order,
                order__lt=old_order
            ).update(order=F('order') + 1)

        folder_data.order = new_order
        folder_data.save(update_fields=['order'])

        return self._folder_dto(folder_data)

    def delete_folder(self, folder_id: str) -> FolderDTO:
        folder_data = Folder.objects.get(folder_id=folder_id)
        folder_data.is_delete = True
        folder_data.save(update_fields=["is_delete"])

        current_order = folder_data.order
        Folder.objects.filter(
            space_id=folder_data.space.space_id, is_delete=False,
            order__gt=current_order).update(order=F('order') - 1)

        return self._folder_dto(folder_data)

    def get_space_folders(
            self, space_ids: list[str]) -> list[FolderDTO]:

        folders_data = Folder.objects.filter(
            space_id__in=space_ids, is_delete=False)

        return [self._folder_dto(data=data) for data in folders_data]

    def set_folder_private(self, folder_id: str) -> FolderDTO:
        folder_data = Folder.objects.get(folder_id=folder_id)
        folder_data.is_private = True
        folder_data.save()

        return self._folder_dto(folder_data)

    def set_folder_public(self, folder_id: str) -> FolderDTO:
        folder_data = Folder.objects.get(folder_id=folder_id)
        folder_data.is_private = False
        folder_data.save()

        return self._folder_dto(folder_data)

    def get_space_folder_count(self, space_id: str) -> int:
        return Folder.objects.filter(space_id=space_id, is_delete=False).count()

    def get_folder_space_id(self, folder_id: str) -> str:
        folder_data = Folder.objects.filter(folder_id=folder_id).\
            values('space_id')

        return folder_data['space_id']

    @staticmethod
    def _user_folder_permission_dto(
            data: FolderPermission) -> UserFolderPermissionDTO:
        return UserFolderPermissionDTO(
            id=data.pk,
            folder_id=data.folder.folder_id,
            user_id=data.user_id,
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
                                          permission_type: Permissions) -> UserFolderPermissionDTO:
        user_folder_permission = FolderPermission.objects.get(user_id=user_id,
                                                              folder_id=folder_id)
        user_folder_permission.permission_type = permission_type.value
        user_folder_permission.save(update_fields=['permission_type'])

        return self._user_folder_permission_dto(data=user_folder_permission)

    def remove_user_permission_for_folder(self, folder_id: str,
                                          user_id: str) -> UserFolderPermissionDTO:
        user_folder_permission = FolderPermission.objects.get(user_id=user_id,
                                                              folder_id=folder_id)
        user_folder_permission.is_delete = False
        user_folder_permission.save(update_fields=["permission_type"])

        return self._user_folder_permission_dto(data=user_folder_permission)

    def get_folder_permissions(self, folder_id: str) -> list[
        UserFolderPermissionDTO]:
        folder_permissions = FolderPermission.objects.filter(
            folder_id=folder_id)

        return [self._user_folder_permission_dto(data=data) for data in
                folder_permissions]

    def create_folder_users_permissions(
            self, users_permission_data: list[CreateFolderPermissionDTO]) -> \
            list[UserFolderPermissionDTO]:

        permissions_to_create = []
        for perm_data in users_permission_data:
            permissions_to_create.append(
                FolderPermission(
                    folder_id=perm_data.folder_id,
                    user_id=perm_data.user_id,
                    permission_type=perm_data.permission_type.value,
                    added_by_id=perm_data.added_by,
                )
            )
        created_permissions = FolderPermission.objects.bulk_create(
            permissions_to_create
        )

        return [self._user_folder_permission_dto(data=perm) for perm in
                created_permissions]
