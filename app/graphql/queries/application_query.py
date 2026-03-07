import graphene
from app.graphql.types.application_type import ApplicationType
from app.models.application import ApplicationModel


class ApplicationQuery(graphene.ObjectType):
    """
    All READ operations related to Applications.
    
    Available in GraphiQL:
        query { allApplications { id role status studentId ideaId } }
    """

    all_applications = graphene.List(ApplicationType)

    def resolve_all_applications(root, info):
        applications = ApplicationModel.get_all()
        return [ApplicationType(**a) for a in applications]
