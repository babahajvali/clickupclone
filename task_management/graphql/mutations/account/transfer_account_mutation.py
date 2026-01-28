import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import AccountNotFoundType, \
    InactiveAccountType, UserNotAccountOwnerType, UserNotFoundType, \
    InactiveUserType
from task_management.graphql.types.input_types import TransferAccountInputParams
from task_management.graphql.types.response_types import TransferAccountResponse
from task_management.graphql.types.types import AccountType
from task_management.interactors.account_interactor.account_interactors import \
    AccountInteractor
from task_management.storages.account_member_storage import \
    AccountMemberStorage
from task_management.storages.account_storage import AccountStorage
from task_management.storages.user_storage import UserStorage


class TransferAccountMutation(graphene.Mutation):
    class Arguments:
        params = TransferAccountInputParams(required=True)

    Output = TransferAccountResponse

    @staticmethod
    def mutate(root, info, params):
        account_id = params.account_id
        old_owner_id = params.old_owner_id
        new_owner_id = params.new_owner_id

        user_storage = UserStorage()
        account_storage = AccountStorage()
        account_member_storage = AccountMemberStorage()

        interactor = AccountInteractor(user_storage=user_storage,
                                       account_member_storage=account_member_storage,
                                       account_storage=account_storage)

        try:
            result = interactor.transfer_account(
                account_id=account_id,
                old_owner_id=old_owner_id,
                new_owner_id=new_owner_id
            )

            return AccountType(
                account_id=result.account_id,
                name=result.name,
                description=result.description,
                owner_id=result.owner_id,
                is_active=result.is_active,
            )

        except custom_exceptions.AccountNotFoundException as e:
            return AccountNotFoundType(account_id=e.account_id)

        except custom_exceptions.InactiveAccountException as e:
            return InactiveAccountType(account_id=e.account_id)

        except custom_exceptions.UserNotAccountOwnerException as e:
            return UserNotAccountOwnerType(user_id=e.user_id)

        except custom_exceptions.UserNotFoundException as e:
            return UserNotFoundType(user_id=e.user_id)

        except custom_exceptions.InactiveUserException as e:
            return InactiveUserType(user_id=e.user_id)
