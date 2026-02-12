import pytest
from unittest.mock import create_autospec

from task_management.exceptions.enums import  Visibility, Role
from task_management.interactors.dtos import WorkspaceMemberDTO
from task_management.interactors.list.list_interactor import \
    ListInteractor
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface
from task_management.interactors.storage_interfaces.field_storage_interface import \
    FieldStorageInterface
from task_management.interactors.storage_interfaces.list_storage_interface import \
    ListStorageInterface
from task_management.interactors.storage_interfaces.folder_storage_interface import \
    FolderStorageInterface
from task_management.interactors.storage_interfaces.space_storage_interface import \
    SpaceStorageInterface

from task_management.interactors.storage_interfaces.list_permission_storage_interface import \
    ListPermissionStorageInterface

from task_management.exceptions.custom_exceptions import (
    ModificationNotAllowedException,
    ListNotFoundException,
    InactiveListException,
)
from task_management.interactors.storage_interfaces.template_storage_interface import \
    TemplateStorageInterface


def make_permission(role: Role):
    return WorkspaceMemberDTO(
        id=1,
        workspace_id="workspace_id1",
        role=role,
        user_id="user_id",
        is_active=True,
        added_by="admin"
    )


class TestSetListPrivate:

    def setup_method(self):
        self.list_storage = create_autospec(ListStorageInterface)
        self.folder_storage = create_autospec(FolderStorageInterface)

        self.list_permission_storage = create_autospec(
            ListPermissionStorageInterface)
        self.template_storage = create_autospec(TemplateStorageInterface)
        self.field_storage = create_autospec(FieldStorageInterface)
       
        self.space_storage = create_autospec(SpaceStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)

        self.interactor = ListInteractor(
            list_storage=self.list_storage,
            folder_storage=self.folder_storage,
            space_storage=self.space_storage,
            
            workspace_storage=self.workspace_storage,
        )

    def test_set_list_private_success(self, snapshot):
        self.workspace_storage.get_workspace_member.return_value = (
            make_permission(Role.MEMBER)
        )
        self.interactor.list_storage.get_list.return_value = type(
            "List", (), {"is_active": True}
        )()

        result = self.interactor.set_list_visibility("list_1",
                                                     user_id="user_1",
                                                     visibility=Visibility.PRIVATE)

        self.interactor.list_storage.make_list_private.assert_called_once_with(
            "list_1")

    def test_permission_denied(self, snapshot):
        self.workspace_storage.get_workspace_member.return_value = (
            make_permission(Role.GUEST)
        )

        with pytest.raises(ModificationNotAllowedException) as exc:
            self.interactor.set_list_visibility("list_1", user_id="user_1",
                                                visibility=Visibility.PRIVATE)

        snapshot.assert_match(repr(exc.value), "permission_denied.txt")

    def test_list_not_found(self, snapshot):
        self.workspace_storage.get_workspace_member.return_value = (
            make_permission(Role.MEMBER)
        )
        self.interactor.list_storage.get_list.return_value = None

        with pytest.raises(ListNotFoundException) as exc:
            self.interactor.set_list_visibility("list_1", user_id="user_1",
                                                visibility=Visibility.PRIVATE)

        snapshot.assert_match(repr(exc.value), "list_not_found.txt")

    def test_list_inactive(self, snapshot):
        self.workspace_storage.get_workspace_member.return_value = (
            make_permission(Role.MEMBER)
        )
        self.interactor.list_storage.get_list.return_value = type(
            "List", (), {"is_active": False}
        )()

        with pytest.raises(InactiveListException) as exc:
            self.interactor.set_list_visibility("list_1", user_id="user_1",
                                                visibility=Visibility.PRIVATE)

        snapshot.assert_match(repr(exc.value), "list_inactive.txt")
