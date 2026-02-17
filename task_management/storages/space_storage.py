from django.db import transaction
from django.db.models import F

from task_management.exceptions.enums import Permissions
from task_management.interactors.dtos import  SpaceDTO, \
    CreateSpaceDTO, UserSpacePermissionDTO, CreateUserSpacePermissionDTO
from task_management.interactors.storage_interfaces.space_storage_interface import \
    SpaceStorageInterface
from task_management.models import Space, Workspace, User, SpacePermission


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

    def create_space(self, create_space_data: CreateSpaceDTO) -> SpaceDTO:
        workspace = Workspace.objects.get(
            workspace_id=create_space_data.workspace_id)
        created_by = User.objects.get(user_id=create_space_data.created_by)

        last_space = Space.objects.filter(
            workspace=workspace, is_active=True).order_by('-order').first()
        next_order = (last_space.order + 1) if last_space else 1

        space = Space.objects.create(
            name=create_space_data.name,
            description=create_space_data.description,
            workspace=workspace,
            order=next_order,
            is_private=create_space_data.is_private,
            created_by=created_by
        )

        return self._to_dto(space)

    def update_space(self, space_id: str, update_fields: dict) -> SpaceDTO:
        Space.objects.filter(space_id=space_id).update(**update_fields)
        space = Space.objects.get(space_id=space_id)

        return self._to_dto(space)

    def delete_space(self, space_id: str) -> SpaceDTO:
        space = Space.objects.get(space_id=space_id)
        current_order = space.order
        workspace_id = space.workspace.workspace_id

        space.is_active = False
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

    def get_space_workspace_id(self,space_id: str) -> str:
        return Space.objects.filter(space_id=space_id).values_list('workspace_id', flat=True)[0]

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
        permission.is_active = False
        permission.save()

        return self._to_permission_dto(permission)

    def get_space_permissions(self, space_id: str) -> list[
        UserSpacePermissionDTO]:
        permissions = SpacePermission.objects.filter(space_id=space_id,
                                                     is_active=True)

        return [self._to_permission_dto(perm) for perm in permissions]

    def create_user_space_permissions(self, permission_data: list[
        CreateUserSpacePermissionDTO]) -> list[UserSpacePermissionDTO]:
        space_ids = list(set(perm.space_id for perm in permission_data))
        user_ids = list(set(perm.user_id for perm in permission_data))
        added_by_ids = list(set(perm.added_by for perm in permission_data))

        spaces = {str(s.space_id): s for s in
                  Space.objects.filter(space_id__in=space_ids)}
        users = {str(u.user_id): u for u in
                 User.objects.filter(user_id__in=user_ids)}
        added_by_users = {str(u.user_id): u for u in
                          User.objects.filter(user_id__in=added_by_ids)}

        permissions_to_create = []
        for perm_data in permission_data:
            space = spaces.get(str(perm_data.space_id))
            user = users.get(str(perm_data.user_id))
            added_by_user = added_by_users.get(str(perm_data.added_by))

            permissions_to_create.append(
                SpacePermission(
                    space=space,
                    user=user,
                    permission_type=perm_data.permission_type.value,
                    added_by=added_by_user,
                    is_active=True
                )
            )

        SpacePermission.objects.bulk_create(
            permissions_to_create,
            ignore_conflicts=True
        )

        created_permissions = SpacePermission.objects.filter(
            space_id__in=space_ids,
            user_id__in=user_ids,
            is_active=True
        )

        return [self._to_permission_dto(perm) for perm in created_permissions]

