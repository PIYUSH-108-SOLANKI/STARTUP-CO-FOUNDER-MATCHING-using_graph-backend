# 🚀 Startup Co-Founder Matching — GraphQL API

A GraphQL API built with **Python**, **Graphene**, **FastAPI**, and **Neo4j Aura** to connect students for startup co-founder partnerships.

---

## 📌 Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Web Framework | FastAPI + Uvicorn |
| GraphQL Library | Graphene |
| GraphQL Bridge | starlette-graphene |
| Database | Neo4j Aura (Graph Database) |
| Query Language | Cypher |

---

## 🗂️ Project Structure

```
graphql_external_assignment/
├── .env                          ← DB credentials (not in git)
├── requirements.txt              ← Python dependencies
├── test.py                       ← Quick DB connection test
└── app/
    ├── main.py                   ← FastAPI server entry point
    ├── core/
    │   ├── config.py             ← Loads .env settings
    │   └── database.py           ← Neo4j connection
    ├── models/                   ← Cypher queries (database layer)
    │   ├── student.py
    │   ├── idea.py
    │   ├── application.py
    │   └── milestone.py
    └── graphql/
        ├── schema.py             ← GraphQL schema (Query + Mutation)
        ├── types/                ← Response shapes
        ├── queries/              ← READ operations
        └── mutations/            ← WRITE operations
```

---

## ⚙️ Setup & Run

### 1. Clone the repository
```bash
git clone https://github.com/PIYUSH-108-SOLANKI/graphql_external_assignment.git
cd graphql_external_assignment
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create your `.env` file
```
NEO4J_URI=neo4j+s://your-instance.databases.neo4j.io
NEO4J_USERNAME=your-username
NEO4J_PASSWORD=your-password
```

### 5. Test DB connection
```bash
python test.py
```

### 6. Start the server
```bash
uvicorn app.main:app --reload --port 8000
```

### 7. Open GraphiQL
Visit: **http://localhost:8000/graphql**

---

## 🧪 Test Cases (All 6 Requirements)

### 1. Domain Filter
```graphql
query {
  ideas(domain: "fintech") {
    title
  }
}
```

### 2. Role Assignment
```graphql
mutation {
  applyIdea(input: {
    ideaId: "<idea-id>"
    studentId: "<student-id>"
    role: "CTO"
  }) {
    ok
    message
    application { id role status }
  }
}
```

### 3. Application Workflow + 4. Partnership Creation
```graphql
mutation {
  updateApplicationStatus(
    applicationId: "<app-id>"
    status: "accepted"
  ) {
    ok
    message
    application { status }
  }
}
```

### 5. Milestone Tracking
```graphql
mutation {
  addMilestone(ideaId: "<idea-id>", title: "Build MVP") {
    ok
    milestone { id title status }
  }
}
```

### 6. Duplicate Prevention
Run the same `applyIdea` mutation twice → second returns `ok: false`

---

## 📊 Graph Data Model

```
(Student) -[:POSTED]---------> (Idea)
(Student) -[:APPLIED_TO]-----> (Idea)       { role, status }
(Student) -[:PARTNERS_WITH]--> (Student)    { ideaId }
(Idea)    -[:HAS_MILESTONE]--> (Milestone)
```

---

## 👤 Author

**Piyush Solanki**
