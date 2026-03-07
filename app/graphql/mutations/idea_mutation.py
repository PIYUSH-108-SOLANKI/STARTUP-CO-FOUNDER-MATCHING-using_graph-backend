import graphene
from app.graphql.types.idea_type import IdeaType
from app.models.idea import IdeaModel


class CreateIdea(graphene.Mutation):
    """
    Mutation to create a new Idea node in Neo4j.
    Also creates a POSTED relationship from the student to the idea.
    
    Usage in GraphiQL:
        mutation {
          createIdea(
            title: "AI Tutor"
            domain: "edtech"
            description: "Personalised learning with AI"
            postedByStudentId: "<student-id>"
          ) {
            ok
            message
            idea { id title domain description }
          }
        }
    """

    # ── Part 1: Arguments ──────────────────────────────────────────────────
    class Arguments:
        title               = graphene.String(required=True)
        # REQUIREMENT: domain must be one of fintech, edtech, healthtech
        domain              = graphene.String(required=True)
        description         = graphene.String(required=True)
        posted_by_student_id = graphene.String(required=True)  # who is posting this?

    # ── Part 2: Return fields ──────────────────────────────────────────────
    ok      = graphene.Boolean()
    message = graphene.String()
    idea    = graphene.Field(IdeaType)

    # ── Part 3: mutate() ───────────────────────────────────────────────────
    def mutate(root, info, title, domain, description, posted_by_student_id):
        # Validate domain — only these 3 are allowed
        allowed_domains = ["fintech", "edtech", "healthtech"]
        if domain not in allowed_domains:
            return CreateIdea(
                ok=False,
                message=f"Invalid domain '{domain}'. Choose from: {allowed_domains}",
                idea=None
            )

        result = IdeaModel.create(title, domain, description, posted_by_student_id)

        if result:
            idea_obj = IdeaType(**result)
            return CreateIdea(ok=True, message="Idea created successfully!", idea=idea_obj)

        return CreateIdea(ok=False, message="Failed to create idea. Check if student ID is correct.", idea=None)


# ── Mutation root ──────────────────────────────────────────────────────────
class IdeaMutation(graphene.ObjectType):
    create_idea = CreateIdea.Field()
