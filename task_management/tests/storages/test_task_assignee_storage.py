import pytest

from task_management.storages.task_storage import TaskStorage
from task_management.tests.factories.storage_factory import TaskAssigneeFactory, TaskFactory, UserFactory, ListFactory


class TestTaskAssigneeStorage:

    @pytest.mark.django_db
    def test_assign_task_assignee_success(self, snapshot):
        # Arrange
        task_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        assigned_by_id = "12345678-1234-5678-1234-567812345680"
        list_id = "12345678-1234-5678-1234-567812345678"
        list_obj = ListFactory(list_id=list_id)
        user = UserFactory(user_id=user_id)
        assigned_by = UserFactory(user_id=assigned_by_id)
        task = TaskFactory(task_id=task_id, list=list_obj, created_by=user)
        storage = TaskStorage()

        # Act
        result = storage.assign_task_assignee(task_id=str(task_id), user_id=str(user_id), assigned_by=str(assigned_by_id))

        # Assert
        # snapshot.assert_match(repr(result), "test_assign_task_assignee_success.txt")
        assert str(result.task_id) == task_id

    @pytest.mark.django_db
    def test_remove_task_assignee_success(self, snapshot):
        # Arrange
        assign_id = "12345678-1234-5678-1234-567812345678"
        list_id = "12345678-1234-5678-1234-567812345679"
        user_id = "12345678-1234-5678-1234-567812345678"
        assigned_by_id = "12345678-1234-5678-1234-567812345680"
        task_id = "12345678-1234-5678-1234-567812345678"
        list_obj = ListFactory(list_id=list_id)
        user = UserFactory(user_id=user_id)
        assigned_by = UserFactory(user_id=assigned_by_id)
        task = TaskFactory(task_id= task_id,list=list_obj, created_by=user)
        TaskAssigneeFactory(assign_id=assign_id, task=task, user=user, assigned_by=assigned_by, is_active=True)
        storage = TaskStorage()

        # Act
        result = storage.remove_task_assignee(assign_id=str(assign_id))

        # Assert
        snapshot.assert_match(repr(result), "test_remove_task_assignee_success.txt")

    @pytest.mark.django_db
    def test_get_task_assignee_success(self, snapshot):
        # Arrange
        assign_id = "12345678-1234-5678-1234-567812345678"
        list_id = "12345678-1234-5678-1234-567812345679"
        user_id = "12345678-1234-5678-1234-567812345678"
        assigned_by_id = "12345678-1234-5678-1234-567812345680"
        task_id = "12345678-1234-5678-1234-567812345678"
        list_obj = ListFactory(list_id=list_id)
        user = UserFactory(user_id=user_id)
        assigned_by = UserFactory(user_id=assigned_by_id)
        task = TaskFactory(task_id=task_id,list=list_obj, created_by=user)
        TaskAssigneeFactory(assign_id=assign_id, task=task, user=user, assigned_by=assigned_by)
        storage = TaskStorage()

        # Act
        result = storage.get_task_assignee(assign_id=str(assign_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_task_assignee_success.txt")

    @pytest.mark.django_db
    def test_get_task_assignees_success(self, snapshot):
        # Arrange
        task_id = "12345678-1234-5678-1234-567812345678"
        list_id = "12345678-1234-5678-1234-567812345679"
        user_id = "12345678-1234-5678-1234-567812345678"
        user_id2 = "12345678-1234-5678-1234-567812345679"
        assigned_by_id = "12345678-1234-5678-1234-567812345680"
        assign_id1 = "12345678-1234-5678-1234-567812345678"
        assign_id2 = "12345678-1234-5678-1234-567812345679"
        list_obj = ListFactory(list_id=list_id)
        user1 = UserFactory(user_id=user_id)
        user2 = UserFactory(user_id=user_id2)
        assigned_by = UserFactory(user_id=assigned_by_id)
        task = TaskFactory(task_id=task_id, list=list_obj, created_by=user1)
        TaskAssigneeFactory(assign_id=assign_id1,task=task, user=user1, assigned_by=assigned_by)
        TaskAssigneeFactory(assign_id=assign_id2,task=task, user=user2, assigned_by=assigned_by)
        storage = TaskStorage()

        # Act
        result = storage.get_task_assignees(task_id=str(task_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_task_assignees_success.txt")

    @pytest.mark.django_db
    def test_get_task_assignees_empty(self, snapshot):
        # Arrange
        task_id = "12345678-1234-5678-1234-567812345678"
        list_id = "12345678-1234-5678-1234-567812345679"
        user_id = "12345678-1234-5678-1234-567812345678"
        list_obj = ListFactory(list_id=list_id)
        user = UserFactory(user_id=user_id)
        TaskFactory(task_id=task_id, list=list_obj, created_by=user)
        storage = TaskStorage()

        # Act
        result = storage.get_task_assignees(task_id=str(task_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_task_assignees_empty.txt")

    @pytest.mark.django_db
    def test_get_user_assigned_tasks_success(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345679"
        user_id = "12345678-1234-5678-1234-567812345678"
        assigned_by_id = "12345678-1234-5678-1234-567812345680"
        assign_id1 = "12345678-1234-5678-1234-567812345681"
        assign_id2 = "12345678-1234-5678-1234-567812345682"
        assign_id3 = "12345678-1234-5678-1234-567812345683"
        task_id1 = "12345678-1234-5678-1234-567812345678"
        task_id2 = "12345678-1234-5678-1234-567812345679"
        task_id3 = "12345678-1234-5678-1234-567812345680"
        list_obj = ListFactory(list_id=list_id)
        user = UserFactory(user_id=user_id)
        assigned_by = UserFactory(user_id=assigned_by_id)
        task1 = TaskFactory(task_id=task_id1,list=list_obj, created_by=user, is_deleted=False)
        task2 = TaskFactory(task_id=task_id2,list=list_obj, created_by=user, is_deleted=False)
        task3 = TaskFactory(task_id=task_id3,list=list_obj, created_by=user, is_deleted=True)
        TaskAssigneeFactory(assign_id=assign_id1,task=task1, user=user, assigned_by=assigned_by, is_active=True)
        TaskAssigneeFactory(assign_id=assign_id2,task=task2, user=user, assigned_by=assigned_by, is_active=True)
        TaskAssigneeFactory(assign_id=assign_id3,task=task3, user=user, assigned_by=assigned_by, is_active=True)
        storage = TaskStorage()

        # Act
        result = storage.get_user_assigned_tasks(user_id=str(user_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_user_assigned_tasks_success.txt")

    @pytest.mark.django_db
    def test_get_user_assigned_tasks_empty(self, snapshot):
        # Arrange
        user_id = "12345678-1234-5678-1234-567812345678"
        UserFactory(user_id=user_id)
        storage = TaskStorage()

        # Act
        result = storage.get_user_assigned_tasks(user_id=str(user_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_user_assigned_tasks_empty.txt")

    @pytest.mark.django_db
    def test_get_user_task_assignee_success(self, snapshot):
        # Arrange
        user_id = "12345678-1234-5678-1234-567812345678"
        task_id = "12345678-1234-5678-1234-567812345679"
        assigned_by_id = "12345678-1234-5678-1234-567812345680"
        list_id = "12345678-1234-5678-1234-567812345678"
        list_obj = ListFactory(list_id=list_id)
        user = UserFactory(user_id=user_id)
        assigned_by = UserFactory(user_id=assigned_by_id)
        assign_id = "12345678-1234-5678-1234-567812345678"
        task = TaskFactory(task_id=task_id, list=list_obj, created_by=user)
        TaskAssigneeFactory(assign_id=assign_id,task=task, user=user, assigned_by=assigned_by)
        storage = TaskStorage()

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
        storage = TaskStorage()

        # Act
        result = storage.get_user_task_assignee(user_id=str(user_id), task_id=str(task_id), assigned_by=str(assigned_by_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_user_task_assignee_failure.txt")

    @pytest.mark.django_db
    def test_reassign_task_assignee_success(self, snapshot):
        # Arrange
        assign_id = "12345678-1234-5678-1234-567812345678"
        list_id = "12345678-1234-5678-1234-567812345679"
        user_id = "12345678-1234-5678-1234-567812345678"
        assigned_by_id = "12345678-1234-5678-1234-567812345680"
        list_obj = ListFactory(list_id=list_id)
        user = UserFactory(user_id=user_id)
        task_id = "12345678-1234-5678-1234-567812345678"
        assigned_by = UserFactory(user_id=assigned_by_id)
        task = TaskFactory(task_id=task_id,list=list_obj, created_by=user)
        TaskAssigneeFactory(assign_id=assign_id, task=task, user=user, assigned_by=assigned_by, is_active=False)
        storage = TaskStorage()

        # Act
        result = storage.reassign_task_assignee(assign_id=str(assign_id))

        # Assert
        snapshot.assert_match(repr(result), "test_reassign_task_assignee_success.txt")