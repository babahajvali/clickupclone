from django.db import transaction
from django.db.models import F

from task_management.interactors.dtos import UpdateSpaceDTO, SpaceDTO, \
    CreateSpaceDTO
from task_management.interactors.storage_interface.space_storage_interface import \
    SpaceStorageInterface
from task_management.models import Space, Workspace, User


class SpaceStorage(SpaceStorageInterface):

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
            created_by=str(space_data.created_by.user_id))

    def get_space(self, space_id: str) -> SpaceDTO:
        space_data = Space.objects.get(space_id=space_id)

        return self._to_dto(space_data=space_data)

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

    def update_space(self, update_space_data: UpdateSpaceDTO) -> SpaceDTO:
        space = Space.objects.get(space_id=update_space_data.space_id)

        if update_space_data.name is not None:
            space.name = update_space_data.name

        if update_space_data.description is not None:
            space.description = update_space_data.description

        space.save()

        return self._to_dto(space)

    def remove_space(self, space_id: str) -> SpaceDTO:
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

    def get_workspace_spaces(self, workspace_id: str) -> list[SpaceDTO]:
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
