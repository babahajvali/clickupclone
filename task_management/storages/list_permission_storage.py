from task_management.exceptions.enums import PermissionsEnum
from task_management.interactors.dtos import UserListPermissionDTO, \
    CreateUserListPermissionDTO
from task_management.interactors.storage_interface.list_permission_storage_interface import \
    ListPermissionStorageInterface
from task_management.models import ListPermission, List, User


class ListPermissionStorage(ListPermissionStorageInterface):

    @staticmethod
    def _list_permission_dto(
            permission_data: ListPermission) -> UserListPermissionDTO:
        return UserListPermissionDTO(
            id=permission_data.pk,
            list_id=permission_data.list.list_id,
            user_id=permission_data.user.user_id,
            permission_type=permission_data.permission_type,
            is_active=permission_data.is_active,
            added_by=permission_data.added_by.user_id,
        )

    def update_user_permission_for_list(self, list_id: str, user_id: str,
                                        permission_type: PermissionsEnum) -> UserListPermissionDTO:
        permission = ListPermission.objects.get(
            list_id=list_id,
            user_id=user_id
        )
        permission.permission_type = permission_type.value
        permission.save()

        return self._list_permission_dto(permission_data=permission)

    def get_list_permissions(self, list_id: str) -> list[
        UserListPermissionDTO]:
        permissions = ListPermission.objects.filter(
            list_id=list_id
        )

        return [self._list_permission_dto(perm) for perm in permissions]

    def get_user_permission_for_list(self, user_id: str,
                                     list_id: str) -> UserListPermissionDTO | None:
        try:
            permission = ListPermission.objects.get(
                list_id=list_id,
                user_id=user_id
            )

            return self._list_permission_dto(permission_data=permission)
        except ListPermission.DoesNotExist:
            return None

    def add_user_permission_for_list(self, list_id: str, user_id: str,
                                     permission_type: PermissionsEnum) -> UserListPermissionDTO:
        pass

    def remove_user_permission_for_list(self, list_id: str,
                                        user_id: str) -> UserListPermissionDTO:
        permission = ListPermission.objects.get(
            list_id=list_id,
            user_id=user_id
        )
        permission.is_active = False
        permission.save()

        return self._list_permission_dto(permission_data=permission)

    def create_list_users_permissions(self, user_permissions: list[
        CreateUserListPermissionDTO]) -> list[UserListPermissionDTO]:
        list_ids = list(set(perm.list_id for perm in user_permissions))
        user_ids = list(set(perm.user_id for perm in user_permissions))
        added_by_ids = list(set(perm.added_by for perm in user_permissions))

        lists = {str(l.list_id): l for l in
                 List.objects.filter(list_id__in=list_ids)}
        users = {str(u.user_id): u for u in
                 User.objects.filter(user_id__in=user_ids)}
        added_by_users = {str(u.user_id): u for u in
                          User.objects.filter(user_id__in=added_by_ids)}

        permissions_to_create = []
        for perm_data in user_permissions:
            list_obj = lists.get(str(perm_data.list_id))
            user = users.get(str(perm_data.user_id))
            added_by_user = added_by_users.get(str(perm_data.added_by))
            permissions_to_create.append(
                ListPermission(
                    list=list_obj,
                    user=user,
                    permission_type=perm_data.permission_type.value,
                    added_by=added_by_user,
                )
            )

        created_permissions = ListPermission.objects.bulk_create(
            permissions_to_create)

        return [self._list_permission_dto(perm) for perm in
                created_permissions]
