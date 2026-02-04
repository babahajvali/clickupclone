import pytest
from unittest.mock import create_autospec, patch

from task_management.interactors.list_interactors.list_interactors import \
    ListInteractor
from task_management.interactors.storage_interface.field_storage_interface import \
    FieldStorageInterface
from task_management.interactors.storage_interface.folder_storage_interface import (
    FolderStorageInterface
)
from task_management.interactors.storage_interface.list_storage_interface import (
    ListStorageInterface
)
from task_management.interactors.storage_interface.space_storage_interface import (
    SpaceStorageInterface
)
from task_management.interactors.storage_interface.space_permission_storage_interface import (
    SpacePermissionStorageInterface
)
from task_management.interactors.storage_interface.list_permission_storage_interface import (
    ListPermissionStorageInterface
)
from task_management.interactors.storage_interface.folder_permission_storage_interface import (
    FolderPermissionStorageInterface
)
from task_management.exceptions.custom_exceptions import (
    FolderNotFoundException,
    InactiveFolderException,
)
from task_management.interactors.storage_interface.template_storage_interface import \
    TemplateStorageInterface


class TestGetFolderLists:

    def setup_method(self):
        self.list_storage = create_autospec(ListStorageInterface)
        self.folder_storage = create_autospec(FolderStorageInterface)

        self.list_permission_storage = create_autospec(
            ListPermissionStorageInterface)
        self.folder_permission_storage = create_autospec(
            FolderPermissionStorageInterface)
        self.space_permission_storage = create_autospec(
            SpacePermissionStorageInterface)
        self.template_storage = create_autospec(TemplateStorageInterface)
        self.field_storage = create_autospec(FieldStorageInterface)

        self.interactor = ListInteractor(
            list_storage=self.list_storage,
            folder_storage=self.folder_storage,
            space_storage=create_autospec(SpaceStorageInterface),
            list_permission_storage=self.list_permission_storage,
            folder_permission_storage=self.folder_permission_storage,
            space_permission_storage=self.space_permission_storage,
            template_storage=self.template_storage,
            field_storage=self.field_storage
        )

    # ✅ SUCCESS
    def test_get_folder_lists_success(self, snapshot):
        self.folder_storage.get_folder.return_value = type(
            "Folder", (), {"is_active": True}
        )()

        self.list_storage.get_folder_lists.return_value = ["LIST1", "LIST2"]

        result = self.interactor.get_folder_lists("folder_1")

        snapshot.assert_match(
            repr(result),
            "get_folder_lists_success.json"
        )

    def test_folder_not_found(self, snapshot):
        with patch("django.core.cache.cache.get", return_value=None):
            self.interactor.folder_storage.get_folder.return_value = None
            with pytest.raises(FolderNotFoundException) as exc:
                self.interactor.get_folder_lists("folder_1")

        snapshot.assert_match(
            repr(exc.value),
            "folder_not_found.txt"
        )

    def test_folder_inactive(self, snapshot):
        with patch("django.core.cache.cache.get", return_value=None):
            self.interactor.folder_storage.get_folder.return_value = type(
                "Folder", (), {"is_active": False}
            )()
            with pytest.raises(InactiveFolderException) as exc:
                self.interactor.get_folder_lists("folder_1")

        snapshot.assert_match(
            repr(exc.value),
            "folder_inactive.txt"
        )
