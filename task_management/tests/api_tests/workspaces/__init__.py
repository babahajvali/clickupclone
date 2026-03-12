import pytest

from task_management.decorators import caching_decorators
from task_management.tests.test_utils import GraphQLBaseTestCase


class BaseWorkspaceGraphQLTestCase(GraphQLBaseTestCase):
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


class BaseCreateWorkspace(BaseWorkspaceGraphQLTestCase):
    QUERY = """
    mutation CreateWorkspace($params: CreateWorkspaceInputParams!) {
      createWorkspace(params: $params) {
        ... on WorkspaceType {
          __typename
          workspaceId
          name
          description
          userId
          accountId
          isDeleted
        }
        ... on AccountNotFoundType {
          __typename
          accountId
        }
        ... on InactiveAccountType {
          __typename
          accountId
        }
        ... on UserNotAccountOwnerType {
          __typename
          userId
        }
        ... on EmptyWorkspaceNameType {
          __typename
          workspaceName
        }
      }
    }
    """


class BaseUpdateWorkspace(BaseWorkspaceGraphQLTestCase):
    QUERY = """
    mutation UpdateWorkspace($params: UpdateWorkspaceInputParams!) {
      updateWorkspace(params: $params) {
        ... on WorkspaceType {
          __typename
          workspaceId
          name
          description
          userId
          accountId
          isDeleted
        }
        ... on WorkspaceNotFoundType {
          __typename
          workspaceId
        }
        ... on DeletedWorkspaceType {
          __typename
          workspaceId
        }
        ... on UserNotWorkspaceOwnerType {
          __typename
          userId
        }
      }
    }
    """


class BaseDeleteWorkspace(BaseWorkspaceGraphQLTestCase):
    QUERY = """
    mutation DeleteWorkspace($params: DeleteWorkspaceInputParams!) {
      deleteWorkspace(params: $params) {
        ... on WorkspaceType {
          __typename
          workspaceId
          name
          description
          userId
          accountId
          isDeleted
        }
        ... on WorkspaceNotFoundType {
          __typename
          workspaceId
        }
        ... on UserNotWorkspaceOwnerType {
          __typename
          userId
        }
      }
    }
    """


class BaseTransferWorkspace(BaseWorkspaceGraphQLTestCase):
    QUERY = """
    mutation TransferWorkspace($params: TransferWorkspaceInputParams!) {
      transferWorkspace(params: $params) {
        ... on WorkspaceType {
          __typename
          workspaceId
          name
          description
          userId
          accountId
          isDeleted
        }
        ... on WorkspaceNotFoundType {
          __typename
          workspaceId
        }
        ... on DeletedWorkspaceType {
          __typename
          workspaceId
        }
        ... on UserNotWorkspaceOwnerType {
          __typename
          userId
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


class BaseAddWorkspaceMember(BaseWorkspaceGraphQLTestCase):
    QUERY = """
    mutation AddWorkspaceMember($params: AddMemberToWorkspaceInputParams!) {
      addMemberToWorkspace(params: $params) {
        ... on WorkspaceMemberType {
          __typename
          id
          workspaceId
          userId
          role
          isActive
          addedBy
        }
        ... on WorkspaceNotFoundType {
          __typename
          workspaceId
        }
        ... on DeletedWorkspaceType {
          __typename
          workspaceId
        }
        ... on UserNotFoundType {
          __typename
          userId
        }
        ... on InactiveUserType {
          __typename
          userId
        }
        ... on UnexpectedRoleType {
          __typename
          role
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


class BaseChangeWorkspaceMemberRole(BaseWorkspaceGraphQLTestCase):
    QUERY = """
    mutation ChangeWorkspaceMemberRole(
      $params: ChangeWorkspaceMemberRoleInputParams!
    ) {
      changeWorkspaceMemberRole(params: $params) {
        ... on WorkspaceMemberType {
          __typename
          id
          workspaceId
          userId
          role
          isActive
          addedBy
        }
        ... on WorkspaceNotFoundType {
          __typename
          workspaceId
        }
        ... on DeletedWorkspaceType {
          __typename
          workspaceId
        }
        ... on UserNotFoundType {
          __typename
          userId
        }
        ... on InactiveUserType {
          __typename
          userId
        }
        ... on UnexpectedRoleType {
          __typename
          role
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


class BaseRemoveWorkspaceMember(BaseWorkspaceGraphQLTestCase):
    QUERY = """
    mutation RemoveWorkspaceMember($params: RemoveWorkspaceMemberInputParams!) {
      removeMemberFromWorkspace(params: $params) {
        ... on WorkspaceMemberType {
          __typename
          id
          workspaceId
          userId
          role
          isActive
          addedBy
        }
        ... on WorkspaceMemberIdNotFoundType {
          __typename
          workspaceMemberId
        }
        ... on InactiveWorkspaceMemberType {
          __typename
          workspaceMemberId
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


class BaseGetWorkspaces(BaseWorkspaceGraphQLTestCase):
    QUERY = """
    query GetWorkspaces($params: GetWorkspaceInputParams!) {
      getWorkspaces(params: $params) {
        ... on WorkspacesType {
          __typename
          workspaces {
            workspaceId
            name
            description
            userId
            accountId
            isDeleted
          }
        }
        ... on InvalidWorkspaceIdsFoundType {
          __typename
          workspaceIds
        }
      }
    }
    """


class BaseGetUserWorkspaces(BaseWorkspaceGraphQLTestCase):
    QUERY = """
    query GetUserWorkspaces($params: GetUserWorkspacesInputParams!) {
      getUserWorkspaces(params: $params) {
        ... on WorkspaceMembersType {
          __typename
          members {
            id
            workspaceId
            userId
            role
            isActive
            addedBy
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
