import uuid
from app.core.database import db

class ApplicationModel:

    @staticmethod
    def apply(student_id, idea_id, role):
        # REQUIREMENT: Duplicate application prevention
        check_query = """
        MATCH (s:Student {id: $student_id})-[a:APPLIED_TO]->(i:Idea {id: $idea_id})
        RETURN a
        """
        existing = db.execute_query(check_query, {"student_id": student_id, "idea_id": idea_id})
        if existing:
            return None  # Already applied — signal duplicate to the mutation

        # Instead of returning the whole relationship object (a),
        # we return each property individually using aliases.
        # This gives us a plain Python dict — safely unpackable with **
        query = """
        MATCH (s:Student {id: $student_id})
        MATCH (i:Idea {id: $idea_id})
        CREATE (s)-[a:APPLIED_TO {
            id: $id,
            role: $role,
            status: 'applied'
        }]->(i)
        RETURN a.id AS id,
               a.role AS role,
               a.status AS status,
               s.id AS student_id,
               i.id AS idea_id
        """
        parameters = {
            "id": str(uuid.uuid4()),
            "student_id": student_id,
            "idea_id": idea_id,
            "role": role
        }
        result = db.execute_query(query, parameters)
        # result[0] is now a plain dict:
        # {"id": "...", "role": "...", "status": "applied", "student_id": "...", "idea_id": "..."}
        return result[0] if result else None

    @staticmethod
    def update_status(application_id, new_status):
        # Return individual properties — not the whole relationship object
        query = """
        MATCH (s:Student)-[a:APPLIED_TO {id: $application_id}]->(i:Idea)
        SET a.status = $status
        RETURN a.id AS id,
               a.role AS role,
               a.status AS status,
               s.id AS student_id,
               i.id AS idea_id
        """
        parameters = {"application_id": application_id, "status": new_status}
        result = db.execute_query(query, parameters)
        return result[0] if result else None

    @staticmethod
    def create_partnership(application_id):
        # REQUIREMENT: Partnership creation when accepted
        query = """
        MATCH (applicant:Student)-[a:APPLIED_TO {id: $application_id}]->(i:Idea)
        MATCH (founder:Student)-[:POSTED]->(i)
        MERGE (applicant)-[:PARTNERS_WITH {ideaId: i.id}]->(founder)
        RETURN applicant.name AS applicant_name, founder.name AS founder_name, i.title AS idea_title
        """
        parameters = {"application_id": application_id}
        result = db.execute_query(query, parameters)
        return result[0] if result else None

    @staticmethod
    def get_all():
        # Return individual properties with student_id and idea_id included
        query = """
        MATCH (s:Student)-[a:APPLIED_TO]->(i:Idea)
        RETURN a.id AS id,
               a.role AS role,
               a.status AS status,
               s.id AS student_id,
               i.id AS idea_id
        """
        result = db.execute_query(query)
        return result  # already a list of plain dicts
