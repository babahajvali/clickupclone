import graphene


class CreateAccountInputParams(graphene.InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String(required=True)
    owner_id = graphene.String(required=True)


class CreateUserInputParams(graphene.InputObjectType):
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    full_name = graphene.String(required=True)
    gender = graphene.String(required=True)
    username = graphene.String(required=True)
    phone_number = graphene.String(required=True)
    image_url = graphene.String(required=True)


class UpdateUserInputParams(graphene.InputObjectType):
    user_id = graphene.String(required=True)
    full_name = graphene.String()
    username = graphene.String()
    gender = graphene.String(required=False)
    email = graphene.String()
    phone_number = graphene.String()
    image_url = graphene.String()


class CreateFieldInputParams(graphene.InputObjectType):
    field_type = graphene.String(required=True)
    field_name = graphene.String(required=True)
    description = graphene.String(required=True)
    template_id = graphene.String(required=True)
    config = graphene.JSONString()
    is_required = graphene.Boolean(required=True)
    created_by = graphene.String(required=True)


class UpdateFieldInputParams(graphene.InputObjectType):
    field_id = graphene.String(required=True)
    description = graphene.String(required=False)
    field_name = graphene.String(required=False)
    config = graphene.JSONString(required=False)
    is_required = graphene.Boolean(required=False)
    user_id = graphene.String(required=True)


class CreateTemplateInputParams(graphene.InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String(required=True)
    list_id = graphene.String(required=True)
    created_by = graphene.String(required=True)


class UserLoginInputParams(graphene.InputObjectType):
    email = graphene.String(required=True)
    password = graphene.String(required=True)


class TransferAccountInputParams(graphene.InputObjectType):
    account_id = graphene.String(required=True)
    old_owner_id = graphene.String(required=True)
    new_owner_id = graphene.String(required=True)


class DeleteWorkspaceInputParams(graphene.InputObjectType):
    workspace_id = graphene.String(required=True)
    user_id = graphene.String(required=True)


class TransferWorkspaceInputParams(graphene.InputObjectType):
    workspace_id = graphene.String(required=True)
    user_id = graphene.String(required=True)
    new_user_id = graphene.String(required=True)


class GetWorkspaceInputParams(graphene.InputObjectType):
    workspace_id = graphene.String(required=True)


class DeleteAccountInputParams(graphene.InputObjectType):
    account_id = graphene.String(required=True)
    deleted_by = graphene.String(required=True)


class GetUserProfileInputParams(graphene.InputObjectType):
    user_id = graphene.String(required=True)


class BlockUserInputParams(graphene.InputObjectType):
    user_id = graphene.String(required=True)


class CreateTaskInputParams(graphene.InputObjectType):
    title = graphene.String(required=True)
    description = graphene.String(required=True)
    list_id = graphene.String(required=True)
    created_by = graphene.String(required=True)


class UpdateTaskInputParams(graphene.InputObjectType):
    task_id = graphene.String(required=True)
    title = graphene.String()
    description = graphene.String()
    user_id = graphene.String(required=True)


class CreateListInputParams(graphene.InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String(required=True)
    space_id = graphene.String(required=True)
    created_by = graphene.String(required=True)
    is_private = graphene.Boolean(required=True)
    folder_id = graphene.String()


class UpdateListInputParams(graphene.InputObjectType):
    list_id = graphene.String(required=True)
    name = graphene.String(required=False)
    description = graphene.String(required=False)
    user_id = graphene.String(required=True)


class CreateViewInputParams(graphene.InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String(required=True)
    view_type = graphene.String(required=True)
    created_by = graphene.String(required=True)


class UpdateViewInputParams(graphene.InputObjectType):
    view_id = graphene.String(required=True)
    name = graphene.String()
    description = graphene.String()


class CreateFolderInputParams(graphene.InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String(required=True)
    space_id = graphene.String(required=True)
    created_by = graphene.String(required=True)
    is_private = graphene.Boolean(required=True)


class UpdateFolderInputParams(graphene.InputObjectType):
    folder_id = graphene.String(required=True)
    name = graphene.String(required=False)
    description = graphene.String(required=False)
    user_id = graphene.String(required=True)


class DeleteFolderInputParams(graphene.InputObjectType):
    folder_id = graphene.String(required=True)
    user_id = graphene.String(required=True)


class CreateSpaceInputParams(graphene.InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String(required=True)
    workspace_id = graphene.String(required=True)
    is_private = graphene.Boolean(required=True)
    created_by = graphene.String(required=True)


class UpdateSpaceInputParams(graphene.InputObjectType):
    space_id = graphene.String(required=True)
    name = graphene.String(required=False)
    description = graphene.String(required=False)
    user_id = graphene.String(required=True)


class CreateWorkspaceInputParams(graphene.InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String(required=True)
    user_id = graphene.String(required=True)
    account_id = graphene.String(required=True)


class UpdateWorkspaceInputParams(graphene.InputObjectType):
    workspace_id = graphene.String(required=True)
    name = graphene.String(required=False)
    description = graphene.String(required=False)
    user_id = graphene.String(required=True)


class AddMemberToWorkspaceInputParams(graphene.InputObjectType):
    workspace_id = graphene.String(required=True)
    user_id = graphene.String(required=True)
    role = graphene.String(required=True)
    added_by = graphene.String(required=True)


class ChangeWorkspaceMemberRoleInputParams(graphene.InputObjectType):
    workspace_id = graphene.String(required=True)
    user_id = graphene.String(required=True)
    role = graphene.String(required=True)
    changed_by = graphene.String(required=True)


class RemoveWorkspaceMemberInputParams(graphene.InputObjectType):
    workspace_member_id = graphene.Int(required=True)
    removed_by = graphene.String(required=True)


class DeleteSpaceInputParams(graphene.InputObjectType):
    space_id = graphene.String(required=True)
    user_id = graphene.String(required=True)


class SetSpaceVisibilityInputParams(graphene.InputObjectType):
    space_id = graphene.String(required=True)
    user_id = graphene.String(required=True)
    visibility = graphene.String(required=True)


class GetWorkspaceSpacesInputParams(graphene.InputObjectType):
    workspace_id = graphene.String(required=True)


class GetSpaceInputParams(graphene.InputObjectType):
    space_id = graphene.String(required=True)


class ReorderSpaceInputParams(graphene.InputObjectType):
    workspace_id = graphene.String(required=True)
    space_id = graphene.String(required=True)
    order = graphene.Int(required=True)
    user_id = graphene.String(required=True)


class CreateFieldValueInputParams(graphene.InputObjectType):
    task_id = graphene.String(required=True)
    field_id = graphene.String(required=True)
    value = graphene.String(required=True)
    created_by = graphene.String(required=True)


class CreateAccountMemberInputParams(graphene.InputObjectType):
    account_id = graphene.String(required=True)
    user_id = graphene.String(required=True)
    role = graphene.String(required=True)
    added_by = graphene.String(required=True)


class ReorderFolderInputParams(graphene.InputObjectType):
    space_id = graphene.String(required=True)
    folder_id = graphene.String(required=True)
    user_id = graphene.String(required=True)
    order = graphene.Int(required=True)


class SetFolderVisibilityInputParams(graphene.InputObjectType):
    folder_id = graphene.String(required=True)
    user_id = graphene.String(required=True)
    visibility = graphene.String(required=True)


class GetSpaceFoldersInputParams(graphene.InputObjectType):
    space_id = graphene.String(required=True)


class GetFolderInputParams(graphene.InputObjectType):
    folder_id = graphene.String(required=True)


class DeleteListInputParams(graphene.InputObjectType):
    list_id = graphene.String(required=True)
    user_id = graphene.String(required=True)


class ReorderListInFolderInputParams(graphene.InputObjectType):
    folder_id = graphene.String(required=True)
    list_id = graphene.String(required=True)
    order = graphene.Int(required=True)
    user_id = graphene.String(required=True)


class ReorderListInSpaceInputParams(graphene.InputObjectType):
    space_id = graphene.String(required=True)
    list_id = graphene.String(required=True)
    order = graphene.Int(required=True)
    user_id = graphene.String(required=True)


class SetListVisibilityInputParams(graphene.InputObjectType):
    list_id = graphene.String(required=True)
    user_id = graphene.String(required=True)
    visibility = graphene.String(required=True)


class GetFolderListsInputParams(graphene.InputObjectType):
    folder_id = graphene.String(required=True)


class GetSpaceListsInputParams(graphene.InputObjectType):
    space_id = graphene.String(required=True)


class GetListInputParams(graphene.InputObjectType):
    list_id = graphene.String(required=True)


class DeleteTaskInputParams(graphene.InputObjectType):
    task_id = graphene.String(required=True)
    user_id = graphene.String(required=True)


class ReorderTaskInputParams(graphene.InputObjectType):
    task_id = graphene.String(required=True)
    order = graphene.Int(required=True)
    user_id = graphene.String(required=True)


class GetListTasksInputParams(graphene.InputObjectType):
    list_id = graphene.String(required=True)


class GetTaskInputParams(graphene.InputObjectType):
    task_id = graphene.String(required=True)


class TaskFilterInputParams(graphene.InputObjectType):
    list_id = graphene.String(required=True)
    user_id = graphene.String(required=True)
    field_filters = graphene.JSONString()
    assignees = graphene.List(graphene.String, )
    offset = graphene.Int(required=False, default_value=1)
    limit = graphene.Int(required=False, default_value=10)


class CreateTaskAssigneeInputParams(graphene.InputObjectType):
    task_id = graphene.String(required=True)
    user_id = graphene.String(required=True)
    assigned_by = graphene.String(required=True)


class RemoveTaskAssigneeInputParams(graphene.InputObjectType):
    assign_id = graphene.String(required=True)
    user_id = graphene.String(required=True)


class GetTaskAssigneesInputParams(graphene.InputObjectType):
    task_id = graphene.String(required=True)


class ReorderFieldInputParams(graphene.InputObjectType):
    field_id = graphene.String(required=True)
    template_id = graphene.String(required=True)
    new_order = graphene.Int(required=True)
    user_id = graphene.String(required=True)


class DeleteFieldInputParams(graphene.InputObjectType):
    field_id = graphene.String(required=True)
    user_id = graphene.String(required=True)


class GetFieldsForTemplateInputParams(graphene.InputObjectType):
    template_id = graphene.String(required=True)


class GetFieldInputParams(graphene.InputObjectType):
    field_id = graphene.String(required=True)


class ApplyListViewInputParams(graphene.InputObjectType):
    view_id = graphene.String(required=True)
    list_id = graphene.String(required=True)
    user_id = graphene.String(required=True)


class RemoveListViewInputParams(graphene.InputObjectType):
    list_id = graphene.String(required=True)
    user_id = graphene.String(required=True)
    view_id = graphene.String(required=True)


class GetListViewsInputParams(graphene.InputObjectType):
    list_id = graphene.String(required=True)


class UpdateAccountMemberRoleInputParams(graphene.InputObjectType):
    account_member_id = graphene.Int(required=True)
    role = graphene.String(required=True)
    changed_by = graphene.String(required=True)


class RemoveAccountMemberInputParams(graphene.InputObjectType):
    account_member_id = graphene.Int(required=True)
    removed_by = graphene.String(required=True)
