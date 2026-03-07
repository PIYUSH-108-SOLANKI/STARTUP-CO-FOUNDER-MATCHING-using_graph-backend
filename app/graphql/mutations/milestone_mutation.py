import graphene
from app.graphql.types.milestone_type import MilestoneType
from app.models.milestone import MilestoneModel


class AddMilestone(graphene.Mutation):
    """
    REQUIREMENT: Milestone tracking.
    
    Add a new milestone to an idea. Starts with status "pending".
    
    Usage in GraphiQL:
        mutation {
          addMilestone(ideaId: "<idea-id>", title: "Build MVP") {
            ok
            message
            milestone { id title status }
          }
        }
    """

    class Arguments:
        idea_id = graphene.String(required=True)
        title   = graphene.String(required=True)

    ok        = graphene.Boolean()
    message   = graphene.String()
    milestone = graphene.Field(MilestoneType)

    def mutate(root, info, idea_id, title):
        result = MilestoneModel.create(idea_id, title)

        if result:
            milestone_obj = MilestoneType(**result)
            return AddMilestone(ok=True, message="Milestone added!", milestone=milestone_obj)

        return AddMilestone(ok=False, message="Failed. Check if idea ID is correct.", milestone=None)


class UpdateMilestoneStatus(graphene.Mutation):
    """
    Mark a milestone as completed (or back to pending).
    
    Usage in GraphiQL:
        mutation {
          updateMilestoneStatus(milestoneId: "<id>", status: "completed") {
            ok
            milestone { title status }
          }
        }
    """

    class Arguments:
        milestone_id = graphene.String(required=True)
        status       = graphene.String(required=True)  # "pending" or "completed"

    ok        = graphene.Boolean()
    message   = graphene.String()
    milestone = graphene.Field(MilestoneType)

    def mutate(root, info, milestone_id, status):
        allowed = ["pending", "completed"]
        if status not in allowed:
            return UpdateMilestoneStatus(
                ok=False,
                message=f"Invalid status. Choose 'pending' or 'completed'.",
                milestone=None
            )

        result = MilestoneModel.update_status(milestone_id, status)

        if result:
            milestone_obj = MilestoneType(**result)
            return UpdateMilestoneStatus(ok=True, message=f"Milestone marked as {status}!", milestone=milestone_obj)

        return UpdateMilestoneStatus(ok=False, message="Milestone not found.", milestone=None)


# ── Mutation root ──────────────────────────────────────────────────────────
class MilestoneMutation(graphene.ObjectType):
    add_milestone           = AddMilestone.Field()
    update_milestone_status = UpdateMilestoneStatus.Field()
