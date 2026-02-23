from django.db import transaction
from django.db.models import F

from task_management.exceptions.enums import Permissions
from task_management.interactors.dtos import SpaceDTO, \
    CreateSpaceDTO, UserSpacePermissionDTO, CreateUserSpacePermissionDTO
from task_management.interactors.storage_interfaces.space_storage_interface import \
    SpaceStorageInterface
from task_management.models import Space, SpacePermission


class SpaceStorage(SpaceStorageInterface):

    @staticmethod
    def _to_permission_dto(
            permission: SpacePermission) -> UserSpacePermissionDTO:
        return UserSpacePermissionDTO(
            id=permission.pk,
            space_id=str(permission.space.space_id),
            user_id=str(permission.user.user_id),
            permission_type=permission.permission_type,
            is_active=permission.is_active,
            added_by=str(permission.added_by.user_id),
        )

    @staticmethod
    def _to_dto(space_data: Space) -> SpaceDTO:
        return SpaceDTO(
            space_id=str(space_data.space_id),
            name=space_data.name,
            description=space_data.description,
            workspace_id=str(space_data.workspace.workspace_id),
            is_active=space_data.is_active,
            order=space_data.order,
            is_private=space_data.is_private,
            created_by=str(space_data.created_by.user_id)
        )

    def get_space(self, space_id: str) -> SpaceDTO | None:
        try:
            space_data = Space.objects.get(space_id=space_id)

            return self._to_dto(space_data=space_data)
        except Space.DoesNotExist:
            return None

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

        return self._to_dto(space)

    def get_next_space_order_in_workspace(self, workspace_id: str) -> int:
        last_space = Space.objects.filter(
            workspace_id=workspace_id, is_active=True).order_by(
            '-order').first()

        next_order = (last_space.order + 1) if last_space else 1

        return next_order


    def update_space(self, space_id: str, field_properties: dict) -> SpaceDTO:
        Space.objects.filter(space_id=space_id).update(**field_properties)
        space = Space.objects.get(space_id=space_id)

        return self._to_dto(space)

    def delete_space(self, space_id: str) -> SpaceDTO:
        space = Space.objects.get(space_id=space_id)
        current_order = space.order
        workspace_id = space.workspace.workspace_id

        space.is_delete = False
        space.save()

        Space.objects.filter(
            workspace_id=workspace_id, is_active=True, order__gt=current_order
        ).update(order=F('order') - 1)

        return self._to_dto(space)

    def set_space_private(self, space_id: str) -> SpaceDTO:
        space = Space.objects.get(space_id=space_id)
        space.is_private = True
        space.save()
        return self._to_dto(space)

    def set_space_public(self, space_id: str) -> SpaceDTO:
        space = Space.objects.get(space_id=space_id)
        space.is_private = False
        space.save()
        return self._to_dto(space)

    def get_active_workspace_spaces(self, workspace_id: str) -> list[SpaceDTO]:
        spaces = Space.objects.filter(
            workspace_id=workspace_id,
            is_active=True
        )

        return [self._to_dto(space) for space in spaces]

    def get_workspace_spaces_count(self, workspace_id: str) -> int:
        return Space.objects.filter(
            workspace_id=workspace_id, is_active=True).count()

    @transaction.atomic
    def reorder_space(self, workspace_id: str, space_id: str,
                      new_order: int) -> SpaceDTO:
        space = Space.objects.get(space_id=space_id)
        old_order = space.order

        if old_order == new_order:
            return self._to_dto(space)

        if new_order > old_order:
            Space.objects.filter(
                workspace_id=workspace_id,
                is_active=True,
                order__gt=old_order,
                order__lte=new_order
            ).update(order=F('order') - 1)
        else:
            Space.objects.filter(
                workspace_id=workspace_id,
                is_active=True,
                order__gte=new_order,
                order__lt=old_order
            ).update(order=F('order') + 1)

        space.order = new_order
        space.save()

        return self._to_dto(space)

    def get_space_workspace_id(self, space_id: str) -> str:
        return Space.objects.filter(space_id=space_id).values_list(
            'workspace_id', flat=True)[0]

    def get_user_permission_for_space(self, user_id: str,
                                      space_id: str) -> UserSpacePermissionDTO | None:
        try:
            permission = SpacePermission.objects.get(
                user_id=user_id,
                space_id=space_id
            )
            return self._to_permission_dto(permission)
        except SpacePermission.DoesNotExist:
            return None

    def update_user_permission_for_space(
            self, user_id: str, space_id: str,
            permission_type: Permissions) -> UserSpacePermissionDTO:
        permission = SpacePermission.objects.get(
            user_id=user_id,
            space_id=space_id
        )
        permission.permission_type = permission_type.value
        permission.save()

        return self._to_permission_dto(permission)

    def remove_user_permission_for_space(self, user_id: str,
                                         space_id: str) -> UserSpacePermissionDTO:
        permission = SpacePermission.objects.get(
            user_id=user_id,
            space_id=space_id
        )
        permission.is_delete = False
        permission.save()

        return self._to_permission_dto(permission)

    def get_space_permissions(self, space_id: str) -> list[
        UserSpacePermissionDTO]:
        permissions = SpacePermission.objects.filter(space_id=space_id,
                                                     is_active=True)

        return [self._to_permission_dto(perm) for perm in permissions]

    def create_user_space_permissions(
            self, permission_data: list[CreateUserSpacePermissionDTO]) \
            -> list[UserSpacePermissionDTO]:


        permissions_to_create = []
        for perm_data in permission_data:

            permissions_to_create.append(
                SpacePermission(
                    space_id=perm_data.space_id,
                    user=perm_data.user_id,
                    permission_type=perm_data.permission_type.value,
                    added_by=perm_data.added_by,
                    is_active=True
                )
            )

        created_permissions = SpacePermission.objects.bulk_create(
            permissions_to_create,
            ignore_conflicts=True
        )


        return [self._to_permission_dto(perm) for perm in created_permissions]

    def check_space_exists(self, space_id: str) -> bool:
        return Space.objects.filter(space_id=space_id).exists()
