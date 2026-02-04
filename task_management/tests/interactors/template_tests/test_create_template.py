from unittest.mock import create_autospec, patch

import pytest
from faker import Faker

from task_management.exceptions.enums import Permissions
from task_management.interactors.dtos import UserListPermissionDTO
from task_management.interactors.storage_interface.field_storage_interface import (
    FieldStorageInterface
)
from task_management.interactors.storage_interface.list_permission_storage_interface import \
    ListPermissionStorageInterface
from task_management.interactors.storage_interface.list_storage_interface import (
    ListStorageInterface
)
from task_management.interactors.storage_interface.template_storage_interface import (
    TemplateStorageInterface
)
from task_management.interactors.template_interactors.create_template_interactor import (
    CreateTemplateInteractor
)
from task_management.tests.factories.interactor_factory import (
    CreateTemplateDTOFactory,
    TemplateDTOFactory
)

Faker.seed(0)


class TestCreateTemplateInteractor:

    def setup_method(self):
        self.field_storage = create_autospec(FieldStorageInterface)
        self.permission_storage = create_autospec(
            ListPermissionStorageInterface)
        self.template_storage = create_autospec(TemplateStorageInterface)
        self.list_storage = create_autospec(ListStorageInterface)

        self.interactor = CreateTemplateInteractor(
            field_storage=self.field_storage,
            permission_storage=self.permission_storage,
            template_storage=self.template_storage,
            list_storage=self.list_storage
        )

    def test_create_template_success(self, snapshot):
        create_template_dto = CreateTemplateDTOFactory()

        template_dto = TemplateDTOFactory(
            name=create_template_dto.name,
            list_id=create_template_dto.list_id,
            description=create_template_dto.description,
        )

        self.list_storage.get_list.return_value = type(
            "List", (), {"is_active": True}
        )()

        self.permission_storage.get_user_permission_for_list.return_value = UserListPermissionDTO(
            id=1,
            list_id="list_id",
            permission_type=Permissions.FULL_EDIT.value,
            user_id="user_id",
            is_active=True,
            added_by="admin"
        )

        self.template_storage.create_template.return_value = template_dto

        result = self.interactor.create_template(create_template_dto)

        snapshot.assert_match(
            repr(result),
            "create_template_success.json"
        )

    def test_create_template_duplicate_name(self, snapshot):
        # Arrange
        create_template_dto = CreateTemplateDTOFactory()
        self.template_storage.is_template_name_exist.return_value = True

        # Act & Assert
        with pytest.raises(Exception) as exc:
            self.interactor.create_template(create_template_dto)

        self.template_storage.create_template.assert_not_called()

        snapshot.assert_match(repr(exc.value), "duplicate_template_name.txt")

    def test_create_template_list_not_found(self):
        # Arrange
        create_template_dto = CreateTemplateDTOFactory()

        # Act & Assert
        with pytest.raises(Exception):
            self.interactor.create_template(create_template_dto)

        self.template_storage.create_template.assert_not_called()

    def test_create_template_permission_denied(self):
        create_template_dto = CreateTemplateDTOFactory()

        self.list_storage.get_list.return_value = type(
            "List", (), {"is_active": True}
        )()

        self.permission_storage.get_user_permission_for_list.return_value = (
            Permissions.VIEW.value
        )

        with pytest.raises(Exception):
            self.interactor.create_template(create_template_dto)

        self.template_storage.create_template.assert_not_called()
