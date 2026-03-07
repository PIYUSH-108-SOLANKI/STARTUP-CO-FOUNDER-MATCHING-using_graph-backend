import graphene

# graphene.ObjectType = "This is a TYPE that GraphQL can return"
# Each field here = one field the client can request in GraphiQL
#
# Think of this as: "What does a Student LOOK LIKE in the API?"
# Answer: it has id, name, email — all strings.

class StudentType(graphene.ObjectType):
    id    = graphene.String()   # unique identifier
    name  = graphene.String()   # student's name
    email = graphene.String()   # student's email
