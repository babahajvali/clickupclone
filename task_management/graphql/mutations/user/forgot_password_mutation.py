import graphene
from django.conf import settings

from task_management.email_service.email_service import EmailService
from task_management.exceptions.custom_exceptions import \
    NotExistedEmailFoundException, InvalidResetTokenFound, ResetTokenExpired
from task_management.graphql.types.error_types import NotExistedEmailFoundType, \
    InvalidResetTokenFoundType, ResetTokenExpiredType
from task_management.graphql.types.input_types import ForgotPasswordReqParams, \
    ResetPasswordReqParams
from task_management.graphql.types.response_types import \
    ForgotPasswordResponse, ResetPasswordResponse
from task_management.graphql.types.types import PasswordResetResponseType, \
    UserType
from task_management.interactors.user_interactor.reset_password_interator import \
    UserPasswordInteractor
from task_management.storages.password_reset_storage import \
    PasswordResetStorage
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

            interactor = UserPasswordInteractor(
                user_storage=user_storage,
                email_service=email_service,
                password_reset_storage=PasswordResetStorage()
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

        except NotExistedEmailFoundException as e:
            print(f"❌ Email not found: {e.email}")
            return NotExistedEmailFoundType(email=e.email)

        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
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
            password_reset_storage = PasswordResetStorage()
            interactor = UserPasswordInteractor(user_storage=user_storage,
                                                password_reset_storage=password_reset_storage)

            result = interactor.reset_password(
                token=token,
                new_password=new_password
            )

            return UserType(
                user_id=str(result.user_id),
                full_name=result.full_name,
                gender=result.gender,
                username=result.username,
                email=result.email,
                phone_number=result.phone_number,
                is_active=result.is_active,
                image_url=result.image_url
            )

        except InvalidResetTokenFound as e:
            return InvalidResetTokenFoundType(token=e.token)

        except ResetTokenExpired as e:
            return ResetTokenExpiredType(token=e.token)
