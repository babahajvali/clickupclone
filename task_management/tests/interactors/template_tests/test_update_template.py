from unittest.mock import create_autospec
import pytest
from faker import Faker

from task_management.exceptions.custom_exceptions import (
    TemplateNameAlreadyExistsException,
    ModificationNotAllowedException
)
from task_management.exceptions.enums import PermissionsEnum
from task_management.interactors.dtos import UserListPermissionDTO
from task_management.interactors.storage_interface.list_permission_storage_interface import (
    ListPermissionStorageInterface
)
from task_management.interactors.template_interactors.update_template_interactor import (
    UpdateTemplateInteractor
)
from task_management.interactors.storage_interface.list_storage_interface import (
    ListStorageInterface
)
from task_management.interactors.storage_interface.template_storage_interface import (
    TemplateStorageInterface
)
from task_management.tests.factories.interactor_factory import (
    UpdateTemplateDTOFactory,
    TemplateDTOFactory
)

Faker.seed(0)

def make_permission(permission_type: PermissionsEnum):
    return UserListPermissionDTO(
        id=1,
        list_id="list_id",
        permission_type=permission_type,
        user_id="user_id",
        is_active=True,
        added_by="admin"
    )

class TestUpdateTemplateInteractor:

    def setup_method(self):
        self.list_storage = create_autospec(ListStorageInterface)
        self.template_storage = create_autospec(TemplateStorageInterface)
        self.permission_storage = create_autospec(ListPermissionStorageInterface)

        self.interactor = UpdateTemplateInteractor(
            list_storage=self.list_storage,
            template_storage=self.template_storage,
            permission_storage=self.permission_storage
        )

    def _mock_active_list(self):
        return type("List", (), {"is_active": True})()

    def _mock_template(self):
        return type("Template",(),{"list_id": "list_123"})()

    def test_update_template_success(self, snapshot):
        update_dto = UpdateTemplateDTOFactory()
        list_id = "list_id1"

        updated_template = TemplateDTOFactory(
            template_id=update_dto.template_id,
            name=update_dto.name,
            list_id=list_id,
            description=update_dto.description,
        )

        self.template_storage.get_template_by_id.return_value = self._mock_template()
        self.list_storage.get_list.return_value = self._mock_active_list()
        self.permission_storage.get_user_permission_for_list.return_value = (
            make_permission(PermissionsEnum.FULL_EDIT)
        )
        self.template_storage.is_template_name_exist.return_value = False
        self.template_storage.update_template.return_value = updated_template

        result = self.interactor.update_template(update_dto,user_id="user_id")

        snapshot.assert_match(
            repr(result),
            "update_template_success.json"
        )


    def test_update_template_template_not_found(self):
        update_dto = UpdateTemplateDTOFactory()

        self.template_storage.get_template_by_id.side_effect = Exception(
            "Template not found"
        )

        with pytest.raises(Exception):
            self.interactor.update_template(update_dto,user_id="user_id")

        self.template_storage.update_template.assert_not_called()


    def test_update_template_list_not_found(self):
        update_dto = UpdateTemplateDTOFactory()

        self.template_storage.get_template_by_id.return_value = self._mock_template()
        self.list_storage.get_list.return_value = None

        with pytest.raises(Exception):
            self.interactor.update_template(update_dto,user_id="user_id")

        self.template_storage.update_template.assert_not_called()


    def test_update_template_permission_denied(self):
        update_dto = UpdateTemplateDTOFactory()

        self.template_storage.get_template_by_id.return_value = self._mock_template()
        self.list_storage.get_list.return_value = self._mock_active_list()
        self.permission_storage.get_user_permission_for_list.return_value = (
            make_permission(PermissionsEnum.VIEW)
        )
        with pytest.raises(ModificationNotAllowedException):
            self.interactor.update_template(update_dto,user_id="user_id")

        self.template_storage.update_template.assert_not_called()


    def test_update_template_duplicate_name(self, snapshot):
        update_dto = UpdateTemplateDTOFactory()

        self.template_storage.get_template_by_id.return_value = self._mock_template()
        self.list_storage.get_list.return_value = self._mock_active_list()
        self.permission_storage.get_user_permission_for_list.return_value = (
            make_permission(PermissionsEnum.FULL_EDIT)
        )
        self.template_storage.check_template_name_exist_except_this_template.return_value = True

        with pytest.raises(TemplateNameAlreadyExistsException) as exc:
            self.interactor.update_template(update_dto,user_id="user_id")

        snapshot.assert_match(
            repr(exc.value.template_name),
            "update_template_duplicate_name.txt"
        )

