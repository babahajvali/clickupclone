import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import \
    AccountNameAlreadyExistsType
from task_management.graphql.types.input_types import CreateAccountInputParams
from task_management.graphql.types.response_types import CreateAccountResponse
from task_management.graphql.types.types import AccountType
from task_management.interactors.account_interactor.account_interactors import \
    AccountInteractor
from task_management.interactors.dtos import CreateAccountDTO
from task_management.storages.account_member_storage import \
    AccountMemberStorage
from task_management.storages.account_storage import AccountStorage
from task_management.storages.user_storage import UserStorage


class CreateAccountMutation(graphene.Mutation):
    class Arguments:
        params = CreateAccountInputParams(required=True)

    Output = CreateAccountResponse

    @staticmethod
    def mutate(root, info, params):
        name = params.name
        description = params.description
        owner_id = info.context.user_id

        user_storage = UserStorage()
        account_storage = AccountStorage()
        account_member_storage = AccountMemberStorage()

        interactor = AccountInteractor(user_storage=user_storage,
                                       account_member_storage=account_member_storage,
                                       account_storage=account_storage)

        try:
            create_account_dto = CreateAccountDTO(name=name,
                                                  description=description,
                                                  owner_id=owner_id)
            result = interactor.create_account(
                create_account_data=create_account_dto)

            return AccountType(
                account_id=result.account_id,
                name=result.name,
                description=result.description,
                owner_id=result.owner_id,
                is_active=result.is_active,
            )
        except custom_exceptions.AccountNameAlreadyExistsException as e:
            return AccountNameAlreadyExistsType(name=e.name)
