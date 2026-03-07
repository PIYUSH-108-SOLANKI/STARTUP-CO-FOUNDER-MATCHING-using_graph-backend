import os
import uvicorn
from fastapi import FastAPI
from starlette_graphene import GraphQLApp

from app.graphql.schema import schema

# Create the FastAPI app
app = FastAPI()

# Mount the GraphQL endpoint — exactly like sir's approach
# graphiql=True → enables the GraphiQL browser testing UI automatically
app.mount("/graphql", GraphQLApp(schema=schema, graphiql=True))


if __name__ == "__main__":
    # PORT is set by Render in production, defaults to 8000 locally
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)

