from types import SimpleNamespace

import pytest

from task_management.exceptions.enums import Role
from task_management.interactors.dtos import FolderDTO, WorkspaceMemberDTO
from task_management.tests.api_tests.folders import BaseDeleteFolder


def get_folder_mock(mocker):
    return mocker.patch(
        "task_management.storages.folder_storage.FolderStorage.get_folder"
    )


def get_workspace_id_mock(mocker):
    return mocker.patch(
        "task_management.storages.folder_storage.FolderStorage.get_workspace_id_from_folder_id"
    )


def get_workspace_member_mock(mocker):
    return mocker.patch(
        "task_management.storages.workspace_storage.WorkspaceStorage.get_workspace_member"
    )


def delete_folder_mock(mocker):
    return mocker.patch(
        "task_management.storages.folder_storage.FolderStorage.delete_folder"
    )


def make_folder() -> FolderDTO:
    return FolderDTO(
        folder_id="folder_1",
        name="Product",
        description="Product folder",
        space_id="space_1",
        order=1,
        is_deleted=True,
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
class TestDeleteFolderAPI(BaseDeleteFolder):
    def _setup_common(self, mocker, role=Role.MEMBER):
        get_folder = get_folder_mock(mocker)
        get_folder.return_value = make_folder()

        get_workspace_id = get_workspace_id_mock(mocker)
        get_workspace_id.return_value = "workspace_1"

        get_workspace_member = get_workspace_member_mock(mocker)
        get_workspace_member.return_value = make_workspace_member(role=role)

    def test_delete_folder_successfully(self, snapshot, mocker):
        self._setup_common(mocker)

        delete_folder = delete_folder_mock(mocker)
        delete_folder.return_value = make_folder()

        variables = {"params": {"folderId": "folder_1"}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_delete_folder_not_found(self, snapshot, mocker):
        get_folder = get_folder_mock(mocker)
        get_folder.return_value = None

        variables = {"params": {"folderId": "folder_404"}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_delete_folder_permission_denied(self, snapshot, mocker):
        self._setup_common(mocker, role=Role.GUEST)

        variables = {"params": {"folderId": "folder_1"}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
