from unittest.mock import create_autospec

import pytest
from faker import Faker

from task_management.exceptions.custom_exceptions import \
    AlreadyExistedTemplateNameException, DefaultTemplateAlreadyExistedException
from task_management.exceptions.enums import PermissionsEnum
from task_management.interactors.template_interactors.update_template_interactor import (
    UpdateTemplateInteractor
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
from task_management.tests.factories.interactor_factory import (
    UpdateTemplateDTOFactory,
    TemplateDTOFactory
)

Faker.seed(0)


class TestUpdateTemplateInteractor:

    def setup_method(self):
        self.list_storage = create_autospec(ListStorageInterface)
        self.user_storage = create_autospec(UserStorageInterface)
        self.template_storage = create_autospec(TemplateStorageInterface)
        self.permission_storage = create_autospec(PermissionStorageInterface)

        self.interactor = UpdateTemplateInteractor(
            list_storage=self.list_storage,
            user_storage=self.user_storage,
            template_storage=self.template_storage,
            permission_storage=self.permission_storage
        )


    def test_update_template_success(self, snapshot):
        update_template_dto = UpdateTemplateDTOFactory()

        updated_template = TemplateDTOFactory(
            template_id=update_template_dto.template_id,
            name=update_template_dto.name,
            list_id=update_template_dto.list_id,
            description=update_template_dto.description,
            is_default=update_template_dto.is_default,
            created_by=update_template_dto.created_by,
        )

        self.template_storage.check_template_exist.return_value = True
        self.user_storage.check_user_exists.return_value = True
        self.list_storage.check_list_exist.return_value = True
        self.template_storage.check_template_name_exist_except_this_template.return_value = False
        self.template_storage.update_template.return_value = updated_template

        self.permission_storage.get_user_access_permissions.return_value = PermissionsEnum.ADMIN

        result = self.interactor.update_template(update_template_dto)

        snapshot.assert_match(repr(result),"update_template_success.json")


    def test_update_template_template_not_found(self):
        update_template_dto = UpdateTemplateDTOFactory()

        self.template_storage.check_template_exist.side_effect = Exception(
            "Template not found"
        )

        with pytest.raises(Exception):
            self.interactor.update_template(update_template_dto)

        self.template_storage.update_template.assert_not_called()

    def test_update_template_user_not_found(self):
        update_template_dto = UpdateTemplateDTOFactory()

        self.template_storage.check_template_exist.return_value = True
        self.user_storage.check_user_exists.side_effect = Exception(
            "User not found"
        )

        with pytest.raises(Exception):
            self.interactor.update_template(update_template_dto)

        self.template_storage.update_template.assert_not_called()

    def test_update_template_list_not_found(self):
        update_template_dto = UpdateTemplateDTOFactory()

        self.template_storage.check_template_exist.return_value = True
        self.user_storage.check_user_exists.return_value = True
        self.list_storage.check_list_exist.return_value = False

        with pytest.raises(Exception):
            self.interactor.update_template(update_template_dto)

        self.template_storage.update_template.assert_not_called()

    def test_update_template_permission_denied(self):
        update_template_dto = UpdateTemplateDTOFactory()

        self.template_storage.check_template_exist.return_value = True
        self.user_storage.check_user_exists.return_value = True
        self.list_storage.check_list_exist.return_value = True

        self.permission_storage.get_user_access_permissions.return_value = PermissionsEnum.GUEST

        with pytest.raises(Exception):
            self.interactor.update_template(update_template_dto)

        self.template_storage.update_template.assert_not_called()

    def test_update_template_duplicate_name(self, snapshot):
        update_template_dto = UpdateTemplateDTOFactory()

        self.template_storage.check_template_exist.return_value = True
        self.user_storage.check_user_exists.return_value = True
        self.list_storage.check_list_exist.return_value = True

        self.permission_storage.get_user_access_permissions.return_value = PermissionsEnum.ADMIN

        self.template_storage.check_template_name_exist_except_this_template.return_value = True

        with pytest.raises(AlreadyExistedTemplateNameException) as exc:
            self.interactor.update_template(update_template_dto)

        snapshot.assert_match(repr(exc.value.template_name),"update_template_duplicate_name.txt")

    def test_update_default_template_already_exists(self, snapshot):
        update_template_dto = UpdateTemplateDTOFactory(is_default=True)

        self.template_storage.check_template_exist.return_value = True
        self.user_storage.check_user_exists.return_value = True
        self.list_storage.check_list_exist.return_value = True

        self.permission_storage.get_user_access_permissions.return_value = PermissionsEnum.ADMIN

        self.template_storage.check_template_name_exist_except_this_template.return_value = False
        self.template_storage.check_default_template_exist.return_value = True

        with pytest.raises(DefaultTemplateAlreadyExistedException) as exc:
            self.interactor.update_template(update_template_dto)

        snapshot.assert_match(repr(exc.value.template_name),"update_default_template_already_exists.txt")
