from enum import Enum
from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    TemplateNotFound,
    UnsupportedFieldType,
    FieldNameAlreadyExists,
    ModificationNotAllowed,
    EmptyName,
    MissingFieldConfig,
    DropdownOptionsMissing,
    InvalidFieldConfig,
)
from task_management.exceptions.enums import FieldType, Role
from task_management.interactors.fields.field_interactor import (
    FieldInteractor
)
from task_management.interactors.dtos import CreateFieldDTO, FieldDTO, \
    WorkspaceMemberDTO
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface
from task_management.interactors.storage_interfaces.field_storage_interface import (
    FieldStorageInterface
)
from task_management.interactors.storage_interfaces.template_storage_interface import (
    TemplateStorageInterface
)



class InvalidFieldEnum(Enum):
    INVALID = "invalid"


def make_permission_dto(role: Role):
    return WorkspaceMemberDTO(
        id=1,
        workspace_id="workspace_id1",
        role=role,
        user_id="user_1",
        is_active=True,
        added_by="admin_1"
    )


class TestCreateFieldInteractor:
    @staticmethod
    def _get_field_dto():
        return FieldDTO(
            field_id="field_1",
            field_type=FieldType.TEXT,
            description="Task priority",
            template_id="tpl_1",
            field_name="Priority",
            is_delete=True,
            order=1,
            config={"max_length": 10},
            is_required=True,
            created_by="user_1",
        )

    def _get_interactor(
            self,
            *,
            template_exists=True,
            role: Role = Role.MEMBER,
            name_exists=False,
    ):
        field_storage = create_autospec(FieldStorageInterface)
        template_storage = create_autospec(TemplateStorageInterface)
        workspace_storage = create_autospec(WorkspaceStorageInterface)

        template_storage.validate_template_exists.return_value = template_exists
        template_storage.get_workspace_id_from_template_id.return_value = (
            "workspace_id1"
        )

        workspace_storage.get_workspace_member.return_value = (
            make_permission_dto(role)
        )

        field_storage.is_field_name_exists.return_value = name_exists
        field_storage.get_next_field_order_in_template.return_value = 1
        field_storage.create_field.return_value = self._get_field_dto()

        return FieldInteractor(
            field_storage=field_storage,
            template_storage=template_storage,
            workspace_storage=workspace_storage
        )

    def test_create_field_success(self, snapshot):
        interactor = self._get_interactor()

        dto = CreateFieldDTO(
            field_type=FieldType.TEXT,
            field_name="Priority",
            description="Task priority",
            template_id="tpl_1",
            config={"max_length": 10},
            is_required=True,
            created_by_user_id="user_1",
        )

        result = interactor.create_field(dto)

        snapshot.assert_match(
            repr(result),
            "test_create_field_success.txt"
        )

    def test_create_field_template_not_found(self, snapshot):
        interactor = self._get_interactor(template_exists=False)

        dto = CreateFieldDTO(
            field_type=FieldType.TEXT,
            field_name="Priority",
            description="",
            template_id="invalid_tpl",
            config={},
            is_required=False,
            created_by_user_id="user_1",
        )

        with pytest.raises(TemplateNotFound) as exc:
            interactor.create_field(dto)

        snapshot.assert_match(
            repr(exc.value.template_id),
            "test_create_field_template_not_found.txt"
        )

    # ❌ INVALID FIELD TYPE
    def test_create_field_invalid_field_type(self, snapshot):
        interactor = self._get_interactor()

        dto = CreateFieldDTO(
            field_type=InvalidFieldEnum.INVALID,
            field_name="Priority",
            description="",
            template_id="tpl_1",
            config={},
            is_required=False,
            created_by_user_id="user_1",
        )

        with pytest.raises(UnsupportedFieldType) as exc:
            interactor.create_field(dto)

        snapshot.assert_match(
            repr(exc.value.field_type),
            "test_create_field_invalid_field_type.txt"
        )

    def test_create_field_permission_denied(self, snapshot):
        interactor = self._get_interactor(
            role=Role.GUEST
        )

        dto = CreateFieldDTO(
            field_type=FieldType.TEXT,
            field_name="Priority",
            description="",
            template_id="tpl_1",
            config={},
            is_required=False,
            created_by_user_id="user_1",
        )

        with pytest.raises(ModificationNotAllowed) as exc:
            interactor.create_field(dto)

        snapshot.assert_match(
            repr(exc.value.user_id),
            "test_create_field_permission_denied.txt"
        )

    def test_create_field_duplicate_name(self, snapshot):
        interactor = self._get_interactor(name_exists=True)

        dto = CreateFieldDTO(
            field_type=FieldType.TEXT,
            field_name="Priority",
            description="",
            template_id="tpl_1",
            config={},
            is_required=False,
            created_by_user_id="user_1",
        )

        with pytest.raises(FieldNameAlreadyExists) as exc:
            interactor.create_field(dto)

        snapshot.assert_match(
            repr(exc.value.field_name),
            "test_create_field_duplicate_name.txt"
        )

    def test_create_field_empty_name(self, snapshot):
        interactor = self._get_interactor()

        dto = CreateFieldDTO(
            field_type=FieldType.TEXT,
            field_name="   ",
            description="",
            template_id="tpl_1",
            config={},
            is_required=False,
            created_by_user_id="user_1",
        )

        with pytest.raises(EmptyName) as exc:
            interactor.create_field(dto)

        snapshot.assert_match(
            repr(exc.value.name),
            "test_create_field_empty_name.txt"
        )

    def test_create_field_missing_config_for_dropdown(self, snapshot):
        interactor = self._get_interactor()

        dto = CreateFieldDTO(
            field_type=FieldType.DROPDOWN,
            field_name="Priority",
            description="",
            template_id="tpl_1",
            config={},
            is_required=False,
            created_by_user_id="user_1",
        )

        with pytest.raises(MissingFieldConfig) as exc:
            interactor.create_field(dto)

        snapshot.assert_match(
            repr(exc.value.field_type),
            "test_create_field_missing_config_for_dropdown.txt"
        )

    def test_create_field_dropdown_options_missing(self, snapshot):
        interactor = self._get_interactor()

        dto = CreateFieldDTO(
            field_type=FieldType.DROPDOWN,
            field_name="Priority",
            description="",
            template_id="tpl_1",
            config={"default": "High"},
            is_required=False,
            created_by_user_id="user_1",
        )

        with pytest.raises(DropdownOptionsMissing) as exc:
            interactor.create_field(dto)

        snapshot.assert_match(
            repr(exc.value.field_type),
            "test_create_field_dropdown_options_missing.txt"
        )

    def test_create_field_invalid_config_keys(self, snapshot):
        interactor = self._get_interactor()

        dto = CreateFieldDTO(
            field_type=FieldType.TEXT,
            field_name="Priority",
            description="",
            template_id="tpl_1",
            config={"bad_key": 1},
            is_required=False,
            created_by_user_id="user_1",
        )

        with pytest.raises(InvalidFieldConfig) as exc:
            interactor.create_field(dto)

        snapshot.assert_match(
            repr(exc.value.invalid_keys),
            "test_create_field_invalid_config_keys.txt"
        )
