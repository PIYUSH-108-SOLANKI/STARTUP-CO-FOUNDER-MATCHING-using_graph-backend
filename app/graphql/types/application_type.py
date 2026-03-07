import graphene

# Remember: in Neo4j, Application is a RELATIONSHIP (APPLIED_TO)
# not a node. But in GraphQL, we still represent it as a Type
# with its own fields.
#
# The APPLIED_TO relationship has these properties:
#   id     → unique ID of the application itself
#   role   → what role the student wants (e.g. "developer", "designer")
#   status → "applied", "accepted", or "rejected"
#
# We also include student_id and idea_id so the client knows
# WHO applied to WHAT.

class ApplicationType(graphene.ObjectType):
    id         = graphene.String()  # unique id of this application
    role       = graphene.String()  # role student wants in the startup
    status     = graphene.String()  # "applied" / "accepted" / "rejected"
    student_id = graphene.String()  # which student applied
    idea_id    = graphene.String()  # which idea they applied to
