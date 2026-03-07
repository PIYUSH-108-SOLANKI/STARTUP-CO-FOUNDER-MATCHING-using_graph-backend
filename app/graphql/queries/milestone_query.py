import graphene
from app.graphql.types.milestone_type import MilestoneType
from app.models.milestone import MilestoneModel


class MilestoneQuery(graphene.ObjectType):
    """
    All READ operations related to Milestones.
    
    Available in GraphiQL:
        query { milestonesByIdea(ideaId: "...") { id title status } }
    """

    milestones_by_idea = graphene.List(
        MilestoneType,
        idea_id=graphene.String(required=True)
    )

    def resolve_milestones_by_idea(root, info, idea_id):
        milestones = MilestoneModel.get_by_idea(idea_id)
        return [MilestoneType(**m) for m in milestones]
