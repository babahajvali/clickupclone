from task_management.exceptions.enums import PermissionsEnum
from task_management.interactors.dtos import UserSpacePermissionDTO, \
    CreateUserSpacePermissionDTO
from task_management.interactors.storage_interface.space_permission_storage_interface import \
    SpacePermissionStorageInterface
from task_management.models import SpacePermission, User, Space


class SpacePermissionStorage(SpacePermissionStorageInterface):

    @staticmethod
    def _to_dto(permission: SpacePermission) -> UserSpacePermissionDTO:
        return UserSpacePermissionDTO(
            id=permission.pk,
            space_id=str(permission.space.space_id),
            user_id=str(permission.user.user_id),
            permission_type=permission.permission_type,
            is_active=permission.is_active,
            added_by=str(permission.added_by.user_id),
        )

    def get_user_permission_for_space(self, user_id: str,
                                      space_id: str) -> UserSpacePermissionDTO | None:
        try:
            permission = SpacePermission.objects.get(
                user_id=user_id,
                space_id=space_id
            )
            return self._to_dto(permission)
        except SpacePermission.DoesNotExist:
            return None

    def update_user_permission_for_space(
            self, user_id: str, space_id: str,
            permission_type: PermissionsEnum) -> UserSpacePermissionDTO:
        permission = SpacePermission.objects.get(
            user_id=user_id,
            space_id=space_id
        )
        permission.permission_type = permission_type.value
        permission.save()

        return self._to_dto(permission)

    def remove_user_permission_for_space(self, user_id: str,
                                         space_id: str) -> UserSpacePermissionDTO:
        permission = SpacePermission.objects.get(
            user_id=user_id,
            space_id=space_id
        )
        permission.is_active = False
        permission.save()

        return self._to_dto(permission)

    def get_space_permissions(self, space_id: str) -> list[
        UserSpacePermissionDTO]:
        permissions = SpacePermission.objects.filter(space_id=space_id,
                                                     is_active=True)

        return [self._to_dto(perm) for perm in permissions]

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

        return [self._to_dto(perm) for perm in created_permissions]
