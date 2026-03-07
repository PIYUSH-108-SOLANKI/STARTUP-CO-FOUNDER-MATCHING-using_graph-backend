import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette_graphene import GraphQLApp

from app.graphql.schema import schema

# Create the FastAPI app
app = FastAPI()

# ── CORS — allows the frontend (file://, localhost, or any origin) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # allow ALL origins (fine for a student project)
    allow_methods=["*"],       # allow GET, POST, OPTIONS, etc.
    allow_headers=["*"],       # allow all headers including Content-Type
)

# Mount the GraphQL endpoint — exactly like sir's approach
app.mount("/graphql", GraphQLApp(schema=schema, graphiql=True))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)


