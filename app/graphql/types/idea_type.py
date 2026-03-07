import graphene

# Notice: IdeaType does NOT import MilestoneType here.
# That would cause a circular import problem.
# Instead, milestones will be queried separately.
#
# "What does an Idea LOOK LIKE in the API?"
# It has: id, title, domain, description — all strings.

class IdeaType(graphene.ObjectType):
    id          = graphene.String()  # unique identifier
    title       = graphene.String()  # e.g. "AI Tutor App"
    domain      = graphene.String()  # one of: fintech, edtech, healthtech
    description = graphene.String()  # short description of the idea
