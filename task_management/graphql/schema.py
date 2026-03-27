import graphene

from task_management.graphql.mutations import CreateAccount, CreateUser, \
    UpdateUser, BlockUser, UserLogin, DeleteAccount, \
    CreateWorkspace, TransferWorkspace, DeleteWorkspace, UpdateWorkspace, \
    CreateSpace, UpdateSpace, DeleteSpace, ReorderSpace, SetSpaceVisibility, \
    CreateFolder, UpdateFolder, DeleteFolder, ReorderFolder, \
    SetFolderVisibility, CreateList, UpdateList, DeleteList, \
    ReorderListInFolder, SetListVisibility, ReorderListInSpace, CreateTask, \
    UpdateTask, ReorderTask, DeleteTask, AddMemberToWorkspace, \
    ChangeWorkspaceMemberRole, RemoveMemberFromWorkspace, TaskAssignee, \
    RemoveTaskAssignee, UpdateField, CreateField, DeleteField, \
    ReorderField, ApplyListView, RemoveListView, UpdateFieldValue, \
    ForgotPassword, ResetPassword, ValidateResetToken, UpdateAccount, \
    AddUserForListPermission, UpdateListView
from task_management.graphql.mutations.subscription_mutations import \
    SubscriptionMutations
from task_management.graphql.queries import GetUser, GetWorkspace, \
    GetWorkspaceSpaces, GetSpace, GetSpaceFolders, GetFolder, GetList, \
    GetFolderLists, GetSpaceLists, GetTaskFilters, GetTask, GetListTasks, \
    GetTaskAssignees, GetViews, GetTemplateFields, GetFields, GetListViews, \
    GetUserWorkspaces, GetWorkspaceMembers, GetUserTasks, \
    GetAccounts, GetUserWithEmail
from task_management.graphql.subscription_queries import SubscriptionQueries

QUERY_CLASSES = [
    GetUser, GetWorkspace, GetWorkspaceSpaces, GetSpace, GetSpaceFolders,
    GetFolder, GetList, GetFolderLists, GetSpaceLists, GetTaskFilters, GetTask,
    GetListTasks, GetTaskAssignees, GetViews, GetTemplateFields, GetFields,
    GetListViews, GetUserWorkspaces, GetWorkspaceMembers,
    GetUserTasks, GetAccounts, GetUserWithEmail, SubscriptionQueries]

MUTATION_CLASSES = [
    CreateAccount, CreateUser, UpdateUser, BlockUser, UserLogin, DeleteAccount,
    CreateWorkspace, TransferWorkspace, DeleteWorkspace, UpdateWorkspace,
    CreateSpace, UpdateSpace, SetSpaceVisibility, ReorderSpace, DeleteSpace,
    CreateFolder, UpdateFolder, DeleteFolder, ReorderFolder,
    SetFolderVisibility, CreateList, UpdateList, DeleteList,
    ReorderListInFolder, SetListVisibility, ReorderListInSpace, CreateTask,
    UpdateTask, ReorderTask, DeleteTask, AddMemberToWorkspace,
    TaskAssignee, ChangeWorkspaceMemberRole, RemoveMemberFromWorkspace,
    RemoveTaskAssignee, UpdateField, CreateField, DeleteField, UpdateListView,
    ReorderField, ApplyListView, RemoveListView, ResetPassword,
    UpdateFieldValue, ForgotPassword, ValidateResetToken, UpdateAccount,
    AddUserForListPermission, SubscriptionMutations]


class Query(*QUERY_CLASSES, graphene.ObjectType):
    pass


class Mutation(*MUTATION_CLASSES, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
