from contextlib import nullcontext
from types import SimpleNamespace

import pytest

from task_management.exceptions.enums import ListEntityType, Role
from task_management.interactors.dtos import ListDTO, SpaceDTO, \
    WorkspaceMemberDTO
from task_management.tests.api_tests.lists import BaseReorderListInSpace


def get_space_lists_count_mock(mocker):
    return mocker.patch(
        "task_management.storages.list_storage.ListStorage.get_space_lists_count"
    )


def get_list_mock(mocker):
    return mocker.patch(
        "task_management.storages.list_storage.ListStorage.get_list"
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


def shift_lists_down_mock(mocker):
    return mocker.patch(
        "task_management.storages.list_storage.ListStorage.shift_lists_down_in_space"
    )


def shift_lists_up_mock(mocker):
    return mocker.patch(
        "task_management.storages.list_storage.ListStorage.shift_lists_up_in_space"
    )


def update_list_order_mock(mocker):
    return mocker.patch(
        "task_management.storages.list_storage.ListStorage.update_list_order_in_space"
    )


def reorder_list_lock_mock(mocker):
    return mocker.patch(
        "task_management.interactors.lists.reorder_list_in_space_interactor.redis_lock",
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


def make_list(order=1, is_deleted=False) -> ListDTO:
    return ListDTO(
        list_id="list_1",
        name="Sprint Board",
        description="List description",
        is_deleted=is_deleted,
        order=order,
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
class TestReorderListInSpaceAPI(BaseReorderListInSpace):
    def _setup_common(self, mocker, role=Role.MEMBER):
        count = get_space_lists_count_mock(mocker)
        count.return_value = 3

        get_list = get_list_mock(mocker)
        get_list.return_value = make_list(order=1)

        get_space = get_space_mock(mocker)
        get_space.return_value = make_space()

        get_workspace_id = get_space_workspace_id_mock(mocker)
        get_workspace_id.return_value = "workspace_1"

        get_workspace_member = get_workspace_member_mock(mocker)
        get_workspace_member.return_value = make_workspace_member(role=role)

        reorder_list_lock_mock(mocker)

    def test_reorder_list_in_space_successfully(self, snapshot, mocker):
        self._setup_common(mocker)
        shift_lists_down_mock(mocker)
        shift_lists_up_mock(mocker)

        update_order = update_list_order_mock(mocker)
        update_order.return_value = make_list(order=2)

        variables = {
            "params": {
                "spaceId": "space_1",
                "listId": "list_1",
                "order": 2,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_reorder_list_in_space_invalid_order(self, snapshot, mocker):
        self._setup_common(mocker)

        variables = {
            "params": {
                "spaceId": "space_1",
                "listId": "list_1",
                "order": 0,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_reorder_list_in_space_not_found(self, snapshot, mocker):
        self._setup_common(mocker)
        get_list = get_list_mock(mocker)
        get_list.return_value = None

        variables = {
            "params": {
                "spaceId": "space_1",
                "listId": "list_404",
                "order": 2,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
