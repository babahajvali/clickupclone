from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    ModificationNotAllowed,
    FieldNotFound,
    InactiveField,
)
from task_management.exceptions.enums import FieldType, Role
from task_management.interactors.dtos import FieldDTO, WorkspaceMemberDTO
from task_management.interactors.fields.field_interactor import FieldInteractor
from task_management.interactors.storage_interfaces import (
    FieldStorageInterface,
    TemplateStorageInterface,
    WorkspaceStorageInterface,
)


def make_permission_dto(role: Role):
    return WorkspaceMemberDTO(
        id=1,
        workspace_id="workspace_id",
        role=role,
        user_id="user_1",
        is_active=True,
        added_by="admin_1",
    )


class TestDeleteFieldInteractor:
    @staticmethod
    def _get_field_dto():
        return FieldDTO(
            field_id="field_1",
            field_type=FieldType.TEXT,
            description="Task priority",
            template_id="tpl_1",
            field_name="Priority",
            order=1,
            is_active=True,
            config={"max_length": 10},
            is_required=True,
            created_by="user_1",
        )

    def _get_interactor(
            self,
            *,
            role: Role = Role.MEMBER,
            field_data: FieldDTO | None = None,
    ):
        field_storage = create_autospec(FieldStorageInterface)
        template_storage = create_autospec(TemplateStorageInterface)
        workspace_storage = create_autospec(WorkspaceStorageInterface)

        if field_data is None:
            field_data = self._get_field_dto()

        field_storage.get_field_by_id.return_value = field_data
        field_storage.delete_field.return_value = field_data

        template_storage.get_workspace_id_from_template_id.return_value = (
            "workspace_id"
        )
        workspace_storage.get_workspace_member.return_value = (
            make_permission_dto(role)
        )

        return FieldInteractor(
            field_storage=field_storage,
            template_storage=template_storage,
            workspace_storage=workspace_storage,
        )

    def test_delete_field_success(self, snapshot):
        interactor = self._get_interactor()

        result = interactor.delete_field(
            field_id="field_1",
            user_id="user_1",
        )

        snapshot.assert_match(
            repr(result),
            "test_delete_field_success.txt",
        )

    def test_delete_field_not_found(self, snapshot):
        interactor = self._get_interactor(field_data=None)
        interactor.field_storage.get_field_by_id.return_value = None

        with pytest.raises(FieldNotFound) as exc:
            interactor.delete_field(
                field_id="field_1",
                user_id="user_1",
            )

        snapshot.assert_match(
            repr(exc.value.field_id),
            "test_delete_field_not_found.txt",
        )

    def test_delete_field_inactive(self, snapshot):
        field_data = self._get_field_dto()
        field_data.is_active = False
        interactor = self._get_interactor(field_data=field_data)

        with pytest.raises(InactiveField) as exc:
            interactor.delete_field(
                field_id="field_1",
                user_id="user_1",
            )

        snapshot.assert_match(
            repr(exc.value.field_id),
            "test_delete_field_inactive.txt",
        )

    def test_delete_field_permission_denied(self, snapshot):
        interactor = self._get_interactor(role=Role.GUEST)

        with pytest.raises(ModificationNotAllowed) as exc:
            interactor.delete_field(
                field_id="field_1",
                user_id="user_1",
            )

        snapshot.assert_match(
            repr(exc.value.user_id),
            "test_delete_field_permission_denied.txt",
        )
