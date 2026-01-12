from django.db.models import F

from task_management.interactors.dtos import ListDTO, CreateListDTO, \
    UpdateListDTO
from task_management.interactors.storage_interface.list_storage_interface import \
    ListStorageInterface
from task_management.models import List, Template, Space, Folder, User


class ListStorage(ListStorageInterface):

    @staticmethod
    def _list_dto(list_data: List) -> ListDTO:
        return ListDTO(
            list_id=list_data.list_id,
            name=list_data.name,
            description=list_data.description,
            space_id=list_data.space.space_id,
            is_active=list_data.is_active,
            order=list_data.order,
            created_by=list_data.created_by.user_id,
            folder_id=list_data.folder.folder_id if list_data.folder else None,
            is_private=list_data.is_private,
        )

    def get_template_id_by_list_id(self, list_id: str) -> str:
        return Template.objects.get(list_id=list_id).template_id

    def get_list(self, list_id: str) -> ListDTO | None:
        try:
            list_data = List.objects.select_related(
                'space', 'folder', 'created_by'
            ).get(list_id=list_id)

            return self._list_dto(list_data=list_data)
        except List.DoesNotExist:
            return None

    def create_list(self, create_list_data: CreateListDTO) -> ListDTO:
        space = Space.objects.get(space_id=create_list_data.space_id)
        folder = None
        if create_list_data.folder_id:
            folder = Folder.objects.get(folder_id=create_list_data.folder_id)
        user = User.objects.get(user_id=create_list_data.created_by)

        if folder:
            last_list = List.objects.filter(
                folder=folder, is_active=True).order_by('-order').first()
        else:
            last_list = List.objects.filter(
                space=space, folder__isnull=True, is_active=True).order_by(
                '-order').first()

        next_order = (last_list.order + 1) if last_list else 1

        list_obj = List.objects.create(
            name=create_list_data.name,
            description=create_list_data.description,
            space=space,
            folder=folder,
            order=next_order,
            is_private=create_list_data.is_private,
            created_by=user
        )
        
        # Refresh with related objects for DTO conversion
        list_obj = List.objects.select_related(
            'space', 'folder', 'created_by'
        ).get(list_id=list_obj.list_id)

        return self._list_dto(list_data=list_obj)

    def update_list(self, update_list_data: UpdateListDTO) -> ListDTO:
        list_data = List.objects.select_related(
            'space', 'folder', 'created_by'
        ).get(list_id=update_list_data.list_id)
        if update_list_data.description is not None:
            list_data.description = update_list_data.description

        if update_list_data.name is not None:
            list_data.name = update_list_data.name

        list_data.save()

        return self._list_dto(list_data=list_data)

    def get_folder_lists(self, folder_ids: list[str]) -> list[ListDTO]:
        folder_lists = List.objects.filter(
            folder_id__in=folder_ids,
            is_active=True
        ).select_related('space', 'folder', 'created_by')

        return [self._list_dto(list_data=data) for data in folder_lists]

    def get_space_lists(self, space_ids: list[str]) -> list[ListDTO]:
        space_lists = List.objects.filter(
            space_id__in=space_ids, folder__isnull=True, is_active=True
        ).select_related('space', 'folder', 'created_by')

        return [self._list_dto(list_data=data) for data in space_lists]

    def remove_list(self, list_id: str) -> ListDTO:
        # update the is_active false
        list_data = List.objects.select_related('space', 'folder').get(
            list_id=list_id
        )
        list_data.is_active = False
        list_data.save()

        current_order = list_data.order
        if list_data.folder:
            List.objects.filter(
                folder_id=list_data.folder.folder_id, is_active=True,
                order__gt=current_order).update(order=F('order') - 1)
        else:
            List.objects.filter(
                space_id=list_data.space.space_id, is_active=True,
                folder__isnull=True, order__gt=current_order).update(
                order=F('order') - 1)

        return self._list_dto(list_data=list_data)

    def make_list_private(self, list_id: str) -> ListDTO:
        # set the is_private is true
        list_data = List.objects.select_related(
            'space', 'folder', 'created_by'
        ).get(list_id=list_id)
        list_data.is_private = True
        list_data.save()

        return self._list_dto(list_data=list_data)

    def make_list_public(self, list_id: str) -> ListDTO:
        # set is_private false
        list_data = List.objects.select_related(
            'space', 'folder', 'created_by'
        ).get(list_id=list_id)
        list_data.is_private = False
        list_data.save()

        return self._list_dto(list_data=list_data)

    def reorder_list_in_folder(self, folder_id: str, list_id: str,
                               order: int) -> ListDTO:
        list_data = List.objects.select_related(
            'space', 'folder', 'created_by'
        ).get(list_id=list_id)
        old_order = list_data.order
        new_order = order

        if old_order == new_order:
            return self._list_dto(list_data=list_data)

        if new_order > old_order:
            List.objects.filter(
                folder_id=folder_id,
                is_active=True,
                order__gt=old_order,
                order__lte=new_order
            ).update(order=F('order') - 1)
        else:
            List.objects.filter(
                folder_id=folder_id,
                is_active=True,
                order__gte=new_order,
                order__lt=old_order
            ).update(order=F('order') + 1)

        list_data.order = new_order
        list_data.save()

        return self._list_dto(list_data=list_data)

    def reorder_list_in_space(self, space_id: str, list_id: str, order: int) -> \
            ListDTO:
        list_data = List.objects.select_related(
            'space', 'folder', 'created_by'
        ).get(list_id=list_id)
        old_order = list_data.order
        new_order = order

        if old_order == new_order:
            return self._list_dto(list_data=list_data)

        if new_order > old_order:
            List.objects.filter(
                space_id=space_id,
                folder__isnull=True,
                is_active=True,
                order__gt=old_order,
                order__lte=new_order
            ).update(order=F('order') - 1)
        else:
            List.objects.filter(
                space_id=space_id,
                folder__isnull=True,
                is_active=True,
                order__gte=new_order,
                order__lt=old_order
            ).update(order=F('order') + 1)

        list_data.order = new_order
        list_data.save()

        return self._list_dto(list_data=list_data)

    def get_folder_lists_count(self, folder_id: str) -> int:
        return List.objects.filter(folder_id=folder_id, is_active=True).count()

    def get_space_lists_count(self, space_id: str) -> int:
        return List.objects.filter(
            space_id=space_id, folder__isnull=True, is_active=True).count()
