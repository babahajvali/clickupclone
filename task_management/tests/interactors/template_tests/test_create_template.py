from unittest.mock import create_autospec, patch

import pytest
from faker import Faker

from task_management.interactors.storage_interface.field_storage_interface import (
    FieldStorageInterface
)
from task_management.interactors.storage_interface.list_storage_interface import (
    ListStorageInterface
)
from task_management.interactors.storage_interface.permission_storage_interface import (
    PermissionStorageInterface
)
from task_management.interactors.storage_interface.template_storage_interface import (
    TemplateStorageInterface
)
from task_management.interactors.storage_interface.user_storage_interface import (
    UserStorageInterface
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
        self.user_storage = create_autospec(UserStorageInterface)
        self.field_storage = create_autospec(FieldStorageInterface)
        self.permission_storage = create_autospec(PermissionStorageInterface)
        self.template_storage = create_autospec(TemplateStorageInterface)
        self.list_storage = create_autospec(ListStorageInterface)

        self.interactor = CreateTemplateInteractor(
            user_storage=self.user_storage,
            field_storage=self.field_storage,
            permission_storage=self.permission_storage,
            template_storage=self.template_storage,
            list_storage=self.list_storage
        )

    @patch("task_management.interactors.template_interactors.create_template_interactor.CreateFieldInteractor")
    def test_create_template_success(self,mock_create_field_interactor,snapshot):
        # Arrange
        create_template_dto = CreateTemplateDTOFactory()

        template_dto = TemplateDTOFactory(
            name=create_template_dto.name,
            list_id=create_template_dto.list_id,
            description=create_template_dto.description,
            is_default=create_template_dto.is_default,
            created_by=create_template_dto.created_by,
        )

        self.template_storage.check_template_name_exist.return_value = False
        self.template_storage.create_template.return_value = template_dto

        # Act
        result = self.interactor.create_template(create_template_dto)

        # Assert
        snapshot.assert_match(repr(result),"create_template_success.json")


    def test_create_template_duplicate_name(self, snapshot):
        # Arrange
        create_template_dto = CreateTemplateDTOFactory()
        self.template_storage.check_template_name_exist.return_value = True

        # Act & Assert
        with pytest.raises(Exception) as exc:
            self.interactor.create_template(create_template_dto)

        self.template_storage.create_template.assert_not_called()

        snapshot.assert_match(repr(exc.value),"duplicate_template_name.txt")

    def test_create_default_template_already_exists(self, snapshot):
        # Arrange
        create_template_dto = CreateTemplateDTOFactory(is_default=True)

        self.template_storage.check_template_name_exist.return_value = False
        self.template_storage.check_default_template_exist.return_value = True

        # Act & Assert
        with pytest.raises(Exception) as exc:
            self.interactor.create_template(create_template_dto)

        snapshot.assert_match(repr(exc.value),"default_template_already_exists.txt")


    def test_create_template_list_not_found(self):
        # Arrange
        create_template_dto = CreateTemplateDTOFactory()
        self.list_storage.check_list_exist.return_value = False

        # Act & Assert
        with pytest.raises(Exception):
            self.interactor.create_template(create_template_dto)

        self.template_storage.create_template.assert_not_called()

    def test_create_template_permission_denied(self):
        # Arrange
        create_template_dto = CreateTemplateDTOFactory()

        self.permission_storage.get_user_access_permissions.return_value = {
            "List": type("Enum", (), {"value": "GUEST"})()
        }

        # Act & Assert
        with pytest.raises(Exception):
            self.interactor.create_template(create_template_dto)

        self.template_storage.create_template.assert_not_called()
