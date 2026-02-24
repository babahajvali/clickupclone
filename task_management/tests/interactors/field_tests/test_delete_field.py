from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    ModificationNotAllowed,
    FieldNotFound,
    DeletedFieldException,
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
            is_deleted=False,
            config={"max_length": 10},
            is_required=True,
            created_by="user_1",
        )

    def setup_method(self):
        self.field_storage = create_autospec(FieldStorageInterface)
        self.template_storage = create_autospec(TemplateStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)

        self.interactor = FieldInteractor(
            field_storage=self.field_storage,
            template_storage=self.template_storage,
            workspace_storage=self.workspace_storage,
        )

    def _setup_delete_field_dependencies(
            self,
            *,
            role: Role = Role.MEMBER,
            field_data: FieldDTO | None = None,
    ):
        if field_data is None:
            field_data = self._get_field_dto()

        self.field_storage.get_field.return_value = field_data
        self.field_storage.delete_field.return_value = field_data

        self.template_storage.get_workspace_id_from_template_id.return_value = (
            "workspace_id"
        )
        self.workspace_storage.get_workspace_member.return_value = (
            make_permission_dto(role)
        )

    def test_delete_field_success(self, snapshot):
        # Arrange
        self._setup_delete_field_dependencies()

        # Act
        result = self.interactor.delete_field(
            field_id="field_1",
            user_id="user_1",
        )

        snapshot.assert_match(
            repr(result),
            "test_delete_field_success.txt",
        )

    def test_delete_field_not_found(self, snapshot):
        # Arrange
        self._setup_delete_field_dependencies(field_data=None)
        self.field_storage.get_field.return_value = None

        # Act
        with pytest.raises(FieldNotFound) as exc:
            self.interactor.delete_field(
                field_id="field_1",
                user_id="user_1",
            )

        snapshot.assert_match(
            repr(exc.value.field_id),
            "test_delete_field_not_found.txt",
        )

    def test_delete_field_permission_denied(self, snapshot):
        # Arrange
        self._setup_delete_field_dependencies(role=Role.GUEST)

        # Act
        with pytest.raises(ModificationNotAllowed) as exc:
            self.interactor.delete_field(
                field_id="field_1",
                user_id="user_1",
            )

        snapshot.assert_match(
            repr(exc.value.user_id),
            "test_delete_field_permission_denied.txt",
        )
