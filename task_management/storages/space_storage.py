from typing import Optional, List

from django.db import transaction
from django.db.models import F

from task_management.exceptions.enums import VisibilityType
from task_management.interactors.dtos import SpaceDTO, \
    CreateSpaceDTO, UserSpacePermissionDTO, CreateUserSpacePermissionDTO
from task_management.interactors.storage_interfaces.space_storage_interface import \
    SpaceStorageInterface
from task_management.models import Space, SpacePermission


class SpaceStorage(SpaceStorageInterface):

    @staticmethod
    def _convert_space_permission_to_dto(
            permission_obj: SpacePermission) -> UserSpacePermissionDTO:
        return UserSpacePermissionDTO(
            id=permission_obj.pk,
            space_id=str(permission_obj.space_id),
            user_id=str(permission_obj.user_id),
            permission_type=permission_obj.permission_type,
            is_active=permission_obj.is_active,
            added_by=str(permission_obj.added_by_id)
            if permission_obj.added_by_id else None)

    @staticmethod
    def _convert_space_to_dto(space_obj: Space) -> SpaceDTO:
        return SpaceDTO(
            space_id=str(space_obj.space_id),
            name=space_obj.name,
            description=space_obj.description,
            workspace_id=str(space_obj.workspace_id),
            is_deleted=space_obj.is_deleted,
            order=space_obj.order,
            is_private=space_obj.is_private,
            created_by=str(space_obj.created_by_id)
        )

    def get_space(self, space_id: str) -> SpaceDTO | None:
        space_obj = Space.objects.filter(space_id=space_id).first()

        if space_obj is None:
            return None

        return self._convert_space_to_dto(space_obj=space_obj)

    def create_space(
            self, create_space_dto: CreateSpaceDTO, order: int) -> SpaceDTO:

        space_obj = Space.objects.create(
            name=create_space_dto.name,
            description=create_space_dto.description,
            workspace_id=create_space_dto.workspace_id,
            order=order,
            is_private=create_space_dto.is_private,
            created_by_id=create_space_dto.created_by
        )

        return self._convert_space_to_dto(space_obj=space_obj)

    def get_last_space_order_in_workspace(self, workspace_id: str) -> int:

        last_order = Space.objects.filter(
            workspace_id=workspace_id, is_deleted=False
        ).order_by('-order').values_list('order', flat=True).first()

        return last_order or 0

    def update_space(
            self, space_id: str, name: Optional[str],
            description: Optional[str]) -> SpaceDTO:

        space_properties = {}
        if name is not None:
            space_properties['name'] = name

        if description is not None:
            space_properties['description'] = description

        Space.objects.filter(space_id=space_id).update(**space_properties)

        return self.get_space(space_id=space_id)

    @transaction.atomic
    def delete_space(self, space_id: str) -> SpaceDTO:

        Space.objects.filter(space_id=space_id).update(is_deleted=True)

        space_dto = self.get_space(space_id=space_id)

        Space.objects.filter(
            workspace_id=space_dto.workspace_id, is_deleted=False,
            order__gt=space_dto.order).update(order=F('order') - 1)

        return space_dto

    def update_space_visibility(
            self, space_id: str, visibility: str) -> SpaceDTO:
        is_private = visibility == VisibilityType.PRIVATE.value

        Space.objects.filter(space_id=space_id).update(
            is_private=is_private)

        return self.get_space(space_id=space_id)

    def get_workspace_spaces(self, workspace_id: str) -> List[SpaceDTO]:

        space_objs = Space.objects.filter(
            workspace_id=workspace_id,
            is_deleted=False
        )

        return [self._convert_space_to_dto(space_obj=space_obj) for
                space_obj in space_objs]

    def get_workspace_spaces_count(self, workspace_id: str) -> int:
        return Space.objects.filter(
            workspace_id=workspace_id, is_deleted=False).count()

    def update_space_order(self, space_id: str, new_order: int) -> SpaceDTO:

        Space.objects.filter(space_id=space_id).update(order=new_order)

        return self.get_space(space_id=space_id)

    def shift_spaces_down(
            self, workspace_id: str, current_order: int, new_order: int):

        Space.objects.filter(
            workspace_id=workspace_id,
            is_deleted=False,
            order__gt=current_order,
            order__lte=new_order
        ).update(order=F('order') - 1)

    def shift_spaces_up(
            self, workspace_id: str, current_order: int, new_order: int):

        Space.objects.filter(
            workspace_id=workspace_id,
            is_deleted=False,
            order__gte=new_order,
            order__lt=current_order
        ).update(order=F('order') + 1)

    def get_space_workspace_id(self, space_id: str) -> str:

        return Space.objects.filter(space_id=space_id).values_list(
            'workspace_id', flat=True).first()

    def create_user_space_permissions(
            self, permission_dtos: List[CreateUserSpacePermissionDTO]) \
            -> List[UserSpacePermissionDTO]:

        permissions_to_create = []
        for perm_data in permission_dtos:
            permissions_to_create.append(
                SpacePermission(
                    space_id=perm_data.space_id,
                    user_id=perm_data.user_id,
                    permission_type=perm_data.permission_type.value,
                    added_by_id=perm_data.added_by,
                    is_active=True
                )
            )

        created_permissions = SpacePermission.objects.bulk_create(
            permissions_to_create,
            ignore_conflicts=True
        )

        return [self._convert_space_permission_to_dto(space_perm) for
                space_perm in created_permissions]

    def get_user_space_permission(
            self, space_id: str, user_id: str) -> UserSpacePermissionDTO:
        permission_obj = SpacePermission.objects.filter(
            space_id=space_id, user_id=user_id).first()

        return self._convert_space_permission_to_dto(
            permission_obj=permission_obj)
