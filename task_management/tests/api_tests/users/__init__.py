from task_management.tests.test_utils import GraphQLBaseTestCase


class BaseCreateUser(GraphQLBaseTestCase):
    QUERY = """
    mutation CreateUser($params: CreateUserInputParams!) {
      createUser(params: $params) {
        ... on UserType {
          __typename
          userId
          username
          email
          fullName
          phoneNumber
          imageUrl
          isActive
          gender
        }
        ... on UsernameAlreadyExists {
          __typename
          username
        }
        ... on EmailAlreadyExists {
          __typename
          email
        }
        ... on PhoneNumberAlreadyExists {
          __typename
          phoneNumber
        }
      }
    }
    """


class BaseUpdateUser(GraphQLBaseTestCase):
    QUERY = """
    mutation UpdateUser($params: UpdateUserInputParams!) {
      updateUser(params: $params) {
        ... on UserType {
          __typename
          userId
          username
          email
          fullName
          phoneNumber
          imageUrl
          isActive
          gender
        }
        ... on UserNotFoundType {
          __typename
          userId
        }
        ... on InactiveUserType {
          __typename
          userId
        }
        ... on UsernameAlreadyExists {
          __typename
          username
        }
        ... on EmailAlreadyExists {
          __typename
          email
        }
        ... on PhoneNumberAlreadyExists {
          __typename
          phoneNumber
        }
      }
    }
    """


class BaseBlockUser(GraphQLBaseTestCase):
    QUERY = """
    mutation BlockUser($params: BlockUserInputParams!) {
      blockUser(params: $params) {
        ... on UserType {
          __typename
          userId
          username
          email
          fullName
          phoneNumber
          imageUrl
          isActive
          gender
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


class BaseUserLogin(GraphQLBaseTestCase):
    QUERY = """
    mutation UserLogin($params: UserLoginInputParams!) {
      userLogin(params: $params) {
        ... on UserType {
          __typename
          userId
          username
          email
          fullName
          phoneNumber
          imageUrl
          isActive
          gender
          accessToken
        }
        ... on EmailNotFound {
          __typename
          email
        }
        ... on IncorrectPassword {
          __typename
          password
        }
        ... on CaptchaValidationFailedType {
          __typename
          message
        }
        ... on InactiveUserType {
          __typename
          userId
        }
      }
    }
    """


class BaseGetUserProfile(GraphQLBaseTestCase):
    QUERY = """
    query GetUserProfile($params: GetUserProfileInputParams!) {
      getUserProfile(params: $params) {
        ... on UserType {
          __typename
          userId
          username
          email
          fullName
          phoneNumber
          imageUrl
          isActive
          gender
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


class BaseForgotPassword(GraphQLBaseTestCase):
    QUERY = """
    mutation ForgotPassword($params: ForgotPasswordReqParams!) {
      forgetPassword(params: $params) {
        ... on PasswordResetResponseType {
          __typename
          success
          message
        }
        ... on EmailNotFound {
          __typename
          email
        }
      }
    }
    """


class BaseResetPassword(GraphQLBaseTestCase):
    QUERY = """
    mutation ResetPassword($params: ResetPasswordReqParams!) {
      resetPassword(params: $params) {
        ... on UserType {
          __typename
          userId
          username
          email
          fullName
          phoneNumber
          imageUrl
          isActive
          gender
        }
        ... on InvalidResetToken {
          __typename
          token
        }
        ... on ResetTokenExpired {
          __typename
          token
        }
      }
    }
    """


class BaseValidateResetToken(GraphQLBaseTestCase):
    QUERY = """
    mutation ValidateResetToken($token: String!) {
      validateResetToken(token: $token) {
        ... on ValidateResetTokenType {
          __typename
          isValid
        }
        ... on InvalidResetToken {
          __typename
          token
        }
        ... on ResetTokenExpired {
          __typename
          token
        }
      }
    }
    """
