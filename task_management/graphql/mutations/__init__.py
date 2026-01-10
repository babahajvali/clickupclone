import graphene

from task_management.graphql.mutations.account.create_account_mutation import \
    CreateAccountMutation
from task_management.graphql.mutations.account.delete_account_mutation import \
    DeleteAccountMutation
from task_management.graphql.mutations.account.transfer_account_mutation import \
    TransferAccountMutation
from task_management.graphql.mutations.space.create_space_mutation import \
    CreateSpaceMutation
from task_management.graphql.mutations.space.delete_space_mutation import \
    DeleteSpaceMutation
from task_management.graphql.mutations.space.reorder_space_mutation import \
    ReorderSpaceMutation
from task_management.graphql.mutations.space.set_space_visibility_mutation import \
    SetSpaceVisibilityMutation
from task_management.graphql.mutations.space.update_space_mutation import \
    UpdateSpaceMutation
from task_management.graphql.mutations.user.block_user_mutation import \
    BlockUserMutation
from task_management.graphql.mutations.user.create_user_mutation import \
    CreateUserMutation
from task_management.graphql.mutations.user.update_user_mutation import \
    UpdateUserMutation
from task_management.graphql.mutations.user.user_login_mutation import \
    UserLoginMutation
from task_management.graphql.mutations.workspace.create_workspace_mutation import \
    CreateWorkspaceMutation
from task_management.graphql.mutations.workspace.delete_wrkspace_mutation import \
    DeleteWorkspaceMutation
from task_management.graphql.mutations.workspace.transfer_workspace_mutation import \
    TransferWorkspaceMutation
from task_management.graphql.mutations.workspace.update_workspace_mutation import \
    UpdateWorkspaceMutation


class CreateAccount(graphene.ObjectType):
    create_account = CreateAccountMutation.Field(required=True)

class CreateUser(graphene.ObjectType):
    create_user = CreateUserMutation.Field(required=True)

class UpdateUser(graphene.ObjectType):
    update_user = UpdateUserMutation.Field(required=True)

class BlockUser(graphene.ObjectType):
    block_user = BlockUserMutation.Field(required=True)

class UserLogin(graphene.ObjectType):
    user_login = UserLoginMutation.Field(required=True)

class TransferAccount(graphene.ObjectType):
    transfer_account = TransferAccountMutation.Field(required=True)

class DeleteAccount(graphene.ObjectType):
    delete_account = DeleteAccountMutation.Field(required=True)

class CreateWorkspace(graphene.ObjectType):
    create_workspace = CreateWorkspaceMutation.Field(required=True)

class UpdateWorkspace(graphene.ObjectType):
    update_workspace = UpdateWorkspaceMutation.Field(required=True)

class DeleteWorkspace(graphene.ObjectType):
    delete_workspace = DeleteWorkspaceMutation.Field(required=True)

class TransferWorkspace(graphene.ObjectType):
    transfer_workspace = TransferWorkspaceMutation.Field(required=True)

class CreateSpace(graphene.ObjectType):
    create_space = CreateSpaceMutation.Field(required=True)

class UpdateSpace(graphene.ObjectType):
    update_space = UpdateSpaceMutation.Field(required=True)

class DeleteSpace(graphene.ObjectType):
    delete_space = DeleteSpaceMutation.Field(required=True)

class ReorderSpace(graphene.ObjectType):
    reorder_space = ReorderSpaceMutation.Field(required=True)

class SetSpaceVisibility(graphene.ObjectType):
    set_space_visibility = SetSpaceVisibilityMutation.Field(required=True)