import pytest

from task_management.interactors.dtos import CreateTemplateDTO
from task_management.storages.template_storage import TemplateStorage
from task_management.tests.factories.storage_factory import (
    TemplateFactory,
    ListFactory,
    UserFactory,
    WorkspaceFactory,
    SpaceFactory,
    FolderFactory
)
class TestTemplateStorage:

    @pytest.mark.django_db
    def test_get_template_by_id_success(self, snapshot):
        # Arrange
        user_id = "12345678-1234-5678-1234-567812345678"
        workspace_id = "12345678-1234-5678-1234-567812345679"
        user = UserFactory(user_id=user_id)
        workspace = WorkspaceFactory(created_by=user,workspace_id=workspace_id)
        space_id = "12345678-1234-5678-1234-567812345680"
        folder_id = "12345678-1234-5678-1234-567812345681"
        list_id = "12345678-1234-5678-1234-567812345682"
        template_id = "12345678-1234-5678-1234-567812345683"
        space = SpaceFactory(space_id=space_id,workspace=workspace, created_by=user)
        folder = FolderFactory(folder_id=folder_id,space=space, created_by=user)
        list_obj = ListFactory(list_id=list_id,space=space, folder=folder, created_by=user)
        template = TemplateFactory(list=list_obj,template_id=template_id)

        storage = TemplateStorage()

        # Act
        result = storage.get_template_by_id(
            template_id=str(template.template_id)
        )

        # Assert
        snapshot.assert_match(
            repr(result),
            "test_get_template_by_id_success.txt"
        )

    @pytest.mark.django_db
    def test_create_template(self, snapshot):
        # Arrange
        user_id = "12345678-1234-5678-1234-567812345678"
        workspace_id = "12345678-1234-5678-1234-567812345679"
        user = UserFactory(user_id=user_id)
        workspace = WorkspaceFactory(created_by=user,
                                     workspace_id=workspace_id)
        space_id = "12345678-1234-5678-1234-567812345680"
        folder_id = "12345678-1234-5678-1234-567812345681"
        list_id = "12345678-1234-5678-1234-567812345682"
        space = SpaceFactory(space_id=space_id, workspace=workspace,
                             created_by=user)
        folder = FolderFactory(folder_id=folder_id, space=space,
                               created_by=user)
        list_obj = ListFactory(list_id=list_id, space=space, folder=folder,
                               created_by=user)

        dto = CreateTemplateDTO(
            name="Bug Template",
            description="Bug tasks templates",
            list_id=str(list_obj.list_id),
            created_by=list_obj.created_by
        )

        storage = TemplateStorage()

        # Act
        result = storage.create_template(template_data=dto)

        # Assert
        # snapshot.assert_match(
        #     repr(result),
        #     "test_create_template.txt"
        # )
        assert result.name == dto.name

    @pytest.mark.django_db
    def test_check_template_name_exist_except_this_template_true(self):
        # Arrange
        template1 = TemplateFactory(name="Template One")
        template2 = TemplateFactory(name="Template Two")
        storage = TemplateStorage()

        # Act & Assert
        assert storage.check_template_name_exist_except_this_template(
            template_name="Template One",
            template_id=str(template2.template_id)
        ) is True

    @pytest.mark.django_db
    def test_check_template_name_exist_except_this_template_false(self):
        # Arrange
        template = TemplateFactory(name="Only Template")
        storage = TemplateStorage()

        # Act & Assert
        assert storage.check_template_name_exist_except_this_template(
            template_name="Only Template",
            template_id=str(template.template_id)
        ) is False

    @pytest.mark.django_db
    def test_update_template(self, snapshot):
        # Arrange
        user_id = "12345678-1234-5678-1234-567812345678"
        workspace_id = "12345678-1234-5678-1234-567812345679"
        user = UserFactory(user_id=user_id)
        workspace = WorkspaceFactory(created_by=user,
                                     workspace_id=workspace_id)
        space_id = "12345678-1234-5678-1234-567812345680"
        folder_id = "12345678-1234-5678-1234-567812345681"
        list_id = "12345678-1234-5678-1234-567812345682"
        template_id = "12345678-1234-5678-1234-567812345683"
        space = SpaceFactory(space_id=space_id, workspace=workspace,
                             created_by=user)
        folder = FolderFactory(folder_id=folder_id, space=space,
                               created_by=user)
        list_obj = ListFactory(list_id=list_id, space=space, folder=folder,
                               created_by=user)

        template = TemplateFactory(
            template_id=template_id,
            list=list_obj,
            name="Old Template",
            description="Old description"
        )

        name="Updated Template",
        description="Updated description"


        storage = TemplateStorage()

        # Act
        result = storage.update_template(template_id=template_id, field_properties={"name": name, 'description': description})

        # Assert
        snapshot.assert_match(
            repr(result),
            "test_update_template.txt"
        )
