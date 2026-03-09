import pytest

from task_management.decorators import caching_decorators
from task_management.tests.test_utils import GraphQLBaseTestCase


class BaseAccountGraphQLTestCase(GraphQLBaseTestCase):
    @pytest.fixture(autouse=True)
    def _stub_cache_backend(self, monkeypatch):
        monkeypatch.setattr(caching_decorators.cache, "get",
                            lambda *args, **kwargs: None)
        monkeypatch.setattr(caching_decorators.cache, "set",
                            lambda *args, **kwargs: True)
        monkeypatch.setattr(caching_decorators.cache, "delete_pattern",
                            lambda *args, **kwargs: True)


class BaseCreateAccount(BaseAccountGraphQLTestCase):
    QUERY = """
    mutation CreateAccount($params: CreateAccountInputParams!) {
      createAccount(params: $params) {
        ... on AccountType {
          __typename
          accountId
          description
          isActive
          ownerId
          name
        }
        ... on AccountNameAlreadyExistsType {
          __typename
          name
        }
        ... on EmptyAccountNameExistsType {
          __typename
          accountName
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


class BaseUpdateAccount(BaseAccountGraphQLTestCase):
    QUERY = """
    mutation UpdateAccount($params: UpdateAccountInputParams!) {
      updateAccount(params: $params) {
        ... on AccountType {
          __typename
          accountId
          description
          isActive
          ownerId
          name
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
        ... on AccountNameAlreadyExistsType {
          __typename
          name
        }
        ... on NothingToUpdateAccountType {
          __typename
          accountId
        }
        ... on EmptyAccountNameExistsType {
          __typename
          accountName
        }
      }
    }
    """


class BaseDeleteAccount(BaseAccountGraphQLTestCase):
    QUERY = """
    mutation DeleteAccount($params: DeleteAccountInputParams!) {
      deleteAccount(params: $params) {
        ... on AccountType {
          __typename
          accountId
          description
          isActive
          ownerId
          name
        }
        ... on AccountNotFoundType {
          __typename
          accountId
        }
        ... on UserNotAccountOwnerType {
          __typename
          userId
        }
      }
    }
    """


class BaseGetAccounts(BaseAccountGraphQLTestCase):
    QUERY = """
    query GetAccounts($params: GetAccountsInputParams!) {
      getAccounts(params: $params) {
        ... on AccountsType {
          __typename
          accounts {
            accountId
            description
            isActive
            ownerId
            name
          }
        }
        ... on InvalidAccountIdsType {
          __typename
          accountIds
        }
      }
    }
    """
