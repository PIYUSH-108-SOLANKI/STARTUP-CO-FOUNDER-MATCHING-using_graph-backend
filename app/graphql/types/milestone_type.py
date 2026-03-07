import graphene

# "What does a Milestone LOOK LIKE in the API?"
# It belongs to an Idea. It has a title and a status.
# Status can be: "pending" or "completed"

class MilestoneType(graphene.ObjectType):
    id     = graphene.String()  # unique identifier
    title  = graphene.String()  # e.g. "Build MVP"
    status = graphene.String()  # "pending" or "completed"
