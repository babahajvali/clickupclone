import graphene
from django.conf import settings

from task_management.email_service.email_service import EmailService
from task_management.exceptions.custom_exceptions import \
    EmailNotFoundException, InvalidResetTokenException, \
    ResetTokenExpiredException
from task_management.graphql.types.error_types import EmailNotFound, \
    InvalidResetToken, ResetTokenExpired
from task_management.graphql.types.input_types import ForgotPasswordReqParams, \
    ResetPasswordReqParams
from task_management.graphql.types.response_types import \
    ForgotPasswordResponse, ResetPasswordResponse
from task_management.graphql.types.types import PasswordResetResponseType, \
    UserType
from task_management.interactors.user.reset_password_interator import \
    PasswordResetInteractor
from task_management.storages.user_storage import UserStorage


class ForgotPasswordMutation(graphene.Mutation):
    class Arguments:
        params = ForgotPasswordReqParams(required=True)

    Output = ForgotPasswordResponse

    @staticmethod
    def mutate(root, info, params):
        try:
            email = params.email
            # print(f"\n{'=' * 60}")
            # print(f"🔐 Password reset requested for: {email}")
            # print(f"{'=' * 60}\n")

            user_storage = UserStorage()

            email_service = EmailService()

            interactor = PasswordResetInteractor(
                user_storage=user_storage,
                email_service=email_service,
            )

            base_url = settings.FRONTEND_URL

            success = interactor.request_password_reset(
                email=email,
                base_url=base_url
            )

            if success:
                return PasswordResetResponseType(
                    success=True,
                    message="Password reset email sent successfully. Please check your inbox."
                )
            else:
                return PasswordResetResponseType(
                    success=False,
                    message="Failed to send email. Please try again later."
                )

        except EmailNotFoundException as e:
            return EmailNotFound(email=e.email)

        except Exception as e:
            import traceback
            traceback.print_exc()
            return PasswordResetResponseType(
                success=False,
                message="An unexpected error occurred."
            )


class ResetPasswordMutation(graphene.Mutation):
    class Arguments:
        params = ResetPasswordReqParams(required=True)

    Output = ResetPasswordResponse

    @staticmethod
    def mutate(root, info, params):
        try:
            token = params.token
            new_password = params.new_password

            user_storage = UserStorage()
            interactor = PasswordResetInteractor(user_storage=user_storage)

            result = interactor.reset_password(
                token=token,
                new_password=new_password
            )

            return UserType(
                user_id=result.user_id,
                full_name=result.full_name,
                gender=result.gender,
                username=result.username,
                email=result.email,
                phone_number=result.phone_number,
                is_active=result.is_active,
                image_url=result.image_url
            )

        except InvalidResetTokenException as e:
            return InvalidResetToken(token=e.token)

        except ResetTokenExpiredException as e:
            return ResetTokenExpired(token=e.token)
