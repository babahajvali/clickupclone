from dataclasses import dataclass, replace
from enum import Enum
from typing import Optional
from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    TemplateNotFoundException,
    FieldNameAlreadyExistsException,
    ModificationNotAllowedException,
)
from task_management.exceptions.enums import FieldType, PermissionsEnum
from task_management.interactors.dtos import (
    FieldDTO,
    UserListPermissionDTO,
)
from task_management.interactors.field_interactors.field_interactors import (
    FieldInteractor
)
from task_management.interactors.storage_interface.field_storage_interface import (
    FieldStorageInterface
)
from task_management.interactors.storage_interface.list_permission_storage_interface import (
    ListPermissionStorageInterface
)
from task_management.interactors.storage_interface.template_storage_interface import (
    TemplateStorageInterface
)

@dataclass
class UpdateFieldDTO:
    field_id: str
    description: Optional[str]
    field_name: Optional[str]
    config: Optional[dict]
    is_required: Optional[bool]


def make_permission_dto(permission_type: PermissionsEnum):
    return UserListPermissionDTO(
        id=1,
        list_id="list_1",
        permission_type=permission_type,
        user_id="user_1",
        is_active=True,
        added_by="admin_1",
    )


class DummyTemplate:
    def __init__(self, list_id: str):
        self.list_id = list_id


class FieldEnum(Enum):
    INVALID = "invalid"



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
            config={"max_length": 10},
            is_required=True,
            created_by="user_1",
        )

    def _get_interactor(
        self,
        *,
        template_exists: bool = True,
        permission: PermissionsEnum = PermissionsEnum.FULL_EDIT,
        name_exists: bool = False,
    ):
        field_storage = create_autospec(FieldStorageInterface)
        template_storage = create_autospec(TemplateStorageInterface)
        permission_storage = create_autospec(ListPermissionStorageInterface)

        field_storage.is_field_exists.return_value = True
        field_storage.check_field_name_except_this_field.return_value = name_exists
        field_storage.update_field.return_value = self._get_field_dto()
        field_storage.get_field_by_id.return_value = self._get_field_dto()

        if template_exists:
            template_storage.get_template_by_id.return_value = DummyTemplate(
                list_id="list_1"
            )
        else:
            template_storage.get_template_by_id.return_value = None

        permission_storage.get_user_permission_for_list.return_value = (
            make_permission_dto(permission)
        )

        return FieldInteractor(
            field_storage=field_storage,
            permission_storage=permission_storage,
            template_storage=template_storage,
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
            permission=PermissionsEnum.VIEW
        )
        dto = self._get_update_dto()

        with pytest.raises(ModificationNotAllowedException) as exc:
            interactor.update_field(dto, user_id="user_1")

        snapshot.assert_match(
            repr(exc.value.user_id),
            "test_update_field_permission_denied.txt",
        )

    def test_update_field_duplicate_name(self, snapshot):
        interactor = self._get_interactor(name_exists=True)
        dto = self._get_update_dto(field_name="Priority")

        with pytest.raises(FieldNameAlreadyExistsException) as exc:
            interactor.update_field(dto, user_id="user_1")

        snapshot.assert_match(
            repr(exc.value.field_name),
            "test_update_field_duplicate_name.txt",
        )


    def test_update_field_template_not_found(self):
        interactor = self._get_interactor(template_exists=False)
        dto = self._get_update_dto()

        with pytest.raises(TemplateNotFoundException):
            interactor.update_field(dto, user_id="user_1")
