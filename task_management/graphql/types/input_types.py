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
    gender = graphene.String()
    email = graphene.String()
    phone_number = graphene.String()
    image_url = graphene.String()


class CreateFieldInputParams(graphene.InputObjectType):
    field_type = graphene.String(required=True)
    field_name = graphene.String(required=True)
    description = graphene.String(required=True)
    template_id = graphene.String(required=True)
    config = graphene.JSONString(required=True)
    is_required = graphene.Boolean(required=True)
    created_by = graphene.String(required=True)


class UpdateFieldInputParams(graphene.InputObjectType):
    field_id = graphene.String(required=True)
    description = graphene.String(required=False)
    field_name = graphene.String(required=False)
    config = graphene.JSONString(required=False)
    is_required = graphene.Boolean(required=False)


class CreateTemplateInputParams(graphene.InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String(required=True)
    list_id = graphene.String(required=True)
    created_by = graphene.String(required=True)


class UserLoginInputParams(graphene.InputObjectType):
    email = graphene.String(required=True)
    password = graphene.String(required=True)


class UpdateTemplateInputParams(graphene.InputObjectType):
    template_id = graphene.String(required=True)
    name = graphene.String(required=False)
    description = graphene.String(required=False)

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
    title = graphene.String(required=True)
    description = graphene.String(required=True)


class CreateListInputParams(graphene.InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String(required=True)
    space_id = graphene.String(required=True)
    created_by = graphene.String(required=True)
    is_private = graphene.Boolean(required=True)
    folder_id = graphene.String(required=False)


class UpdateListInputParams(graphene.InputObjectType):
    list_id = graphene.String(required=True)
    name = graphene.String(required=False)
    description = graphene.String(required=False)


class CreateViewInputParams(graphene.InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String(required=True)
    view_type = graphene.String(required=True)
    created_by = graphene.String(required=True)


class UpdateViewInputParams(graphene.InputObjectType):
    view_id = graphene.String(required=True)
    name = graphene.String(required=True)
    description = graphene.String(required=True)


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


class CreateUserSpacePermissionInputParams(graphene.InputObjectType):
    space_id = graphene.String(required=True)
    user_id = graphene.String(required=True)
    permission_type = graphene.String(required=True)
    added_by = graphene.String(required=True)

class DeleteSpaceInputParams(graphene.InputObjectType):
    space_id = graphene.String(required=True)
    user_id = graphene.String(required=True)

class SetSpaceVisibilityInputParams(graphene.InputObjectType):
    space_id = graphene.String(required=True)
    user_id = graphene.String(required=True)
    visibility = graphene.String(required=True)


class GetWorkspaceSpacesInputParams(graphene.InputObjectType):
    workspace_id = graphene.String(required=True)


class GetSpacePermissionsInputParams(graphene.InputObjectType):
    space_id = graphene.String(required=True)


class GetSpaceInputParams(graphene.InputObjectType):
    space_id = graphene.String(required=True)


class CreateUserFolderPermissionInputParams(graphene.InputObjectType):
    folder_id = graphene.String(required=True)
    user_id = graphene.String(required=True)
    permission_type = graphene.String(required=True)
    added_by = graphene.String(required=True)

class ReorderSpaceInputParams(graphene.InputObjectType):
    workspace_id = graphene.String(required=True)
    space_id = graphene.String(required=True)
    order = graphene.Int(required=True)
    user_id = graphene.String(required=True)

class CreateUserListPermissionInputParams(graphene.InputObjectType):
    list_id = graphene.String(required=True)
    permission_type = graphene.String(required=True)
    user_id = graphene.String(required=True)
    added_by = graphene.String(required=True)


class UpdateFieldValueInputParams(graphene.InputObjectType):
    task_id = graphene.String(required=True)
    field_id = graphene.String(required=True)
    value = graphene.String(required=True)


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


class FilterInputParams(graphene.InputObjectType):
    list_id = graphene.String(required=True)
    field_filters = graphene.JSONString(required=False)
    assignees = graphene.List(graphene.String, required=False)
    offset = graphene.Int(required=False, default_value=1)
    limit = graphene.Int(required=False, default_value=10)
