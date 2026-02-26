from enum import Enum
from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    TemplateNotFound,
    UnsupportedFieldType,
    FieldNameAlreadyExists,
    ModificationNotAllowed,
    MissingFieldConfig,
    DropdownOptionsMissing,
    InvalidFieldConfig, EmptyFieldName,
)
from task_management.exceptions.enums import FieldType, Role
from task_management.interactors.fields.field_interactor import FieldInteractor
from task_management.interactors.dtos import (
    CreateFieldDTO,
    FieldDTO,
    WorkspaceMemberDTO,
)
from task_management.interactors.storage_interfaces import \
    FieldStorageInterface, TemplateStorageInterface, WorkspaceStorageInterface


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
            is_deleted=True,
            order=1,
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

    def _setup_create_field_dependencies(
            self,
            *,
            template_exists: bool = True,
            role: Role = Role.MEMBER,
            name_exists: bool = False,
    ):
        self.template_storage.validate_template_exists.return_value = (
            template_exists
        )
        self.template_storage.get_workspace_id_from_template_id.return_value = (
            "workspace_id1"
        )

        self.workspace_storage.get_workspace_member.return_value = (
            make_permission_dto(role)
        )

        self.field_storage.is_field_name_exists.return_value = name_exists
        self.field_storage.get_last_field_order_in_template.return_value = 1
        self.field_storage.create_field.return_value = self._get_field_dto()

    def test_create_field_success(self, snapshot):
        # Arrange
        self._setup_create_field_dependencies()

        dto = CreateFieldDTO(
            field_type=FieldType.TEXT,
            field_name="Priority",
            description="Task priority",
            template_id="tpl_1",
            config={"max_length": 10},
            is_required=True,
            created_by_user_id="user_1",
        )

        # Act
        result = self.interactor.create_field(dto)

        snapshot.assert_match(
            repr(result),
            "test_create_field_success.txt"
        )

    def test_create_field_template_not_found(self, snapshot):
        # Arrange
        self._setup_create_field_dependencies(template_exists=False)

        dto = CreateFieldDTO(
            field_type=FieldType.TEXT,
            field_name="Priority",
            description="",
            template_id="invalid_tpl",
            config={},
            is_required=False,
            created_by_user_id="user_1",
        )

        # Act
        with pytest.raises(TemplateNotFound) as exc:
            self.interactor.create_field(dto)

        snapshot.assert_match(
            repr(exc.value.template_id),
            "test_create_field_template_not_found.txt"
        )

    # ❌ INVALID FIELD TYPE
    def test_create_field_invalid_field_type(self, snapshot):
        # Arrange
        self._setup_create_field_dependencies()

        dto = CreateFieldDTO(
            field_type=InvalidFieldEnum.INVALID,
            field_name="Priority",
            description="",
            template_id="tpl_1",
            config={},
            is_required=False,
            created_by_user_id="user_1",
        )

        # Act
        with pytest.raises(UnsupportedFieldType) as exc:
            self.interactor.create_field(dto)

        snapshot.assert_match(
            repr(exc.value.field_type),
            "test_create_field_invalid_field_type.txt"
        )

    def test_create_field_permission_denied(self, snapshot):
        # Arrange
        self._setup_create_field_dependencies(role=Role.GUEST)

        dto = CreateFieldDTO(
            field_type=FieldType.TEXT,
            field_name="Priority",
            description="",
            template_id="tpl_1",
            config={},
            is_required=False,
            created_by_user_id="user_1",
        )

        # Act
        with pytest.raises(ModificationNotAllowed) as exc:
            self.interactor.create_field(dto)

        snapshot.assert_match(
            repr(exc.value.user_id),
            "test_create_field_permission_denied.txt"
        )

    def test_create_field_duplicate_name(self, snapshot):
        # Arrange
        self._setup_create_field_dependencies(name_exists=True)

        dto = CreateFieldDTO(
            field_type=FieldType.TEXT,
            field_name="Priority",
            description="",
            template_id="tpl_1",
            config={},
            is_required=False,
            created_by_user_id="user_1",
        )

        # Act
        with pytest.raises(FieldNameAlreadyExists) as exc:
            self.interactor.create_field(dto)

        snapshot.assert_match(
            repr(exc.value.field_name),
            "test_create_field_duplicate_name.txt"
        )

    def test_create_field_empty_name(self, snapshot):
        # Arrange
        self._setup_create_field_dependencies()

        dto = CreateFieldDTO(
            field_type=FieldType.TEXT,
            field_name="   ",
            description="",
            template_id="tpl_1",
            config={},
            is_required=False,
            created_by_user_id="user_1",
        )

        # Act
        with pytest.raises(EmptyFieldName) as exc:
            self.interactor.create_field(dto)

        snapshot.assert_match(
            repr(exc.value.field_name),
            "test_create_field_empty_name.txt"
        )

    def test_create_field_missing_config_for_dropdown(self, snapshot):
        # Arrange
        self._setup_create_field_dependencies()

        dto = CreateFieldDTO(
            field_type=FieldType.DROPDOWN,
            field_name="Priority",
            description="",
            template_id="tpl_1",
            config={},
            is_required=False,
            created_by_user_id="user_1",
        )

        # Act
        with pytest.raises(MissingFieldConfig) as exc:
            self.interactor.create_field(dto)

        snapshot.assert_match(
            repr(exc.value.field_type),
            "test_create_field_missing_config_for_dropdown.txt"
        )

    def test_create_field_dropdown_options_missing(self, snapshot):
        # Arrange
        self._setup_create_field_dependencies()

        dto = CreateFieldDTO(
            field_type=FieldType.DROPDOWN,
            field_name="Priority",
            description="",
            template_id="tpl_1",
            config={"default": "High"},
            is_required=False,
            created_by_user_id="user_1",
        )

        # Act
        with pytest.raises(DropdownOptionsMissing) as exc:
            self.interactor.create_field(dto)

        snapshot.assert_match(
            repr(exc.value.field_type),
            "test_create_field_dropdown_options_missing.txt"
        )

    def test_create_field_invalid_config_keys(self, snapshot):
        # Arrange
        self._setup_create_field_dependencies()

        dto = CreateFieldDTO(
            field_type=FieldType.TEXT,
            field_name="Priority",
            description="",
            template_id="tpl_1",
            config={"bad_key": 1},
            is_required=False,
            created_by_user_id="user_1",
        )

        # Act
        with pytest.raises(InvalidFieldConfig) as exc:
            self.interactor.create_field(dto)

        snapshot.assert_match(
            repr(exc.value.invalid_keys),
            "test_create_field_invalid_config_keys.txt"
        )
