from types import SimpleNamespace

import pytest

from task_management.exceptions.enums import ListEntityType, Role
from task_management.interactors.dtos import ListDTO, WorkspaceMemberDTO
from task_management.tests.api_tests.lists import BaseSetListVisibility


def get_list_mock(mocker):
    return mocker.patch(
        "task_management.storages.list_storage.ListStorage.get_list"
    )


def get_workspace_id_mock(mocker):
    return mocker.patch(
        "task_management.storages.list_storage.ListStorage.get_workspace_id_by_list_id"
    )


def get_workspace_member_mock(mocker):
    return mocker.patch(
        "task_management.storages.workspace_storage.WorkspaceStorage.get_workspace_member"
    )


def update_visibility_mock(mocker):
    return mocker.patch(
        "task_management.storages.list_storage.ListStorage.update_list_visibility"
    )


def make_list(is_deleted=False) -> ListDTO:
    return ListDTO(
        list_id="list_1",
        name="Sprint Board",
        description="List description",
        is_deleted=is_deleted,
        order=1,
        is_private=False,
        created_by="user_1",
        entity_type=ListEntityType.SPACE,
        entity_id="space_1",
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
class TestSetListVisibilityAPI(BaseSetListVisibility):
    def _setup_common(self, mocker, role=Role.MEMBER):
        get_list = get_list_mock(mocker)
        get_list.return_value = make_list()

        get_workspace_id = get_workspace_id_mock(mocker)
        get_workspace_id.return_value = "workspace_1"

        get_workspace_member = get_workspace_member_mock(mocker)
        get_workspace_member.return_value = make_workspace_member(role=role)

    def test_set_list_visibility_successfully(self, snapshot, mocker):
        self._setup_common(mocker)

        update_visibility = update_visibility_mock(mocker)
        update_visibility.return_value = make_list()

        variables = {
            "params": {"listId": "list_1", "visibility": "PRIVATE"}
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_set_list_visibility_not_found(self, snapshot, mocker):
        get_list = get_list_mock(mocker)
        get_list.return_value = None

        variables = {
            "params": {"listId": "list_404", "visibility": "PRIVATE"}
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_set_list_visibility_permission_denied(self, snapshot, mocker):
        self._setup_common(mocker, role=Role.GUEST)

        variables = {
            "params": {"listId": "list_1", "visibility": "PRIVATE"}
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
