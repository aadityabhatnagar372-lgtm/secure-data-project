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

---

## 2026-08-13 — Use Psycopg 3 for PostgreSQL access

**Decision**

Use Psycopg 3 as the Python PostgreSQL driver for the first implementation.

**Why this approach**

The project needs precise control over database queries because one of its main goals is to retrieve only the data requested by the user. Psycopg 3 lets the application execute explicit SQL queries without adding an ORM abstraction at this early stage.

**Alternatives considered**

- SQLAlchemy — powerful and useful for larger applications, but adds an additional abstraction layer that is not necessary for the first database implementation.
- SQLite — simpler, but does not represent the server-based PostgreSQL data-node architecture we are building.

**Libraries / technologies involved**

- Psycopg 3
- PostgreSQL

**Why this library / technology**

Psycopg 3 provides direct Python access to PostgreSQL and allows the application to explicitly control which columns are selected.

**Security impact**

Direct query control supports the project's data-minimization requirement. Queries will still need parameterization and authorization checks; the database driver alone does not provide those protections.

**Trade-offs / risks**

Using direct SQL means we must carefully handle parameterization, transactions, connection management, and schema changes ourselves.

**Files changed**

- `decision.md`

**Code impact**

No application code yet. This decision selects the database driver for the upcoming FastAPI-to-PostgreSQL integration.

**Follow-up**

Install Psycopg 3 and implement a small database connection layer.git status

---

## 2026-08-13 — Keep database connection settings outside application code

**Decision**

Read the PostgreSQL connection settings from environment variables instead of hardcoding them in Python source code.

**Why this approach**

Database passwords and connection details should not be embedded directly in application source files. Environment variables let the same application code work with different development, testing, and deployment configurations.

**Alternatives considered**

- Hardcode the database credentials in `database.py` — simpler for the first test, but exposes secrets in source code.
- Store credentials directly in Git-tracked configuration — not appropriate because secrets could be committed accidentally.

**Libraries / technologies involved**

- Python `os` environment-variable support

**Why this technology**

It is built into Python, so no additional dependency is required for this basic configuration layer.

**Security impact**

Positive because the database password does not need to be stored in the Python source code.

**Trade-offs / risks**

Environment variables still need to be protected properly. The current Docker Compose development configuration uses a simple development password and should be replaced with safer secret handling before production use.

**Files changed**

- `decision.md`
- `app/database.py`

**Code impact**

The database module will read its connection settings from environment variables.

**Follow-up**

Implement the connection function and verify that the FastAPI application can connect to PostgreSQL.

---

## 2026-08-13 — Initial customer data schema

**Decision**

Use a simple `customers` table with the fields `id`, `name`, `email`, `phone`, and `address` for the first data-minization demonstration.

**Why this approach**

The project needs a realistic record containing multiple pieces of information so we can demonstrate the difference between retrieving an entire record and retrieving only the specific field requested by the user.

For example, a customer record can contain five fields, while a request such as `customer/101/email` should return only the email.

**Alternatives considered**

- Use only one field — too simple to demonstrate data minimization.
- Use a much larger enterprise schema — unnecessary complexity for the first prototype.
- Store the test data in JSON files — less representative of the PostgreSQL data-node architecture.

**Libraries / technologies involved**

- PostgreSQL

**Why this technology**

PostgreSQL allows the application to explicitly select individual columns, which directly supports the project's data-minimization goal.

**Security impact**

The schema intentionally contains multiple fields so that later authorization and query controls can demonstrate that unauthorized or unnecessary fields are not returned.

**Trade-offs / risks**

This is demonstration data, not a production customer schema. Real deployments would require stronger privacy controls, constraints, indexing, access policies, and appropriate handling of sensitive information.

**Files changed**

- `decision.md`
- `app/schema.sql`

**Code impact**

The schema will define the first customer data structure used by the PostgreSQL data node.

**Follow-up**

Create the table and insert safe sample data for testing the first field-specific request.

---

## 2026-08-13 — Use dummy customer data for development

**Decision**

Use fictional customer records for the initial database and API testing.

**Why this approach**

The project needs multiple fields in a realistic record so we can test data minimization safely. Fictional data lets us demonstrate the workflow without using real personal information.

**Alternatives considered**

- Use real customer data — inappropriate for development because of privacy and security concerns.
- Use only one field — would not demonstrate the project's ability to prevent unnecessary data exposure.

**Libraries / technologies involved**

- PostgreSQL

**Why this technology**

PostgreSQL provides the structured test database in which the fictional records can be queried field-by-field.

**Security impact**

Positive because no real personal information is introduced into the development environment.

**Trade-offs / risks**

The sample data is intentionally simple and does not represent a production customer schema.

**Files changed**

- `app/schema.sql`
- `decision.md`

**Code impact**

Added three fictional customer records for controlled testing.

**Follow-up**

Use these records to verify that the application can retrieve one requested field without returning the complete customer record.

---

## 2026-08-13 — Use a field-specific customer data endpoint

**Decision**

Create an endpoint in the form:

`GET /customer/{customer_id}/email`

that returns only the customer's email address.

**Why this approach**

This endpoint directly demonstrates the project's main data-minimization goal. The client explicitly asks for one field, so the server should retrieve and return only that field rather than retrieving the complete customer record.

**Alternatives considered**

- `GET /customer/{customer_id}` returning the full customer record — simpler, but exposes unnecessary information.
- `GET /customer/{customer_id}?field=email` — possible, but the field-specific route makes the intended resource and allowed operation explicit for the first prototype.
- Return the full record and filter it on the client — insecure for this project because unnecessary data would already have been exposed.

**Libraries / technologies involved**

- FastAPI
- Psycopg 3
- PostgreSQL

**Why these technologies**

FastAPI handles the HTTP request, Psycopg 3 provides direct PostgreSQL access, and PostgreSQL allows the application to select only the requested `email` column.

**Security impact**

Positive because the endpoint is designed to expose only one requested field. This is an initial data-minimization control, although authentication and authorization have not yet been implemented.

**Trade-offs / risks**

This first endpoint is intentionally narrow. More fields and operations will require a consistent authorization and validation strategy to prevent unauthorized field access.

**Files changed**

- `decision.md`
- `app/routes.py`
- `app/main.py`
- `app/database.py`

**Code impact**

The application will gain its first database-backed API endpoint.

**Follow-up**

Implement the endpoint, query only the `email` column, and verify that the response contains no other customer fields.

---

## 2026-08-13 — Use JWT for initial authentication

**Decision**

Use JSON Web Tokens (JWT) for the first authentication implementation.

**Why this approach**

The project exposes HTTP APIs, so the client needs a way to prove that it has successfully authenticated when making later requests. JWT provides a compact token that can be sent with API requests without requiring the API to keep the user's login session in server memory.

**Alternatives considered**

- Server-side sessions — simple and secure when implemented correctly, but require server-side session storage and session management.
- API keys — simple for service-to-service access, but less suitable for the initial user login flow.
- OAuth 2.0 / OpenID Connect — powerful and appropriate for larger production systems, but more complex than needed for the first local prototype.

**Libraries / technologies involved**

- JWT
- Python authentication library to be selected during implementation

**Why this technology**

JWT fits the API-based architecture and gives us a clear separation between authentication and the later authorization layer.

**Security impact**

Authentication will prevent anonymous users from accessing protected endpoints once implemented. JWT signing keys must be protected, token lifetime must be limited appropriately, and tokens must be validated on every protected request.

**Trade-offs / risks**

JWT does not automatically provide authorization. A valid token only proves that the token was issued for an authenticated identity. The application must separately check whether that identity is allowed to access the requested data.

**Files changed**

- `decision.md`

**Code impact**

No application code yet. This decision defines the authentication mechanism for the next implementation stage.

**Follow-up**

Select the Python JWT library, implement login, issue a short-lived authentication token, and protect the customer email endpoint.

---

## 2026-08-13 — Use database-backed username/password login

**Decision**

Use a simple username and password login backed by PostgreSQL for the initial authentication prototype.

**Why this approach**

The project needs a clear authentication step before users can access protected data. A database-backed login gives us a simple way to associate an authenticated identity with the permissions that will later be checked by the authorization layer.

**Alternatives considered**

- Hardcoded demo credentials — simple, but not representative of a real application and unsuitable for the authorization architecture we are building.
- OAuth 2.0 / OpenID Connect — stronger for production identity management, but unnecessarily complex for the first local prototype.
- API keys as the primary login mechanism — better suited to service-to-service authentication than interactive user login.

**Libraries / technologies involved**

- PostgreSQL
- FastAPI
- Password-hashing library to be selected during implementation
- PyJWT

**Why these technologies**

PostgreSQL stores the user record and password hash. FastAPI handles the login request. A dedicated password-hashing library will protect passwords rather than storing them directly. PyJWT creates the authentication token after successful login.

**Security impact**

Passwords must never be stored in plaintext. The login process must verify a password against its stored hash, issue a signed JWT only after successful verification, and avoid exposing password information in API responses or logs.

**Trade-offs / risks**

This is a prototype authentication system. A production deployment would need stronger identity management, account lockout/rate limiting, MFA, password-reset mechanisms, secure secret management, and additional monitoring.

**Files changed**

- `decision.md`

**Code impact**

No application code yet. This decision defines the login architecture for the next implementation step.

**Follow-up**

Select a password-hashing library, create the users table, add a test user, and implement the login endpoint.

---

## 2026-08-13 — Use Argon2 for password hashing

**Decision**

Use Argon2 for hashing user passwords before storing them in PostgreSQL.

**Why this approach**

Passwords must never be stored in plaintext. Argon2 is designed specifically for password hashing and is intentionally expensive to compute, which makes large-scale password guessing more difficult.

**Alternatives considered**

- Plain SHA-256/SHA-512 — fast general-purpose hashes are not appropriate for password storage because attackers can test large numbers of guesses quickly.
- PBKDF2 — a valid password-hashing approach, but Argon2 is the preferred choice for this prototype.
- bcrypt — also widely used and suitable, but Argon2 provides the password-hashing design selected for this project.

**Libraries / technologies involved**

- Argon2 password hashing library
- PostgreSQL

**Why this library / technology**

The password-hashing library will handle salt generation, password hashing, and password verification instead of requiring us to implement cryptographic password handling ourselves.

**Security impact**

Positive. Passwords will be stored as password hashes rather than plaintext. Password verification will compare the submitted password against the stored hash.

**Trade-offs / risks**

Password hashing is intentionally computationally expensive, so login operations require more CPU resources than simple hashing. The hashing parameters should be reviewed before production deployment.

**Files changed**

- `decision.md`

**Code impact**

No application code yet. This decision selects the password-hashing mechanism for the login implementation.

**Follow-up**

Install the Argon2 library, create the users table, add a development user with a hashed password, and implement password verification.

---

## 2026-08-13 — Validate JWTs with a FastAPI dependency

**Decision**

Use a FastAPI dependency to extract and validate the bearer JWT before allowing access to protected endpoints.

**Why this approach**

The project will eventually have multiple protected endpoints. A reusable dependency gives us one consistent place to validate the JWT instead of duplicating authentication checks inside every route.

**Alternatives considered**

- Validate the JWT separately inside every route — duplicates security logic and makes inconsistent checks more likely.
- Middleware for all requests — broader than necessary because public endpoints such as `/health` do not need authentication.
- Server-side session lookup — possible, but the current architecture is already using JWT-based authentication.

**Libraries / technologies involved**

- FastAPI security dependencies
- PyJWT

**Security impact**

Positive because protected endpoints will reject requests that do not contain a valid bearer token.

JWT signature, expiration, and required claims must be validated before the protected route continues.

**Trade-offs / risks**

JWT validation only establishes that the token is valid and identifies the user. It does not determine whether that user is allowed to access a particular customer or field. Authorization will be implemented separately.

**Files changed**

- `decision.md`
- `app/auth.py`
- `app/routes.py`

**Code impact**

Protected routes will depend on a reusable JWT-validation function.

**Follow-up**

Implement JWT validation, protect the customer email endpoint, and verify that requests without a valid token are rejected.

---

## 2026-08-13 — Use user-to-customer ownership for initial authorization

**Decision**

For the first authorization implementation, associate each user with the customer record they are allowed to access.

**Why this approach**

The project needs to demonstrate a distinction between authentication and authorization. Authentication proves who the user is; ownership determines whether that authenticated user is allowed to access the requested customer data.

A simple user-to-customer relationship makes this easy to understand, test, and extend later.

**Alternatives considered**

- Allow every authenticated user to access every customer — simpler, but does not demonstrate meaningful authorization.
- Role-based access control (RBAC) immediately — useful for larger systems, but more complex than necessary for the first authorization prototype.
- Attribute-based access control (ABAC) — flexible, but unnecessary complexity at this stage.

**Libraries / technologies involved**

- PostgreSQL
- FastAPI
- PyJWT

**Why this technology**

The JWT provides the authenticated user ID, while PostgreSQL can store the relationship between the user and the customer they are authorized to access.

**Security impact**

Positive because a valid JWT alone will no longer be sufficient to access arbitrary customer records. The server will explicitly check the authenticated user's permission.

**Trade-offs / risks**

Ownership is intentionally simple and is not a complete enterprise authorization system. Future versions may need roles, groups, permissions, delegated access, or attribute-based policies.

**Files changed**

- `decision.md`
- `app/users.sql`
- `app/routes.py`

**Code impact**

The users data model will gain an authorization relationship, and protected routes will check that relationship before returning customer data.

**Follow-up**

Add the user-to-customer relationship, create test authorization data, implement the authorization check, and verify both allowed and denied requests.

---

## 2026-08-13 — Use a metadata directory for data-node discovery

**Decision**

Use a lightweight metadata directory to map logical data identifiers to the node or service responsible for storing that data.

**Why this approach**

The API needs a reliable way to determine where a requested record is stored when data is distributed across multiple nodes.

The directory will contain routing metadata, such as which node owns a customer record, but it will not contain the customer's full data.

**Alternatives considered**

- Hardcode node addresses in application code — simple for a tiny prototype, but difficult to maintain as nodes are added or moved.
- Broadcast every request to all nodes — avoids a directory, but increases network traffic and unnecessary data access.
- Fully peer-to-peer discovery — possible, but adds substantial complexity for the first prototype.

**Libraries / technologies involved**

- PostgreSQL or a small metadata store for the initial directory
- FastAPI for the discovery API/service

**Why this technology**

A simple metadata store is enough for the initial prototype and is easy to inspect and test. It can later be replaced by a dedicated service-discovery mechanism if the architecture grows.

**Security impact**

The directory should expose only the metadata required to route requests. It should not expose customer data or sensitive database credentials.

**Trade-offs / risks**

A central metadata directory can itself become a point of failure if it is not replicated. It is intentionally a routing component, not the central repository for all application data.

**Files changed**

- `decision.md`

**Code impact**

No code yet. This decision defines how the system will locate distributed data before querying a data node.

**Follow-up**

Create a small node-directory structure and verify that a customer identifier can be mapped to a data node.

---

## 2026-08-13 — Use an allowlisted field-selection layer for data minimization

**Decision**

Use an allowlist of permitted fields and a dedicated data-minimization layer to control which customer fields can be returned.

**Why this approach**

The core goal of the project is to return only the data explicitly requested by the user. An allowlist prevents arbitrary column selection and provides one controlled place to define which fields are available.

For example:

`email` → allowed

`phone` → allowed if explicitly requested

`password_hash` → never exposed

**Alternatives considered**

- Let the client provide any SQL column name — rejected because it could expose fields that should never be returned.
- Retrieve the full customer record and filter it afterward — rejected because unnecessary data would already have been retrieved.
- Hardcode separate SQL queries inside every endpoint — works for a tiny prototype, but makes the data-minimization rules harder to maintain consistently.

**Libraries / technologies involved**

- Python
- Psycopg 3
- PostgreSQL

**Why this technology**

Python can maintain the field allowlist, while Psycopg 3 and PostgreSQL allow the application to retrieve only the selected column.

**Security impact**

Positive. The allowlist prevents arbitrary field access and reduces unnecessary data retrieval and exposure.

**Trade-offs / risks**

The allowlist must be maintained whenever the database schema changes. Authorization must still be performed separately; allowing a field does not mean every user is authorized to access it.

**Files changed**

- `decision.md`
- Future data-minimization module

**Code impact**

A reusable data-minimization layer will control which fields can be queried and returned.

**Follow-up**

Implement the field allowlist and connect the customer email endpoint to it.

---

## 2026-08-13 — Separate the customer data node from the API

**Decision**

Create a separate customer data service that owns access to the customer PostgreSQL database.

**Why this approach**

The project's core architecture is distributed. The API should not directly access every database node. A separate data service makes the node boundary explicit and allows the system to add additional nodes later.

The flow becomes:

Client
    ↓
API
    ↓
Node Directory
    ↓
Customer Data Node
    ↓
Customer PostgreSQL database

**Alternatives considered**

- API connects directly to every PostgreSQL node — simpler, but tightly couples the API to every data store and does not clearly demonstrate independent data nodes.
- Put all data behind one database service — simpler, but does not demonstrate distributed data ownership.
- Create three physical servers immediately — unnecessary complexity for the local prototype.

**Libraries / technologies involved**

- FastAPI
- Docker Compose
- PostgreSQL

**Why these technologies**

FastAPI provides the data-node service API, Docker Compose lets us run the node independently on the local machine, and PostgreSQL remains the persistent data store.

**Security impact**

Positive when service boundaries are enforced. The customer database should not be directly accessible by the client.

**Trade-offs / risks**

Introducing a separate service increases network communication and deployment complexity. The prototype will initially run all services locally in Docker.

**Files changed**

- `decision.md`
- `docker-compose.yml`
- Future customer-node service files

**Code impact**

The customer data service will become the owner of customer-data access, while the main API becomes the request coordinator.

**Follow-up**

Create the customer data-node service and run it as a separate Docker container.

---

## 2026-08-13 — Use HTTP between the API and data nodes

**Decision**

Use HTTP API calls for communication between the main API and individual data-node services.

**Why this approach**

The project already uses FastAPI for its services. HTTP provides a simple service boundary and allows the main API to communicate with data nodes independently of their internal implementation.

This also makes the architecture easier to expand later:

Main API
    ↓
Node Directory
    ↓
HTTP
    ↓
Node 1 / Node 2 / Node 3

**Alternatives considered**

- Direct PostgreSQL connections from the main API — simpler initially, but tightly couples the main API to every database node.
- Message queues — useful for asynchronous workflows, but unnecessary for the synchronous data-request path at this stage.
- gRPC — efficient and strongly typed, but adds complexity that is not needed for the first prototype.

**Libraries / technologies involved**

- FastAPI
- HTTP
- Python HTTP client to be selected during implementation

**Why this technology**

HTTP works naturally with FastAPI and is easy to test using Postman, browsers, and standard HTTP clients.

**Security impact**

The data-node service should not be exposed directly to users. Only trusted service-to-service requests should reach the node in the intended architecture.

**Trade-offs / risks**

HTTP introduces network latency and requires service authentication and error handling. The first prototype will run locally, but production deployment would require encrypted transport and stronger service-to-service authentication.

**Files changed**

- `decision.md`
- Future main API / customer-node files

**Code impact**

The main API will stop querying the customer database directly and instead request customer data from the appropriate data node.

**Follow-up**

Add a customer-data endpoint to the customer node and make the main API call it through the node-directory mapping.

---

## 2026-08-13 — Add a second data node for distributed testing

**Decision**

Add a second customer data node running as an independent service for distributed-system testing.

**Why this approach**

The project is intended to demonstrate multiple data nodes rather than a single service. A second node gives us a concrete environment for testing node discovery, routing, failure handling, and later replication.

**Alternatives considered**

- Continue with only one node — simpler, but does not demonstrate distributed behavior.
- Add three nodes immediately — closer to the final architecture, but adds complexity before the two-node workflow is verified.
- Use a remote server for Node 2 — unnecessary for the local prototype.

**Libraries / technologies involved**

- FastAPI
- Docker / local service processes
- PostgreSQL

**Why this technology**

The same service pattern as Node 1 keeps the architecture consistent while allowing the node address and storage configuration to differ.

**Security impact**

A second node increases the attack surface, so node-to-node and API-to-node trust controls will need to be added later.

**Trade-offs / risks**

Running multiple nodes locally increases configuration complexity. Until replication is implemented, the nodes may contain different data and should not be assumed to be consistent.

**Files changed**

- `decision.md`
- Future Node 2 service files

**Code impact**

A second independent customer-data service will be added to the local distributed architecture.

**Follow-up**

Create Node 2, expose its health endpoint, and verify that both nodes can run independently.

---

## 2026-08-13 — Use an established cryptographic library for data protection

**Decision**

Use an established Python cryptographic library for application-level encryption rather than implementing cryptographic algorithms manually.

**Why this approach**

The project needs to protect sensitive data while avoiding custom cryptographic implementations. Established libraries provide tested implementations of standard encryption primitives and reduce the risk of cryptographic programming errors.

The first implementation will use authenticated encryption so that confidentiality and integrity are provided together.

**Alternatives considered**

- Custom encryption code — rejected because cryptographic implementations should not be invented for this project.
- Plain encoding such as Base64 — rejected because encoding does not provide confidentiality.
- Encryption without authentication — weaker because confidentiality is provided without reliable integrity protection.

**Libraries / technologies involved**

- Python cryptographic library to be selected during implementation
- Established authenticated-encryption algorithm

**Why this technology**

The selected library will provide standard cryptographic primitives and avoid implementing encryption logic from scratch.

**Security impact**

Positive. Properly implemented authenticated encryption can protect data confidentiality and detect tampering.

Encryption keys must be protected separately from application data and must never be hardcoded into Git-tracked source files.

**Trade-offs / risks**

Encryption introduces key-management requirements. Losing or exposing encryption keys can make protected data inaccessible or compromise its confidentiality.

**Files changed**

- `decision.md`

**Code impact**

No application code yet. This decision defines the cryptographic approach for the next implementation stage.

**Follow-up**

Select the cryptographic library and authenticated-encryption method, then implement a small encryption/decryption service and verify round-trip behavior.

---

## 2026-08-13 — Use cryptography Fernet for initial application encryption

**Decision**

Use the Python `cryptography` library with Fernet symmetric authenticated encryption for the first application-level encryption implementation.

**Why this approach**

The project needs an established encryption mechanism that provides confidentiality and integrity without requiring us to implement encryption algorithms ourselves.

Fernet provides a simple API for encrypting and decrypting data using a secret key and includes authentication so tampering can be detected.

**Alternatives considered**

- AES implemented manually — rejected because cryptographic primitives should not be assembled manually when a well-established library is available.
- Base64 encoding — rejected because encoding does not provide confidentiality.
- RSA/public-key encryption for this first milestone — unnecessary complexity because the service currently needs to protect application data with a shared secret.

**Libraries / technologies involved**

- `cryptography`
- Fernet
- Symmetric encryption

**Why this library / technology**

The `cryptography` library is a widely used Python cryptography library, and Fernet provides a straightforward authenticated-encryption interface suitable for the initial prototype.

**Security impact**

Positive when keys are stored securely and are not committed to Git. Fernet provides confidentiality and integrity protection for the encrypted payload.

**Trade-offs / risks**

The same secret key is required for decryption. Key management is therefore critical. The prototype will use an environment variable for the encryption key, and production deployment will require a dedicated secret/key-management solution.

**Files changed**

- `decision.md`

**Code impact**

No application code yet. This decision selects the cryptographic implementation for the next milestone.

**Follow-up**

Install `cryptography`, generate a development encryption key, implement an encryption service, and verify encryption/decryption round-trip behavior.

---

## 2026-08-13 — Use a short-lived scoped access key for protected data

**Decision**

Issue a cryptographically random, short-lived access key for an authorized data request.

The key will be scoped to the authenticated user, requested customer, and requested field, and will expire after approximately 10 minutes.

**Why this approach**

The project requires more than simple user authentication. After a user is authenticated and authorized, the system should be able to issue a temporary access credential that limits the lifetime and scope of access to the requested data.

This reduces the usefulness of a stolen access key because it expires automatically and is associated with a specific access scope.

**Alternatives considered**

- Use the JWT itself as the temporary data-access credential — rejected because authentication and short-lived data access are separate concerns in this project.
- Long-lived API key — rejected because compromise would provide a larger abuse window.
- One key for unrestricted data access — rejected because the key should be scoped to the specific authorized request.
- Use a custom cryptographic algorithm — rejected because randomness and cryptographic primitives should come from established libraries.

**Libraries / technologies involved**

- Python `secrets`
- Time-based expiration using Python datetime/time utilities
- Existing JWT authentication

**Why this technology**

Python's `secrets` module provides cryptographically secure random values suitable for generating unpredictable access tokens.

The server can associate each token with an expiration timestamp and validate that expiration before allowing access.

**Security impact**

Positive when the token is:

- cryptographically random
- short-lived
- scoped to the authorized resource
- validated server-side on every use
- never stored or logged in plaintext where avoidable

The access key does not replace authentication or authorization.

**Trade-offs / risks**

The server must store or otherwise validate issued access keys and their expiration state. Short expiration increases the need to issue new keys for subsequent access.

Clock handling and token cleanup must also be considered.

**Files changed**

- `decision.md`

**Code impact**

No application code yet. This decision defines the short-lived access-key mechanism for the next implementation stage.

**Follow-up**

Implement the short-lived access-key service, generate a 10-minute token for an authorized request, and verify that expired keys are rejected.

---

## 2026-08-13 — Use the short-lived access key as a scoped data-access credential

**Decision**

Require the 10-minute access key for the final customer-data retrieval step after JWT authentication and authorization have succeeded.

**Why this approach**

The JWT identifies the authenticated user, while the short-lived access key limits access to a specific customer and field for a limited period.

This separates long-lived identity/authentication from temporary, narrowly scoped data access.

**Flow**

JWT
    ↓
Authentication
    ↓
Authorization
    ↓
Issue scoped 10-minute access key
    ↓
Client presents access key
    ↓
Validate key
    ↓
Retrieve requested data

**Alternatives considered**

- Use only the JWT for data access — simpler, but does not provide the separate temporary credential required by the project design.
- Generate a new JWT for every data request — mixes authentication and temporary resource access concerns.
- Use an unscoped temporary key — weaker because the key could potentially be reused for unrelated data.

**Libraries / technologies involved**

- Existing JWT authentication
- Existing access-key generator
- Existing access-key store
- FastAPI

**Security impact**

Positive because the temporary credential is limited by:

- user identity
- customer ID
- requested field
- expiration time

The server validates all of these before allowing access.

**Trade-offs / risks**

The client must obtain and present the temporary access key correctly. The access-key store must remain available while the key is valid.

**Files changed**

- `decision.md`
- Future access-key and route files

**Code impact**

The customer-data workflow will gain a separate temporary authorization step before data retrieval.

**Follow-up**

Implement issuance and validation of the access key in the customer-data workflow and verify that an expired or incorrectly scoped key is rejected.

---

## 2026-08-13 — Use explicit primary and replica routing for initial failover

**Decision**

Represent a primary data node and one or more replica nodes in the node directory and use explicit failover logic when the primary node is unavailable.

**Why this approach**

The project needs to demonstrate that failure of one data node does not automatically stop data access. Explicit primary/replica metadata makes the failover decision visible and testable in the prototype.

**Alternatives considered**

- No failover — simpler, but violates the availability goal of the distributed architecture.
- Randomly select any node — does not distinguish the authoritative node from replicas.
- Full PostgreSQL replication immediately — realistic, but adds substantial database configuration complexity before the application-level failover behavior is verified.

**Libraries / technologies involved**

- Python
- FastAPI
- PostgreSQL
- Docker

**Security impact**

Failover must preserve the same authentication, authorization, data-minimization, and access-key requirements. A replica must not become a bypass around existing security controls.

**Trade-offs / risks**

Application-level failover does not itself guarantee that replicas contain current data. Replication consistency must be implemented and verified separately.

**Files changed**

- `decision.md`
- `app/node_directory.py`
- Future failover/routing code

**Code impact**

The node directory will represent primary and replica nodes, and the request path will attempt a replica when the primary is unavailable.

**Follow-up**

Implement primary/replica metadata, add failover routing, then simulate primary-node failure and verify that an authorized request can still reach an available replica.