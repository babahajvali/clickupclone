from types import SimpleNamespace

import pytest

from task_management.exceptions.enums import FieldType, Role
from task_management.interactors.dtos import FieldDTO, WorkspaceMemberDTO
from task_management.tests.api_tests.fields import BaseDeleteField


def get_field_mock(mocker):
    return mocker.patch(
        "task_management.storages.field_storage.FieldStorage.get_field")


def get_workspace_id_from_field_id_mock(mocker):
    return mocker.patch(
        "task_management.storages.field_storage.FieldStorage.get_workspace_id_from_field_id"
    )


def get_workspace_member_mock(mocker):
    return mocker.patch(
        "task_management.storages.workspace_storage.WorkspaceStorage.get_workspace_member"
    )


def delete_field_mock(mocker):
    return mocker.patch(
        "task_management.storages.field_storage.FieldStorage.delete_field")


def create_workspace_member_dto(role: Role) -> WorkspaceMemberDTO:
    return WorkspaceMemberDTO(
        id=1,
        workspace_id="workspace_1",
        role=role,
        user_id="user_1",
        is_active=True,
        added_by="admin_1",
    )


def create_field_dto(*, is_deleted=True) -> FieldDTO:
    return FieldDTO(
        field_id="field_1",
        field_type=FieldType.TEXT,
        description="Task priority",
        template_id="tpl_1",
        field_name="Priority",
        is_deleted=is_deleted,
        order=2,
        config={"max_length": 10},
        is_required=True,
        created_by="user_1",
    )


@pytest.mark.django_db
class TestDeleteFieldAPI(BaseDeleteField):

    def _setup_common(self, mocker, *, role=Role.MEMBER, field_exists=True):
        field_data = get_field_mock(mocker)
        field_data.return_value = create_field_dto(
            is_deleted=False) if field_exists else None

        workspace_id = get_workspace_id_from_field_id_mock(mocker)
        workspace_id.return_value = "workspace_1"

        workspace_member = get_workspace_member_mock(mocker)
        workspace_member.return_value = create_workspace_member_dto(role=role)

    def test_delete_field_successfully(self, snapshot, mocker):
        self._setup_common(mocker)
        deleted = delete_field_mock(mocker)
        deleted.return_value = create_field_dto(is_deleted=True)

        variables = {"params": {"fieldId": "field_1"}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_delete_field_not_found(self, snapshot, mocker):
        self._setup_common(mocker, field_exists=False)

        variables = {"params": {"fieldId": "field_404"}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_delete_field_permission_denied(self, snapshot, mocker):
        self._setup_common(mocker, role=Role.GUEST)

        variables = {"params": {"fieldId": "field_1"}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_delete_field_user_not_workspace_member(self, snapshot, mocker):
        self._setup_common(mocker)
        workspace_member = get_workspace_member_mock(mocker)
        workspace_member.return_value = None

        variables = {"params": {"fieldId": "field_1"}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
