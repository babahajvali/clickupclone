from unittest.mock import create_autospec, patch

from task_management.exceptions.enums import Permissions
from task_management.interactors.dtos import CreateSpaceDTO, SpaceDTO
from task_management.interactors.spaces.space_creation_handler import (
    SpaceCreationHandler,
)
from task_management.interactors.storage_interfaces import (
    SpaceStorageInterface,
    WorkspaceStorageInterface,
)


def make_space(is_private: bool = False) -> SpaceDTO:
    return SpaceDTO(
        space_id="space_1",
        name="Space",
        description="Desc",
        workspace_id="workspace_1",
        order=1,
        is_deleted=False,
        is_private=is_private,
        created_by="user_1",
    )


class TestSpaceCreationHandler:
    def setup_method(self):
        self.space_storage = create_autospec(SpaceStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)

        self.handler = SpaceCreationHandler(
            space_storage=self.space_storage,
            workspace_storage=self.workspace_storage,
        )

    def test_handle_space_creation_public_success(self, snapshot):
        dto = CreateSpaceDTO(
            name="Space",
            description="Desc",
            workspace_id="workspace_1",
            is_private=False,
            created_by="user_1",
        )

        with patch.object(
            self.handler, "_create_space", return_value=make_space(is_private=False)
        ) as create_space, patch.object(
            self.handler, "_create_space_permission_for_user"
        ) as create_permission:
            result = self.handler.handle_space_creation(space_input=dto)

        snapshot.assert_match(
            repr(result), "handle_space_creation_public_success.txt"
        )
        create_space.assert_called_once_with(space_input=dto)
        create_permission.assert_not_called()

    def test_handle_space_creation_private_calls_permission(self, snapshot):
        dto = CreateSpaceDTO(
            name="Space",
            description="Desc",
            workspace_id="workspace_1",
            is_private=True,
            created_by="user_1",
        )

        with patch.object(
            self.handler, "_create_space", return_value=make_space(is_private=True)
        ) as create_space, patch.object(
            self.handler, "_create_space_permission_for_user"
        ) as create_permission:
            result = self.handler.handle_space_creation(space_input=dto)

        snapshot.assert_match(
            repr(result), "handle_space_creation_private_success.txt"
        )
        create_space.assert_called_once_with(space_input=dto)
        create_permission.assert_called_once_with(
            space_id="space_1", user_id="user_1"
        )

    def test_create_space_permission_for_user_builds_dto(self, snapshot):
        with patch.object(
            self.handler, "_get_create_space_interactor"
        ) as get_interactor:
            interactor = get_interactor.return_value

            self.handler._create_space_permission_for_user(
                space_id="space_1", user_id="user_1"
            )

        interactor.add_user_for_space_permission.assert_called_once()
        called_user_data = interactor.add_user_for_space_permission.call_args.kwargs[
            "user_data"
        ]

        snapshot.assert_match(
            repr(called_user_data),
            "create_space_permission_for_user_builds_dto.txt",
        )
        assert called_user_data.permission_type == Permissions.FULL_EDIT
