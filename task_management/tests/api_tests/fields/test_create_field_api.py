import json
from types import SimpleNamespace

import pytest

from task_management.exceptions.enums import FieldType, Role
from task_management.interactors.dtos import FieldDTO, WorkspaceMemberDTO
from task_management.tests.api_tests.fields import BaseCreateField


def validate_template_exists_mock(mocker):
    return mocker.patch(
        "task_management.storages.template_storage.TemplateStorage.validate_template_exists"
    )


def get_workspace_id_from_template_id_mock(mocker):
    return mocker.patch(
        "task_management.storages.template_storage.TemplateStorage.get_workspace_id_from_template_id"
    )


def get_workspace_member_mock(mocker):
    return mocker.patch(
        "task_management.storages.workspace_storage.WorkspaceStorage.get_workspace_member"
    )


def is_field_name_exists_mock(mocker):
    return mocker.patch(
        "task_management.storages.field_storage.FieldStorage.is_field_name_exists"
    )


def get_last_field_order_in_template_mock(mocker):
    return mocker.patch(
        "task_management.storages.field_storage.FieldStorage.get_last_field_order_in_template"
    )


def create_field_mock(mocker):
    return mocker.patch(
        "task_management.storages.field_storage.FieldStorage.create_field"
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


def create_field_dto() -> FieldDTO:
    return FieldDTO(
        field_id="field_1",
        field_type=FieldType.TEXT,
        description="Task priority",
        template_id="tpl_1",
        field_name="Priority",
        is_deleted=False,
        order=2,
        config={"max_length": 10, "default": "P1"},
        is_required=True,
        created_by="49bb508e-c6d1-4882-95fd-1991d103f7dd",
    )


@pytest.mark.django_db
class TestCreateFieldAPI(BaseCreateField):

    def _setup_common_success_path(self, mocker, *, role=Role.MEMBER):
        template_exists = validate_template_exists_mock(mocker)
        template_exists.return_value = True

        template_workspace = get_workspace_id_from_template_id_mock(mocker)
        template_workspace.return_value = "workspace_1"

        workspace_member = get_workspace_member_mock(mocker)
        workspace_member.return_value = create_workspace_member_dto(role=role)

        field_name_exists = is_field_name_exists_mock(mocker)
        field_name_exists.return_value = False

        last_order = get_last_field_order_in_template_mock(mocker)
        last_order.return_value = 1

    def test_create_field_successfully(self, snapshot, mocker):
        self._setup_common_success_path(mocker)
        create_mock = create_field_mock(mocker)
        create_mock.return_value = create_field_dto()

        variables = {
            "params": {
                "fieldType": "TEXT",
                "fieldName": "comment",
                "description": "Task priority",
                "templateId": "tpl_1",
                "config": json.dumps({"max_length": 10, "default": "Test"}),
                "isRequired": True,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(
                user_id="49bb508e-c6d1-4882-95fd-1991d103f7dd"),
        )

    def test_create_field_template_not_found(self, snapshot, mocker):
        template_exists = validate_template_exists_mock(mocker)
        template_exists.return_value = False

        is_name_exists = is_field_name_exists_mock(mocker)
        is_name_exists.return_value = False

        variables = {
            "params": {
                "fieldType": "TEXT",
                "fieldName": "Priority",
                "description": "Task priority",
                "templateId": "invalid_tpl",
                "config": json.dumps({"max_length": 10}),
                "isRequired": True,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_create_field_with_duplicate_name(self, snapshot, mocker):
        self._setup_common_success_path(mocker)
        is_name_exists = is_field_name_exists_mock(mocker)
        is_name_exists.return_value = True

        variables = {
            "params": {
                "fieldType": "TEXT",
                "fieldName": "Priority",
                "description": "Task priority",
                "templateId": "tpl_1",
                "config": json.dumps({"max_length": 10}),
                "isRequired": True,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_create_field_permission_denied(self, snapshot, mocker):
        self._setup_common_success_path(mocker, role=Role.GUEST)

        variables = {
            "params": {
                "fieldType": "TEXT",
                "fieldName": "Priority",
                "description": "Task priority",
                "templateId": "tpl_1",
                "config": json.dumps({"max_length": 10}),
                "isRequired": True,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_create_field_with_empty_name(self, snapshot, mocker):
        self._setup_common_success_path(mocker)

        variables = {
            "params": {
                "fieldType": "TEXT",
                "fieldName": "",
                "description": "Task priority",
                "templateId": "tpl_1",
                "config": json.dumps({"max_length": 10}),
                "isRequired": True,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_create_field_with_invalid_config_keys(self, snapshot, mocker):
        self._setup_common_success_path(mocker)

        variables = {
            "params": {
                "fieldType": "TEXT",
                "fieldName": "Priority",
                "description": "Task priority",
                "templateId": "tpl_1",
                "config": json.dumps({"bad_key": 1}),
                "isRequired": True,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_create_field_text_default_exceeds_max_length(
            self, snapshot, mocker):
        self._setup_common_success_path(mocker)

        variables = {
            "params": {
                "fieldType": "TEXT",
                "fieldName": "Priority",
                "description": "Task priority",
                "templateId": "tpl_1",
                "config": json.dumps({"max_length": 3, "default": "HIGH"}),
                "isRequired": True,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_create_field_number_default_below_minimum(self, snapshot, mocker):
        self._setup_common_success_path(mocker)

        variables = {
            "params": {
                "fieldType": "NUMBER",
                "fieldName": "Estimate",
                "description": "Hours estimate",
                "templateId": "tpl_1",
                "config": json.dumps({"min": 10, "default": 5}),
                "isRequired": False,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_create_field_number_default_above_maximum(self, snapshot, mocker):
        self._setup_common_success_path(mocker)

        variables = {
            "params": {
                "fieldType": "NUMBER",
                "fieldName": "Estimate",
                "description": "Hours estimate",
                "templateId": "tpl_1",
                "config": json.dumps({"max": 5, "default": 10}),
                "isRequired": False,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_create_field_with_max_less_than_min(self, snapshot, mocker):
        self._setup_common_success_path(mocker)

        variables = {
            "params": {
                "fieldType": "NUMBER",
                "fieldName": "Estimate",
                "description": "Hours estimate",
                "templateId": "tpl_1",
                "config": json.dumps({"min": 10, "max": 2}),
                "isRequired": False,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_create_field_dropdown_missing_config(self, snapshot, mocker):
        self._setup_common_success_path(mocker)

        variables = {
            "params": {
                "fieldType": "DROPDOWN",
                "fieldName": "Priority",
                "description": "Task priority",
                "templateId": "tpl_1",
                "config": json.dumps({}),
                "isRequired": True,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_create_field_dropdown_options_missing(self, snapshot, mocker):
        self._setup_common_success_path(mocker)

        variables = {
            "params": {
                "fieldType": "DROPDOWN",
                "fieldName": "Priority",
                "description": "Task priority",
                "templateId": "tpl_1",
                "config": json.dumps({"default": "High"}),
                "isRequired": True,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_create_field_dropdown_default_not_in_options(
            self, snapshot, mocker):
        self._setup_common_success_path(mocker)

        variables = {
            "params": {
                "fieldType": "DROPDOWN",
                "fieldName": "Priority",
                "description": "Task priority",
                "templateId": "tpl_1",
                "config": json.dumps({
                    "options": ["Low", "Medium"],
                    "default": "High",
                }),
                "isRequired": True,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
