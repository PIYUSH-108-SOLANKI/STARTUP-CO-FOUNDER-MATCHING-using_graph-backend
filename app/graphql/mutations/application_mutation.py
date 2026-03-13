import graphene
from app.graphql.types.application_type import ApplicationType
from app.models.application import ApplicationModel


# ── Input type — matches assignment spec exactly ───────────────────────────────
# mutation { applyIdea(input:{ ideaId:"..." studentId:"..." role:"CTO" }){ id } }
class ApplyIdeaInput(graphene.InputObjectType):
    idea_id    = graphene.String(required=True)
    student_id = graphene.String(required=True)
    role       = graphene.String(required=True)


class ApplyToIdea(graphene.Mutation):
    """
    REQUIREMENT: Role assignment when applying + Duplicate prevention.
    
    A student applies to an idea with a specific role.
    If they already applied, returns an error (no duplicate).
    
    Usage in GraphiQL:
        mutation {
          applyToIdea(
            studentId: "<student-id>"
            ideaId: "<idea-id>"
            role: "developer"
          ) {
            ok
            message
            application { id role status }
          }
        }
    """

    class Arguments:
        student_id = graphene.String(required=True)
        idea_id    = graphene.String(required=True)
        role       = graphene.String(required=True)  # e.g. "developer", "designer"

    ok          = graphene.Boolean()
    message     = graphene.String()
    application = graphene.Field(ApplicationType)

    def mutate(root, info, student_id, idea_id, role):
        result = ApplicationModel.apply(student_id, idea_id, role)

        # Handle errors (duplicate or founder applying to own idea)
        if result and "error" in result:
            return ApplyToIdea(
                ok=False,
                message=result["error"],
                application=None
            )
        elif result is None: # Fallback
            return ApplyToIdea(ok=False, message="Failed to apply to idea.", application=None)

        app_obj = ApplicationType(**result)
        return ApplyToIdea(ok=True, message="Application submitted!", application=app_obj)


class UpdateApplicationStatus(graphene.Mutation):
    """
    REQUIREMENT: Application workflow (applied → accepted/rejected).
    REQUIREMENT: Partnership creation when accepted.
    
    The idea founder can accept or reject an application.
    If accepted → automatically creates a PARTNERS_WITH relationship.
    
    Usage in GraphiQL:
        mutation {
          updateApplicationStatus(
            applicationId: "<app-id>"
            status: "accepted"
          ) {
            ok
            message
            application { id status }
          }
        }
    """

    class Arguments:
        application_id = graphene.String(required=True)
        # status must be "accepted" or "rejected"
        status         = graphene.String(required=True)

    ok          = graphene.Boolean()
    message     = graphene.String()
    application = graphene.Field(ApplicationType)

    def mutate(root, info, application_id, status):
        # Validate: only these two statuses are allowed here
        allowed = ["accepted", "rejected"]
        if status not in allowed:
            return UpdateApplicationStatus(
                ok=False,
                message=f"Invalid status. Choose 'accepted' or 'rejected'.",
                application=None
            )

        # Step 1: Update the status on the APPLIED_TO relationship
        result = ApplicationModel.update_status(application_id, status)

        if not result:
            return UpdateApplicationStatus(
                ok=False,
                message="Application not found.",
                application=None
            )

        # REQUIREMENT: Partnership creation when accepted
        # Step 2: If accepted, automatically create a PARTNERS_WITH relationship
        if status == "accepted":
            ApplicationModel.create_partnership(application_id)
            message = "Application accepted! Partnership created between students."
        else:
            message = "Application rejected."

        app_obj = ApplicationType(**result)
        return UpdateApplicationStatus(ok=True, message=message, application=app_obj)


# ── ApplyIdea — matches assignment spec exactly ────────────────────────────────
# mutation { applyIdea(input:{ ideaId:"..." studentId:"..." role:"CTO" }){ id } }
class ApplyIdea(graphene.Mutation):
    class Arguments:
        input = ApplyIdeaInput(required=True)

    ok          = graphene.Boolean()
    message     = graphene.String()
    application = graphene.Field(ApplicationType)

    def mutate(root, info, input):
        result = ApplicationModel.apply(input.student_id, input.idea_id, input.role)
        if result and "error" in result:
            return ApplyIdea(ok=False, message=result["error"], application=None)
        elif result is None:
            return ApplyIdea(ok=False, message="Failed to apply to idea.", application=None)

        return ApplyIdea(ok=True, message="Application submitted!", application=ApplicationType(**result))


# ── Mutation root ──────────────────────────────────────────────────────────────
class ApplicationMutation(graphene.ObjectType):
    apply_to_idea             = ApplyToIdea.Field()       # original style
    apply_idea                = ApplyIdea.Field()          # spec style with input
    update_application_status = UpdateApplicationStatus.Field()
