from contextlib import contextmanager

import pytest

from task_management.decorators import caching_decorators
from task_management.tests.test_utils import GraphQLBaseTestCase


@contextmanager
def _dummy_redis_lock(*args, **kwargs):
    yield


class BaseTaskGraphQLTestCase(GraphQLBaseTestCase):
    @pytest.fixture(autouse=True)
    def _stub_cache_backend(self, monkeypatch):
        monkeypatch.setattr(caching_decorators.cache, "get",
                            lambda *args, **kwargs: None)
        monkeypatch.setattr(caching_decorators.cache, "set",
                            lambda *args, **kwargs: True)
        monkeypatch.setattr(caching_decorators.cache, "delete_pattern",
                            lambda *args, **kwargs: True)
        monkeypatch.setattr(
            "task_management.interactors.tasks.create_task_interactor.redis_lock",
            _dummy_redis_lock,
        )
        monkeypatch.setattr(
            "task_management.interactors.tasks.reorder_task_interactor.redis_lock",
            _dummy_redis_lock,
        )


class BaseCreateTask(BaseTaskGraphQLTestCase):
    QUERY = """
    mutation CreateTask($params: CreateTaskInputParams!) {
      createTask(params: $params) {
        ... on TaskType {
          __typename
          taskId
          title
          description
          listId
          order
          createdBy
          isDeleted
        }
        ... on ListNotFoundType {
          __typename
          listId
        }
        ... on DeletedListType {
          __typename
          listId
        }
        ... on EmptyTaskTitleType {
          __typename
          title
        }
        ... on UserNotWorkspaceMemberType {
          __typename
          userId
        }
        ... on ModificationNotAllowedType {
          __typename
          userId
        }
      }
    }
    """


class BaseUpdateTask(BaseTaskGraphQLTestCase):
    QUERY = """
    mutation UpdateTask($params: UpdateTaskInputParams!) {
      updateTask(params: $params) {
        ... on TaskType {
          __typename
          taskId
          title
          description
          listId
          order
          createdBy
          isDeleted
        }
        ... on TaskNotFoundType {
          __typename
          taskId
        }
        ... on DeletedTaskType {
          __typename
          taskId
        }
        ... on NothingToUpdateTaskType {
          __typename
          taskId
        }
        ... on UserNotWorkspaceMemberType {
          __typename
          userId
        }
        ... on ModificationNotAllowedType {
          __typename
          userId
        }
      }
    }
    """


class BaseDeleteTask(BaseTaskGraphQLTestCase):
    QUERY = """
    mutation DeleteTask($params: DeleteTaskInputParams!) {
      deleteTask(params: $params) {
        ... on TaskType {
          __typename
          taskId
          title
          description
          listId
          order
          createdBy
          isDeleted
        }
        ... on TaskNotFoundType {
          __typename
          taskId
        }
        ... on UserNotWorkspaceMemberType {
          __typename
          userId
        }
        ... on ModificationNotAllowedType {
          __typename
          userId
        }
      }
    }
    """


class BaseReorderTask(BaseTaskGraphQLTestCase):
    QUERY = """
    mutation ReorderTask($params: ReorderTaskInputParams!) {
      reorderTask(params: $params) {
        ... on TaskType {
          __typename
          taskId
          title
          description
          listId
          order
          createdBy
          isDeleted
        }
        ... on TaskNotFoundType {
          __typename
          taskId
        }
        ... on DeletedTaskType {
          __typename
          taskId
        }
        ... on InvalidOrderType {
          __typename
          order
        }
        ... on UserNotWorkspaceMemberType {
          __typename
          userId
        }
        ... on ModificationNotAllowedType {
          __typename
          userId
        }
      }
    }
    """


class BaseTaskAssignee(BaseTaskGraphQLTestCase):
    CREATE_QUERY = """
    mutation TaskAssignee($params: CreateTaskAssigneeInputParams!) {
      taskAssignee(params: $params) {
        ... on TaskAssigneeType {
          __typename
          assignId
          userId
          taskId
          assignedBy
          isActive
        }
        ... on TaskNotFoundType {
          __typename
          taskId
        }
        ... on DeletedTaskType {
          __typename
          taskId
        }
        ... on UserNotFoundType {
          __typename
          userId
        }
        ... on InactiveUserType {
          __typename
          userId
        }
        ... on ModificationNotAllowedType {
          __typename
          userId
        }
      }
    }
    """
    REMOVE_QUERY = """
    mutation RemoveTaskAssignee($params: RemoveTaskAssigneeInputParams!) {
      removeTaskAssignee(params: $params) {
        ... on TaskAssigneeType {
          __typename
          assignId
          userId
          taskId
          assignedBy
          isActive
        }
        ... on TaskAssigneeNotFoundType {
          __typename
          assignId
        }
        ... on ModificationNotAllowedType {
          __typename
          userId
        }
      }
    }
    """


class BaseGetTask(BaseTaskGraphQLTestCase):
    QUERY = """
    query GetTask($params: GetTaskInputParams!) {
      getTask(params: $params) {
        ... on TaskType {
          __typename
          taskId
          title
          description
          listId
          order
          createdBy
          isDeleted
        }
        ... on TaskNotFoundType {
          __typename
          taskId
        }
        ... on DeletedTaskType {
          __typename
          taskId
        }
      }
    }
    """


class BaseGetListTasks(BaseTaskGraphQLTestCase):
    QUERY = """
    query GetListTasks($params: GetListTasksInputParams!) {
      getListTasks(params: $params) {
        ... on TaskDetailsType {
          __typename
          tasks {
            task {
              taskId
              title
              description
              listId
              order
              createdBy
              isDeleted
            }
            assignees {
              assignId
              userId
              taskId
              assignedBy
              isActive
            }
            fieldValues {
              fieldId
              value
            }
          }
        }
        ... on ListNotFoundType {
          __typename
          listId
        }
        ... on DeletedListType {
          __typename
          listId
        }
      }
    }
    """


class BaseGetTaskAssignees(BaseTaskGraphQLTestCase):
    QUERY = """
    query GetTaskAssignees($params: GetTaskAssigneesInputParams!) {
      getTaskAssignees(params: $params) {
        ... on TaskAssigneesType {
          __typename
          assignees {
            assignId
            userId
            taskId
            assignedBy
            isActive
          }
        }
        ... on TaskNotFoundType {
          __typename
          taskId
        }
        ... on DeletedTaskType {
          __typename
          taskId
        }
      }
    }
    """


class BaseGetUserTasks(BaseTaskGraphQLTestCase):
    QUERY = """
    query GetUserTasks($params: GetUserTasksInputParams!) {
      getUserTasks(params: $params) {
        ... on GetUserTaskType {
          __typename
          userId
          tasks {
            taskId
            title
            description
            listId
            order
            createdBy
            isDeleted
          }
        }
        ... on UserNotFoundType {
          __typename
          userId
        }
        ... on InactiveUserType {
          __typename
          userId
        }
      }
    }
    """


class BaseTaskFilter(BaseTaskGraphQLTestCase):
    QUERY = """
    query GetTaskFilters($params: TaskFilterInputParams!) {
      getTaskFilters(params: $params) {
        ... on TasksType {
          __typename
          tasks {
            taskId
            title
            description
            listId
            order
            createdBy
            isDeleted
          }
        }
        ... on ListNotFoundType {
          __typename
          listId
        }
        ... on DeletedListType {
          __typename
          listId
        }
        ... on InvalidOffset {
          __typename
          offset
        }
        ... on InvalidLimitType {
          __typename
          limit
        }
      }
    }
    """
