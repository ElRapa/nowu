# Deployment View

> This document describes how the system is deployed to infrastructure
> environments (dev, staging, production), using a C4 Deployment view.

last_updated: YYYY-MM-DD  
owner: architecture

---

## Production Deployment

```mermaid
C4Deployment
    title Production deployment

    Deployment_Node_Cloud(cloud, "Cloud Provider", "Region X")
    Deployment_Node_K8s(k8s, "Kubernetes Cluster", "Namespace: nowu-prod")
    Deployment_Node_Pods(api_pod, "API Pods", "Docker image: nowu-api")
    Deployment_Node_Pods(worker_pod, "Worker Pods", "Docker image: nowu-worker")
    Deployment_Node_Db(db_node, "Managed DB", "Postgres")
    Deployment_Node_Queue(queue_node, "Queue Service", "e.g. SQS/RabbitMQ")

    Rel(api_pod, db_node, "Read/Write", "TCP 5432")
    Rel(api_pod, queue_node, "Enqueue/Dequeue tasks")
    Rel(worker_pod, db_node, "Read/Write", "TCP 5432")
    Rel(worker_pod, queue_node, "Consume tasks")
```

**Notes:**

- Scale-out:
    - API and Worker pods can be scaled horizontally.
- Availability:
    - DB uses provider-managed high availability where possible.
- Secrets:
    - Injected via environment variables or secret manager.

---

## Staging / Development

Describe any differences from production:

- Smaller instance sizes.
- Fewer replicas.
- Possibly shared infrastructure between environments.

---

## Environment-Specific Concerns

List any environment-specific constraints or practices:

- Logging retention in production vs. staging.
- Feature flags that differ by environment.
