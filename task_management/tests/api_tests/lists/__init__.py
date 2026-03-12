import pytest

from task_management.decorators import caching_decorators
from task_management.tests.test_utils import GraphQLBaseTestCase


class BaseListGraphQLTestCase(GraphQLBaseTestCase):
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


class BaseCreateList(BaseListGraphQLTestCase):
    QUERY = """
    mutation CreateList($params: CreateListInputParams!) {
      createList(params: $params) {
        ... on ListType {
          __typename
          listId
          name
          description
          entityType
          entityId
          isDeleted
          order
          isPrivate
          createdBy
        }
        ... on SpaceNotFoundType {
          __typename
          spaceId
        }
        ... on DeletedSpaceType {
          __typename
          spaceId
        }
        ... on FolderNotFoundType {
          __typename
          folderId
        }
        ... on DeletedFolderType {
          __typename
          folderId
        }
        ... on EmptyListNameType {
          __typename
          listName
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


class BaseUpdateList(BaseListGraphQLTestCase):
    QUERY = """
    mutation UpdateList($params: UpdateListInputParams!) {
      updateList(params: $params) {
        ... on ListType {
          __typename
          listId
          name
          description
          entityType
          entityId
          isDeleted
          order
          isPrivate
          createdBy
        }
        ... on ListNotFoundType {
          __typename
          listId
        }
        ... on DeletedListType {
          __typename
          listId
        }
        ... on NothingToUpdateListType {
          __typename
          listId
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


class BaseDeleteList(BaseListGraphQLTestCase):
    QUERY = """
    mutation DeleteList($params: DeleteListInputParams!) {
      deleteList(params: $params) {
        ... on ListType {
          __typename
          listId
          name
          description
          entityType
          entityId
          isDeleted
          order
          isPrivate
          createdBy
        }
        ... on ListNotFoundType {
          __typename
          listId
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


class BaseReorderListInFolder(BaseListGraphQLTestCase):
    QUERY = """
    mutation ReorderListInFolder($params: ReorderListInFolderInputParams!) {
      reorderListInFolder(params: $params) {
        ... on ListType {
          __typename
          listId
          name
          description
          entityType
          entityId
          isDeleted
          order
          isPrivate
          createdBy
        }
        ... on ListNotFoundType {
          __typename
          listId
        }
        ... on DeletedListType {
          __typename
          listId
        }
        ... on FolderNotFoundType {
          __typename
          folderId
        }
        ... on DeletedFolderType {
          __typename
          folderId
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


class BaseReorderListInSpace(BaseListGraphQLTestCase):
    QUERY = """
    mutation ReorderListInSpace($params: ReorderListInSpaceInputParams!) {
      reorderListInSpace(params: $params) {
        ... on ListType {
          __typename
          listId
          name
          description
          entityType
          entityId
          isDeleted
          order
          isPrivate
          createdBy
        }
        ... on ListNotFoundType {
          __typename
          listId
        }
        ... on DeletedListType {
          __typename
          listId
        }
        ... on SpaceNotFoundType {
          __typename
          spaceId
        }
        ... on DeletedSpaceType {
          __typename
          spaceId
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


class BaseSetListVisibility(BaseListGraphQLTestCase):
    QUERY = """
    mutation SetListVisibility($params: SetListVisibilityInputParams!) {
      setListVisibility(params: $params) {
        ... on ListType {
          __typename
          listId
          name
          description
          entityType
          entityId
          isDeleted
          order
          isPrivate
          createdBy
        }
        ... on ListNotFoundType {
          __typename
          listId
        }
        ... on DeletedListType {
          __typename
          listId
        }
        ... on UnsupportedVisibilityType {
          __typename
          visibility
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


class BaseGetList(BaseListGraphQLTestCase):
    QUERY = """
    query GetList($params: GetListInputParams!) {
      getList(params: $params) {
        ... on ListType {
          __typename
          listId
          name
          description
          entityType
          entityId
          isDeleted
          order
          isPrivate
          createdBy
        }
        ... on ListNotFoundType {
          __typename
          listId
        }
      }
    }
    """


class BaseGetFolderLists(BaseListGraphQLTestCase):
    QUERY = """
    query GetFolderLists($params: GetFolderListsInputParams!) {
      getFolderLists(params: $params) {
        ... on ListsType {
          __typename
          lists {
            listId
            name
            description
            entityType
            entityId
            isDeleted
            order
            isPrivate
            createdBy
          }
        }
        ... on FolderNotFoundType {
          __typename
          folderId
        }
        ... on DeletedFolderType {
          __typename
          folderId
        }
      }
    }
    """


class BaseGetSpaceLists(BaseListGraphQLTestCase):
    QUERY = """
    query GetSpaceLists($params: GetSpaceListsInputParams!) {
      getSpaceLists(params: $params) {
        ... on ListsType {
          __typename
          lists {
            listId
            name
            description
            entityType
            entityId
            isDeleted
            order
            isPrivate
            createdBy
          }
        }
        ... on SpaceNotFoundType {
          __typename
          spaceId
        }
        ... on DeletedSpaceType {
          __typename
          spaceId
        }
      }
    }
    """
