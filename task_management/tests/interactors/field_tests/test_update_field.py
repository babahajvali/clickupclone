from dataclasses import replace
from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    FieldNameAlreadyExists,
    ModificationNotAllowed,
    NothingToUpdateField,
    FieldNotFound,
    InactiveField,
    EmptyName,
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
            is_active=True,
            config={"max_length": 10},
            is_required=True,
            created_by="user_1",
        )

    def _get_interactor(
            self,
            *,
            role: Role = Role.MEMBER,
            name_exists: bool = False,
    ):
        field_storage = create_autospec(FieldStorageInterface)
        template_storage = create_autospec(TemplateStorageInterface)
        workspace_storage = create_autospec(WorkspaceStorageInterface)

        field_storage.is_field_name_exists.return_value = name_exists
        field_storage.update_field.return_value = self._get_field_dto()
        field_storage.get_field_by_id.return_value = self._get_field_dto()

        template_storage.get_workspace_id_from_template_id.return_value = (
            "workspace_id"
        )

        workspace_storage.get_workspace_member.return_value = (
            make_permission_dto(role)
        )

        return FieldInteractor(
            field_storage=field_storage,
            template_storage=template_storage,
            workspace_storage=workspace_storage
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
        interactor = self._get_interactor()
        dto = self._get_update_dto()

        result = interactor.update_field(dto, user_id="user_1")

        snapshot.assert_match(
            repr(result),
            "test_update_field_successfully.txt",
        )

    def test_update_field_permission_denied(self, snapshot):
        interactor = self._get_interactor(
            role=Role.GUEST
        )
        dto = self._get_update_dto()

        with pytest.raises(ModificationNotAllowed) as exc:
            interactor.update_field(dto, user_id="user_1")

        snapshot.assert_match(
            repr(exc.value.user_id),
            "test_update_field_permission_denied.txt",
        )

    def test_update_field_duplicate_name(self, snapshot):
        interactor = self._get_interactor(name_exists=True)
        dto = self._get_update_dto(field_name="Priority")

        with pytest.raises(FieldNameAlreadyExists) as exc:
            interactor.update_field(dto, user_id="user_1")

        snapshot.assert_match(
            repr(exc.value.field_name),
            "test_update_field_duplicate_name.txt",
        )

    def test_update_field_not_found(self, snapshot):
        interactor = self._get_interactor()
        interactor.field_storage.get_field_by_id.return_value = None
        dto = self._get_update_dto()

        with pytest.raises(FieldNotFound) as exc:
            interactor.update_field(dto, user_id="user_1")

        snapshot.assert_match(
            repr(exc.value.field_id),
            "test_update_field_not_found.txt",
        )

    def test_update_field_without_updates(self, snapshot):
        interactor = self._get_interactor()
        dto = self._get_update_dto(
            field_name=None,
            description=None,
            config=None,
            is_required=None,
        )

        with pytest.raises(NothingToUpdateField) as exc:
            interactor.update_field(dto, user_id="user_1")

        snapshot.assert_match(
            repr(exc.value.field_id),
            "test_update_field_without_updates.txt",
        )

    def test_update_field_inactive(self, snapshot):
        interactor = self._get_interactor()
        inactive_field = self._get_field_dto()
        inactive_field.is_active = False
        interactor.field_storage.get_field_by_id.return_value = inactive_field
        dto = self._get_update_dto()

        with pytest.raises(InactiveField) as exc:
            interactor.update_field(dto, user_id="user_1")

        snapshot.assert_match(
            repr(exc.value.field_id),
            "test_update_field_inactive.txt",
        )

    def test_update_field_empty_name(self, snapshot):
        interactor = self._get_interactor()
        dto = self._get_update_dto(field_name="   ")

        with pytest.raises(EmptyName) as exc:
            interactor.update_field(dto, user_id="user_1")

        snapshot.assert_match(
            repr(exc.value.name),
            "test_update_field_empty_name.txt",
        )

    def test_update_field_invalid_config_keys(self, snapshot):
        interactor = self._get_interactor()
        dto = self._get_update_dto(config={"bad_key": 1})

        with pytest.raises(InvalidFieldConfig) as exc:
            interactor.update_field(dto, user_id="user_1")

        snapshot.assert_match(
            repr(exc.value.invalid_keys),
            "test_update_field_invalid_config_keys.txt",
        )
