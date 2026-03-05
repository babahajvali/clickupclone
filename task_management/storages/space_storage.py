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
            permission: SpacePermission) -> UserSpacePermissionDTO:
        return UserSpacePermissionDTO(
            id=permission.pk,
            space_id=str(permission.space.space_id),
            user_id=str(permission.user.user_id),
            permission_type=permission.permission_type,
            is_active=permission.is_active,
            added_by=str(
                permission.added_by.user_id) if permission.added_by else None,
        )

    @staticmethod
    def _convert_space_to_dto(space_data: Space) -> SpaceDTO:
        return SpaceDTO(
            space_id=str(space_data.space_id),
            name=space_data.name,
            description=space_data.description,
            workspace_id=str(space_data.workspace.workspace_id),
            is_deleted=space_data.is_deleted,
            order=space_data.order,
            is_private=space_data.is_private,
            created_by=str(space_data.created_by.user_id)
        )

    def get_space(self, space_id: str) -> SpaceDTO | None:
        space_data = Space.objects.filter(space_id=space_id).first()

        if space_data is None:
            return None

        return self._convert_space_to_dto(space_data=space_data)

    def create_space(
            self, space_data: CreateSpaceDTO, order: int) -> SpaceDTO:

        space = Space.objects.create(
            name=space_data.name,
            description=space_data.description,
            workspace_id=space_data.workspace_id,
            order=order,
            is_private=space_data.is_private,
            created_by_id=space_data.created_by
        )

        return self._convert_space_to_dto(space)

    def get_last_space_order_in_workspace(self, workspace_id: str) -> int:

        last_space = Space.objects.filter(
            workspace_id=workspace_id, is_deleted=False).order_by(
            '-order').first()

        order = 0
        if last_space:
            order = last_space.order

        return order

    def update_space(
            self, space_id: str, name: Optional[str],
            description: Optional[str]) -> SpaceDTO:

        space_data = Space.objects.get(space_id=space_id)

        if name is not None:
            space_data.name = name

        if description is not None:
            space_data.description = description

        space_data.save()

        return self._convert_space_to_dto(space_data)

    def delete_space(self, space_id: str) -> SpaceDTO:

        space = Space.objects.get(space_id=space_id)
        space.is_deleted = True
        space.save(update_fields=["is_deleted"])

        current_order = space.order
        workspace_id = space.workspace.workspace_id

        Space.objects.filter(
            workspace_id=workspace_id, is_deleted=False,
            order__gt=current_order).update(order=F('order') - 1)

        return self._convert_space_to_dto(space)

    def update_space_visibility(
            self, space_id: str, visibility: str) -> SpaceDTO:

        space = Space.objects.get(space_id=space_id)
        space.is_private = visibility == VisibilityType.PRIVATE.value
        space.save(update_fields=["is_private"])

        return self._convert_space_to_dto(space)

    def get_workspace_spaces(self, workspace_id: str) -> List[SpaceDTO]:

        spaces = Space.objects.filter(
            workspace_id=workspace_id,
            is_deleted=False
        )

        return [self._convert_space_to_dto(space) for space in spaces]

    def get_workspace_spaces_count(self, workspace_id: str) -> int:
        return Space.objects.filter(
            workspace_id=workspace_id, is_deleted=False).count()

    @transaction.atomic
    def update_space_order(self, space_id: str, new_order: int) -> SpaceDTO:

        space = Space.objects.get(space_id=space_id)
        space.order = new_order
        space.save()

        return self._convert_space_to_dto(space)

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
            'workspace_id', flat=True)[0]

    def create_user_space_permissions(
            self, permission_data: List[CreateUserSpacePermissionDTO]) \
            -> List[UserSpacePermissionDTO]:

        permissions_to_create = []
        for perm_data in permission_data:
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

        return [self._convert_space_permission_to_dto(perm) for perm in
                created_permissions]
