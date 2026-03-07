import graphene

# ── Import the combined Query root (already assembled from all query files) ──
from app.graphql.queries.query import Query

# ── Import all individual Mutation classes ──
from app.graphql.mutations.student_mutation import CreateStudent
from app.graphql.mutations.idea_mutation import CreateIdea
from app.graphql.mutations.application_mutation import ApplyToIdea, ApplyIdea, UpdateApplicationStatus
from app.graphql.mutations.milestone_mutation import AddMilestone, UpdateMilestoneStatus


# ── Mutation root class ──────────────────────────────────────────────────────
# Just like Query uses multiple inheritance, here we list ALL mutations.
# Each line = one operation available in GraphiQL under "mutation { ... }"

class Mutation(graphene.ObjectType):

    # Student
    create_student = CreateStudent.Field()

    # Idea
    create_idea = CreateIdea.Field()

    # Application workflow
    apply_to_idea              = ApplyToIdea.Field()    # original style
    apply_idea                 = ApplyIdea.Field()       # matches assignment spec
    update_application_status  = UpdateApplicationStatus.Field()

    # Milestone tracking
    add_milestone           = AddMilestone.Field()
    update_milestone_status = UpdateMilestoneStatus.Field()


# ── The Schema — this is the SINGLE object that represents your entire API ──
# query=Query    → all the READ operations
# mutation=Mutation → all the WRITE operations
# Graphene combines them into one schema that Starlette will serve.

schema = graphene.Schema(query=Query, mutation=Mutation)