import graphene
from app.graphql.types.student_type import StudentType
from app.models.student import StudentModel


class StudentQuery(graphene.ObjectType):
    """
    All READ operations related to Students.
    
    Available in GraphiQL:
        query { allStudents { id name email } }
        query { student(id: "...") { name email } }
    """

    all_students = graphene.List(StudentType)
    student      = graphene.Field(StudentType, id=graphene.String(required=True))

    def resolve_all_students(root, info):
        students = StudentModel.get_all()
        return [StudentType(**s) for s in students]

    def resolve_student(root, info, id):
        student = StudentModel.get_by_id(id)
        return StudentType(**student) if student else None
