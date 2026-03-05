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
