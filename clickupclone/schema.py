import graphene

from task_management.graphql.schema import Query as BaseQuery
from task_management.graphql.schema import Mutation as BaseMutation


class Query(BaseQuery, graphene.ObjectType):
    pass


class Mutation(BaseMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
