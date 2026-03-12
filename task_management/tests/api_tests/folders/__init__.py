import pytest

from task_management.decorators import caching_decorators
from task_management.tests.test_utils import GraphQLBaseTestCase


class BaseFolderGraphQLTestCase(GraphQLBaseTestCase):
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


class BaseCreateFolder(BaseFolderGraphQLTestCase):
    QUERY = """
    mutation CreateFolder($params: CreateFolderInputParams!) {
      createFolder(params: $params) {
        ... on FolderType {
          __typename
          folderId
          name
          description
          spaceId
          order
          isDeleted
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
        ... on EmptyFolderNameType {
          __typename
          folderName
        }
        ... on UserNotWorkspaceMemberType {
          __typename
          userId
        }
      }
    }
    """


class BaseUpdateFolder(BaseFolderGraphQLTestCase):
    QUERY = """
    mutation UpdateFolder($params: UpdateFolderInputParams!) {
      updateFolder(params: $params) {
        ... on FolderType {
          __typename
          folderId
          name
          description
          spaceId
          order
          isDeleted
          isPrivate
          createdBy
        }
        ... on FolderNotFoundType {
          __typename
          folderId
        }
        ... on DeletedFolderType {
          __typename
          folderId
        }
        ... on NothingToUpdateFolderType {
          __typename
          folderId
        }
        ... on UserNotWorkspaceMemberType {
          __typename
          userId
        }
      }
    }
    """


class BaseDeleteFolder(BaseFolderGraphQLTestCase):
    QUERY = """
    mutation DeleteFolder($params: DeleteFolderInputParams!) {
      deleteFolder(params: $params) {
        ... on FolderType {
          __typename
          folderId
          name
          description
          spaceId
          order
          isDeleted
          isPrivate
          createdBy
        }
        ... on FolderNotFoundType {
          __typename
          folderId
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


class BaseReorderFolder(BaseFolderGraphQLTestCase):
    QUERY = """
    mutation ReorderFolder($params: ReorderFolderInputParams!) {
      reorderFolder(params: $params) {
        ... on FolderType {
          __typename
          folderId
          name
          description
          spaceId
          order
          isDeleted
          isPrivate
          createdBy
        }
        ... on FolderNotFoundType {
          __typename
          folderId
        }
        ... on DeletedFolderType {
          __typename
          folderId
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


class BaseSetFolderVisibility(BaseFolderGraphQLTestCase):
    QUERY = """
    mutation SetFolderVisibility($params: SetFolderVisibilityInputParams!) {
      setFolderVisibility(params: $params) {
        ... on FolderType {
          __typename
          folderId
          name
          description
          spaceId
          order
          isDeleted
          isPrivate
          createdBy
        }
        ... on FolderNotFoundType {
          __typename
          folderId
        }
        ... on DeletedFolderType {
          __typename
          folderId
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


class BaseGetFolder(BaseFolderGraphQLTestCase):
    QUERY = """
    query GetFolder($params: GetFolderInputParams!) {
      getFolder(params: $params) {
        ... on FolderType {
          __typename
          folderId
          name
          description
          spaceId
          order
          isDeleted
          isPrivate
          createdBy
        }
        ... on FolderNotFoundType {
          __typename
          folderId
        }
      }
    }
    """


class BaseGetSpaceFolders(BaseFolderGraphQLTestCase):
    QUERY = """
    query GetSpaceFolders($params: GetSpaceFoldersInputParams!) {
      getSpaceFolders(params: $params) {
        ... on SpaceFoldersType {
          __typename
          folders {
            folderId
            name
            description
            spaceId
            order
            isDeleted
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
