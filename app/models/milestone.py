import uuid
from app.core.database import db

class MilestoneModel:

    @staticmethod
    def create(idea_id, title):
        # REQUIREMENT: Milestone tracking
        # We create a Milestone node and connect it to its Idea
        # with a HAS_MILESTONE relationship
        #
        # MATCH (i:Idea ...) = find the idea this milestone belongs to
        # CREATE (m:Milestone {...}) = create the milestone node
        # CREATE (i)-[:HAS_MILESTONE]->(m) = link idea to milestone
        query = """
        MATCH (i:Idea {id: $idea_id})
        CREATE (m:Milestone {
            id: $id,
            title: $title,
            status: 'pending'
        })
        CREATE (i)-[:HAS_MILESTONE]->(m)
        RETURN m
        """
        parameters = {
            "id": str(uuid.uuid4()),
            "idea_id": idea_id,
            "title": title
        }
        result = db.execute_query(query, parameters)
        return result[0]["m"] if result else None

    @staticmethod
    def get_by_idea(idea_id):
        # Get ALL milestones that belong to a specific idea
        # We traverse the graph: Idea -[:HAS_MILESTONE]-> Milestone
        query = """
        MATCH (i:Idea {id: $idea_id})-[:HAS_MILESTONE]->(m:Milestone)
        RETURN m
        """
        parameters = {"idea_id": idea_id}
        result = db.execute_query(query, parameters)
        return [row["m"] for row in result]

    @staticmethod
    def update_status(milestone_id, new_status):
        # Update a milestone's status (e.g., pending → completed)
        query = """
        MATCH (m:Milestone {id: $id})
        SET m.status = $status
        RETURN m
        """
        parameters = {"id": milestone_id, "status": new_status}
        result = db.execute_query(query, parameters)
        return result[0]["m"] if result else None
