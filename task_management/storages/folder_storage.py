from typing import Optional, List

from django.db import transaction
from django.db.models import F

from task_management.exceptions.enums import VisibilityType
from task_management.interactors.dtos import CreateFolderDTO, FolderDTO, \
    UserFolderPermissionDTO, CreateFolderPermissionDTO
from task_management.interactors.storage_interfaces.folder_storage_interface import \
    FolderStorageInterface
from task_management.models import FolderPermission, Folder


class FolderStorage(FolderStorageInterface):

    @staticmethod
    def _convert_folder_to_dto(folder_obj: Folder) -> FolderDTO:
        return FolderDTO(
            folder_id=folder_obj.folder_id,
            name=folder_obj.name,
            description=folder_obj.description,
            space_id=folder_obj.space_id,
            order=folder_obj.order,
            is_deleted=folder_obj.is_deleted,
            created_by=folder_obj.created_by_id,
            is_private=folder_obj.is_private,
        )

    @staticmethod
    def _convert_folder_permission_to_dto(
            folder_permission_obj: FolderPermission) -> UserFolderPermissionDTO:
        return UserFolderPermissionDTO(
            id=folder_permission_obj.pk,
            folder_id=folder_permission_obj.folder_id,
            user_id=folder_permission_obj.user_id,
            permission_type=folder_permission_obj.permission_type,
            is_active=folder_permission_obj.is_active,
            added_by=folder_permission_obj.added_by_id,
        )

    def get_folder(self, folder_id: str) -> FolderDTO | None:

        folder_obj = Folder.objects.filter(folder_id=folder_id).first()

        if not folder_obj:
            return None

        return self._convert_folder_to_dto(folder_obj=folder_obj)

    def create_folder(
            self, create_folder_dto: CreateFolderDTO, order: int) \
            -> FolderDTO:

        folder_obj = Folder.objects.create(
            name=create_folder_dto.name,
            order=order,
            description=create_folder_dto.description,
            space_id=create_folder_dto.space_id,
            is_private=create_folder_dto.is_private,
            created_by_id=create_folder_dto.created_by,
        )

        return self._convert_folder_to_dto(folder_obj=folder_obj)

    def get_last_folder_order_in_space(self, space_id: str) -> int:
        last_order = Folder.objects.filter(
            space_id=space_id, is_deleted=False
        ).order_by('-order').values_list('order', flat=True).first()
        return last_order or 0

    def update_folder(
            self, folder_id: str, name: Optional[str],
            description: Optional[str]) -> FolderDTO:

        folder_properties = {}
        if name is not None:
            folder_properties['name'] = name
        if description is not None:
            folder_properties['description'] = description

        Folder.objects.filter(folder_id=folder_id).update(**folder_properties)
        return self.get_folder(folder_id=folder_id)

    def update_folder_order(self, folder_id: str, new_order: int) -> FolderDTO:

        Folder.objects.filter(folder_id=folder_id).update(order=new_order)
        return self.get_folder(folder_id=folder_id)

    def shift_folders_down(
            self, space_id: str, current_order: int, new_order: int):

        Folder.objects.filter(
            space_id=space_id,
            is_deleted=False,
            order__gt=current_order,
            order__lte=new_order
        ).update(order=F('order') - 1)

    def shift_folders_up(
            self, space_id: str, current_order: int, new_order: int):
        Folder.objects.filter(
            space_id=space_id,
            is_deleted=False,
            order__gte=new_order,
            order__lt=current_order
        ).update(order=F('order') + 1)

    @transaction.atomic
    def delete_folder(self, folder_id: str) -> FolderDTO:

        Folder.objects.filter(folder_id=folder_id).update(is_deleted=True)
        folder_dto = self.get_folder(folder_id=folder_id)
        Folder.objects.filter(
            space_id=folder_dto.space_id, is_deleted=False,
            order__gt=folder_dto.order).update(order=F('order') - 1)

        return folder_dto

    def get_workspace_id_from_folder_id(self, folder_id: str) -> str:
        return str(Folder.objects.values_list(
            'space__workspace_id', flat=True
        ).get(folder_id=folder_id))

    def get_space_folders(
            self, space_ids: list[str]) -> list[FolderDTO]:

        folders_data = Folder.objects.filter(
            space_id__in=space_ids, is_deleted=False)

        return [self._convert_folder_to_dto(folder_obj=data) for data in
                folders_data]

    def update_folder_visibility(
            self, folder_id: str, visibility: str) -> FolderDTO:

        is_private = visibility == VisibilityType.PRIVATE.value
        Folder.objects.filter(folder_id=folder_id).update(
            is_private=is_private)
        return self.get_folder(folder_id=folder_id)

    def get_space_folder_count(self, space_id: str) -> int:
        return Folder.objects.filter(
            space_id=space_id, is_deleted=False).count()

    def get_folder_space_id(self, folder_id: str) -> str:
        return str(Folder.objects.values_list(
            'space_id', flat=True).get(folder_id=folder_id))

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

        return [self._convert_folder_permission_to_dto(
            folder_permission_obj=permission_obj) for permission_obj in
            created_permissions]

    def get_user_folder_permission(
            self, folder_id: str, user_id: str) -> UserFolderPermissionDTO:
        permission_obj = FolderPermission.objects.filter(
            folder_id=folder_id,
            user_id=user_id,
            is_active=True,
        ).first()

        if permission_obj is None:
            return None

        return self._convert_folder_permission_to_dto(
            folder_permission_obj=permission_obj)
