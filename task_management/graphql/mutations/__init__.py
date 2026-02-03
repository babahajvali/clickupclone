import graphene

from task_management.graphql.mutations.account.create_account_mutation import \
    CreateAccountMutation
from task_management.graphql.mutations.account.delete_account_mutation import \
    DeleteAccountMutation

from task_management.graphql.mutations.account.transfer_account_mutation import \
    TransferAccountMutation
from task_management.graphql.mutations.field.create_field_mutation import \
    CreateFieldMutation
from task_management.graphql.mutations.field.delete_field_mutation import \
    DeleteFieldMutation
from task_management.graphql.mutations.field.reorder_field_mutation import \
    ReorderFieldMutation
from task_management.graphql.mutations.field.set_field_value_mutation import \
    SetFieldValueMutation
from task_management.graphql.mutations.field.update_field_mutation import \
    UpdateFieldMutation
from task_management.graphql.mutations.folder.create_folder_mutation import \
    CreateFolderMutation
from task_management.graphql.mutations.folder.delete_folder_mutation import \
    DeleteFolderMutation
from task_management.graphql.mutations.folder.reorder_folder_mutation import \
    ReorderFolderMutation
from task_management.graphql.mutations.folder.set_folder_visibility_mutation import \
    SetFolderVisibilityMutation
from task_management.graphql.mutations.folder.update_folder_mutation import \
    UpdateFolderMutation
from task_management.graphql.mutations.list.create_list_mutation import \
    CreateListMutation
from task_management.graphql.mutations.list.delete_list_mutation import \
    DeleteListMutation
from task_management.graphql.mutations.list.reorder_list_in_folder_mutation import \
    ReorderListInFolderMutation
from task_management.graphql.mutations.list.reorder_list_in_pace import \
    ReorderListInSpaceMutation
from task_management.graphql.mutations.list.set_list_visibility import \
    SetListVisibilityMutation
from task_management.graphql.mutations.list.update_list_mutation import \
    UpdateListMutation
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
from task_management.graphql.mutations.task.assign_task_assignee_mutation import \
    AssignTaskAssigneeMutation
from task_management.graphql.mutations.task.create_task_mutation import \
    CreateTaskMutation
from task_management.graphql.mutations.task.delete_task_mutation import \
    DeleteTaskMutation
from task_management.graphql.mutations.task.remove_task_assignee_mutation import \
    RemoveTaskAssigneeMutation
from task_management.graphql.mutations.task.reorder_task_mutation import \
    ReorderTaskMutation
from task_management.graphql.mutations.task.update_task_mutation import \
    UpdateTaskMutation
from task_management.graphql.mutations.user.block_user_mutation import \
    BlockUserMutation
from task_management.graphql.mutations.user.create_user_mutation import \
    CreateUserMutation
from task_management.graphql.mutations.user.forgot_password_mutation import \
    ForgotPasswordMutation, ResetPasswordMutation
from task_management.graphql.mutations.user.update_user_mutation import \
    UpdateUserMutation
from task_management.graphql.mutations.user.user_login_mutation import \
    UserLoginMutation
from task_management.graphql.mutations.view.apply_list_view_mutation import \
    ApplyListViewMutation
from task_management.graphql.mutations.view.create_view_mutation import \
    CreateViewMutation
from task_management.graphql.mutations.view.remove_list_view_mutation import \
    RemoveListViewMutation
from task_management.graphql.mutations.view.update_view_mutation import \
    UpdateViewMutation
from task_management.graphql.mutations.workspace.add_workspace_member_mutation import \
    AddMemberToWorkspaceMutation
from task_management.graphql.mutations.workspace.change_workspace_member_role import \
    ChangeMemberRoleMutation
from task_management.graphql.mutations.workspace.create_workspace_mutation import \
    CreateWorkspaceMutation
from task_management.graphql.mutations.workspace.delete_workspace_mutation import \
    DeleteWorkspaceMutation
from task_management.graphql.mutations.workspace.remove_workspace_member_mutation import \
    RemoveMemberFromWorkspaceMutation
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


class CreateFolder(graphene.ObjectType):
    create_folder = CreateFolderMutation.Field(required=True)


class UpdateFolder(graphene.ObjectType):
    update_folder = UpdateFolderMutation.Field(required=True)


class DeleteFolder(graphene.ObjectType):
    delete_folder = DeleteFolderMutation.Field(required=True)


class ReorderFolder(graphene.ObjectType):
    reorder_folder = ReorderFolderMutation.Field(required=True)


class SetFolderVisibility(graphene.ObjectType):
    set_folder_visibility = SetFolderVisibilityMutation.Field(required=True)


class CreateList(graphene.ObjectType):
    create_list = CreateListMutation.Field(required=True)


class UpdateList(graphene.ObjectType):
    update_list = UpdateListMutation.Field(required=True)


class DeleteList(graphene.ObjectType):
    delete_list = DeleteListMutation.Field(required=True)


class ReorderListInFolder(graphene.ObjectType):
    reorder_list_in_folder = ReorderListInFolderMutation.Field(required=True)


class SetListVisibility(graphene.ObjectType):
    set_list_visibility = SetListVisibilityMutation.Field(required=True)


class ReorderListInSpace(graphene.ObjectType):
    reorder_list_inspace = ReorderListInSpaceMutation.Field(required=True)


class CreateTask(graphene.ObjectType):
    create_task = CreateTaskMutation.Field(required=True)


class UpdateTask(graphene.ObjectType):
    update_task = UpdateTaskMutation.Field(required=True)


class DeleteTask(graphene.ObjectType):
    delete_task = DeleteTaskMutation.Field(required=True)


class ReorderTask(graphene.ObjectType):
    reorder_task = ReorderTaskMutation.Field(required=True)


class CreateView(graphene.ObjectType):
    create_view = CreateViewMutation.Field(required=True)


class AddMemberToWorkspace(graphene.ObjectType):
    add_member_to_workspace = AddMemberToWorkspaceMutation.Field(required=True)


class ChangeWorkspaceMemberRole(graphene.ObjectType):
    change_workspace_member_role = ChangeMemberRoleMutation.Field(
        required=True)


class RemoveMemberFromWorkspace(graphene.ObjectType):
    remove_member_from_workspace = RemoveMemberFromWorkspaceMutation.Field(
        required=True)


class TaskAssignee(graphene.ObjectType):
    task_assignee = AssignTaskAssigneeMutation.Field(required=True)


class RemoveTaskAssignee(graphene.ObjectType):
    remove_task_assignee = RemoveTaskAssigneeMutation.Field(required=True)


class UpdateView(graphene.ObjectType):
    update_view = UpdateViewMutation.Field(required=True)


class CreateField(graphene.ObjectType):
    create_field = CreateFieldMutation.Field(required=True)


class UpdateField(graphene.ObjectType):
    update_field = UpdateFieldMutation.Field(required=True)


class DeleteField(graphene.ObjectType):
    delete_field = DeleteFieldMutation.Field(required=True)


class ReorderField(graphene.ObjectType):
    reorder_field = ReorderFieldMutation.Field(required=True)


class ApplyListView(graphene.ObjectType):
    apply_list_view = ApplyListViewMutation.Field(required=True)


class RemoveListView(graphene.ObjectType):
    remove_list_view = RemoveListViewMutation.Field(required=True)



class UpdateFieldValue(graphene.ObjectType):
    update_field_value = SetFieldValueMutation.Field(required=True)


class ForgotPassword(graphene.ObjectType):
    forget_password = ForgotPasswordMutation.Field(required=True)


class ResetPassword(graphene.ObjectType):
    reset_password = ResetPasswordMutation.Field(required=True)
