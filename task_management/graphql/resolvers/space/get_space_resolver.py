from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import SpaceNotFoundType
from task_management.graphql.types.types import SpaceType
from task_management.interactors.spaces.get_space_interactor import \
    GetSpaceInteractor

from task_management.storages import SpaceStorage


def get_space_resolver(root, info, params):
    space_id = params.space_id

    space_storage = SpaceStorage()

    interactor = GetSpaceInteractor(
        space_storage=space_storage,
    )

    try:
        space_dto = interactor.get_space(space_id=space_id)

        space_output = SpaceType(
            space_id=space_dto.space_id,
            name=space_dto.name,
            description=space_dto.description,
            workspace_id=space_dto.workspace_id,
            order=space_dto.order,
            is_deleted=space_dto.is_deleted,
            is_private=space_dto.is_private,
            created_by=space_dto.created_by
        )

        return space_output

    except custom_exceptions.SpaceNotFound as e:
        return SpaceNotFoundType(space_id=e.space_id)
