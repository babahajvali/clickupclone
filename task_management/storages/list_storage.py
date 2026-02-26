from django.db.models import F
from typing import Optional

from task_management.exceptions.enums import Permissions, Visibility
from task_management.interactors.dtos import ListDTO, CreateListDTO, \
    UserListPermissionDTO, CreateListPermissionDTO
from task_management.interactors.storage_interfaces.list_storage_interface import \
    ListStorageInterface
from task_management.models import ListPermission, List, Template


class ListStorage(ListStorageInterface):

    @staticmethod
    def _list_dto(list_data: List) -> ListDTO:
        return ListDTO(
            list_id=list_data.list_id,
            name=list_data.name,
            description=list_data.description,
            space_id=list_data.space.space_id,
            is_deleted=list_data.is_deleted,
            order=list_data.order,
            created_by=list_data.created_by.user_id,
            folder_id=list_data.folder.folder_id if list_data.folder else None,
            is_private=list_data.is_private,
        )

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

    def get_template_id_by_list_id(self, list_id: str) -> str:
        return Template.objects.get(list_id=list_id).template_id

    def get_list(self, list_id: str) -> ListDTO | None:
        list_data = List.objects.filter(list_id=list_id).first()

        if list_data is None:
            return None

        return self._list_dto(list_data=list_data)

    def is_list_exists(self, list_id: str) -> bool:
        return List.objects.filter(list_id=list_id).exists()

    def create_list(self, list_data: CreateListDTO, order: int) -> ListDTO:

        list_data = List.objects.create(
            name=list_data.name,
            description=list_data.description,
            space_id=list_data.space_id,
            folder_id=list_data.folder_id,
            order=order,
            is_private=list_data.is_private,
            created_by_id=list_data.created_by
        )

        return self._list_dto(list_data=list_data)

    def get_last_list_order_in_folder(self, folder_id: str) -> int:
        last_list = List.objects.filter(
            folder_id=folder_id, is_deleted=False).order_by('-order').first()
        order = 0

        if last_list:
            order = last_list.order

        return order

    def get_last_list_order_in_space(self, space_id: str) -> int:
        list_data = List.objects.filter(
            space_id=space_id, folder__isnull=True, is_deleted=False).order_by(
            '-order').first()

        order = 0
        if list_data:
            order = list_data.order

        return order

    def get_workspace_id_by_list_id(self, list_id: str) -> str:
        list_data = List.objects.select_related("space__workspace").get(
            list_id=list_id)

        return list_data.space.workspace.workspace_id

    def update_list(self, list_id: str, name: Optional[str],
                    description: Optional[str]) -> ListDTO:

        list_data = List.objects.get(list_id=list_id)
        is_name_provided = name is not None
        is_description_provided = description is not None

        if is_name_provided:
            list_data.name = name

        if is_description_provided:
            list_data.description = description

        list_data.save()

        return self._list_dto(list_data=list_data)

    def get_folder_lists(self, folder_ids: list[str]) -> list[ListDTO]:
        folder_lists = List.objects.filter(folder_id__in=folder_ids,
                                           is_deleted=False)

        return [self._list_dto(list_data=data) for data in folder_lists]

    def get_space_lists(self, space_ids: list[str]) -> list[ListDTO]:
        space_lists = List.objects.filter(
            space_id__in=space_ids, folder__isnull=True, is_deleted=False)

        return [self._list_dto(list_data=data) for data in space_lists]

    def delete_list(self, list_id: str) -> ListDTO:

        list_data = List.objects.get(list_id=list_id)
        list_data.is_deleted = True
        list_data.save(update_fields=["is_deleted"])

        current_order = list_data.order
        if list_data.folder:
            List.objects.filter(
                folder_id=list_data.folder.folder_id, is_deleted=False,
                order__gt=current_order).update(order=F('order') - 1)
        else:
            List.objects.filter(
                space_id=list_data.space.space_id, is_deleted=False,
                folder__isnull=True, order__gt=current_order).update(
                order=F('order') - 1)

        return self._list_dto(list_data=list_data)


    def update_list_visibility(self, list_id: str, visibility: str) -> ListDTO:
        # set is_private false
        list_data = List.objects.get(list_id=list_id)
        list_data.is_private = visibility == Visibility.PRIVATE.value

        list_data.save(update_fields=["is_private"])

        return self._list_dto(list_data=list_data)

    def update_list_order_in_folder(
            self, folder_id: str, list_id: str, order: int) -> ListDTO:

        list_data = List.objects.get(list_id=list_id)

        list_data.order = order
        list_data.save()

        return self._list_dto(list_data=list_data)

    def shift_lists_down_in_folder(
            self, folder_id: str, old_order: int, new_order: int):

        List.objects.filter(
            folder_id=folder_id,
            is_delted=False,
            order__gt=old_order,
            order__lte=new_order
        ).update(order=F('order') - 1)

    def shift_lists_up_in_folder(
            self, folder_id: str, old_order: int, new_order: int):

        List.objects.filter(
            folder_id=folder_id,
            is_deleted=False,
            order__gte=new_order,
            order_lt=old_order
        ).update(order=F('order') + 1)

    def update_list_order_in_space(
            self, space_id: str, list_id: str, order: int) -> ListDTO:

        list_data = List.objects.get(list_id=list_id)

        list_data.order = order
        list_data.save(update_fields=["order"])

        return self._list_dto(list_data=list_data)

    def shift_lists_down_in_space(
            self, space_id: str, old_order: int, new_order: int):

        List.objects.filter(
            space_id=space_id,
            is_deleted=False,
            order__gt=old_order,
            order__lte=new_order
        ).update(order=F('order') - 1)

    def shift_lists_up_in_space(
            self, space_id: str, old_order: int, new_order: int):

        List.objects.filter(
            space_id=space_id,
            is_deleted=False,
            order__gte=old_order,
            order__lt=new_order
        ).update(order=F('order') + 1)

    def get_folder_lists_count(self, folder_id: str) -> int:

        return List.objects.filter(
            folder_id=folder_id, is_deleted=False).count()

    def get_space_lists_count(self, space_id: str) -> int:

        return List.objects.filter(
            space_id=space_id, folder__isnull=True, is_deleted=False).count()

    def get_list_space_id(self, list_id: str) -> str:

        return List.objects.filter(list_id=list_id).values_list(
            'space_id', flat=True)[0]

    def update_user_permission_for_list(
            self, list_id: str, user_id: str, permission_type: Permissions) \
            -> UserListPermissionDTO:

        permission = ListPermission.objects.get(
            list_id=list_id,
            user_id=user_id
        )
        permission.permission_type = permission_type.value
        permission.save()

        return self._list_permission_dto(permission_data=permission)

    def get_list_permissions(
            self, list_id: str) -> list[UserListPermissionDTO]:

        permissions = ListPermission.objects.filter(
            list_id=list_id
        )

        return [self._list_permission_dto(perm) for perm in permissions]

    def get_user_permission_for_list(
            self, user_id: str, list_id: str) -> UserListPermissionDTO | None:

        permission = ListPermission.objects.filter(
            list_id=list_id, user_id=user_id).order_by('created_at').last()

        return self._list_permission_dto(permission_data=permission)

    def remove_user_permission_for_list(
            self, list_id: str, user_id: str) -> UserListPermissionDTO:

        permission = ListPermission.objects.get(
            list_id=list_id,
            user_id=user_id
        )
        permission.is_active = False
        permission.save(update_fields=["is_active"])

        return self._list_permission_dto(permission_data=permission)

    def create_list_users_permission(
            self, user_permissions: list[CreateListPermissionDTO]) \
            -> list[UserListPermissionDTO]:

        permissions_to_create = []
        for perm_data in user_permissions:
            permissions_to_create.append(
                ListPermission(
                    list_id=perm_data.list_id,
                    user_id=perm_data.user_id,
                    permission_type=perm_data.permission_type.value,
                    added_by_id=perm_data.added_by,
                )
            )

        created_permissions = ListPermission.objects.bulk_create(
            permissions_to_create)

        return [self._list_permission_dto(perm) for perm in
                created_permissions]
