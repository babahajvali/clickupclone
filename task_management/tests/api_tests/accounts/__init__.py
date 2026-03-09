from task_management.tests.test_utils import GraphQLBaseTestCase


class BaseCreateAccount(GraphQLBaseTestCase):
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


class BaseUpdateAccount(GraphQLBaseTestCase):
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


class BaseDeleteAccount(GraphQLBaseTestCase):
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


class BaseGetAccounts(GraphQLBaseTestCase):
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
