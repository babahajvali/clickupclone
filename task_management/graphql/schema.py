import graphene

from task_management.graphql.mutations import CreateAccount, CreateUser, \
    UpdateUser, BlockUser, UserLogin, TransferAccount, DeleteAccount, \
    CreateWorkspace, TransferWorkspace, DeleteWorkspace, UpdateWorkspace, \
    CreateSpace, UpdateSpace, DeleteSpace, ReorderSpace, SetSpaceVisibility, \
    CreateFolder, UpdateFolder, DeleteFolder, ReorderFolder, \
    SetFolderVisibility, CreateList, UpdateList, DeleteList, \
    ReorderListInFolder, SetListVisibility, ReorderListInSpace, CreateTask, \
    UpdateTask, ReorderTask, DeleteTask, CreateView, AddMemberToWorkspace, \
    ChangeWorkspaceMemberRole, RemoveMemberFromWorkspace, TaskAssignee
from task_management.graphql.queries import GetUser, GetWorkspace, \
    GetWorkspaceSpaces, GetSpace, GetSpaceFolders, GetFolder, GetList, \
    GetFolderLists, GetSpaceLists, GetTaskFilters, GetTask, GetListTasks

QUERY_CLASSES = [GetUser, GetWorkspace, GetWorkspaceSpaces, GetSpace,
                 GetSpaceFolders, GetFolder, GetList, GetFolderLists,
                 GetSpaceLists, GetTaskFilters, GetTask, GetListTasks]

MUTATION_CLASSES = [CreateAccount, CreateUser, UpdateUser, BlockUser,
                    UserLogin, TransferAccount, DeleteAccount, CreateWorkspace,
                    TransferWorkspace, DeleteWorkspace, UpdateWorkspace,
                    CreateSpace, UpdateSpace, SetSpaceVisibility, ReorderSpace,
                    DeleteSpace, CreateFolder, UpdateFolder, DeleteFolder,
                    ReorderFolder, SetFolderVisibility, CreateList, UpdateList,
                    DeleteList, ReorderListInFolder, SetListVisibility,
                    ReorderListInSpace, CreateTask, UpdateTask, ReorderTask,
                    DeleteTask, CreateView, AddMemberToWorkspace,TaskAssignee,
                    ChangeWorkspaceMemberRole,RemoveMemberFromWorkspace]


class Query(*QUERY_CLASSES, graphene.ObjectType):
    pass


class Mutation(*MUTATION_CLASSES, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
