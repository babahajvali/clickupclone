import pytest
from factory.random import reseed_random
from freezegun import freeze_time

from task_management.exceptions.enums import FieldType
from task_management.interactors.dtos import CreateFieldDTO, UpdateFieldDTO
from task_management.storages.field_storage import FieldStorage
from task_management.tests.factories.storage_factory import FieldFactory, \
    TemplateFactory, UserFactory, ListFactory
from task_management.models import Field


@freeze_time("2024-01-15 10:00:00")
class TestFieldStorage:
    @pytest.fixture(autouse=True)
    def setup(self):
        """Reset faker seed before each test"""
        reseed_random(12345)
        yield

    @pytest.mark.django_db
    def test_create_field_success(self, snapshot):
        # Arrange
        template_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        list_id = "12345678-1234-5678-1234-567812345680"

        list_obj = ListFactory(list_id=list_id)
        template = TemplateFactory(template_id=template_id, list=list_obj)
        user = UserFactory(user_id=user_id)
        create_field_data = CreateFieldDTO(
            field_name="Test Field",
            description="Test description",
            field_type=FieldType.TEXT,
            template_id=str(template_id),
            config={},
            is_required=False,
            created_by_user_id=str(user_id)
        )
        storage = FieldStorage()

        # Act
        result = storage.create_field(create_field_data=create_field_data)

        # Assert
        assert result.field_name == create_field_data.field_name

    @pytest.mark.django_db
    def test_create_field_with_existing_fields(self, snapshot):
        # Arrange
        template_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        list_id = "12345678-1234-5678-1234-567812345680"
        field1_id = "12345678-1234-5678-1234-567812345681"
        field2_id = "12345678-1234-5678-1234-567812345682"

        list_obj = ListFactory(list_id=list_id)
        template = TemplateFactory(template_id=template_id, list=list_obj)
        user = UserFactory(user_id=user_id)
        FieldFactory(field_id=field1_id, template=template, order=1,
                     created_by=user)
        FieldFactory(field_id=field2_id, template=template, order=2,
                     created_by=user)
        create_field_data = CreateFieldDTO(
            field_name="New Field",
            description="New fields description",
            field_type=FieldType.NUMBER,
            template_id=str(template_id),
            config={},
            is_required=True,
            created_by_user_id=str(user_id)
        )
        storage = FieldStorage()

        # Act
        result = storage.create_field(create_field_data=create_field_data)

        # Assert
        assert result.field_name == create_field_data.field_name

    @pytest.mark.django_db
    def test_is_field_name_exists_success(self, snapshot):
        # Arrange
        template_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        list_id = "12345678-1234-5678-1234-567812345680"
        field_id = "12345678-1234-5678-1234-567812345681"
        field_name = "Existing Field"

        list_obj = ListFactory(list_id=list_id)
        template = TemplateFactory(template_id=template_id, list=list_obj)
        user = UserFactory(user_id=user_id)
        FieldFactory(field_id=field_id, template=template,
                     field_name=field_name, created_by=user)
        storage = FieldStorage()

        # Act
        result = storage.is_field_name_exists(field_name=field_name,
                                              template_id=str(template_id))

        # Assert
        snapshot.assert_match(repr(result),
                              "test_is_field_name_exists_success.txt")

    @pytest.mark.django_db
    def test_is_field_name_exists_failure(self, snapshot):
        # Arrange
        template_id = "12345678-1234-5678-1234-567812345678"
        list_id = "12345678-1234-5678-1234-567812345679"
        field_name = "Non Existing Field"

        list_obj = ListFactory(list_id=list_id)
        TemplateFactory(template_id=template_id, list=list_obj)
        storage = FieldStorage()

        # Act
        result = storage.is_field_name_exists(field_name=field_name,
                                              template_id=str(template_id))

        # Assert
        snapshot.assert_match(repr(result),
                              "test_is_field_name_exists_failure.txt")

    @pytest.mark.django_db
    def test_get_field_by_id_success(self, snapshot):
        # Arrange
        field_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        list_id = "12345678-1234-5678-1234-567812345680"
        template_id = "12345678-1234-5678-1234-567812345681"

        list_obj = ListFactory(list_id=list_id)
        template = TemplateFactory(template_id=template_id, list=list_obj)
        user = UserFactory(user_id=user_id)
        FieldFactory(field_id=field_id, template=template, created_by=user)
        storage = FieldStorage()

        # Act
        result = storage.get_field_by_id(field_id=str(field_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_field_by_id_success.txt")

    @pytest.mark.django_db
    def test_get_field_by_id_failure(self, snapshot):
        # Arrange
        field_id = "12345678-1234-5678-1234-567812345678"
        storage = FieldStorage()

        # Act
        result = storage.get_field_by_id(field_id=str(field_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_field_by_id_failure.txt")

    @pytest.mark.django_db
    def test_update_field_success(self, snapshot):
        # Arrange
        field_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        list_id = "12345678-1234-5678-1234-567812345680"
        template_id = "12345678-1234-5678-1234-567812345681"

        list_obj = ListFactory(list_id=list_id)
        template = TemplateFactory(template_id=template_id, list=list_obj)
        user = UserFactory(user_id=user_id)
        FieldFactory(
            field_id=field_id,
            template=template,
            created_by=user,
            field_name="Old Name",
            description="Old description"
        )
        update_field_data = UpdateFieldDTO(
            field_id=str(field_id),
            field_name="New Name",
            description="New description",
            is_required=True,
            config={"key": "value"}
        )
        storage = FieldStorage()

        # Act
        result = storage.update_field(field_id=field_id,
                                      update_field_data=update_field_data)

        # Assert
        snapshot.assert_match(repr(result), "test_update_field_success.txt")

    @pytest.mark.django_db
    def test_is_field_exists_success(self, snapshot):
        # Arrange
        field_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        list_id = "12345678-1234-5678-1234-567812345680"
        template_id = "12345678-1234-5678-1234-567812345681"

        list_obj = ListFactory(list_id=list_id)
        template = TemplateFactory(template_id=template_id, list=list_obj)
        user = UserFactory(user_id=user_id)
        FieldFactory(field_id=field_id, template=template, created_by=user)
        storage = FieldStorage()

        # Act
        result = storage.is_field_exists(field_id=str(field_id))

        # Assert
        snapshot.assert_match(repr(result), "test_is_field_exists_success.txt")

    @pytest.mark.django_db
    def test_is_field_exists_failure(self, snapshot):
        # Arrange
        field_id = "12345678-1234-5678-1234-567812345678"
        storage = FieldStorage()

        # Act
        result = storage.is_field_exists(field_id=str(field_id))

        # Assert
        snapshot.assert_match(repr(result), "test_is_field_exists_failure.txt")

    @pytest.mark.django_db
    def test_check_field_name_except_this_field_success(self, snapshot):
        # Arrange
        field_id = "12345678-1234-5678-1234-567812345678"
        other_field_id = "12345678-1234-5678-1234-567812345679"
        template_id = "12345678-1234-5678-1234-567812345680"
        user_id = "12345678-1234-5678-1234-567812345681"
        list_id = "12345678-1234-5678-1234-567812345682"
        field_name = "Test Field"

        list_obj = ListFactory(list_id=list_id)
        template = TemplateFactory(template_id=template_id, list=list_obj)
        user = UserFactory(user_id=user_id)
        FieldFactory(field_id=field_id, template=template, created_by=user,
                     field_name="Current Field")
        FieldFactory(field_id=other_field_id, template=template,
                     created_by=user, field_name=field_name)
        storage = FieldStorage()

        # Act
        result = storage.check_field_name_except_this_field(
            field_id=str(field_id),
            field_name=field_name,
            template_id=str(template_id)
        )

        # Assert
        snapshot.assert_match(repr(result),
                              "test_check_field_name_except_this_field_success.txt")

    @pytest.mark.django_db
    def test_check_field_name_except_this_field_failure(self, snapshot):
        # Arrange
        field_id = "12345678-1234-5678-1234-567812345678"
        template_id = "12345678-1234-5678-1234-567812345680"
        user_id = "12345678-1234-5678-1234-567812345681"
        list_id = "12345678-1234-5678-1234-567812345682"
        field_name = "Unique Field"

        list_obj = ListFactory(list_id=list_id)
        template = TemplateFactory(template_id=template_id, list=list_obj)
        user = UserFactory(user_id=user_id)
        FieldFactory(field_id=field_id, template=template, created_by=user,
                     field_name="Current Field")
        storage = FieldStorage()

        # Act
        result = storage.check_field_name_except_this_field(
            field_id=str(field_id),
            field_name=field_name,
            template_id=str(template_id)
        )

        # Assert
        snapshot.assert_match(repr(result),
                              "test_check_field_name_except_this_field_failure.txt")

    @pytest.mark.django_db
    def test_get_fields_for_template_success(self, snapshot):
        # Arrange
        template_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        list_id = "12345678-1234-5678-1234-567812345680"
        field1_id = "12345678-1234-5678-1234-567812345681"
        field2_id = "12345678-1234-5678-1234-567812345682"
        field3_id = "12345678-1234-5678-1234-567812345683"

        list_obj = ListFactory(list_id=list_id)
        template = TemplateFactory(template_id=template_id, list=list_obj)
        user = UserFactory(user_id=user_id)
        FieldFactory(field_id=field1_id, template=template, created_by=user,
                     is_active=True, order=1)
        FieldFactory(field_id=field2_id, template=template, created_by=user,
                     is_active=True, order=2)
        FieldFactory(field_id=field3_id, template=template, created_by=user,
                     is_active=False, order=3)
        storage = FieldStorage()

        # Act
        result = storage.get_active_fields_for_template(
            template_id=str(template_id))

        # Assert
        snapshot.assert_match(repr(result),
                              "test_get_fields_for_template_success.txt")

    @pytest.mark.django_db
    def test_get_fields_for_template_empty(self, snapshot):
        # Arrange
        template_id = "12345678-1234-5678-1234-567812345678"
        list_id = "12345678-1234-5678-1234-567812345679"

        list_obj = ListFactory(list_id=list_id)
        TemplateFactory(template_id=template_id, list=list_obj)
        storage = FieldStorage()

        # Act
        result = storage.get_active_fields_for_template(
            template_id=str(template_id))

        # Assert
        snapshot.assert_match(repr(result),
                              "test_get_fields_for_template_empty.txt")

    @pytest.mark.django_db
    def test_reorder_fields_move_down_success(self, snapshot):
        # Arrange
        template_id = "12345678-1234-5678-1234-567812345678"
        field_id = "12345678-1234-5678-1234-567812345679"
        user_id = "12345678-1234-5678-1234-567812345680"
        list_id = "12345678-1234-5678-1234-567812345681"
        field2_id = "12345678-1234-5678-1234-567812345682"
        field3_id = "12345678-1234-5678-1234-567812345683"

        list_obj = ListFactory(list_id=list_id)
        template = TemplateFactory(template_id=template_id, list=list_obj)
        user = UserFactory(user_id=user_id)
        FieldFactory(field_id=field_id, template=template, created_by=user,
                     order=1)
        FieldFactory(field_id=field2_id, template=template, created_by=user,
                     order=2)
        FieldFactory(field_id=field3_id, template=template, created_by=user,
                     order=3)
        storage = FieldStorage()

        # Act
        result = storage.reorder_fields(field_id=str(field_id),
                                        template_id=str(template_id),
                                        new_order=3)

        # Assert
        snapshot.assert_match(repr(result),
                              "test_reorder_fields_move_down_success.txt")

    @pytest.mark.django_db
    def test_reorder_fields_move_up_success(self, snapshot):
        # Arrange
        template_id = "12345678-1234-5678-1234-567812345678"
        field_id = "12345678-1234-5678-1234-567812345679"
        user_id = "12345678-1234-5678-1234-567812345680"
        list_id = "12345678-1234-5678-1234-567812345681"
        field1_id = "12345678-1234-5678-1234-567812345682"
        field2_id = "12345678-1234-5678-1234-567812345683"

        list_obj = ListFactory(list_id=list_id)
        template = TemplateFactory(template_id=template_id, list=list_obj)
        user = UserFactory(user_id=user_id)
        FieldFactory(field_id=field1_id, template=template, created_by=user,
                     order=1)
        FieldFactory(field_id=field2_id, template=template, created_by=user,
                     order=2)
        FieldFactory(field_id=field_id, template=template, created_by=user,
                     order=3)
        storage = FieldStorage()

        # Act
        result = storage.reorder_fields(field_id=str(field_id),
                                        template_id=str(template_id),
                                        new_order=1)

        # Assert
        snapshot.assert_match(repr(result),
                              "test_reorder_fields_move_up_success.txt")

    @pytest.mark.django_db
    def test_reorder_fields_same_position(self, snapshot):
        # Arrange
        template_id = "12345678-1234-5678-1234-567812345678"
        field_id = "12345678-1234-5678-1234-567812345679"
        user_id = "12345678-1234-5678-1234-567812345680"
        list_id = "12345678-1234-5678-1234-567812345681"

        list_obj = ListFactory(list_id=list_id)
        template = TemplateFactory(template_id=template_id, list=list_obj)
        user = UserFactory(user_id=user_id)
        FieldFactory(field_id=field_id, template=template, created_by=user,
                     order=2)
        storage = FieldStorage()

        # Act
        result = storage.reorder_fields(field_id=str(field_id),
                                        template_id=str(template_id),
                                        new_order=2)

        # Assert
        snapshot.assert_match(repr(result),
                              "test_reorder_fields_same_position.txt")

    @pytest.mark.django_db
    def test_template_fields_count_success(self, snapshot):
        # Arrange
        template_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        list_id = "12345678-1234-5678-1234-567812345680"
        field1_id = "12345678-1234-5678-1234-567812345681"
        field2_id = "12345678-1234-5678-1234-567812345682"
        field3_id = "12345678-1234-5678-1234-567812345683"

        list_obj = ListFactory(list_id=list_id)
        template = TemplateFactory(template_id=template_id, list=list_obj)
        user = UserFactory(user_id=user_id)
        FieldFactory(field_id=field1_id, template=template, created_by=user,
                     is_active=True)
        FieldFactory(field_id=field2_id, template=template, created_by=user,
                     is_active=True)
        FieldFactory(field_id=field3_id, template=template, created_by=user,
                     is_active=False)
        storage = FieldStorage()

        # Act
        result = storage.template_fields_count(template_id=str(template_id))

        # Assert
        snapshot.assert_match(repr(result),
                              "test_template_fields_count_success.txt")

    @pytest.mark.django_db
    def test_template_fields_count_empty(self, snapshot):
        # Arrange
        template_id = "12345678-1234-5678-1234-567812345678"
        list_id = "12345678-1234-5678-1234-567812345679"

        list_obj = ListFactory(list_id=list_id)
        TemplateFactory(template_id=template_id, list=list_obj)
        storage = FieldStorage()

        # Act
        result = storage.template_fields_count(template_id=str(template_id))

        # Assert
        snapshot.assert_match(repr(result),
                              "test_template_fields_count_empty.txt")

    @pytest.mark.django_db
    def test_delete_field_success(self, snapshot):
        # Arrange
        field_id = "12345678-1234-5678-1234-567812345678"
        template_id = "12345678-1234-5678-1234-567812345679"
        user_id = "12345678-1234-5678-1234-567812345680"
        list_id = "12345678-1234-5678-1234-567812345681"
        field2_id = "12345678-1234-5678-1234-567812345682"
        field3_id = "12345678-1234-5678-1234-567812345683"

        list_obj = ListFactory(list_id=list_id)
        template = TemplateFactory(template_id=template_id, list=list_obj)
        user = UserFactory(user_id=user_id)
        FieldFactory(field_id=field_id, template=template, created_by=user,
                     order=1, is_active=True)
        FieldFactory(field_id=field2_id, template=template, created_by=user,
                     order=2, is_active=True)
        FieldFactory(field_id=field3_id, template=template, created_by=user,
                     order=3, is_active=True)
        storage = FieldStorage()

        # Act
        result = storage.delete_field(field_id=str(field_id))

        # Assert
        snapshot.assert_match(repr(result), "test_delete_field_success.txt")
