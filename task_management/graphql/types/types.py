import graphene


class AccountType(graphene.ObjectType):
    account_id = graphene.String(required=True)
    name = graphene.String(required=True)
    description = graphene.String(required=True)
    owner_id = graphene.String(required=True)
    is_active = graphene.Boolean(required=True)


class UserType(graphene.ObjectType):
    user_id = graphene.String(required=True)
    username = graphene.String(required=True)
    email = graphene.String(required=True)
    full_name = graphene.String(required=True)
    is_active = graphene.Boolean(required=True)
    phone_number = graphene.String(required=True)
    gender = graphene.String(required=True)
    image_url = graphene.String()


class WorkspaceType(graphene.ObjectType):
    workspace_id = graphene.String(required=True)
    name = graphene.String(required=True)
    description = graphene.String(required=True)
    user_id = graphene.String(required=True)
    account_id = graphene.String(required=True)
    is_active = graphene.Boolean(required=True)


class WorkspaceMemberType(graphene.ObjectType):
    id = graphene.Int(required=True)
    workspace_id = graphene.String(required=True)
    user_id = graphene.String(required=True)
    role = graphene.String(required=True)
    is_active = graphene.Boolean(required=True)
    added_by = graphene.String(required=True)


class SpaceType(graphene.ObjectType):
    space_id = graphene.String(required=True)
    name = graphene.String(required=True)
    description = graphene.String(required=True)
    workspace_id = graphene.String(required=True)
    order = graphene.Int(required=True)
    is_active = graphene.Boolean(required=True)
    is_private = graphene.Boolean(required=True)
    created_by = graphene.String(required=True)

class WorkspaceSpacesType(graphene.ObjectType):
    spaces = graphene.List(SpaceType)

class FolderType(graphene.ObjectType):
    folder_id = graphene.String()
    name = graphene.String(required=True)
    description = graphene.String(required=True)
    space_id = graphene.String(required=True)
    order = graphene.Int(required=True)
    is_active = graphene.Boolean(required=True)
    created_by = graphene.String(required=True)
    is_private = graphene.Boolean(required=True)


class SpaceFoldersType(graphene.ObjectType):
    folders = graphene.List(FolderType)


class ListType(graphene.ObjectType):
    list_id = graphene.String(required=True)
    name = graphene.String(required=True)
    description = graphene.String(required=True)
    space_id = graphene.String(required=True)
    is_active = graphene.Boolean(required=True)
    order = graphene.Int(required=True)
    is_private = graphene.Boolean(required=True)
    created_by = graphene.String(required=True)
    folder_id = graphene.String()

class ListsType(graphene.ObjectType):
    lists = graphene.List(ListType)

class TaskType(graphene.ObjectType):
    task_id = graphene.String(required=True)
    title = graphene.String(required=True)
    description = graphene.String(required=True)
    list_id = graphene.String(required=True)
    order = graphene.Int(required=True)
    created_by = graphene.String(required=True)
    is_delete = graphene.Boolean(required=True)

class TasksType(graphene.ObjectType):
    tasks = graphene.List(TaskType)

class TaskAssigneeType(graphene.ObjectType):
    assign_id = graphene.String(required=True)
    user_id = graphene.String(required=True)
    task_id = graphene.String(required=True)
    assigned_by = graphene.String(required=True)
    is_active = graphene.Boolean(required=True)

class TaskAssigneesType(graphene.ObjectType):
    assignees = graphene.List(TaskAssigneeType)


class TemplateType(graphene.ObjectType):
    template_id = graphene.String(required=True)
    name = graphene.String(required=True)
    list_id = graphene.String(required=True)
    description = graphene.String(required=True)
    created_by = graphene.String(required=True)


class FieldType(graphene.ObjectType):
    field_id = graphene.String(required=True)
    field_type = graphene.String(required=True)
    description = graphene.String(required=True)
    template_id = graphene.String(required=True)
    field_name = graphene.String(required=True)
    is_active = graphene.String(required=True)
    order = graphene.Int(required=True)
    config = graphene.JSONString(required=True)
    is_required = graphene.Boolean(required=True)
    created_by = graphene.String(required=True)

class FieldsType(graphene.ObjectType):
    fields = graphene.List(FieldType)

class ViewType(graphene.ObjectType):
    view_id = graphene.String(required=True)
    name = graphene.String(required=True)
    description = graphene.String(required=True)
    view_type = graphene.String(required=True)
    created_by = graphene.String(required=True)

class ViewsType(graphene.ObjectType):
    views = graphene.List(ViewType)


class UserSpacePermissionType(graphene.ObjectType):
    id = graphene.Int(required=True)
    space_id = graphene.String(required=True)
    permission_type = graphene.String(required=True)
    user_id = graphene.String(required=True)
    is_active = graphene.Boolean(required=True)
    added_by = graphene.String(required=True)


class UserFolderPermissionType(graphene.ObjectType):
    id = graphene.Int(required=True)
    folder_id = graphene.String(required=True)
    permission_type = graphene.String(required=True)
    user_id = graphene.String(required=True)
    is_active = graphene.Boolean(required=True)
    added_by = graphene.String(required=True)


class UserListPermissionType(graphene.ObjectType):
    id = graphene.Int(required=True)
    list_id = graphene.String(required=True)
    permission_type = graphene.String(required=True)
    user_id = graphene.String(required=True)
    is_active = graphene.Boolean(required=True)
    added_by = graphene.String(required=True)


class AccountMemberType(graphene.ObjectType):
    id = graphene.Int(required=True)
    user_id = graphene.String(required=True)
    account_id = graphene.String(required=True)
    role = graphene.String(required=True)
    added_by = graphene.String(required=True)
    is_active = graphene.Boolean(required=True)

class ListViewType(graphene.ObjectType):
    id = graphene.Int(required=True)
    list_id = graphene.String(required=True)
    view_id = graphene.String(required=True)
    applied_by = graphene.String(required=True)
    is_active = graphene.Boolean(required=True)

class ListViewsType(graphene.ObjectType):
    list_views = graphene.List(ListViewType)