import graphene
from app.graphql.types.student_type import StudentType
from app.models.student import StudentModel


class CreateStudent(graphene.Mutation):
    """
    Mutation to create a new Student node in Neo4j.
    
    Usage in GraphiQL:
        mutation {
          createStudent(name: "Piyush", email: "piyush@example.com") {
            ok
            message
            student { id name email }
          }
        }
    """

    # ── Part 1: Arguments (what the client sends) ──────────────────────────
    class Arguments:
        name  = graphene.String(required=True)  # client MUST provide name
        email = graphene.String(required=True)  # client MUST provide email

    # ── Part 2: Return fields (what the API sends back) ────────────────────
    ok      = graphene.Boolean()             # True if success, False if failed
    message = graphene.String()              # e.g. "Student created!" or "Error"
    student = graphene.Field(StudentType)    # the newly created student data

    # ── Part 3: mutate() — the function that runs when mutation is called ──
    def mutate(root, info, name, email):
        result = StudentModel.create(name, email)

        if result:
            # Convert the raw dict from Neo4j into a StudentType object
            student_obj = StudentType(**result)
            return CreateStudent(ok=True, message="Student created successfully!", student=student_obj)

        return CreateStudent(ok=False, message="Failed to create student.", student=None)


# ── Mutation root: groups all student mutations together ──────────────────
class StudentMutation(graphene.ObjectType):
    create_student = CreateStudent.Field()
