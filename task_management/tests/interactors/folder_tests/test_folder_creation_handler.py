from unittest.mock import create_autospec, patch

from task_management.exceptions.enums import Permissions
from task_management.interactors.dtos import CreateFolderDTO, FolderDTO
from task_management.interactors.folders.folder_creation_handler import (
    FolderCreationHandler,
)
from task_management.interactors.storage_interfaces import (
    FolderStorageInterface,
    SpaceStorageInterface,
    WorkspaceStorageInterface,
)


def make_folder() -> FolderDTO:
    return FolderDTO(
        folder_id="folder_1",
        name="Folder",
        description="Desc",
        space_id="space_1",
        order=1,
        is_deleted=False,
        created_by="user_1",
        is_private=False,
    )


class TestFolderCreationHandler:
    def setup_method(self):
        self.folder_storage = create_autospec(FolderStorageInterface)
        self.space_storage = create_autospec(SpaceStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)

        self.handler = FolderCreationHandler(
            folder_storage=self.folder_storage,
            space_storage=self.space_storage,
            workspace_storage=self.workspace_storage,
        )

    def test_handle_folder_creation_success(self, snapshot):
        dto = CreateFolderDTO(
            name="Folder",
            description="Desc",
            space_id="space_1",
            created_by="user_1",
            is_private=False,
        )

        with patch.object(
            self.handler, "_create_folder", return_value=make_folder()
        ) as create_folder, patch.object(
            self.handler, "_create_folder_permission_for_user"
        ) as create_permission:
            result = self.handler.handle_folder_creation(folder_data=dto)

        snapshot.assert_match(repr(result), "handle_folder_creation_success.txt")
        create_folder.assert_called_once_with(folder_data=dto)
        create_permission.assert_not_called()

    def test_create_folder_permission_for_user_builds_dto(self, snapshot):
        with patch.object(
            self.handler, "_get_permission_interactor"
        ) as get_permission_interactor:
            permission_interactor = get_permission_interactor.return_value

            self.handler._create_folder_permission_for_user(
                folder_id="folder_1", user_id="user_1"
            )

        permission_interactor.add_user_for_folder_permission.assert_called_once()
        called_permission_dto = (
            permission_interactor.add_user_for_folder_permission.call_args.kwargs[
                "permission_data"
            ]
        )

        snapshot.assert_match(
            repr(called_permission_dto),
            "create_folder_permission_for_user_builds_dto.txt",
        )
        assert called_permission_dto.permission_type == Permissions.FULL_EDIT
