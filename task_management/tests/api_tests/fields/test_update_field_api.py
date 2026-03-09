import json
from types import SimpleNamespace

import pytest

from task_management.exceptions.enums import FieldType, Role
from task_management.interactors.dtos import FieldDTO, WorkspaceMemberDTO
from task_management.tests.api_tests.fields import BaseUpdateField


def get_field_mock(mocker):
    return mocker.patch(
        "task_management.storages.field_storage.FieldStorage.get_fields"
    )


def is_field_name_exists_mock(mocker):
    return mocker.patch(
        "task_management.storages.field_storage.FieldStorage.is_field_name_exists"
    )


def get_workspace_id_from_field_id_mock(mocker):
    return mocker.patch(
        "task_management.storages.field_storage.FieldStorage.get_workspace_id_from_field_id"
    )


def get_workspace_member_mock(mocker):
    return mocker.patch(
        "task_management.storages.workspace_storage.WorkspaceStorage.get_workspace_member"
    )


def update_field_mock(mocker):
    return mocker.patch(
        "task_management.storages.field_storage.FieldStorage.update_field"
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


def create_field_dto(
        *,
        field_type=FieldType.TEXT,
        is_deleted=False,
        config=None) -> FieldDTO:
    if config is None:
        config = {"max_length": 10, "default": "P1"}
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
        created_by="49bb508e-c6d1-4882-95fd-1991d103f7dd",
    )


@pytest.mark.django_db
class TestUpdateFieldAPI(BaseUpdateField):

    def _setup_common_success_path(self, mocker, *, role=Role.MEMBER):
        field_data = get_field_mock(mocker)
        field_data.return_value = create_field_dto()

        name_exists = is_field_name_exists_mock(mocker)
        name_exists.return_value = False

        workspace_id = get_workspace_id_from_field_id_mock(mocker)
        workspace_id.return_value = "workspace_1"

        workspace_member = get_workspace_member_mock(mocker)
        workspace_member.return_value = create_workspace_member_dto(role=role)

    def test_update_field_successfully(self, snapshot, mocker):
        self._setup_common_success_path(mocker)
        updated = update_field_mock(mocker)
        updated.return_value = create_field_dto()

        variables = {
            "params": {
                "fieldId": "field_1",
                "fieldName": "Priority",
                "description": "Task priority",
                "config": json.dumps({"max_length": 10, "default": "P1"}),
                "isRequired": True,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_update_field_not_found(self, snapshot, mocker):
        field_data = get_field_mock(mocker)
        field_data.return_value = None

        variables = {
            "params": {
                "fieldId": "field_1",
                "fieldName": "Priority",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_update_field_deleted(self, snapshot, mocker):
        field_data = get_field_mock(mocker)
        field_data.return_value = create_field_dto(is_deleted=True)

        variables = {
            "params": {
                "fieldId": "field_1",
                "fieldName": "Priority",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_update_field_duplicate_name(self, snapshot, mocker):
        self._setup_common_success_path(mocker)
        name_exists = is_field_name_exists_mock(mocker)
        name_exists.return_value = True

        variables = {
            "params": {
                "fieldId": "field_1",
                "fieldName": "Priority",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_update_field_empty_name(self, snapshot, mocker):
        self._setup_common_success_path(mocker)

        variables = {
            "params": {
                "fieldId": "field_1",
                "fieldName": "",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_update_field_without_updates(self, snapshot, mocker):
        self._setup_common_success_path(mocker)

        variables = {
            "params": {
                "fieldId": "field_1",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_update_field_permission_denied(self, snapshot, mocker):
        self._setup_common_success_path(mocker, role=Role.GUEST)

        variables = {
            "params": {
                "fieldId": "field_1",
                "fieldName": "Priority",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_update_field_user_not_workspace_member(self, snapshot, mocker):
        self._setup_common_success_path(mocker)
        workspace_member = get_workspace_member_mock(mocker)
        workspace_member.return_value = None

        variables = {
            "params": {
                "fieldId": "field_1",
                "fieldName": "Priority",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_update_field_invalid_config_keys(self, snapshot, mocker):
        self._setup_common_success_path(mocker)

        variables = {
            "params": {
                "fieldId": "field_1",
                "config": json.dumps({"bad_key": 1}),
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_update_field_text_default_exceeds_max_length(
            self, snapshot, mocker):
        field_data = get_field_mock(mocker)
        field_data.return_value = create_field_dto(field_type=FieldType.TEXT)

        variables = {
            "params": {
                "fieldId": "field_1",
                "config": json.dumps({"max_length": 3, "default": "HIGH"}),
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_update_field_number_default_below_minimum(self, snapshot, mocker):
        field_data = get_field_mock(mocker)
        field_data.return_value = create_field_dto(field_type=FieldType.NUMBER)

        variables = {
            "params": {
                "fieldId": "field_1",
                "config": json.dumps({"min": 10, "default": 5}),
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_update_field_number_default_above_maximum(self, snapshot, mocker):
        field_data = get_field_mock(mocker)
        field_data.return_value = create_field_dto(field_type=FieldType.NUMBER)

        variables = {
            "params": {
                "fieldId": "field_1",
                "config": json.dumps({"max": 5, "default": 10}),
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_update_field_with_max_less_than_min(self, snapshot, mocker):
        field_data = get_field_mock(mocker)
        field_data.return_value = create_field_dto(field_type=FieldType.NUMBER)

        variables = {
            "params": {
                "fieldId": "field_1",
                "config": json.dumps({"min": 10, "max": 2}),
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_update_field_dropdown_missing_config(self, snapshot, mocker):
        field_data = get_field_mock(mocker)
        field_data.return_value = create_field_dto(
            field_type=FieldType.DROPDOWN)

        variables = {
            "params": {
                "fieldId": "field_1",
                "config": json.dumps({}),
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_update_field_dropdown_options_missing(self, snapshot, mocker):
        field_data = get_field_mock(mocker)
        field_data.return_value = create_field_dto(
            field_type=FieldType.DROPDOWN)

        variables = {
            "params": {
                "fieldId": "field_1",
                "config": json.dumps({"default": "High"}),
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_update_field_dropdown_default_not_in_options(
            self, snapshot, mocker):
        field_data = get_field_mock(mocker)
        field_data.return_value = create_field_dto(
            field_type=FieldType.DROPDOWN)

        variables = {
            "params": {
                "fieldId": "field_1",
                "config": json.dumps({
                    "options": ["Low", "Medium"],
                    "default": "High",
                }),
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
