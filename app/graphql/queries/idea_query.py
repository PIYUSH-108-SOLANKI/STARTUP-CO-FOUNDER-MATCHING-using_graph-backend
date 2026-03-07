import graphene
from app.graphql.types.idea_type import IdeaType
from app.models.idea import IdeaModel


class IdeaQuery(graphene.ObjectType):
    """
    All READ operations related to Ideas.

    Available in GraphiQL:
        query { ideas(domain: "fintech") { title } }   ← matches assignment spec exactly
        query { allIdeas { id title domain } }
        query { idea(id: "...") { title domain description } }
    """

    # 'ideas' with optional domain — matches assignment spec: query { ideas(domain:"fintech"){ title } }
    ideas          = graphene.List(IdeaType, domain=graphene.String())
    all_ideas      = graphene.List(IdeaType)
    idea           = graphene.Field(IdeaType, id=graphene.String(required=True))

    def resolve_ideas(root, info, domain=None):
        # If domain is provided → filter. If not → return all.
        # This handles BOTH: ideas(domain:"fintech") AND ideas()
        if domain:
            return [IdeaType(**i) for i in IdeaModel.get_by_domain(domain)]
        return [IdeaType(**i) for i in IdeaModel.get_all()]

    def resolve_all_ideas(root, info):
        return [IdeaType(**i) for i in IdeaModel.get_all()]

    def resolve_idea(root, info, id):
        idea = IdeaModel.get_by_id(id)
        return IdeaType(**idea) if idea else None
