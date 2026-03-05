from typing import Optional, List as ListType

from django.db.models import F

from task_management.exceptions.enums import VisibilityType, \
    ListEntityType
from task_management.interactors.dtos import ListDTO, CreateListDTO, \
    UserListPermissionDTO, CreateListPermissionDTO
from task_management.interactors.storage_interfaces.list_storage_interface import \
    ListStorageInterface
from task_management.models import ListPermission, List, Template, Folder, \
    Space


class ListStorage(ListStorageInterface):

    @staticmethod
    def _convert_list_to_dto(list_data: List) -> ListDTO:

        return ListDTO(
            list_id=str(list_data.list_id),
            name=list_data.name,
            description=list_data.description,
            entity_type=ListEntityType(list_data.entity_type),
            entity_id=str(list_data.entity_id),
            is_deleted=list_data.is_deleted,
            order=list_data.order,
            created_by=list_data.created_by.user_id,
            is_private=list_data.is_private,
        )

    @staticmethod
    def _convert_list_permission_to_dto(
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

        return self._convert_list_to_dto(list_data=list_data)

    def create_list(self, list_data: CreateListDTO, order: int) -> ListDTO:

        list_obj = List.objects.create(
            name=list_data.name,
            description=list_data.description,
            entity_type=list_data.entity_type.value,
            entity_id=list_data.entity_id,
            order=order,
            is_private=list_data.is_private,
            created_by_id=list_data.created_by
        )

        return self._convert_list_to_dto(list_data=list_obj)

    def get_last_list_order(
            self, entity_type: str, entity_id: str) -> int:

        list_data = List.objects.filter(
            entity_type=entity_type,
            entity_id=entity_id,
            is_deleted=False,
        ).order_by("-order").first()

        return list_data.order if list_data else 0

    def get_workspace_id_by_list_id(self, list_id: str) -> str:
        list_data = List.objects.get(list_id=list_id)
        if list_data.entity_type == ListEntityType.SPACE.value:
            return Space.objects.values_list(
                "workspace_id", flat=True).get(space_id=list_data.entity_id)

        return Folder.objects.values_list(
            "space__workspace_id", flat=True).get(
            folder_id=list_data.entity_id)

    def update_list(
            self, list_id: str, name: Optional[str],
            description: Optional[str]) -> ListDTO:

        list_data = List.objects.get(list_id=list_id)
        is_name_provided = name is not None
        is_description_provided = description is not None

        if is_name_provided:
            list_data.name = name

        if is_description_provided:
            list_data.description = description

        list_data.save()

        return self._convert_list_to_dto(list_data=list_data)

    def get_folder_lists(self, folder_ids: ListType[str]) -> ListType[ListDTO]:
        folder_lists = List.objects.filter(
            entity_type=ListEntityType.FOLDER.value,
            entity_id__in=folder_ids,
            is_deleted=False)

        return [self._convert_list_to_dto(list_data=data) for data in
                folder_lists]

    def get_space_lists(self, space_ids: ListType[str]) -> ListType[ListDTO]:
        space_lists = List.objects.filter(
            entity_type=ListEntityType.SPACE.value,
            entity_id__in=space_ids,
            is_deleted=False)

        return [self._convert_list_to_dto(list_data=data) for data in
                space_lists]

    def delete_list(self, list_id: str) -> ListDTO:

        list_data = List.objects.get(list_id=list_id)
        list_data.is_deleted = True
        list_data.save(update_fields=["is_deleted"])

        current_order = list_data.order
        if list_data.entity_type == ListEntityType.FOLDER.value:
            List.objects.filter(
                entity_type=ListEntityType.FOLDER.value,
                entity_id=list_data.entity_id,
                is_deleted=False,
                order__gt=current_order).update(order=F('order') - 1)
        else:
            List.objects.filter(
                entity_type=ListEntityType.SPACE.value,
                entity_id=list_data.entity_id,
                is_deleted=False,
                order__gt=current_order).update(
                order=F('order') - 1)

        return self._convert_list_to_dto(list_data=list_data)

    def update_list_visibility(self, list_id: str, visibility: str) -> ListDTO:
        # set is_private false
        list_data = List.objects.get(list_id=list_id)
        list_data.is_private = visibility == VisibilityType.PRIVATE.value

        list_data.save(update_fields=["is_private"])

        return self._convert_list_to_dto(list_data=list_data)

    def update_list_order_in_folder(
            self, folder_id: str, list_id: str, order: int) -> ListDTO:

        list_data = List.objects.get(list_id=list_id)

        list_data.order = order
        list_data.save()

        return self._convert_list_to_dto(list_data=list_data)

    def shift_lists_down_in_folder(
            self, folder_id: str, old_order: int, new_order: int):

        List.objects.filter(
            entity_type=ListEntityType.FOLDER.value,
            entity_id=folder_id,
            is_deleted=False,
            order__gt=old_order,
            order__lte=new_order
        ).update(order=F('order') - 1)

    def shift_lists_up_in_folder(
            self, folder_id: str, old_order: int, new_order: int):

        List.objects.filter(
            entity_type=ListEntityType.FOLDER.value,
            entity_id=folder_id,
            is_deleted=False,
            order__gte=new_order,
            order__lt=old_order
        ).update(order=F('order') + 1)

    def update_list_order_in_space(
            self, space_id: str, list_id: str, order: int) -> ListDTO:

        list_data = List.objects.get(
            list_id=list_id,
            entity_type=ListEntityType.SPACE.value,
            entity_id=space_id,
        )

        list_data.order = order
        list_data.save(update_fields=["order"])

        return self._convert_list_to_dto(list_data=list_data)

    def shift_lists_down_in_space(
            self, space_id: str, old_order: int, new_order: int):

        List.objects.filter(
            entity_type=ListEntityType.SPACE.value,
            entity_id=space_id,
            is_deleted=False,
            order__gt=old_order,
            order__lte=new_order
        ).update(order=F('order') - 1)

    def shift_lists_up_in_space(
            self, space_id: str, old_order: int, new_order: int):

        List.objects.filter(
            entity_type=ListEntityType.SPACE.value,
            entity_id=space_id,
            is_deleted=False,
            order__gte=new_order,
            order__lt=old_order
        ).update(order=F('order') + 1)

    def get_folder_lists_count(self, folder_id: str) -> int:

        return List.objects.filter(
            entity_type=ListEntityType.FOLDER.value,
            entity_id=folder_id,
            is_deleted=False).count()

    def get_space_lists_count(self, space_id: str) -> int:

        return List.objects.filter(
            entity_type=ListEntityType.SPACE.value,
            entity_id=space_id,
            is_deleted=False).count()

    def get_list_space_id(self, list_id: str) -> str:
        list_data = List.objects.get(list_id=list_id)
        if list_data.entity_type == ListEntityType.SPACE.value:
            return list_data.entity_id

        return Folder.objects.values_list(
            "space_id", flat=True).get(folder_id=list_data.entity_id)

    def get_user_permission_for_list(
            self, user_id: str, list_id: str) -> UserListPermissionDTO | None:

        permission = ListPermission.objects.filter(
            list_id=list_id,
            user_id=user_id,
            is_active=True
        ).order_by('-created_at').first()

        if permission is None:
            return None

        return self._convert_list_permission_to_dto(permission_data=permission)

    def create_list_users_permission(
            self, user_permissions: ListType[CreateListPermissionDTO]) \
            -> ListType[UserListPermissionDTO]:

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

        return [self._convert_list_permission_to_dto(perm) for perm in
                created_permissions]
