import pytest

from task_management.interactors.dtos import UpdateFieldValueDTO, CreateFieldValueDTO
from task_management.storages.field_value_storage import FieldValueStorage
from task_management.tests.factories.storage_factory import FieldValueFactory, TaskFactory, FieldFactory, UserFactory, TemplateFactory, ListFactory


class TestFieldValueStorage:

    @pytest.mark.django_db
    def test_set_task_field_value_success(self, snapshot):
        # Arrange
        task_id = "12345678-1234-5678-1234-567812345678"
        field_id = "12345678-1234-5678-1234-567812345679"
        list_obj = ListFactory()
        template = TemplateFactory(list=list_obj)
        user = UserFactory()
        task = TaskFactory(task_id=task_id, list=list_obj, created_by=user)
        field = FieldFactory(field_id=field_id, template=template, created_by=user)
        FieldValueFactory(task=task, field=field, value={"text": "old value"}, created_by=user)
        field_value_data = UpdateFieldValueDTO(
            task_id=str(task_id),
            field_id=str(field_id),
            value={"text": "new value"}
        )
        storage = FieldValueStorage()

        # Act
        result = storage.set_task_field_value(field_value_data=field_value_data)

        # Assert
        snapshot.assert_match(repr(result), "test_set_task_field_value_success.txt")

    @pytest.mark.django_db
    def test_get_field_values_by_task_ids_success(self, snapshot):
        # Arrange
        task_id_1 = "12345678-1234-5678-1234-567812345678"
        task_id_2 = "12345678-1234-5678-1234-567812345679"
        field_id_1 = "12345678-1234-5678-1234-567812345680"
        field_id_2 = "12345678-1234-5678-1234-567812345681"
        list_obj = ListFactory()
        template = TemplateFactory(list=list_obj)
        user = UserFactory()
        task_1 = TaskFactory(task_id=task_id_1, list=list_obj, created_by=user)
        task_2 = TaskFactory(task_id=task_id_2, list=list_obj, created_by=user)
        field_1 = FieldFactory(field_id=field_id_1, template=template, created_by=user)
        field_2 = FieldFactory(field_id=field_id_2, template=template, created_by=user)
        FieldValueFactory(task=task_1, field=field_1, value={"text": "value1"}, created_by=user)
        FieldValueFactory(task=task_1, field=field_2, value={"text": "value2"}, created_by=user)
        FieldValueFactory(task=task_2, field=field_1, value={"text": "value3"}, created_by=user)
        task_ids = [str(task_id_1), str(task_id_2)]
        storage = FieldValueStorage()

        # Act
        result = storage.get_field_values_by_task_ids(task_ids=task_ids)

        # Assert
        snapshot.assert_match(repr(result), "test_get_field_values_by_task_ids_success.txt")

    @pytest.mark.django_db
    def test_get_field_values_by_task_ids_empty(self, snapshot):
        # Arrange
        task_id = "12345678-1234-5678-1234-567812345678"
        list_obj = ListFactory()
        user = UserFactory()
        TaskFactory(task_id=task_id, list=list_obj, created_by=user)
        task_ids = [str(task_id)]
        storage = FieldValueStorage()

        # Act
        result = storage.get_field_values_by_task_ids(task_ids=task_ids)

        # Assert
        snapshot.assert_match(repr(result), "test_get_field_values_by_task_ids_empty.txt")

    @pytest.mark.django_db
    def test_create_bulk_field_values_success(self, snapshot):
        # Arrange
        task_id_1 = "12345678-1234-5678-1234-567812345678"
        task_id_2 = "12345678-1234-5678-1234-567812345679"
        field_id_1 = "12345678-1234-5678-1234-567812345680"
        field_id_2 = "12345678-1234-5678-1234-567812345681"
        user_id = "12345678-1234-5678-1234-567812345682"
        list_obj = ListFactory()
        template = TemplateFactory(list=list_obj)
        user = UserFactory(user_id=user_id)
        task_1 = TaskFactory(task_id=task_id_1, list=list_obj, created_by=user)
        task_2 = TaskFactory(task_id=task_id_2, list=list_obj, created_by=user)
        field_1 = FieldFactory(field_id=field_id_1, template=template, created_by=user)
        field_2 = FieldFactory(field_id=field_id_2, template=template, created_by=user)
        bulk_field_values = [
            CreateFieldValueDTO(
                task_id=str(task_id_1),
                field_id=str(field_id_1),
                value={"text": "value1"},
                created_by=str(user_id)
            ),
            CreateFieldValueDTO(
                task_id=str(task_id_1),
                field_id=str(field_id_2),
                value={"text": "value2"},
                created_by=str(user_id)
            ),
            CreateFieldValueDTO(
                task_id=str(task_id_2),
                field_id=str(field_id_1),
                value={"text": "value3"},
                created_by=str(user_id)
            )
        ]
        storage = FieldValueStorage()

        # Act
        storage.create_bulk_field_values(
            create_bulk_field_values=bulk_field_values)

        # Assert
        from task_management.models import FieldValue
        result = FieldValue.objects.filter(task_id__in=[task_id_1, task_id_2]).count()
        snapshot.assert_match(repr(result), "test_create_bulk_field_values_success.txt")

    @pytest.mark.django_db
    def test_create_bulk_field_values_single_record(self, snapshot):
        # Arrange
        task_id = "12345678-1234-5678-1234-567812345678"
        field_id = "12345678-1234-5678-1234-567812345680"
        user_id = "12345678-1234-5678-1234-567812345682"
        list_obj = ListFactory()
        template = TemplateFactory(list=list_obj)
        user = UserFactory(user_id=user_id)
        task = TaskFactory(task_id=task_id, list=list_obj, created_by=user)
        field = FieldFactory(field_id=field_id, template=template, created_by=user)
        bulk_field_values = [
            CreateFieldValueDTO(
                task_id=str(task_id),
                field_id=str(field_id),
                value={"text": "single value"},
                created_by=str(user_id)
            )
        ]
        storage = FieldValueStorage()

        # Act
        storage.create_bulk_field_values(
            create_bulk_field_values=bulk_field_values)

        # Assert
        from task_management.models import FieldValue
        result = FieldValue.objects.filter(task_id=task_id).count()
        snapshot.assert_match(repr(result), "test_create_bulk_field_values_single_record.txt")