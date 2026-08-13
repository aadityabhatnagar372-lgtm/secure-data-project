Decision Log

This file records meaningful engineering decisions made while developing the project.

Purpose

For every significant code or architecture change, record:

What decision was made

Why it was made

What alternatives were considered

Why the selected approach is better for this project

Any trade-offs or risks

What code/files were affected

Do not log trivial formatting changes, typo fixes, or obvious mechanical edits unless they affect behavior.

Entry Template

[DATE] — [DECISION TITLE]

Decision

What was changed or selected.

Why this approach

Explain the technical and project-specific reason for choosing it.

Alternatives considered

Alternative 1 — why it was not selected

Alternative 2 — why it was not selected

Libraries / technologies involved

List the library, framework, API, protocol, algorithm, or design pattern used.

Why this library / technology

Explain why it is appropriate, including simplicity, security, performance, maintainability, compatibility, or project requirements.

Security impact

Explain whether the decision improves, weakens, or does not materially affect security.

Trade-offs / risks

Mention limitations, complexity, performance costs, dependency risks, or future migration concerns.

Files changed

path/to/file

Code impact

Briefly describe what behavior changed.

Follow-up

Any testing, review, or later decision required.

Initial Project Decisions

2026-08-13 — Project architecture

Decision

Use a distributed data-access architecture instead of relying on a single central data server.

Why this approach

The project is intended to reduce dependence on a single point of failure. Data can be stored across multiple nodes, with replication or failover used where availability is required.

Alternatives considered

Single centralized database — simpler, but creates a stronger single point of failure.

Fully peer-to-peer design — potentially more complex for authorization, discovery, monitoring, and consistency.

Libraries / technologies involved

Not selected yet. Technology choices should be recorded when implementation begins.

Security impact

Reduces concentration of data and can limit the blast radius of a single-node compromise, but distributed systems also introduce additional attack surfaces and trust relationships.

Trade-offs / risks

More components mean more configuration, monitoring, failure handling, and synchronization complexity.

Files changed

decision.md

Code impact

Architecture decision only at this stage; no application code has been changed yet.

Follow-up

Choose the first prototype architecture and document the concrete technologies when implementation begins.

2026-08-13 — Data minimization

Decision

The system should retrieve and transmit only the exact data requested by the user.

Why this approach

Sending only the required field or object reduces unnecessary data exposure, network traffic, and the amount of sensitive information available to the client.

Alternatives considered

Fetch the full record and filter it at the client — easier in some applications, but exposes unnecessary information.

Fetch a broad server-side object and filter later — better than client-side filtering, but still causes unnecessary internal data movement.

Libraries / technologies involved

Not selected yet.

Security impact

Positive when implemented correctly because less data is exposed to the client and less unnecessary information crosses service boundaries.

Trade-offs / risks

Fine-grained queries may require more careful API design and authorization checks.

Files changed

decision.md

Code impact

Future APIs should be designed around resource/field-level requests rather than broad record downloads.

2026-08-13 — Short-lived access

Decision

Use short-lived access credentials with a target validity of 10 minutes.

Why this approach

A short lifetime limits the usefulness of a stolen credential and reduces the time window in which an authorization artifact can be abused.

Alternatives considered

Long-lived API keys — easier to implement, but larger compromise window.

Permanent session credentials — simpler user experience, but weaker containment.

One-time credentials — stronger restriction, but may be inconvenient for repeated access during a short session.

Libraries / technologies involved

Not selected yet. The final design should prefer an established authentication/authorization mechanism and a proper key-management solution rather than inventing cryptography.

Security impact

Positive if expiration is enforced server-side and credentials cannot be extended or reused after expiry.

Trade-offs / risks

Short lifetimes can increase refresh/authorization traffic and require correct clock handling and revocation behavior.

Files changed

decision.md

Code impact

Future authorization and cryptographic access code must enforce the 10-minute lifetime.

Ongoing Log

Add new entries below this line for every meaningful implementation decision.

2026-08-13 — Verify the initial API before adding complexity

Decision

Keep the first milestone deliberately small: verify the API root and health-check endpoints before adding authentication, databases, encryption, or distributed nodes.

Why this approach

A small verified foundation makes failures easier to isolate. It also lets the project establish a known-good API entry point before additional components are introduced.

Alternatives considered

Add authentication and database access immediately — faster feature growth, but harder to determine which layer caused a failure.

Build the complete distributed architecture first — higher complexity and more difficult debugging at the beginning.

Libraries / technologies involved

FastAPI

Uvicorn

Why these technologies

They provide the minimal runtime needed to expose and verify the project's first HTTP endpoints.

Security impact

This milestone does not implement meaningful security controls yet. It establishes the API foundation only.

Trade-offs / risks

The current API is intentionally incomplete and must not be treated as production-secure.

Files changed

app/main.py

requirements.txt

decision.md

flow.md

Code impact

Added the initial FastAPI application with / and /health endpoints and verified both endpoints locally.

Follow-up

Add the first controlled data-request endpoint, then introduce authentication and authorization before exposing sensitive data.

---

## 2026-08-13 — Use PostgreSQL for the first data node

**Decision**

Use PostgreSQL as the database for the first Docker-based data node.

**Why this approach**

PostgreSQL gives the project a reliable relational database for storing structured test data. It integrates well with Python and can run as an isolated Docker container, which makes it suitable for gradually expanding the prototype into multiple data nodes.

**Alternatives considered**

- SQLite — very simple, but less representative of a server-based distributed data architecture.
- MongoDB — possible, but the initial project data is structured and relational, so PostgreSQL is a better fit for the first prototype.

**Libraries / technologies involved**

- PostgreSQL
- Docker

**Why this technology**

PostgreSQL supports precise queries such as selecting only the requested field. Docker lets us run the database as an isolated node and later create additional nodes or replicas.

**Security impact**

The database will not be exposed directly to the user. The application will control which fields can be requested and returned.

**Trade-offs / risks**

Running multiple database nodes increases configuration and synchronization complexity. PostgreSQL itself does not provide the project's authorization or data-minimization logic; those controls must be implemented by the application.

**Files changed**

- `decision.md`

**Code impact**

No application code yet. This decision defines the database technology for the first data node.

**Follow-up**

Create the first PostgreSQL Docker service and verify that the application can communicate with it.