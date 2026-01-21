import pytest

from task_management.interactors.dtos import CreateTaskDTO, UpdateTaskDTO, FilterDTO
from task_management.storages.task_storage import TaskStorage
from task_management.tests.factories.storage_factory import TaskFactory, UserFactory, ListFactory, TaskAssigneeFactory, FieldValueFactory, FieldFactory, TemplateFactory


class TestTaskStorage:

    @pytest.mark.django_db
    def test_create_task_success(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        list_obj = ListFactory(list_id=list_id)
        user = UserFactory(user_id=user_id)
        task_data = CreateTaskDTO(
            title="Test Task",
            description="Test description",
            list_id=str(list_id),
            created_by=str(user_id)
        )
        storage = TaskStorage()

        # Act
        result = storage.create_task(task_data=task_data)

        # Assert
        snapshot.assert_match(repr(result), "test_create_task_success.txt")

    @pytest.mark.django_db
    def test_create_task_with_existing_tasks(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        list_obj = ListFactory(list_id=list_id)
        user = UserFactory(user_id=user_id)
        TaskFactory(list=list_obj, created_by=user, order=1, is_deleted=False)
        TaskFactory(list=list_obj, created_by=user, order=2, is_deleted=False)
        task_data = CreateTaskDTO(
            title="New Task",
            description="New description",
            list_id=str(list_id),
            created_by=str(user_id)
        )
        storage = TaskStorage()

        # Act
        result = storage.create_task(task_data=task_data)

        # Assert
        snapshot.assert_match(repr(result), "test_create_task_with_existing_tasks.txt")

    @pytest.mark.django_db
    def test_update_task_success(self, snapshot):
        # Arrange
        task_id = "12345678-1234-5678-1234-567812345678"
        list_obj = ListFactory()
        user = UserFactory()
        TaskFactory(task_id=task_id, list=list_obj, created_by=user, title="Old Title", description="Old description")
        update_task_data = UpdateTaskDTO(
            task_id=str(task_id),
            title="New Title",
            description="New description"
        )
        storage = TaskStorage()

        # Act
        result = storage.update_task(update_task_data=update_task_data)

        # Assert
        snapshot.assert_match(repr(result), "test_update_task_success.txt")

    @pytest.mark.django_db
    def test_get_task_by_id_success(self, snapshot):
        # Arrange
        task_id = "12345678-1234-5678-1234-567812345678"
        list_obj = ListFactory()
        user = UserFactory()
        TaskFactory(task_id=task_id, list=list_obj, created_by=user)
        storage = TaskStorage()

        # Act
        result = storage.get_task_by_id(task_id=str(task_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_task_by_id_success.txt")

    @pytest.mark.django_db
    def test_get_list_tasks_success(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345678"
        list_obj = ListFactory(list_id=list_id)
        user = UserFactory()
        TaskFactory(list=list_obj, created_by=user, is_deleted=False)
        TaskFactory(list=list_obj, created_by=user, is_deleted=False)
        TaskFactory(list=list_obj, created_by=user, is_deleted=True)
        storage = TaskStorage()

        # Act
        result = storage.get_list_tasks(list_id=str(list_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_list_tasks_success.txt")

    @pytest.mark.django_db
    def test_get_list_tasks_empty(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345678"
        ListFactory(list_id=list_id)
        storage = TaskStorage()

        # Act
        result = storage.get_list_tasks(list_id=str(list_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_list_tasks_empty.txt")

    @pytest.mark.django_db
    def test_remove_task_success(self, snapshot):
        # Arrange
        task_id = "12345678-1234-5678-1234-567812345678"
        list_id = "12345678-1234-5678-1234-567812345679"
        list_obj = ListFactory(list_id=list_id)
        user = UserFactory()
        TaskFactory(task_id=task_id, list=list_obj, created_by=user, order=1, is_deleted=False)
        TaskFactory(list=list_obj, created_by=user, order=2, is_deleted=False)
        TaskFactory(list=list_obj, created_by=user, order=3, is_deleted=False)
        storage = TaskStorage()

        # Act
        result = storage.remove_task(task_id=str(task_id))

        # Assert
        snapshot.assert_match(repr(result), "test_remove_task_success.txt")

    @pytest.mark.django_db
    def test_task_filter_data_no_filters(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345678"
        list_obj = ListFactory(list_id=list_id)
        user = UserFactory()
        TaskFactory(list=list_obj, created_by=user, is_deleted=False, order=1)
        TaskFactory(list=list_obj, created_by=user, is_deleted=False, order=2)
        TaskFactory(list=list_obj, created_by=user, is_deleted=True, order=3)
        filter_data = FilterDTO(
            list_id=str(list_id),
            assignees=None,
            field_filters=None,
            offset=1,
            limit=10
        )
        storage = TaskStorage()

        # Act
        result = storage.task_filter_data(filter_data=filter_data)

        # Assert
        snapshot.assert_match(repr(list(result)), "test_task_filter_data_no_filters.txt")


    @pytest.mark.django_db
    def test_task_filter_data_with_field_filters(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345678"
        field_id = "12345678-1234-5678-1234-567812345679"
        list_obj = ListFactory(list_id=list_id)
        template = TemplateFactory(list=list_obj)
        field = FieldFactory(field_id=field_id, template=template)
        user = UserFactory()
        task1 = TaskFactory(list=list_obj, created_by=user, is_deleted=False, order=1)
        task2 = TaskFactory(list=list_obj, created_by=user, is_deleted=False, order=2)
        task3 = TaskFactory(list=list_obj, created_by=user, is_deleted=False, order=3)
        FieldValueFactory(task=task1, field=field, value={"status": "in_progress"}, created_by=user)
        FieldValueFactory(task=task2, field=field, value={"status": "completed"}, created_by=user)
        filter_data = FilterDTO(
            list_id=str(list_id),
            assignees=None,
            field_filters={str(field_id): [{"status": "in_progress"}]},
            offset=1,
            limit=10
        )
        storage = TaskStorage()

        # Act
        result = storage.task_filter_data(filter_data=filter_data)

        # Assert
        snapshot.assert_match(repr(list(result)), "test_task_filter_data_with_field_filters.txt")

    @pytest.mark.django_db
    def test_get_tasks_count_success(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345678"
        list_obj = ListFactory(list_id=list_id)
        user = UserFactory()
        TaskFactory(list=list_obj, created_by=user, is_deleted=False)
        TaskFactory(list=list_obj, created_by=user, is_deleted=False)
        TaskFactory(list=list_obj, created_by=user, is_deleted=True)
        storage = TaskStorage()

        # Act
        result = storage.get_tasks_count(list_id=str(list_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_tasks_count_success.txt")

    @pytest.mark.django_db
    def test_get_tasks_count_empty(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345678"
        ListFactory(list_id=list_id)
        storage = TaskStorage()

        # Act
        result = storage.get_tasks_count(list_id=str(list_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_tasks_count_empty.txt")

    @pytest.mark.django_db
    def test_reorder_tasks_move_down_success(self, snapshot):
        # Arrange
        task_id = "12345678-1234-5678-1234-567812345678"
        list_id = "12345678-1234-5678-1234-567812345679"
        list_obj = ListFactory(list_id=list_id)
        user = UserFactory()
        TaskFactory(task_id=task_id, list=list_obj, created_by=user, order=1, is_deleted=False)
        TaskFactory(list=list_obj, created_by=user, order=2, is_deleted=False)
        TaskFactory(list=list_obj, created_by=user, order=3, is_deleted=False)
        storage = TaskStorage()

        # Act
        result = storage.reorder_tasks(list_id=str(list_id), new_order=3, task_id=str(task_id))

        # Assert
        snapshot.assert_match(repr(result), "test_reorder_tasks_move_down_success.txt")

    @pytest.mark.django_db
    def test_reorder_tasks_move_up_success(self, snapshot):
        # Arrange
        task_id = "12345678-1234-5678-1234-567812345678"
        list_id = "12345678-1234-5678-1234-567812345679"
        list_obj = ListFactory(list_id=list_id)
        user = UserFactory()
        TaskFactory(list=list_obj, created_by=user, order=1, is_deleted=False)
        TaskFactory(list=list_obj, created_by=user, order=2, is_deleted=False)
        TaskFactory(task_id=task_id, list=list_obj, created_by=user, order=3, is_deleted=False)
        storage = TaskStorage()

        # Act
        result = storage.reorder_tasks(list_id=str(list_id), new_order=1, task_id=str(task_id))

        # Assert
        snapshot.assert_match(repr(result), "test_reorder_tasks_move_up_success.txt")

    @pytest.mark.django_db
    def test_reorder_tasks_same_position(self, snapshot):
        # Arrange
        task_id = "12345678-1234-5678-1234-567812345678"
        list_id = "12345678-1234-5678-1234-567812345679"
        list_obj = ListFactory(list_id=list_id)
        user = UserFactory()
        TaskFactory(task_id=task_id, list=list_obj, created_by=user, order=2, is_deleted=False)
        storage = TaskStorage()

        # Act
        result = storage.reorder_tasks(list_id=str(list_id), new_order=2, task_id=str(task_id))

        # Assert
        snapshot.assert_match(repr(result), "test_reorder_tasks_same_position.txt")