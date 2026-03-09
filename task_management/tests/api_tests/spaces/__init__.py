import pytest

from task_management.decorators import caching_decorators
from task_management.tests.test_utils import GraphQLBaseTestCase


class BaseSpaceGraphQLTestCase(GraphQLBaseTestCase):
    @pytest.fixture(autouse=True)
    def _stub_cache_backend(self, monkeypatch):
        monkeypatch.setattr(caching_decorators.cache, "get",
                            lambda *args, **kwargs: None)
        monkeypatch.setattr(caching_decorators.cache, "set",
                            lambda *args, **kwargs: True)
        monkeypatch.setattr(caching_decorators.cache, "delete_pattern",
                            lambda *args, **kwargs: True)


class BaseCreateSpace(BaseSpaceGraphQLTestCase):
    QUERY = """
    mutation CreateSpace($params: CreateSpaceInputParams!) {
      createSpace(params: $params) {
        ... on SpaceType {
          __typename
          spaceId
          name
          description
          workspaceId
          order
          isDeleted
          isPrivate
          createdBy
        }
        ... on WorkspaceNotFoundType {
          __typename
          workspaceId
        }
        ... on DeletedWorkspaceType {
          __typename
          workspaceId
        }
        ... on EmptySpaceNameType {
          __typename
          spaceName
        }
        ... on UserNotWorkspaceMemberType {
          __typename
          userId
        }
      }
    }
    """


class BaseUpdateSpace(BaseSpaceGraphQLTestCase):
    QUERY = """
    mutation UpdateSpace($params: UpdateSpaceInputParams!) {
      updateSpace(params: $params) {
        ... on SpaceType {
          __typename
          spaceId
          name
          description
          workspaceId
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
      }
    }
    """


class BaseDeleteSpace(BaseSpaceGraphQLTestCase):
    QUERY = """
    mutation DeleteSpace($params: DeleteSpaceInputParams!) {
      deleteSpace(params: $params) {
        ... on SpaceType {
          __typename
          spaceId
          name
          description
          workspaceId
          order
          isDeleted
          isPrivate
          createdBy
        }
        ... on SpaceNotFoundType {
          __typename
          spaceId
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


class BaseReorderSpace(BaseSpaceGraphQLTestCase):
    QUERY = """
    mutation ReorderSpace($params: ReorderSpaceInputParams!) {
      reorderSpace(params: $params) {
        ... on SpaceType {
          __typename
          spaceId
          name
          description
          workspaceId
          order
          isDeleted
          isPrivate
          createdBy
        }
        ... on WorkspaceNotFoundType {
          __typename
          workspaceId
        }
        ... on DeletedWorkspaceType {
          __typename
          workspaceId
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


class BaseSetSpaceVisibility(BaseSpaceGraphQLTestCase):
    QUERY = """
    mutation SetSpaceVisibility($params: SetSpaceVisibilityInputParams!) {
      setSpaceVisibility(params: $params) {
        ... on SpaceType {
          __typename
          spaceId
          name
          description
          workspaceId
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


class BaseGetSpace(BaseSpaceGraphQLTestCase):
    QUERY = """
    query GetSpace($params: GetSpaceInputParams!) {
      getSpace(params: $params) {
        ... on SpaceType {
          __typename
          spaceId
          name
          description
          workspaceId
          order
          isDeleted
          isPrivate
          createdBy
        }
        ... on SpaceNotFoundType {
          __typename
          spaceId
        }
      }
    }
    """


class BaseGetWorkspaceSpaces(BaseSpaceGraphQLTestCase):
    QUERY = """
    query GetWorkspaceSpaces($params: GetWorkspaceSpacesInputParams!) {
      getWorkspaceSpaces(params: $params) {
        ... on WorkspaceSpacesType {
          __typename
          spaces {
            spaceId
            name
            description
            workspaceId
            order
            isDeleted
            isPrivate
            createdBy
          }
        }
        ... on WorkspaceNotFoundType {
          __typename
          workspaceId
        }
        ... on DeletedWorkspaceType {
          __typename
          workspaceId
        }
      }
    }
    """
