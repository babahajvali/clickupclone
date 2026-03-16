from types import SimpleNamespace

import pytest

from task_management.exceptions.enums import Role, ViewType
from task_management.interactors.dtos import ListViewDTO, WorkspaceMemberDTO
from task_management.tests.api_tests.views import BaseRemoveListView

LIST_ID = "12345678-1234-5678-1234-567812345678"
LIST_VIEW_ID = 1
MISSING_LIST_VIEW_ID = 999


def is_list_view_exist_mock(mocker):
    return mocker.patch(
        "task_management.storages.view_storage.ViewStorage.is_list_view_exist"
    )


def get_workspace_member_mock(mocker):
    return mocker.patch(
        "task_management.storages.workspace_storage.WorkspaceStorage.get_workspace_member"
    )


def get_workspace_id_by_list_id_mock(mocker):
    return mocker.patch(
        "task_management.storages.list_storage.ListStorage."
        "get_workspace_id_by_list_id"
    )


def remove_list_view_mock(mocker):
    return mocker.patch(
        "task_management.storages.view_storage.ViewStorage.remove_list_view"
    )


def make_workspace_member_dto(role=Role.ADMIN) -> WorkspaceMemberDTO:
    return WorkspaceMemberDTO(
        id=1,
        workspace_id="workspace_1",
        user_id="user_1",
        role=role,
        is_active=True,
        added_by="owner_1",
    )


def make_removed_list_view_dto() -> ListViewDTO:
    return ListViewDTO(
        id=1,
        view_name="Table",
        list_id=LIST_ID,
        view_type=ViewType.TABLE,
        created_by="user_1",
        is_active=False,
    )


@pytest.mark.django_db
class TestRemoveListViewAPI(BaseRemoveListView):
    def test_remove_list_view_successfully(self, snapshot, mocker):
        is_list_view_exist_mock(mocker).return_value = True
        get_workspace_id_by_list_id_mock(mocker).return_value = "workspace_1"
        get_workspace_member_mock(
            mocker).return_value = make_workspace_member_dto()
        remove_list_view_mock(
            mocker).return_value = make_removed_list_view_dto()

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"listViewId": LIST_VIEW_ID}},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_remove_list_view_not_found(self, snapshot, mocker):
        is_list_view_exist_mock(mocker).return_value = False

        self.execute_schema(
            query=self.QUERY,
            variables={
                "params": {"listViewId": MISSING_LIST_VIEW_ID}},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_remove_list_view_no_edit_access(self, snapshot, mocker):
        is_list_view_exist_mock(mocker).return_value = True
        get_workspace_id_by_list_id_mock(mocker).return_value = "workspace_1"
        get_workspace_member_mock(
            mocker).return_value = make_workspace_member_dto(
            role=Role.GUEST
        )

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"listViewId": LIST_VIEW_ID}},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_remove_list_view_user_not_workspace_member(self, snapshot,
                                                        mocker):
        is_list_view_exist_mock(mocker).return_value = True
        get_workspace_id_by_list_id_mock(mocker).return_value = "workspace_1"
        get_workspace_member_mock(mocker).return_value = None

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"listViewId": LIST_VIEW_ID}},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
