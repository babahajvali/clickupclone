import graphene

from task_management.graphql.resolvers.space.get_workspace_spaces_resolver import \
    get_workspace_spaces_resolver
from task_management.graphql.resolvers.user.get_user_resolver import \
    get_user_profile_resolver
from task_management.graphql.resolvers.workspace.get_workspace_resolver import \
    get_workspace_resolver
from task_management.graphql.types.input_types import \
    GetUserProfileInputParams, GetWorkspaceInputParams, \
    GetWorkspaceSpacesInputParams
from task_management.graphql.types.response_types import \
    GetUserProfileResponse, GetWorkspaceResponse, GetWorkspaceSpacesResponse


class GetUser(graphene.ObjectType):
    get_user_profile = graphene.Field(
        GetUserProfileResponse,
        params=GetUserProfileInputParams(required=True),
        resolver=get_user_profile_resolver
    )


class GetWorkspace(graphene.ObjectType):
    get_workspace = graphene.Field(
        GetWorkspaceResponse,
        params=GetWorkspaceInputParams(required=True),
        resolver=get_workspace_resolver
    )


class GetWorkspaceSpaces(graphene.ObjectType):
    get_workspace_spaces = graphene.Field(
        GetWorkspaceSpacesResponse,
        params=GetWorkspaceSpacesInputParams(required=True),
        resolver=get_workspace_spaces_resolver
    )
