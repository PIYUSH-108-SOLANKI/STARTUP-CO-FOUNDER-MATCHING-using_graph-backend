import uuid
from app.core.database import db

class IdeaModel:

    @staticmethod
    def create(title, domain, description, posted_by_student_id):
        # We do TWO things in one Cypher query:
        # 1. CREATE a new Idea node
        # 2. CREATE a POSTED relationship from the Student to the Idea
        #
        # MATCH (s:Student ...) = Find the student who is posting this idea
        # CREATE (i:Idea {...}) = Create the new Idea node
        # CREATE (s)-[:POSTED]->(i) = Draw an arrow from Student to Idea
        # RETURN i = give back the idea we created
        query = """
        MATCH (s:Student {id: $student_id})
        CREATE (i:Idea {
            id: $id,
            title: $title,
            domain: $domain,
            description: $description
        })
        CREATE (s)-[:POSTED]->(i)
        RETURN i
        """
        parameters = {
            "id": str(uuid.uuid4()),
            "title": title,
            "domain": domain,
            "description": description,
            "student_id": posted_by_student_id
        }
        result = db.execute_query(query, parameters)
        return result[0]["i"] if result else None

    @staticmethod
    def get_all():
        # Simple: get every Idea node in the database
        query = """
        MATCH (i:Idea)
        RETURN i
        """
        result = db.execute_query(query)
        return [row["i"] for row in result]

    @staticmethod
    def get_by_domain(domain):
        # This is the DOMAIN FILTER requirement from your project spec!
        # WHERE i.domain = $domain filters ideas by the given domain
        # Valid values: "fintech", "edtech", "healthtech"
        query = """
        MATCH (i:Idea)
        WHERE i.domain = $domain
        RETURN i
        """
        parameters = {"domain": domain}
        result = db.execute_query(query, parameters)
        return [row["i"] for row in result]

    @staticmethod
    def get_by_id(idea_id):
        query = """
        MATCH (i:Idea)
        WHERE i.id = $id
        RETURN i
        """
        parameters = {"id": idea_id}
        result = db.execute_query(query, parameters)
        return result[0]["i"] if result else None
