from contextlib import nullcontext
from types import SimpleNamespace

import pytest

from task_management.exceptions.enums import Role
from task_management.interactors.dtos import FolderDTO, SpaceDTO, \
    WorkspaceMemberDTO
from task_management.tests.api_tests.folders import BaseReorderFolder


def get_space_folder_count_mock(mocker):
    return mocker.patch(
        "task_management.storages.folder_storage.FolderStorage.get_space_folder_count"
    )


def get_folder_mock(mocker):
    return mocker.patch(
        "task_management.storages.folder_storage.FolderStorage.get_folder"
    )


def get_space_mock(mocker):
    return mocker.patch(
        "task_management.storages.space_storage.SpaceStorage.get_space"
    )


def get_space_workspace_id_mock(mocker):
    return mocker.patch(
        "task_management.storages.space_storage.SpaceStorage.get_space_workspace_id"
    )


def get_workspace_member_mock(mocker):
    return mocker.patch(
        "task_management.storages.workspace_storage.WorkspaceStorage.get_workspace_member"
    )


def shift_folders_down_mock(mocker):
    return mocker.patch(
        "task_management.storages.folder_storage.FolderStorage.shift_folders_down"
    )


def shift_folders_up_mock(mocker):
    return mocker.patch(
        "task_management.storages.folder_storage.FolderStorage.shift_folders_up"
    )


def update_folder_order_mock(mocker):
    return mocker.patch(
        "task_management.storages.folder_storage.FolderStorage.update_folder_order"
    )


def reorder_folder_lock_mock(mocker):
    return mocker.patch(
        "task_management.interactors.folders.reorder_folder_interactor.redis_lock",
        return_value=nullcontext(),
    )


def make_space(is_deleted=False) -> SpaceDTO:
    return SpaceDTO(
        space_id="space_1",
        name="Engineering",
        description="Engineering space",
        workspace_id="workspace_1",
        order=1,
        is_deleted=is_deleted,
        is_private=False,
        created_by="user_1",
    )


def make_folder(order=1, is_deleted=False) -> FolderDTO:
    return FolderDTO(
        folder_id="folder_1",
        name="Product",
        description="Product folder",
        space_id="space_1",
        order=order,
        is_deleted=is_deleted,
        is_private=False,
        created_by="user_1",
    )


def make_workspace_member(role=Role.MEMBER) -> WorkspaceMemberDTO:
    return WorkspaceMemberDTO(
        id=1,
        workspace_id="workspace_1",
        user_id="user_1",
        role=role,
        is_active=True,
        added_by="owner_1",
    )


@pytest.mark.django_db
class TestReorderFolderAPI(BaseReorderFolder):
    def _setup_common(self, mocker, role=Role.MEMBER):
        folder_count = get_space_folder_count_mock(mocker)
        folder_count.return_value = 3

        get_folder = get_folder_mock(mocker)
        get_folder.return_value = make_folder(order=1)

        get_space = get_space_mock(mocker)
        get_space.return_value = make_space()

        get_workspace_id = get_space_workspace_id_mock(mocker)
        get_workspace_id.return_value = "workspace_1"

        get_workspace_member = get_workspace_member_mock(mocker)
        get_workspace_member.return_value = make_workspace_member(role=role)
        reorder_folder_lock_mock(mocker)

    def test_reorder_folder_successfully(self, snapshot, mocker):
        self._setup_common(mocker)
        shift_folders_down_mock(mocker)
        shift_folders_up_mock(mocker)

        update_order = update_folder_order_mock(mocker)
        update_order.return_value = make_folder(order=2)

        variables = {
            "params": {
                "spaceId": "space_1",
                "folderId": "folder_1",
                "order": 2,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_reorder_folder_invalid_order(self, snapshot, mocker):
        self._setup_common(mocker)

        variables = {
            "params": {
                "spaceId": "space_1",
                "folderId": "folder_1",
                "order": 0,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_reorder_folder_not_found(self, snapshot, mocker):
        self._setup_common(mocker)
        get_folder = get_folder_mock(mocker)
        get_folder.return_value = None

        variables = {
            "params": {
                "spaceId": "space_1",
                "folderId": "folder_404",
                "order": 2,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
