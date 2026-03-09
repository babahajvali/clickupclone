from types import SimpleNamespace

import pytest

from task_management.exceptions.enums import FieldType, Role
from task_management.interactors.dtos import (
    FieldDTO,
    TaskDTO,
    TaskFieldValueDTO,
    WorkspaceMemberDTO,
)
from task_management.tests.api_tests.fields import BaseSetFieldValue


def get_task_mock(mocker):
    return mocker.patch(
        "task_management.storages.task_storage.TaskStorage.get_task")


def get_field_mock(mocker):
    return mocker.patch(
        "task_management.storages.field_storage.FieldStorage.get_fields")


def get_workspace_id_from_field_id_mock(mocker):
    return mocker.patch(
        "task_management.storages.field_storage.FieldStorage.get_workspace_id_from_field_id"
    )


def get_workspace_member_mock(mocker):
    return mocker.patch(
        "task_management.storages.workspace_storage.WorkspaceStorage.get_workspace_member"
    )


def update_or_create_task_field_value_mock(mocker):
    return mocker.patch(
        "task_management.storages.field_storage.FieldStorage.update_or_create_task_field_value"
    )


def create_workspace_member_dto(role: Role) -> WorkspaceMemberDTO:
    return WorkspaceMemberDTO(
        id=1,
        workspace_id="workspace_1",
        role=role,
        user_id="user_1",
        is_active=True,
        added_by="admin_1",
    )


def create_task_dto(*, is_deleted=False) -> TaskDTO:
    return TaskDTO(
        task_id="task_1",
        title="Task",
        description="Description",
        list_id="list_1",
        order=1,
        created_by="user_1",
        is_deleted=is_deleted,
    )


def create_field_dto(
        *,
        field_type=FieldType.TEXT,
        config=None,
        is_deleted=False) -> FieldDTO:
    if config is None:
        config = {"max_length": 10}
    return FieldDTO(
        field_id="field_1",
        field_type=field_type,
        description="Task priority",
        template_id="tpl_1",
        field_name="Priority",
        is_deleted=is_deleted,
        order=2,
        config=config,
        is_required=True,
        created_by="user_1",
    )


def create_task_field_value_dto() -> TaskFieldValueDTO:
    return TaskFieldValueDTO(
        id=1,
        task_id="task_1",
        field_id="field_1",
        value="P1",
    )


@pytest.mark.django_db
class TestSetFieldValueAPI(BaseSetFieldValue):

    def _setup_common(self, mocker, *, role=Role.MEMBER):
        task_data = get_task_mock(mocker)
        task_data.return_value = create_task_dto(is_deleted=False)

        field_data = get_field_mock(mocker)
        field_data.return_value = create_field_dto(
            field_type=FieldType.TEXT,
            config={"max_length": 10},
            is_deleted=False,
        )

        workspace_id = get_workspace_id_from_field_id_mock(mocker)
        workspace_id.return_value = "workspace_1"

        workspace_member = get_workspace_member_mock(mocker)
        workspace_member.return_value = create_workspace_member_dto(role=role)

    def test_set_field_value_successfully(self, snapshot, mocker):
        self._setup_common(mocker)
        field_value = update_or_create_task_field_value_mock(mocker)
        field_value.return_value = create_task_field_value_dto()

        variables = {
            "params": {
                "taskId": "task_1",
                "fieldId": "field_1",
                "value": "P1",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_set_field_value_task_not_found(self, snapshot, mocker):
        task_data = get_task_mock(mocker)
        task_data.return_value = None

        variables = {
            "params": {
                "taskId": "task_404",
                "fieldId": "field_1",
                "value": "P1",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_set_field_value_deleted_task(self, snapshot, mocker):
        task_data = get_task_mock(mocker)
        task_data.return_value = create_task_dto(is_deleted=True)

        variables = {
            "params": {
                "taskId": "task_1",
                "fieldId": "field_1",
                "value": "P1",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_set_field_value_field_not_found(self, snapshot, mocker):
        task_data = get_task_mock(mocker)
        task_data.return_value = create_task_dto()
        field_data = get_field_mock(mocker)
        field_data.return_value = None

        variables = {
            "params": {
                "taskId": "task_1",
                "fieldId": "field_404",
                "value": "P1",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_set_field_value_deleted_field(self, snapshot, mocker):
        task_data = get_task_mock(mocker)
        task_data.return_value = create_task_dto()
        field_data = get_field_mock(mocker)
        field_data.return_value = create_field_dto(is_deleted=True)

        variables = {
            "params": {
                "taskId": "task_1",
                "fieldId": "field_1",
                "value": "P1",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_set_field_value_permission_denied(self, snapshot, mocker):
        self._setup_common(mocker, role=Role.GUEST)

        variables = {
            "params": {
                "taskId": "task_1",
                "fieldId": "field_1",
                "value": "P1",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_set_field_value_user_not_workspace_member(self, snapshot, mocker):
        self._setup_common(mocker)
        workspace_member = get_workspace_member_mock(mocker)
        workspace_member.return_value = None

        variables = {
            "params": {
                "taskId": "task_1",
                "fieldId": "field_1",
                "value": "P1",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_set_field_value_text_exceeds_max_length(self, snapshot, mocker):
        self._setup_common(mocker)
        field_data = get_field_mock(mocker)
        field_data.return_value = create_field_dto(
            field_type=FieldType.TEXT,
            config={"max_length": 3},
        )

        variables = {
            "params": {
                "taskId": "task_1",
                "fieldId": "field_1",
                "value": "LONG",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_set_field_value_invalid_number(self, snapshot, mocker):
        self._setup_common(mocker)
        field_data = get_field_mock(mocker)
        field_data.return_value = create_field_dto(
            field_type=FieldType.NUMBER,
            config={"min": 1, "max": 10},
        )

        variables = {
            "params": {
                "taskId": "task_1",
                "fieldId": "field_1",
                "value": "abc",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_set_field_value_number_below_min(self, snapshot, mocker):
        self._setup_common(mocker)
        field_data = get_field_mock(mocker)
        field_data.return_value = create_field_dto(
            field_type=FieldType.NUMBER,
            config={"min": 5},
        )

        variables = {
            "params": {
                "taskId": "task_1",
                "fieldId": "field_1",
                "value": "2",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_set_field_value_number_exceeds_max(self, snapshot, mocker):
        self._setup_common(mocker)
        field_data = get_field_mock(mocker)
        field_data.return_value = create_field_dto(
            field_type=FieldType.NUMBER,
            config={"max": 5},
        )

        variables = {
            "params": {
                "taskId": "task_1",
                "fieldId": "field_1",
                "value": "10",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_set_field_value_dropdown_option_not_allowed(
            self, snapshot, mocker):
        self._setup_common(mocker)
        field_data = get_field_mock(mocker)
        field_data.return_value = create_field_dto(
            field_type=FieldType.DROPDOWN,
            config={"options": ["Low", "Medium"]},
        )

        variables = {
            "params": {
                "taskId": "task_1",
                "fieldId": "field_1",
                "value": "High",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
