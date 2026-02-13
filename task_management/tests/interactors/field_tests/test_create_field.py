from enum import Enum
from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    TemplateNotFoundException,
    UnsupportedFieldTypeException,
    FieldNameAlreadyExistsException,
    ModificationNotAllowedException,
)
from task_management.exceptions.enums import FieldTypes, Role
from task_management.interactors.field.field_interactor import (
    FieldInteractor
)
from task_management.interactors.dtos import CreateFieldDTO, FieldDTO, \
    WorkspaceMemberDTO
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface
from task_management.interactors.storage_interfaces.field_storage_interface import (
    FieldStorageInterface
)
from task_management.interactors.storage_interfaces.list_storage_interface import \
    ListStorageInterface
from task_management.interactors.storage_interfaces.space_storage_interface import \
    SpaceStorageInterface
from task_management.interactors.storage_interfaces.template_storage_interface import (
    TemplateStorageInterface
)



class InvalidFieldEnum(Enum):
    INVALID = "invalid"


class DummyTemplate:
    def __init__(self, list_id: str):
        self.list_id = list_id


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
            field_type=FieldTypes.TEXT,
            description="Task priority",
            template_id="tpl_1",
            field_name="Priority",
            is_active=True,
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
        list_storage = create_autospec(ListStorageInterface)
        space_storage = create_autospec(SpaceStorageInterface)
        workspace_storage = create_autospec(WorkspaceStorageInterface)

        # template mock
        if template_exists:
            class DummyTemplate:
                def __init__(self, list_id):
                    self.list_id = list_id

            template_storage.get_template_by_id.return_value = DummyTemplate(
                list_id="list_1"
            )
        else:
            template_storage.get_template_by_id.return_value = None
        list_storage.get_list_space_id.return_value = "Space1"

        workspace_storage.get_workspace_member.return_value = (
            make_permission_dto(role)
        )

        field_storage.is_field_name_exists.return_value = name_exists
        field_storage.create_field.return_value = self._get_field_dto()

        return FieldInteractor(
            field_storage=field_storage,
            template_storage=template_storage,
            workspace_storage=workspace_storage,
            list_storage=list_storage,
            space_storage=space_storage
        )

    def test_create_field_success(self, snapshot):
        interactor = self._get_interactor()

        dto = CreateFieldDTO(
            field_type=FieldTypes.TEXT,
            field_name="Priority",
            description="Task priority",
            template_id="tpl_1",
            config={"max_length": 10},
            is_required=True,
            created_by="user_1",
        )

        result = interactor.create_field(dto)

        snapshot.assert_match(
            repr(result),
            "test_create_field_success.txt"
        )

    def test_create_field_template_not_found(self, snapshot):
        interactor = self._get_interactor(template_exists=False)

        dto = CreateFieldDTO(
            field_type=FieldTypes.TEXT,
            field_name="Priority",
            description="",
            template_id="invalid_tpl",
            config={},
            is_required=False,
            created_by="user_1",
        )

        with pytest.raises(TemplateNotFoundException) as exc:
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
            created_by="user_1",
        )

        with pytest.raises(UnsupportedFieldTypeException) as exc:
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
            field_type=FieldTypes.TEXT,
            field_name="Priority",
            description="",
            template_id="tpl_1",
            config={},
            is_required=False,
            created_by="user_1",
        )

        with pytest.raises(ModificationNotAllowedException) as exc:
            interactor.create_field(dto)

        snapshot.assert_match(
            repr(exc.value.user_id),
            "test_create_field_permission_denied.txt"
        )

    def test_create_field_duplicate_name(self, snapshot):
        interactor = self._get_interactor(name_exists=True)

        dto = CreateFieldDTO(
            field_type=FieldTypes.TEXT,
            field_name="Priority",
            description="",
            template_id="tpl_1",
            config={},
            is_required=False,
            created_by="user_1",
        )

        with pytest.raises(FieldNameAlreadyExistsException) as exc:
            interactor.create_field(dto)

        snapshot.assert_match(
            repr(exc.value.field_name),
            "test_create_field_duplicate_name.txt"
        )
