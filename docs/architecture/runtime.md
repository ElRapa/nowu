# Runtime View

> This document describes how the system behaves at runtime for a few
> key scenarios, using C4 Dynamic views and short narratives.

last_updated: YYYY-MM-DD  
owner: architecture

---

## Scenario 1 — Example: User creates a new project

**Description:** Authenticated user creates a new project in the web UI.

**C4 Dynamic Diagram**

```mermaid
C4Dynamic
    title Project creation flow
    Person(user, "User")
    Container_Browser(browser, "Web UI")
    Container_Api(api, "API Service")
    Container_Db(db, "Main DB")

    Rel(user, browser, "Clicks 'Create project'")
    Rel(browser, api, "POST /projects")
    Rel(api, db, "INSERT project row")
    Rel(api, browser, "201 Created + project JSON")
```

**Notes:**

- Validation happens in the API layer.
- Any cross-cutting checks (auth, logging, tracing) are applied in middleware
according to `crosscutting.md`.

---

## Scenario 2 — Example: Background job processes a queue

**Description:** A worker processes tasks from a queue and updates the DB.

```mermaid
C4Dynamic
    title Background job processing
    Container_Worker(worker, "Worker")
    Container_Queue(queue, "Task Queue")
    Container_Db(db, "Main DB")

    Rel(queue, worker, "Deliver next job")
    Rel(worker, db, "UPDATE data based on job")
    Rel(worker, queue, "ACK job")
```

**Notes:**

- Failures are retried with exponential backoff.
- Metrics and logs are emitted per job for observability.

---

## Adding More Scenarios

For each new critical use case (e.g. login, billing, imports):

1. Add a short text description of the runtime behavior.
2. Add a `C4Dynamic` Mermaid diagram.
3. Note any special requirements (idempotency, retries, ordering, etc.).