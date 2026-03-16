from types import SimpleNamespace

import pytest

from task_management.exceptions.enums import Role, ViewType
from task_management.interactors.dtos import ListViewDTO, WorkspaceMemberDTO
from task_management.tests.api_tests.views import BaseApplyListView

LIST_ID = "12345678-1234-5678-1234-567812345678"
VIEW_TYPE = "TABLE"
VIEW_NAME = "Table"
MISSING_LIST_ID = "12345678-1234-5678-1234-567812345680"
INVALID_VIEW_TYPE = "INVALID"


def get_list_view_mock(mocker):
    return mocker.patch(
        "task_management.storages.view_storage.ViewStorage.get_list_view"
    )


def check_view_exists_mock(mocker):
    return mocker.patch(
        "task_management.interactors.views.create_list_view_interactor.CreateListViewInteractor.check_view_exist"
    )


def get_list_mock(mocker):
    return mocker.patch(
        "task_management.storages.list_storage.ListStorage.get_list"
    )


def get_workspace_id_by_list_id_mock(mocker):
    return mocker.patch(
        "task_management.storages.list_storage.ListStorage."
        "get_workspace_id_by_list_id"
    )


def get_workspace_member_mock(mocker):
    return mocker.patch(
        "task_management.storages.workspace_storage.WorkspaceStorage.get_workspace_member"
    )


def apply_view_mock(mocker):
    return mocker.patch(
        "task_management.storages.view_storage.ViewStorage.create_list_view"
    )


def make_list_view_dto() -> ListViewDTO:
    return ListViewDTO(
        id=1,
        view_name="Table",
        list_id=LIST_ID,
        view_type=ViewType.TABLE,
        created_by="user_1",
        is_active=True,
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


@pytest.mark.django_db
class TestApplyListViewAPI(BaseApplyListView):
    def test_apply_list_view_successfully(self, snapshot, mocker):
        get_list_view_mock(mocker).return_value = None
        check_view_exists_mock(mocker).return_value = True
        get_list_mock(mocker).return_value = type(
            "List", (), {"is_deleted": False}
        )()
        get_workspace_id_by_list_id_mock(mocker).return_value = "workspace_1"
        get_workspace_member_mock(
            mocker).return_value = make_workspace_member_dto()
        apply_view_mock(mocker).return_value = make_list_view_dto()

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"listId": LIST_ID, "viewType": VIEW_TYPE, "viewName": VIEW_NAME}},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_apply_list_view_list_not_found(self, snapshot, mocker):
        get_list_view_mock(mocker).return_value = None
        check_view_exists_mock(mocker).return_value = True
        get_list_mock(mocker).return_value = None

        self.execute_schema(
            query=self.QUERY,
            variables={
                "params": {"listId": MISSING_LIST_ID, "viewType": VIEW_TYPE, "viewName": VIEW_NAME}},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_apply_list_view_view_not_found(self, snapshot, mocker):
        get_list_view_mock(mocker).return_value = None
        check_view_exists_mock(mocker).return_value = False
        get_list_mock(mocker).return_value = type(
            "List", (), {"is_deleted": False}
        )()

        self.execute_schema(
            query=self.QUERY,
            variables={
                "params": {"listId": LIST_ID, "viewType": INVALID_VIEW_TYPE, "viewName": VIEW_NAME}},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_apply_list_view_deleted_list(self, snapshot, mocker):
        get_list_view_mock(mocker).return_value = None
        check_view_exists_mock(mocker).return_value = True
        get_list_mock(mocker).return_value = type(
            "List", (), {"is_deleted": True}
        )()

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"listId": LIST_ID, "viewType": VIEW_TYPE, "viewName": VIEW_NAME}},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_apply_list_view_no_edit_access(self, snapshot, mocker):
        get_list_view_mock(mocker).return_value = None
        check_view_exists_mock(mocker).return_value = True
        get_list_mock(mocker).return_value = type(
            "List", (), {"is_deleted": False}
        )()
        get_workspace_id_by_list_id_mock(mocker).return_value = "workspace_1"
        get_workspace_member_mock(
            mocker).return_value = make_workspace_member_dto(
            role=Role.GUEST
        )

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"listId": LIST_ID, "viewType": VIEW_TYPE, "viewName": VIEW_NAME}},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_apply_list_view_user_not_workspace_member(self, snapshot, mocker):
        get_list_view_mock(mocker).return_value = None
        check_view_exists_mock(mocker).return_value = True
        get_list_mock(mocker).return_value = type(
            "List", (), {"is_deleted": False}
        )()
        get_workspace_id_by_list_id_mock(mocker).return_value = "workspace_1"
        get_workspace_member_mock(mocker).return_value = None

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"listId": LIST_ID, "viewType": VIEW_TYPE, "viewName": VIEW_NAME}},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
