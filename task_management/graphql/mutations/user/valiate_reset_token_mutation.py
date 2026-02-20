import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import InvalidResetToken, \
    ResetTokenExpired
from task_management.graphql.types.response_types import \
    ValidateResetTokenResponse
from task_management.graphql.types.types import ValidateResetTokenType
from task_management.interactors.user.reset_password_interator import \
    PasswordResetInteractor
from task_management.storages import UserStorage


class ValidateResetTokenMutation(graphene.Mutation):
    class Arguments:
        token = graphene.String(required=True)

    Output = ValidateResetTokenResponse

    @staticmethod
    def mutate(root, info, token):
        user_storage = UserStorage()

        interactor = PasswordResetInteractor(
            user_storage=user_storage)
        try:
            interactor.validate_reset_token(token=token)
            return ValidateResetTokenType(is_valid=True)

        except custom_exceptions.InvalidResetToken as e:
            return InvalidResetToken(token=e.token)

        except custom_exceptions.ResetTokenExpired as e:
            return ResetTokenExpired(token=e.token)



