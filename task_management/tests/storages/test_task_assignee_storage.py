import pytest
from datetime import date, timedelta
from django.utils import timezone

from task_management.storages.task_assignee_storage import TaskAssigneeStorage
from task_management.tests.factories.storage_factory import TaskAssigneeFactory, TaskFactory, UserFactory, ListFactory


class TestTaskAssigneeStorage:

    @pytest.mark.django_db
    def test_assign_task_assignee_success(self, snapshot):
        # Arrange
        task_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        assigned_by_id = "12345678-1234-5678-1234-567812345680"
        list_obj = ListFactory()
        user = UserFactory(user_id=user_id)
        assigned_by = UserFactory(user_id=assigned_by_id)
        task = TaskFactory(task_id=task_id, list=list_obj, created_by=user)
        storage = TaskAssigneeStorage()

        # Act
        result = storage.assign_task_assignee(task_id=str(task_id), user_id=str(user_id), assigned_by=str(assigned_by_id))

        # Assert
        snapshot.assert_match(repr(result), "test_assign_task_assignee_success.txt")

    @pytest.mark.django_db
    def test_remove_task_assignee_success(self, snapshot):
        # Arrange
        assign_id = "12345678-1234-5678-1234-567812345678"
        list_obj = ListFactory()
        user = UserFactory()
        assigned_by = UserFactory()
        task = TaskFactory(list=list_obj, created_by=user)
        TaskAssigneeFactory(assign_id=assign_id, task=task, user=user, assigned_by=assigned_by, is_active=True)
        storage = TaskAssigneeStorage()

        # Act
        result = storage.remove_task_assignee(assign_id=str(assign_id))

        # Assert
        snapshot.assert_match(repr(result), "test_remove_task_assignee_success.txt")

    @pytest.mark.django_db
    def test_get_task_assignee_success(self, snapshot):
        # Arrange
        assign_id = "12345678-1234-5678-1234-567812345678"
        list_obj = ListFactory()
        user = UserFactory()
        assigned_by = UserFactory()
        task = TaskFactory(list=list_obj, created_by=user)
        TaskAssigneeFactory(assign_id=assign_id, task=task, user=user, assigned_by=assigned_by)
        storage = TaskAssigneeStorage()

        # Act
        result = storage.get_task_assignee(assign_id=str(assign_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_task_assignee_success.txt")

    @pytest.mark.django_db
    def test_get_task_assignees_success(self, snapshot):
        # Arrange
        task_id = "12345678-1234-5678-1234-567812345678"
        list_obj = ListFactory()
        user1 = UserFactory()
        user2 = UserFactory()
        assigned_by = UserFactory()
        task = TaskFactory(task_id=task_id, list=list_obj, created_by=user1)
        TaskAssigneeFactory(task=task, user=user1, assigned_by=assigned_by)
        TaskAssigneeFactory(task=task, user=user2, assigned_by=assigned_by)
        storage = TaskAssigneeStorage()

        # Act
        result = storage.get_task_assignees(task_id=str(task_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_task_assignees_success.txt")

    @pytest.mark.django_db
    def test_get_task_assignees_empty(self, snapshot):
        # Arrange
        task_id = "12345678-1234-5678-1234-567812345678"
        list_obj = ListFactory()
        user = UserFactory()
        TaskFactory(task_id=task_id, list=list_obj, created_by=user)
        storage = TaskAssigneeStorage()

        # Act
        result = storage.get_task_assignees(task_id=str(task_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_task_assignees_empty.txt")

    @pytest.mark.django_db
    def test_get_user_assigned_tasks_success(self, snapshot):
        # Arrange
        user_id = "12345678-1234-5678-1234-567812345678"
        list_obj = ListFactory()
        user = UserFactory(user_id=user_id)
        assigned_by = UserFactory()
        task1 = TaskFactory(list=list_obj, created_by=user, is_deleted=False)
        task2 = TaskFactory(list=list_obj, created_by=user, is_deleted=False)
        task3 = TaskFactory(list=list_obj, created_by=user, is_deleted=True)
        TaskAssigneeFactory(task=task1, user=user, assigned_by=assigned_by, is_active=True)
        TaskAssigneeFactory(task=task2, user=user, assigned_by=assigned_by, is_active=True)
        TaskAssigneeFactory(task=task3, user=user, assigned_by=assigned_by, is_active=True)
        storage = TaskAssigneeStorage()

        # Act
        result = storage.get_user_assigned_tasks(user_id=str(user_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_user_assigned_tasks_success.txt")

    @pytest.mark.django_db
    def test_get_user_assigned_tasks_empty(self, snapshot):
        # Arrange
        user_id = "12345678-1234-5678-1234-567812345678"
        UserFactory(user_id=user_id)
        storage = TaskAssigneeStorage()

        # Act
        result = storage.get_user_assigned_tasks(user_id=str(user_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_user_assigned_tasks_empty.txt")

    @pytest.mark.django_db
    def test_get_user_today_tasks_success(self, snapshot):
        # Arrange
        user_id = "12345678-1234-5678-1234-567812345678"
        list_obj = ListFactory()
        user = UserFactory(user_id=user_id)
        assigned_by = UserFactory()
        task1 = TaskFactory(list=list_obj, created_by=user, is_deleted=False)
        task2 = TaskFactory(list=list_obj, created_by=user, is_deleted=False)
        task3 = TaskFactory(list=list_obj, created_by=user, is_deleted=False)
        today = timezone.now()
        yesterday = today - timedelta(days=1)
        TaskAssigneeFactory(task=task1, user=user, assigned_by=assigned_by, is_active=True, assigned_at=today)
        TaskAssigneeFactory(task=task2, user=user, assigned_by=assigned_by, is_active=True, assigned_at=today)
        TaskAssigneeFactory(task=task3, user=user, assigned_by=assigned_by, is_active=True, assigned_at=yesterday)
        storage = TaskAssigneeStorage()

        # Act
        result = storage.get_user_today_tasks(user_id=str(user_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_user_today_tasks_success.txt")

    @pytest.mark.django_db
    def test_get_user_today_tasks_empty(self, snapshot):
        # Arrange
        user_id = "12345678-1234-5678-1234-567812345678"
        list_obj = ListFactory()
        user = UserFactory(user_id=user_id)
        assigned_by = UserFactory()
        task = TaskFactory(list=list_obj, created_by=user, is_deleted=False)
        yesterday = timezone.now() - timedelta(days=1)
        TaskAssigneeFactory(task=task, user=user, assigned_by=assigned_by, is_active=True, assigned_at=yesterday)
        storage = TaskAssigneeStorage()

        # Act
        result = storage.get_user_today_tasks(user_id=str(user_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_user_today_tasks_empty.txt")

    @pytest.mark.django_db
    def test_get_user_task_assignee_success(self, snapshot):
        # Arrange
        user_id = "12345678-1234-5678-1234-567812345678"
        task_id = "12345678-1234-5678-1234-567812345679"
        assigned_by_id = "12345678-1234-5678-1234-567812345680"
        list_obj = ListFactory()
        user = UserFactory(user_id=user_id)
        assigned_by = UserFactory(user_id=assigned_by_id)
        task = TaskFactory(task_id=task_id, list=list_obj, created_by=user)
        TaskAssigneeFactory(task=task, user=user, assigned_by=assigned_by)
        storage = TaskAssigneeStorage()

        # Act
        result = storage.get_user_task_assignee(user_id=str(user_id), task_id=str(task_id), assigned_by=str(assigned_by_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_user_task_assignee_success.txt")

    @pytest.mark.django_db
    def test_get_user_task_assignee_failure(self, snapshot):
        # Arrange
        user_id = "12345678-1234-5678-1234-567812345678"
        task_id = "12345678-1234-5678-1234-567812345679"
        assigned_by_id = "12345678-1234-5678-1234-567812345680"
        storage = TaskAssigneeStorage()

        # Act
        result = storage.get_user_task_assignee(user_id=str(user_id), task_id=str(task_id), assigned_by=str(assigned_by_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_user_task_assignee_failure.txt")

    @pytest.mark.django_db
    def test_reassign_task_assignee_success(self, snapshot):
        # Arrange
        assign_id = "12345678-1234-5678-1234-567812345678"
        list_obj = ListFactory()
        user = UserFactory()
        assigned_by = UserFactory()
        task = TaskFactory(list=list_obj, created_by=user)
        TaskAssigneeFactory(assign_id=assign_id, task=task, user=user, assigned_by=assigned_by, is_active=False)
        storage = TaskAssigneeStorage()

        # Act
        result = storage.reassign_task_assignee(assign_id=str(assign_id))

        # Assert
        snapshot.assert_match(repr(result), "test_reassign_task_assignee_success.txt")