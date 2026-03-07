from app.graphql.queries.student_query import StudentQuery
from app.graphql.queries.idea_query import IdeaQuery
from app.graphql.queries.application_query import ApplicationQuery
from app.graphql.queries.milestone_query import MilestoneQuery

# This file combines all individual query classes into one single Query class.
#
# HOW MULTIPLE INHERITANCE WORKS HERE:
# Python reads from left to right → StudentQuery, IdeaQuery, ApplicationQuery, MilestoneQuery
# Each class brings its own fields and resolvers.
# The final Query class has ALL of them merged together automatically.
#
# This is exactly how large GraphQL APIs are structured in production.

import graphene

class Query(
    StudentQuery,
    IdeaQuery,
    ApplicationQuery,
    MilestoneQuery,
    graphene.ObjectType   # must always be last
):
    pass   # no extra code needed — everything is inherited from above
