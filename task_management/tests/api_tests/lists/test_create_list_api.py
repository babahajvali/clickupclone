from contextlib import nullcontext
from types import SimpleNamespace

import pytest

from task_management.exceptions.enums import ListEntityType, Role
from task_management.interactors.dtos import ListDTO, SpaceDTO, FolderDTO, \
    WorkspaceMemberDTO
from task_management.tests.api_tests.lists import BaseCreateList


def get_space_mock(mocker):
    return mocker.patch(
        "task_management.storages.space_storage.SpaceStorage.get_space"
    )


def get_space_workspace_id_mock(mocker):
    return mocker.patch(
        "task_management.storages.space_storage.SpaceStorage.get_space_workspace_id"
    )


def get_folder_mock(mocker):
    return mocker.patch(
        "task_management.storages.folder_storage.FolderStorage.get_folder"
    )


def get_folder_space_id_mock(mocker):
    return mocker.patch(
        "task_management.storages.folder_storage.FolderStorage.get_folder_space_id"
    )


def get_workspace_member_mock(mocker):
    return mocker.patch(
        "task_management.storages.workspace_storage.WorkspaceStorage.get_workspace_member"
    )


def get_last_order_mock(mocker):
    return mocker.patch(
        "task_management.storages.list_storage.ListStorage.get_last_list_order"
    )


def create_list_mock(mocker):
    return mocker.patch(
        "task_management.storages.list_storage.ListStorage.create_list"
    )


def create_list_lock_mock(mocker):
    return mocker.patch(
        "task_management.interactors.lists.create_list_interactor.redis_lock",
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


def make_folder(is_deleted=False) -> FolderDTO:
    return FolderDTO(
        folder_id="folder_1",
        name="Product",
        description="Product folder",
        space_id="space_1",
        order=1,
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


def make_list(order=1) -> ListDTO:
    return ListDTO(
        list_id="list_1",
        name="Sprint Board",
        description="List description",
        is_deleted=False,
        order=order,
        is_private=False,
        created_by="user_1",
        entity_type=ListEntityType.SPACE,
        entity_id="space_1",
    )


@pytest.mark.django_db
class TestCreateListAPI(BaseCreateList):
    def _setup_space_common(self, mocker, role=Role.MEMBER):
        get_space = get_space_mock(mocker)
        get_space.return_value = make_space()

        get_workspace_id = get_space_workspace_id_mock(mocker)
        get_workspace_id.return_value = "workspace_1"

        get_workspace_member = get_workspace_member_mock(mocker)
        get_workspace_member.return_value = make_workspace_member(role=role)

        create_list_lock_mock(mocker)

    def _setup_folder_common(self, mocker, role=Role.MEMBER):
        get_folder = get_folder_mock(mocker)
        get_folder.return_value = make_folder()

        get_folder_space_id = get_folder_space_id_mock(mocker)
        get_folder_space_id.return_value = "space_1"

        get_space_workspace_id = get_space_workspace_id_mock(mocker)
        get_space_workspace_id.return_value = "workspace_1"

        get_workspace_member = get_workspace_member_mock(mocker)
        get_workspace_member.return_value = make_workspace_member(role=role)

        create_list_lock_mock(mocker)

    def test_create_list_successfully(self, snapshot, mocker):
        self._setup_space_common(mocker)

        last_order = get_last_order_mock(mocker)
        last_order.return_value = 1

        create_list = create_list_mock(mocker)
        create_list.return_value = make_list(order=2)

        variables = {
            "params": {
                "name": "Sprint Board",
                "description": "List description",
                "entityType": "SPACE",
                "entityId": "space_1",
                "isPrivate": False,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_create_list_space_not_found(self, snapshot, mocker):
        get_space = get_space_mock(mocker)
        get_space.return_value = None
        create_list_lock_mock(mocker)

        variables = {
            "params": {
                "name": "Sprint Board",
                "description": "List description",
                "entityType": "SPACE",
                "entityId": "space_404",
                "isPrivate": False,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_create_list_folder_not_found(self, snapshot, mocker):
        get_folder = get_folder_mock(mocker)
        get_folder.return_value = None
        create_list_lock_mock(mocker)

        variables = {
            "params": {
                "name": "Sprint Board",
                "description": "List description",
                "entityType": "FOLDER",
                "entityId": "folder_404",
                "isPrivate": False,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_create_list_empty_name(self, snapshot, mocker):
        create_list_lock_mock(mocker)

        variables = {
            "params": {
                "name": "   ",
                "description": "List description",
                "entityType": "SPACE",
                "entityId": "space_1",
                "isPrivate": False,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
