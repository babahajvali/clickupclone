from dataclasses import replace
from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    FieldNameAlreadyExists,
    ModificationNotAllowed,
    NothingToUpdateField,
    FieldNotFound,
    DeletedFieldException,
    EmptyFieldName,
    InvalidFieldConfig,
)
from task_management.exceptions.enums import FieldType, Role
from task_management.interactors.dtos import (
    FieldDTO,
    UpdateFieldDTO,
    WorkspaceMemberDTO,
)
from task_management.interactors.fields.field_interactor import FieldInteractor
from task_management.interactors.storage_interfaces import \
    FieldStorageInterface, TemplateStorageInterface, \
    WorkspaceStorageInterface


def make_permission_dto(role: Role):
    return WorkspaceMemberDTO(
        id=1,
        workspace_id="workspace_id",
        role=role,
        user_id="user_1",
        is_active=True,
        added_by="admin_1",
    )


class TestUpdateFieldInteractor:

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

    def _setup_update_field_dependencies(
            self,
            *,
            role: Role = Role.MEMBER,
            name_exists: bool = False,
    ):
        self.field_storage.is_field_name_exists.return_value = name_exists
        self.field_storage.update_field.return_value = self._get_field_dto()
        self.field_storage.get_field.return_value = self._get_field_dto()

        self.template_storage.get_workspace_id_from_template_id.return_value = (
            "workspace_id"
        )

        self.workspace_storage.get_workspace_member.return_value = (
            make_permission_dto(role)
        )

    @staticmethod
    def _get_update_dto(**overrides):
        dto = UpdateFieldDTO(
            field_id="field_1",
            field_name="Priority",
            description="Task priority",
            config={"max_length": 10},
            is_required=True,
        )
        return replace(dto, **overrides)

    def test_update_field_successfully(self, snapshot):
        # Arrange
        self._setup_update_field_dependencies()
        dto = self._get_update_dto()

        # Act
        result = self.interactor.update_field(dto, user_id="user_1")

        snapshot.assert_match(
            repr(result),
            "test_update_field_successfully.txt",
        )

    def test_update_field_permission_denied(self, snapshot):
        # Arrange
        self._setup_update_field_dependencies(role=Role.GUEST)
        dto = self._get_update_dto()

        # Act
        with pytest.raises(ModificationNotAllowed) as exc:
            self.interactor.update_field(dto, user_id="user_1")

        snapshot.assert_match(
            repr(exc.value.user_id),
            "test_update_field_permission_denied.txt",
        )

    def test_update_field_duplicate_name(self, snapshot):
        # Arrange
        self._setup_update_field_dependencies(name_exists=True)
        dto = self._get_update_dto(field_name="Priority")

        # Act
        with pytest.raises(FieldNameAlreadyExists) as exc:
            self.interactor.update_field(dto, user_id="user_1")

        snapshot.assert_match(
            repr(exc.value.field_name),
            "test_update_field_duplicate_name.txt",
        )

    def test_update_field_not_found(self, snapshot):
        # Arrange
        self._setup_update_field_dependencies()
        self.field_storage.get_field.return_value = None
        dto = self._get_update_dto()

        # Act
        with pytest.raises(FieldNotFound) as exc:
            self.interactor.update_field(dto, user_id="user_1")

        snapshot.assert_match(
            repr(exc.value.field_id),
            "test_update_field_not_found.txt",
        )

    def test_update_field_without_updates(self, snapshot):
        # Arrange
        self._setup_update_field_dependencies()
        dto = self._get_update_dto(
            field_name=None,
            description=None,
            config=None,
            is_required=None,
        )

        # Act
        with pytest.raises(NothingToUpdateField) as exc:
            self.interactor.update_field(dto, user_id="user_1")

        snapshot.assert_match(
            repr(exc.value.field_id),
            "test_update_field_without_updates.txt",
        )

    def test_update_field_inactive(self, snapshot):
        # Arrange
        self._setup_update_field_dependencies()
        inactive_field = self._get_field_dto()
        inactive_field.is_deleted = True
        self.field_storage.get_field.return_value = inactive_field
        dto = self._get_update_dto()

        # Act
        with pytest.raises(DeletedFieldException) as exc:
            self.interactor.update_field(dto, user_id="user_1")

        snapshot.assert_match(
            repr(exc.value.field_id),
            "test_update_field_inactive.txt",
        )

    def test_update_field_empty_name(self, snapshot):
        # Arrange
        self._setup_update_field_dependencies()
        dto = self._get_update_dto(field_name="   ")

        # Act
        with pytest.raises(EmptyFieldName) as exc:
            self.interactor.update_field(dto, user_id="user_1")

        snapshot.assert_match(
            repr(exc.value.field_name),
            "test_update_field_empty_name.txt",
        )

    def test_update_field_invalid_config_keys(self, snapshot):
        # Arrange
        self._setup_update_field_dependencies()
        dto = self._get_update_dto(config={"bad_key": 1})

        # Act
        with pytest.raises(InvalidFieldConfig) as exc:
            self.interactor.update_field(dto, user_id="user_1")

        snapshot.assert_match(
            repr(exc.value.invalid_keys),
            "test_update_field_invalid_config_keys.txt",
        )
