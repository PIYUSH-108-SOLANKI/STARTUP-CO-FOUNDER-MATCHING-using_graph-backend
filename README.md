# Startup Co-Founder Matching System

## 1. System Overview
**Case Study:** Student Co-Founder Matching Platform
**Objective:** Build a platform where students can post startup ideas and find co-founders. Students can browse ideas by domain (fintech, edtech, healthtech) and apply for specific roles (e.g., CTO, Developer, Designer).
**How it works:** 
The backend serves a GraphQL API powered by a Neo4j Graph Database. Students can register, post ideas, and apply to existing ideas. The idea's founder can review applications. Upon accepting an application, the system automatically creates a "Partnership" between the two students. The platform also allows students to track the progress of their startup ideas via Milestones.

## 2. Database Design (Graph Models & Relationships)

This system uses Neo4j, a Graph Database. Instead of tables, data is stored as Nodes and Relationships.

### Entities (Nodes)
*   **Student:** `id` (String), `name` (String), `email` (String)
*   **Idea:** `id` (String), `title` (String), `domain` (String), `description` (String)
*   **Milestone:** `id` (String), `title` (String), `status` (String - pending/completed)

### Relationships (Edges)
*   **(Student) `-[POSTED]->` (Idea)**
*   **(Student) `-[APPLIED_TO]->` (Idea)**
    *   *Attributes:* `id` (String), `role` (String), `status` (String - applied/accepted/rejected)
    *   *Note: Applications are inherently modeled as relationships between a Student and an Idea.*
*   **(Student) `-[PARTNERS_WITH]->` (Student)**
    *   *Attributes:* `ideaId` (String)
*   **(Idea) `-[HAS_MILESTONE]->` (Milestone)**

## 3. GraphQL Schema

### Types Definition
*   `StudentType`: id, name, email
*   `IdeaType`: id, title, domain, description
*   `ApplicationType`: id, role, status, studentId, ideaId
*   `MilestoneType`: id, title, status

### Queries (Read)
*   `allStudents`: Returns a list of all students.
*   `student(id: String)`: Returns a single student.
*   `allIdeas`: Returns a list of all ideas.
*   `ideas(domain: String)`: Returns a list of ideas, filtered by domain if provided.
*   `idea(id: String)`: Returns a single idea.
*   `allApplications`: Returns a list of all applications across the system.
*   `milestonesByIdea(ideaId: String!)`: Returns all milestones associated with a specific idea.

### Mutations (Write)
*   `createStudent(name: String!, email: String!)`: Registers a new student.
*   `createIdea(title: String!, domain: String!, description: String!, postedByStudentId: String!)`: Posts a new startup idea.
*   `applyIdea(input: {ideaId: String!, studentId: String!, role: String!})`: Submits an application to an idea.
*   `updateApplicationStatus(applicationId: String!, status: String!)`: Founder accepts or rejects an application.
*   `addMilestone(ideaId: String!, title: String!)`: Adds a new milestone to an idea.
*   `updateMilestoneStatus(milestoneId: String!, status: String!)`: Updates a milestone's status (e.g., to "completed").

## 4. Implementation Details & Live Links

*   **API Framework:** FastAPI with Graphene (`starlette-graphene`)
*   **Database:** Neo4j Aura (Cloud Graph Database)
*   **Language:** Python 3.12
*   **Live GraphQL API Interface:** [https://startup-co-founder-matching-using-graph.onrender.com/graphql/](https://startup-co-founder-matching-using-graph.onrender.com/graphql/)
*   **Backend Repo:** [https://github.com/PIYUSH-108-SOLANKI/STARTUP-CO-FOUNDER-MATCHING-using_graph-backend](https://github.com/PIYUSH-108-SOLANKI/STARTUP-CO-FOUNDER-MATCHING-using_graph-backend)

## 5. Test Execution (Sample Queries & Mutations)

**1. Create a Student (Mutation)**
```graphql
mutation {
  createStudent(name: "Alice", email: "alice@example.com") {
    student { id name }
  }
}
```

**2. Create an Idea (Mutation)**
```graphql
mutation {
  createIdea(title: "AI Fintech App", domain: "fintech", description: "Automated trading", postedByStudentId: "<STUDENT_ID>") {
    idea { id title }
  }
}
```

**3. Filter Ideas by Domain (Query)**
```graphql
query {
  ideas(domain: "fintech") {
    title
    domain
  }
}
```

**4. Apply to an Idea (Mutation)**
```graphql
mutation {
  applyIdea(input: {
    ideaId: "<IDEA_ID>"
    studentId: "<APPLICANT_ID>"
    role: "CTO"
  }) {
    ok
    message
    application { id role status }
  }
}
```
*Output Result:*
```json
{
  "data": {
    "applyIdea": {
      "ok": true,
      "message": "Application submitted!",
      "application": { "id": "uuid", "role": "CTO", "status": "applied" }
    }
  }
}
```

**5. Update Application Status & Form Partnership (Mutation)**
```graphql
mutation {
  updateApplicationStatus(applicationId: "<APP_ID>", status: "accepted") {
    ok
    message
  }
}
```
*Output Result:*
```json
{
  "data": {
    "updateApplicationStatus": {
      "ok": true,
      "message": "Application accepted! Partnership created between students."
    }
  }
}
```

## 6. Documentation (Flow, Validations, Assumptions)

### System Flow
1. Students register for the platform.
2. A student posts a startup idea (becomes the founder).
3. Another student applies to that idea specifying a role (e.g., Designer).
4. The founder reviews applications and can "accept" or "reject". 
5. If accepted, the application status changes, and a `PARTNERS_WITH` relationship is automatically created in the database between the founder and the applicant.
6. Founders can add and complete milestones for their ideas.

### Validations Implemented
1. **Duplicate Application Prevention:** A student cannot apply to the same idea more than once. The API queries the database for an existing `APPLIED_TO` relationship; if found, it rejects the mutation.
2. **Founder Self-Application Prevention:** A student who posted an idea cannot apply to their own idea. The API checks if a `POSTED` relationship exists between the applicant and the idea.
3. **Status Constraints:** Application status updates are strictly limited to `"accepted"` or `"rejected"`.

### Assumptions Made
*   Once a partnership is automatically formed (upon application acceptance), it does not need further confirmation from the applicant.
*   Any student can add milestones to an idea (in a production system, this would be restricted to founders/partners using authentication).
*   Authentication/Authorization via JWT was omitted to focus on the core Graph Database structure and GraphQL schema as required.
