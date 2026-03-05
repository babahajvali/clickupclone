from typing import Optional, List

from django.db.models import F

from task_management.exceptions.enums import VisibilityType
from task_management.interactors.dtos import CreateFolderDTO, FolderDTO, \
    UserFolderPermissionDTO, CreateFolderPermissionDTO
from task_management.interactors.storage_interfaces.folder_storage_interface import \
    FolderStorageInterface
from task_management.models import FolderPermission, Folder


class FolderStorage(FolderStorageInterface):

    @staticmethod
    def _convert_folder_to_dto(data: Folder) -> FolderDTO:
        return FolderDTO(
            folder_id=data.folder_id,
            name=data.name,
            description=data.description,
            space_id=data.space.space_id,
            order=data.order,
            is_deleted=data.is_deleted,
            created_by=data.created_by.user_id,
            is_private=data.is_private,
        )

    def get_folder(self, folder_id: str) -> FolderDTO | None:

        folder_data = Folder.objects.filter(folder_id=folder_id).first()

        if not folder_data:
            return None

        return self._convert_folder_to_dto(folder_data)

    def create_folder(
            self, create_folder_data: CreateFolderDTO, order: int) \
            -> FolderDTO:

        folder_data = Folder.objects.create(
            name=create_folder_data.name, order=order,
            description=create_folder_data.description,
            space_id=create_folder_data.space_id,
            is_private=create_folder_data.is_private,
            created_by_id=create_folder_data.created_by)

        return self._convert_folder_to_dto(folder_data)

    def get_last_folder_order_in_space(self, space_id: str) -> int:
        last_folder = Folder.objects.filter(
            space_id=space_id, is_deleted=False).order_by('-order').first()

        return last_folder.order if last_folder else 0

    def update_folder(
            self, folder_id: str, name: Optional[str],
            description: Optional[str]) -> FolderDTO:

        folder_data = Folder.objects.get(folder_id=folder_id)

        is_name_provided = name is not None
        if is_name_provided:
            folder_data.name = name

        is_description_provided = description is not None
        if is_description_provided:
            folder_data.description = description

        folder_data.save()

        return self._convert_folder_to_dto(folder_data)

    def update_folder_order(self, folder_id: str, new_order: int) -> FolderDTO:

        folder_data = Folder.objects.get(folder_id=folder_id)

        folder_data.order = new_order
        folder_data.save(update_fields=['order'])

        return self._convert_folder_to_dto(folder_data)

    def shift_folders_down(
            self, space_id: str, old_order: int, new_order: int):

        Folder.objects.filter(
            space_id=space_id,
            is_deleted=False,
            order__gt=old_order,
            order__lte=new_order
        ).update(order=F('order') - 1)

    def shift_folders_up(self, space_id: str, old_order: int, new_order: int):
        Folder.objects.filter(
            space_id=space_id,
            is_deleted=False,
            order__gte=new_order,
            order__lt=old_order
        ).update(order=F('order') + 1)

    def delete_folder(self, folder_id: str) -> FolderDTO:

        folder_data = Folder.objects.get(folder_id=folder_id)
        folder_data.is_deleted = True
        folder_data.save(update_fields=["is_deleted"])

        current_order = folder_data.order
        Folder.objects.filter(
            space_id=folder_data.space.space_id, is_deleted=False,
            order__gt=current_order).update(order=F('order') - 1)

        return self._convert_folder_to_dto(folder_data)

    def get_workspace_id_from_folder_id(self, folder_id: str) -> str:
        folder_data = Folder.objects.select_related("space__workspace").get(
            folder_id=folder_id)

        return folder_data.space.workspace.workspace_id

    def get_space_folders(
            self, space_ids: list[str]) -> list[FolderDTO]:

        folders_data = Folder.objects.filter(
            space_id__in=space_ids, is_deleted=False)

        return [self._convert_folder_to_dto(data=data) for data in
                folders_data]

    def update_folder_visibility(
            self, folder_id: str, visibility: str) -> FolderDTO:

        folder_data = Folder.objects.get(folder_id=folder_id)
        folder_data.is_private = visibility == VisibilityType.PRIVATE.value
        folder_data.save(update_fields=["is_private"])

        return self._convert_folder_to_dto(folder_data)

    def get_space_folder_count(self, space_id: str) -> int:
        return Folder.objects.filter(
            space_id=space_id, is_deleted=False).count()

    def get_folder_space_id(self, folder_id: str) -> str:
        folder_data = Folder.objects.filter(folder_id=folder_id). \
            values('space_id')

        return folder_data[0]['space_id']

    @staticmethod
    def _convert_user_folder_permission_to_dto(
            data: FolderPermission) -> UserFolderPermissionDTO:
        return UserFolderPermissionDTO(
            id=data.pk,
            folder_id=data.folder.folder_id,
            user_id=data.user.user_id,
            permission_type=data.permission_type,
            is_active=data.is_active,
            added_by=data.added_by.user_id,
        )

    def create_folder_users_permissions(
            self, users_permission_data: List[CreateFolderPermissionDTO]) -> \
            List[UserFolderPermissionDTO]:

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

        return [self._convert_user_folder_permission_to_dto(data=perm) for perm
                in
                created_permissions]
