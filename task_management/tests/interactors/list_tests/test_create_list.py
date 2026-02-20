import pytest
from unittest.mock import create_autospec, patch

from task_management.exceptions.enums import Role
from task_management.interactors.dtos import  WorkspaceMemberDTO
from task_management.interactors.lists.list_interactor import \
    ListInteractor
from task_management.exceptions.custom_exceptions import (
    ModificationNotAllowed,
    SpaceNotFound,
    InactiveSpace,
)
from task_management.interactors.storage_interfaces import \
    ListStorageInterface, FolderStorageInterface, SpaceStorageInterface, \
    WorkspaceStorageInterface

from task_management.tests.factories.interactor_factory import \
    CreateListDTOFactory




def make_permission(role: Role):
    return WorkspaceMemberDTO(
        id=1,
        workspace_id="workspace_id1",
        role=role,
        user_id="user_id",
        is_active=True,
        added_by="admin"
    )


class TestCreateList:

    def setup_method(self):
        self.list_storage = create_autospec(ListStorageInterface)
        self.folder_storage = create_autospec(FolderStorageInterface)
        self.space_storage = create_autospec(SpaceStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)

        self.interactor = ListInteractor(
            list_storage=self.list_storage,
            folder_storage=self.folder_storage,
            space_storage=self.space_storage,
            workspace_storage=self.workspace_storage
        )

    @patch(
        "task_management.interactors.lists.lists.CreateTemplateInteractor.create_template"
    )
    def test_create_list_success(self, mock_create_template, snapshot):
        mock_create_template.return_value = None

        dto = CreateListDTOFactory(folder_id="folder_123",
                                   space_id="space_123")

        self.workspace_storage.get_user_permission_for_folder.return_value = (
            make_permission(Role.MEMBER)
        )

        self.list_storage.create_list.return_value = type("List", (), {
            "list_id": "list_id",
            "created_by": "user_id",
            "space_id": "space_123", })()

        result = self.interactor.create_list(dto)

        # snapshot.assert_match(
        #     repr(result),
        #     "test_create_list_success.txt"
        # )
        self.list_storage.create_list.assert_called_once()

    def test_permission_denied(self, snapshot):
        dto = CreateListDTOFactory(folder_id=None)

        self.workspace_storage.get_workspace_member.return_value = make_permission(
            Role.GUEST
        )

        with pytest.raises(ModificationNotAllowed) as exc:
            self.interactor.create_list(dto)

        snapshot.assert_match(repr(exc.value), "permission_denied.txt")

    @patch(
        "task_management.interactors.lists.lists.CreateTemplateInteractor.create_template"
    )
    def test_space_not_found(self, mock_create_template, snapshot):
        mock_create_template.return_value = None

        dto = CreateListDTOFactory(folder_id=None)
        dto.space_id = "space_123"  # ✅ REQUIRED

        self.space_storage.get_user_permission_for_space.return_value = (
            make_permission(Role.MEMBER)
        )
        self.space_storage.get_space.return_value = None

        with pytest.raises(SpaceNotFound):
            self.interactor.create_list(dto)

    @patch(
        "task_management.interactors.lists.lists.CreateTemplateInteractor.create_template"
    )
    def test_space_inactive(self, mock_create_template, snapshot):
        mock_create_template.return_value = None

        dto = CreateListDTOFactory(folder_id=None)
        dto.space_id = "space_123"

        self.space_storage.get_user_permission_for_space.return_value = (
            make_permission(Role.MEMBER)
        )
        self.space_storage.get_space.return_value = type(
            "Space", (), {"is_active": False}
        )()

        with pytest.raises(InactiveSpace):
            self.interactor.create_list(dto)
