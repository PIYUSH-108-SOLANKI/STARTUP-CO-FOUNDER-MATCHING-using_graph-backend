import uuid
from app.core.database import db

class StudentModel:

    @staticmethod
    def create(name, email):
        # Cypher: CREATE makes a new node in the graph
        # $id, $name, $email are parameters (like ? in SQL) - safe, no injection
        # RETURN s means give back the node we just created
        query = """
        CREATE (s:Student {
            id: $id,
            name: $name,
            email: $email
        })
        RETURN s
        """
        parameters = {
            "id": str(uuid.uuid4()),  # uuid4() generates a random unique ID
            "name": name,
            "email": email
        }
        result = db.execute_query(query, parameters)
        # result is a list of dicts: [{"s": {"id": ..., "name": ..., "email": ...}}]
        # We return the first (and only) result's "s" node
        return result[0]["s"] if result else None

    @staticmethod
    def get_all():
        # MATCH (s:Student) = "Find ALL nodes with the label Student"
        # RETURN s = give me all of them
        query = """
        MATCH (s:Student)
        RETURN s
        """
        result = db.execute_query(query)
        # result is a list like: [{"s": {...}}, {"s": {...}}, ...]
        # We extract just the student data from each row
        return [row["s"] for row in result]

    @staticmethod
    def get_by_id(student_id):
        # WHERE s.id = $id = filter to only the student with this specific id
        query = """
        MATCH (s:Student)
        WHERE s.id = $id
        RETURN s
        """
        parameters = {"id": student_id}
        result = db.execute_query(query, parameters)
        return result[0]["s"] if result else None