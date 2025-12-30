from enum import Enum
from unittest.mock import create_autospec

import pytest
from faker import Faker

from task_management.exceptions.custom_exceptions import (
    UserNotFoundException,
    TemplateNotFoundException,
    UnexpectedFieldTypeFoundException,
    FieldNameAlreadyExistsException,
    FieldOrderAlreadyExistsException,
    NotAccessToCreationException
)
from task_management.interactors.field_interactors.create_field_interactor import (
    CreateFieldInteractor
)
from task_management.interactors.dtos import (
    CreateFieldDTO,
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

Faker.seed(1)

class FieldEnum(Enum):
    INVALID = "Invalid"


class TestCreateFieldInteractor:

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

    def test_create_field_successfully(self, snapshot):
        # Arrange
        field_storage = create_autospec(FieldStorageInterface)
        user_storage = create_autospec(UserStorageInterface)
        template_storage = create_autospec(TemplateStorageInterface)
        permission_storage = create_autospec(PermissionStorageInterface)


        user_storage.check_user_exist.return_value = True
        template_storage.check_template_exist.return_value = True
        permission_storage.get_user_access_permissions.return_value = PermissionsEnum.ADMIN
        field_storage.check_field_name_exist.return_value = False
        field_storage.check_field_order_exist.return_value = False

        field_storage.create_field.return_value = self._get_field_dto()

        interactor = CreateFieldInteractor(
            field_storage=field_storage,
            user_storage=user_storage,
            template_storage=template_storage,
            permission_storage=permission_storage
        )

        create_field_data = CreateFieldDTO(
            field_type=FieldTypeEnum.Text,
            field_name="Priority",
            description="Task priority",
            template_id="tpl_1",
            order=1,
            config={"max_length": 10},
            is_required=True,
            created_by="user_1"
        )

        # Act
        result = interactor.create_field(create_field_data)

        # Assert
        snapshot.assert_match(
            repr(result),
            "test_create_field_successfully.txt"
        )

    def test_create_field_user_not_found(self, snapshot):
        field_storage = create_autospec(FieldStorageInterface)
        user_storage = create_autospec(UserStorageInterface)
        template_storage = create_autospec(TemplateStorageInterface)
        permission_storage = create_autospec(PermissionStorageInterface)

        user_storage.check_user_exist.return_value = False

        interactor = CreateFieldInteractor(
            field_storage=field_storage,
            user_storage=user_storage,
            template_storage=template_storage,
            permission_storage=permission_storage
        )

        create_field_data = CreateFieldDTO(
            field_type=FieldTypeEnum.Text,
            field_name="Priority",
            description="",
            template_id="tpl_1",
            order=1,
            config={},
            is_required=False,
            created_by="invalid_user"
        )

        with pytest.raises(UserNotFoundException) as exc:
            interactor.create_field(create_field_data)
        snapshot.assert_match(
            repr(exc.value.user_id),"test_create_field_user_not_found.txt"
        )

    def test_create_field_template_not_found(self, snapshot):
        field_storage = create_autospec(FieldStorageInterface)
        user_storage = create_autospec(UserStorageInterface)
        template_storage = create_autospec(TemplateStorageInterface)
        permission_storage = create_autospec(PermissionStorageInterface)

        user_storage.check_user_exist.return_value = True
        template_storage.check_template_exist.return_value = False

        interactor = CreateFieldInteractor(
            field_storage=field_storage,
            user_storage=user_storage,
            template_storage=template_storage,
            permission_storage=permission_storage
        )

        create_field_data = CreateFieldDTO(
            field_type=FieldTypeEnum.Text,
            field_name="Priority",
            description="",
            template_id="invalid_tpl",
            order=1,
            config={},
            is_required=False,
            created_by="user_1"
        )

        with pytest.raises(TemplateNotFoundException) as exc:
            interactor.create_field(create_field_data)

        snapshot.assert_match(
            repr(exc.value.template_id),
            "test_create_field_template_not_found.txt"
        )

    def test_create_field_invalid_field_type(self, snapshot):
        field_storage = create_autospec(FieldStorageInterface)
        user_storage = create_autospec(UserStorageInterface)
        template_storage = create_autospec(TemplateStorageInterface)
        permission_storage = create_autospec(PermissionStorageInterface)

        user_storage.check_user_exist.return_value = True
        template_storage.check_template_exist.return_value = True
        permission_storage.get_user_access_permissions.return_value = PermissionsEnum.ADMIN

        interactor = CreateFieldInteractor(
            field_storage=field_storage,
            user_storage=user_storage,
            template_storage=template_storage,
            permission_storage=permission_storage
        )

        create_field_data = CreateFieldDTO(
            field_type= FieldEnum.INVALID,
            field_name="Priority",
            description="",
            template_id="tpl_1",
            order=1,
            config={},
            is_required=False,
            created_by="user_1"
        )

        with pytest.raises(UnexpectedFieldTypeFoundException) as exc:
            interactor.create_field(create_field_data)

        snapshot.assert_match(
            repr(exc.value.field_type),
            "test_create_field_invalid_field_type.txt"
        )

    def test_create_field_permission_denied(self, snapshot):
        field_storage = create_autospec(FieldStorageInterface)
        user_storage = create_autospec(UserStorageInterface)
        template_storage = create_autospec(TemplateStorageInterface)
        permission_storage = create_autospec(PermissionStorageInterface)

        user_storage.check_user_exist.return_value = True
        template_storage.check_template_exist.return_value = True
        permission_storage.get_user_access_permissions.return_value = PermissionsEnum.GUEST

        interactor = CreateFieldInteractor(
            field_storage=field_storage,
            user_storage=user_storage,
            template_storage=template_storage,
            permission_storage=permission_storage
        )

        create_field_data = CreateFieldDTO(
            field_type=FieldTypeEnum.Text,
            field_name="Priority",
            description="",
            template_id="tpl_1",
            order=1,
            config={},
            is_required=False,
            created_by="user_1"
        )

        with pytest.raises(NotAccessToCreationException) as exc:
            interactor.create_field(create_field_data)

        snapshot.assert_match(
            repr(exc.value.user_id),
            "test_create_field_permission_denied.txt"
        )

    def test_create_field_duplicate_order(self, snapshot):
        # Arrange
        field_storage = create_autospec(FieldStorageInterface)
        user_storage = create_autospec(UserStorageInterface)
        template_storage = create_autospec(TemplateStorageInterface)
        permission_storage = create_autospec(PermissionStorageInterface)

        user_storage.check_user_exist.return_value = True
        template_storage.check_template_exist.return_value = True
        permission_storage.get_user_access_permissions.return_value = PermissionsEnum.ADMIN

        field_storage.check_field_name_exist.return_value = False
        field_storage.check_field_order_exist.return_value = True

        interactor = CreateFieldInteractor(
            field_storage=field_storage,
            user_storage=user_storage,
            template_storage=template_storage,
            permission_storage=permission_storage
        )

        create_field_data = CreateFieldDTO(
            field_type=FieldTypeEnum.Text,
            field_name="Priority",
            description="",
            template_id="tpl_1",
            order=1,
            config={},
            is_required=False,
            created_by="user_1"
        )

        # Act + Assert
        with pytest.raises(FieldOrderAlreadyExistsException) as exc:
            interactor.create_field(create_field_data)

        snapshot.assert_match(
            repr(exc.value.field_order),
            "test_create_field_duplicate_order.txt"
        )

    def test_create_field_duplicate_name(self, snapshot):
        # Arrange
        field_storage = create_autospec(FieldStorageInterface)
        user_storage = create_autospec(UserStorageInterface)
        template_storage = create_autospec(TemplateStorageInterface)
        permission_storage = create_autospec(PermissionStorageInterface)

        user_storage.check_user_exist.return_value = True
        template_storage.check_template_exist.return_value = True
        permission_storage.get_user_access_permissions.return_value = PermissionsEnum.ADMIN

        field_storage.check_field_name_exist.return_value = True
        field_storage.check_field_order_exist.return_value = False

        interactor = CreateFieldInteractor(
            field_storage=field_storage,
            user_storage=user_storage,
            template_storage=template_storage,
            permission_storage=permission_storage
        )

        create_field_data = CreateFieldDTO(
            field_type=FieldTypeEnum.Text,
            field_name="Priority",
            description="",
            template_id="tpl_1",
            order=1,
            config={},
            is_required=False,
            created_by="user_1"
        )

        # Act + Assert
        with pytest.raises(FieldNameAlreadyExistsException) as exc:
            interactor.create_field(create_field_data)

        snapshot.assert_match(
            repr(exc.value.field_name),
            "test_create_field_duplicate_name.txt"
        )



