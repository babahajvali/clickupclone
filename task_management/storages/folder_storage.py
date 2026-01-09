from django.db.models import F

from task_management.interactors.dtos import CreateFolderDTO, FolderDTO, \
    UpdateFolderDTO
from task_management.interactors.storage_interface.folder_storage_interface import \
    FolderStorageInterface
from task_management.models import Folder, Space, User


class FolderStorage(FolderStorageInterface):

    @staticmethod
    def _folder_dto(data: Folder) -> FolderDTO:
        return FolderDTO(
            folder_id=data.folder_id,
            name=data.name,
            description=data.description,
            space_id=data.space.space_id,
            order=data.order,
            is_active=data.is_active,
            created_by=data.created_by.user_id,
            is_private=data.is_private,
        )

    def get_folder(self, folder_id: str):
        folder_data = Folder.objects.get(folder_id=folder_id)

        return self._folder_dto(folder_data)

    def create_folder(self, create_folder_data: CreateFolderDTO) -> FolderDTO:
        space = Space.objects.get(space_id=create_folder_data.space_id)
        user = User.objects.get(user_id=create_folder_data.created_by)
        last_folder = Folder.objects.filter(
            space=space,is_active=True).order_by('-order').first()
        next_order = (last_folder.order + 1) if last_folder else 1

        folder_data = Folder.objects.create(
            name=create_folder_data.name, order=next_order,
            description=create_folder_data.description, space=space,
            is_private=create_folder_data.is_private, created_by=user)

        return self._folder_dto(folder_data)

    def update_folder(self, update_folder_data: UpdateFolderDTO) -> FolderDTO:
        folder_data = Folder.objects.get(
            folder_id=update_folder_data.folder_id)

        if update_folder_data.name is not None:
            folder_data.name = update_folder_data.name

        if update_folder_data.description is not None:
            folder_data.description = update_folder_data.description

        folder_data.save()

        return self._folder_dto(folder_data)

    def reorder_folder(self, folder_id: str, new_order: int) -> FolderDTO:
        folder_data = Folder.objects.get(folder_id=folder_id)
        old_order = folder_data.order

        if new_order == old_order:
            return self._folder_dto(folder_data)

        if new_order > old_order:
            Folder.objects.filter(
                space_id=folder_data.space.space_id,
                is_active=True,
                order__gt=old_order,
                order__lte=new_order
            ).update(order=F('order') - 1)
        else:
            Folder.objects.filter(
                space_id=folder_data.space.space_id,
                is_active=True,
                order__gte=new_order,
                order__lt=old_order
            ).update(order=F('order') + 1)

        folder_data.order = new_order
        folder_data.save()

        return self._folder_dto(folder_data)

    def remove_folder(self, folder_id: str) -> FolderDTO:
        folder_data = Folder.objects.get(folder_id=folder_id)
        folder_data.is_active = False
        folder_data.save()

        current_order = folder_data.order
        Folder.objects.filter(
            space_id=folder_data.space.space_id, is_active=True,
            order__gt=current_order).update(order=F('order') - 1)

        return self._folder_dto(folder_data)

    def get_space_folders(self, space_ids: list[str]) -> list[FolderDTO]:
        folders_data = Folder.objects.filter(space_id__in=space_ids,
                                             is_active=True)

        return [self._folder_dto(data=data) for data in folders_data]

    def set_folder_private(self, folder_id: str) -> FolderDTO:
        folder_data = Folder.objects.get(folder_id=folder_id)
        folder_data.is_private = True
        folder_data.save()

        return self._folder_dto(folder_data)

    def set_folder_public(self, folder_id: str) -> FolderDTO:
        folder_data = Folder.objects.get(folder_id=folder_id)
        folder_data.is_private = False
        folder_data.save()

        return self._folder_dto(folder_data)

    def get_space_folder_count(self, space_id: str) -> int:
        return Folder.objects.filter(space_id=space_id, is_active=True).count()
