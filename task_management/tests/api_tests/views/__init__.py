import pytest

from task_management.decorators import caching_decorators
from task_management.tests.test_utils import GraphQLBaseTestCase


class BaseViewGraphQLTestCase(GraphQLBaseTestCase):
    @pytest.fixture(autouse=True)
    def _stub_cache_backend(self, monkeypatch):
        monkeypatch.setattr(
            caching_decorators.cache,
            "get",
            lambda *args, **kwargs: None,
        )
        monkeypatch.setattr(
            caching_decorators.cache,
            "set",
            lambda *args, **kwargs: True,
        )
        monkeypatch.setattr(
            caching_decorators.cache,
            "delete_pattern",
            lambda *args, **kwargs: True,
        )


class BaseCreateView(BaseViewGraphQLTestCase):
    QUERY = """
    mutation CreateView($params: CreateViewInputParams!) {
      createView(params: $params) {
        ... on ViewType {
          __typename
          viewId
          name
          description
          viewType
          createdBy
        }
        ... on ViewTypeNotFoundType {
          __typename
          viewType
        }
        ... on EmptyViewNameType {
          __typename
          viewName
        }
      }
    }
    """


class BaseUpdateView(BaseViewGraphQLTestCase):
    QUERY = """
    mutation UpdateView($params: UpdateViewInputParams!) {
      updateView(params: $params) {
        ... on ViewType {
          __typename
          viewId
          name
          description
          viewType
          createdBy
        }
        ... on ViewNotFoundType {
          __typename
          viewId
        }
        ... on NothingToUpdateViewType {
          __typename
          viewId
        }
      }
    }
    """


class BaseApplyListView(BaseViewGraphQLTestCase):
    QUERY = """
    mutation ApplyListView($params: CreateListViewInputParams!) {
      applyListView(params: $params) {
        ... on ListViewType {
          __typename
          id
          viewName
          listId
          viewType
          createdBy
          isActive
        }
        ... on ListNotFoundType {
          __typename
          listId
        }
        ... on ViewNotFoundType {
          __typename
          viewId
        }
        ... on DeletedListType {
          __typename
          listId
        }
        ... on ModificationNotAllowedType {
          __typename
          userId
        }
        ... on UserNotWorkspaceMemberType {
          __typename
          userId
        }
      }
    }
    """


class BaseRemoveListView(BaseViewGraphQLTestCase):
    QUERY = """
    mutation RemoveListView($params: RemoveListViewInputParams!) {
      removeListView(params: $params) {
        ... on ListViewType {
          __typename
          id
          viewName
          listId
          viewType
          createdBy
          isActive
        }
        ... on ModificationNotAllowedType {
          __typename
          userId
        }
        ... on ListViewNotFound {
          __typename
          listViewId
        }
        ... on UserNotWorkspaceMemberType {
          __typename
          userId
        }
      }
    }
    """


class BaseGetViews(BaseViewGraphQLTestCase):
    QUERY = """
    query GetViews {
      getViews {
        ... on ViewsType {
          __typename
          views
        }
      }
    }
    """


class BaseGetListViews(BaseViewGraphQLTestCase):
    QUERY = """
    query GetListViews($params: GetListViewsInputParams!) {
      getListViews(params: $params) {
        ... on ListViewsType {
          __typename
          listViews {
            id
            viewName
            listId
            viewType
            createdBy
            isActive
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
