from dataclasses import replace
from enum import Enum
from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    UserNotFoundException,
    TemplateNotFoundException,
    UnexpectedFieldTypeFoundException,
    FieldNameAlreadyExistsException,
    FieldOrderAlreadyExistsException,
    NotAccessToCreateFieldException
)
from task_management.interactors.field_interactors.update_field_interactor import (
    UpdateFieldInteractor
)
from task_management.interactors.dtos import (
    UpdateFieldDTO,
    FieldDTO,
    FieldTypeEnum,
    PermissionsEnum
)
from task_management.interactors.storage_interface.field_storage_interface import \
    FieldStorageInterface
from task_management.interactors.storage_interface.permission_storage_interface import \
    PermissionStorageInterface
from task_management.interactors.storage_interface.template_storage_interface import \
    TemplateStorageInterface
from task_management.interactors.storage_interface.user_storage_interface import \
    UserStorageInterface


class FieldEnum(Enum):
    INVALID = "Invalid"


class TestUpdateFieldInteractor:

    def _get_field_dto(self):
        return FieldDTO(
            field_id="field_1",
            field_type=FieldTypeEnum.Text,
            description="Task priority",
            template_id="tpl_1",
            field_name="Priority",
            order=1,
            config={"max_length": 10},
            is_required=True,
            created_by="user_1"
        )

    def _get_interactor(self, *,
                        user_exists=True,
                        template_exists=True,
                        permission=PermissionsEnum.GUEST,
                        name_exists=False,
                        order_exists=False):

        field_storage = create_autospec(FieldStorageInterface)
        user_storage = create_autospec(UserStorageInterface)
        template_storage = create_autospec(TemplateStorageInterface)
        permission_storage = create_autospec(PermissionStorageInterface)

        field_storage.check_field_exist.return_value = True
        field_storage.check_field_name_except_this_field.return_value = name_exists
        field_storage.check_field_order_exist.return_value = order_exists
        field_storage.update_field.return_value = self._get_field_dto()

        user_storage.check_user_exist.return_value = user_exists
        template_storage.check_template_exist.return_value = template_exists
        permission_storage.get_user_access_permissions.return_value = permission

        interactor = UpdateFieldInteractor(
            user_storage=user_storage,
            field_storage=field_storage,
            permission_storage=permission_storage,
            template_storage=template_storage
        )

        return interactor

    def _get_update_dto(self, **overrides):
        data = UpdateFieldDTO(
            field_id="field_1",
            field_type=FieldTypeEnum.Text,
            field_name="Priority",
            description="Task priority",
            template_id="tpl_1",
            order=1,
            config={"max_length": 10},
            is_required=True,
            created_by="user_1"
        )
        return replace(data, **overrides)


    def test_update_field_successfully(self, snapshot):
        interactor = self._get_interactor()
        update_field_data = self._get_update_dto()

        result = interactor.update_field(update_field_data)

        snapshot.assert_match(
            repr(result),
            "test_update_field_successfully.txt"
        )



    def test_update_field_invalid_field_type(self, snapshot):
        interactor = self._get_interactor()
        update_field_data = self._get_update_dto(
            field_type=FieldEnum.INVALID
        )

        with pytest.raises(UnexpectedFieldTypeFoundException) as exc:
            interactor.update_field(update_field_data)

        snapshot.assert_match(
            repr(exc.value.field_type),
            "test_update_field_invalid_field_type.txt"
        )

    def test_update_field_user_not_found(self, snapshot):
        interactor = self._get_interactor(user_exists=False)
        update_field_data = self._get_update_dto(created_by="invalid_user")

        with pytest.raises(UserNotFoundException) as exc:
            interactor.update_field(update_field_data)

        snapshot.assert_match(
            repr(exc.value.user_id),
            "test_update_field_user_not_found.txt"
        )

    def test_update_field_template_not_found(self, snapshot):
        interactor = self._get_interactor(template_exists=False)
        update_field_data = self._get_update_dto(template_id="invalid_tpl")

        with pytest.raises(TemplateNotFoundException) as exc:
            interactor.update_field(update_field_data)

        snapshot.assert_match(
            repr(exc.value.template_id),
            "test_update_field_template_not_found.txt"
        )

    def test_update_field_permission_denied(self, snapshot):
        interactor = self._get_interactor(permission=PermissionsEnum.ADMIN)
        update_field_data = self._get_update_dto()

        with pytest.raises(NotAccessToCreateFieldException) as exc:
            interactor.update_field(update_field_data)

        snapshot.assert_match(
            repr(exc.value.user_id),
            "test_update_field_permission_denied.txt"
        )

    def test_update_field_duplicate_name(self, snapshot):
        interactor = self._get_interactor(name_exists=True)
        update_field_data = self._get_update_dto()

        with pytest.raises(FieldNameAlreadyExistsException) as exc:
            interactor.update_field(update_field_data)

        snapshot.assert_match(
            repr(exc.value.field_name),
            "test_update_field_duplicate_name.txt"
        )

    def test_update_field_duplicate_order(self, snapshot):
        interactor = self._get_interactor(order_exists=True)
        update_field_data = self._get_update_dto()

        with pytest.raises(FieldOrderAlreadyExistsException) as exc:
            interactor.update_field(update_field_data)

        snapshot.assert_match(
            repr(exc.value.field_order),
            "test_update_field_duplicate_order.txt"
        )
