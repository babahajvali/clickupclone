from types import SimpleNamespace

import pytest

from task_management.exceptions.enums import FieldType, Role
from task_management.interactors.dtos import FieldDTO, WorkspaceMemberDTO
from task_management.tests.api_tests.fields import BaseReorderField


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


def get_field_mock(mocker):
    return mocker.patch(
        "task_management.storages.field_storage.FieldStorage.get_fields")


def template_fields_count_mock(mocker):
    return mocker.patch(
        "task_management.storages.field_storage.FieldStorage.template_fields_count"
    )


def shift_fields_down_mock(mocker):
    return mocker.patch(
        "task_management.storages.field_storage.FieldStorage.shift_fields_down"
    )


def shift_fields_up_mock(mocker):
    return mocker.patch(
        "task_management.storages.field_storage.FieldStorage.shift_fields_up"
    )


def update_field_order_mock(mocker):
    return mocker.patch(
        "task_management.storages.field_storage.FieldStorage.update_field_order"
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


def create_field_dto(*, order=2, is_deleted=False) -> FieldDTO:
    return FieldDTO(
        field_id="field_1",
        field_type=FieldType.TEXT,
        description="Task priority",
        template_id="tpl_1",
        field_name="Priority",
        is_deleted=is_deleted,
        order=order,
        config={"max_length": 10},
        is_required=True,
        created_by="user_1",
    )


@pytest.mark.django_db
class TestReorderFieldAPI(BaseReorderField):

    def _setup_common(self, mocker, *, role=Role.MEMBER, template_exists=True):
        template = validate_template_exists_mock(mocker)
        template.return_value = template_exists

        workspace_id = get_workspace_id_from_template_id_mock(mocker)
        workspace_id.return_value = "workspace_1"

        workspace_member = get_workspace_member_mock(mocker)
        workspace_member.return_value = create_workspace_member_dto(role=role)

        count = template_fields_count_mock(mocker)
        count.return_value = 5

        field_data = get_field_mock(mocker)
        field_data.return_value = create_field_dto(order=2, is_deleted=False)

    def test_reorder_field_successfully(self, snapshot, mocker):
        self._setup_common(mocker)
        shift_fields_down_mock(mocker)
        shift_fields_up_mock(mocker)
        updated = update_field_order_mock(mocker)
        updated.return_value = create_field_dto(order=3, is_deleted=False)

        variables = {"params": {"fieldId": "field_1", "templateId": "tpl_1",
                                "newOrder": 3}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_reorder_field_not_found(self, snapshot, mocker):
        self._setup_common(mocker)
        field_data = get_field_mock(mocker)
        field_data.return_value = None

        variables = {"params": {"fieldId": "field_404", "templateId": "tpl_1",
                                "newOrder": 2}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_reorder_field_deleted(self, snapshot, mocker):
        self._setup_common(mocker)
        field_data = get_field_mock(mocker)
        field_data.return_value = create_field_dto(order=2, is_deleted=True)

        variables = {"params": {"fieldId": "field_1", "templateId": "tpl_1",
                                "newOrder": 3}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_reorder_field_template_not_found(self, snapshot, mocker):
        self._setup_common(mocker, template_exists=False)

        variables = {"params": {"fieldId": "field_1", "templateId": "tpl_404",
                                "newOrder": 2}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_reorder_field_invalid_order_below_one(self, snapshot, mocker):
        self._setup_common(mocker)

        variables = {"params": {"fieldId": "field_1", "templateId": "tpl_1",
                                "newOrder": 0}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_reorder_field_invalid_order_above_count(self, snapshot, mocker):
        self._setup_common(mocker)

        variables = {"params": {"fieldId": "field_1", "templateId": "tpl_1",
                                "newOrder": 10}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_reorder_field_permission_denied(self, snapshot, mocker):
        self._setup_common(mocker, role=Role.GUEST)

        variables = {"params": {"fieldId": "field_1", "templateId": "tpl_1",
                                "newOrder": 3}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_reorder_field_user_not_workspace_member(self, snapshot, mocker):
        self._setup_common(mocker)
        workspace_member = get_workspace_member_mock(mocker)
        workspace_member.return_value = None

        variables = {"params": {"fieldId": "field_1", "templateId": "tpl_1",
                                "newOrder": 3}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
