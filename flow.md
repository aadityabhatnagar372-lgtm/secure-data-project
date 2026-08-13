Flow

Purpose

This file explains the project's code entry point, execution order, relationships between modules/classes/functions, and what AI changed during each coding session.

This document has two parts:

Planned architecture — what the system is intended to look like before implementation is verified.

Code-verified flow — updated from the actual source code whenever code is changed.

Do not guess code relationships. When implementation exists, verify the entry point and call flow from the source.

1. Project Goal

The system is intended to:

Accept a user's request for a specific piece of data.

Authenticate the user.

Authorize access to that exact data.

Locate the node/service that stores the data.

Retrieve only the requested data.

Encrypt/protect the result.

Issue short-lived access credentials targeted at approximately 10 minutes.

Return only the requested data to the user.

Reject access after the credential expires.

Support distributed data nodes so one node failure does not automatically stop the complete system.

2. Planned High-Level Execution Order

User / Client
    |
    v
API / Request Entry Point
    |
    v
Authentication
    |
    v
Authorization
    |
    +---- NO ----> Access Denied
    |
   YES
    |
    v
Data / Service Discovery
    |
    v
Data Node
    |
    v
Data Minimization / Exact Query
    |
    v
Encryption + Key Management
    |
    v
10-Minute Access Credential
    |
    v
Response to Client
    |
    v
Client Uses Requested Data
    |
    v
Credential Expiry
    |
    v
New Request -> New Authorization / New Credential

3. Planned Entry Point

Status: Not verified yet

The actual entry point must be updated after the project code exists.

Examples of possible entry points:

Python: main.py, app.py, or a framework application object

FastAPI: an app = FastAPI() object with route handlers

Flask: an app = Flask(...) object

Node.js: server.js / index.js

Java: main() method / Spring Boot application

Other frameworks: the framework-specific startup module

Do not claim one of these is the real entry point until the source code confirms it.

Verified entry point: TO BE FILLED FROM CODE

4. Planned Module / Class / Function Relationships

The following are conceptual responsibilities, not verified source-code names.

Request Handler
    |
    +--> Authenticator
    |
    +--> Authorizer
    |
    +--> DataDirectory / ServiceDiscovery
    |         |
    |         +--> DataNodeClient
    |
    +--> DataMinimizer / QueryBuilder
    |
    +--> KeyManager
    |
    +--> EncryptionService
    |
    +--> ResponseBuilder

Request Handler

Receives the user's request and starts the request lifecycle.

Authenticator

Verifies who the user is.

Authorizer

Checks whether the authenticated user is allowed to access the requested data.

Data Directory / Service Discovery

Determines where the requested data is located.

Data Node Client

Communicates with the appropriate data node.

Data Minimizer / Query Builder

Ensures that only the required field/object is requested or returned.

Key Manager

Creates, obtains, tracks, or validates short-lived access credentials/keys according to the final security design.

Encryption Service

Protects the requested data before delivery where encryption is part of the selected design.

Response Builder

Returns the minimum required response to the client.

5. Error / Decision Paths

Authentication failure

Request
  |
  v
Authentication
  |
  +--> FAIL --> Reject request

Authorization failure

Authenticated
  |
  v
Authorization
  |
  +--> NOT ALLOWED --> Access denied

Data node unavailable

Find data node
  |
  +--> Node unavailable
          |
          v
    Replica / failover path

This failover behavior must be implemented explicitly; it is not guaranteed by simply using multiple nodes.

Credential expired

Request/use protected data
        |
        v
Credential validation
        |
        +--> Expired --> Reject
        |
        +--> Valid --> Continue

6. What AI Changed in This Session

Session date: 2026-08-13

Code changes: None yet.

Documentation changes:

Created decision.md

Created Flow.md

Added the initial architecture decisions.

Added the planned execution flow.

Added placeholders for the real entry point and source-verified class/function relationships.

When code is changed in future sessions, add entries here using:

Session [DATE]

Files changed

file1

file2

What AI changed

Describe the exact behavior or code structure changed.

Why

Explain the reason for the change.

Functions/classes affected

ClassName.function_name()

other_function()

Execution-flow impact

Explain where the change occurs in the runtime flow.

Tests performed

Test name / command

Result

Related decision

Reference the matching decision.md entry.

7. Code-Verified Flow

This section must be updated after each meaningful implementation change.

Current verified flow

Not available yet — source code has not been provided/created in this session.

Once source code exists, record:

Exact startup/entry file

First function/class executed

Request routing

Authentication call chain

Authorization call chain

Data lookup call chain

Data filtering/minimization call chain

Encryption/key-management call chain

Response generation

Expiration/refresh handling

Error paths

Tests covering each critical path

8. Rules for Maintaining This File

Never invent function names.

Never claim an AI change that was not actually made.

Record exact filenames and symbols when verified.

Keep the execution order chronological.

Update the "What AI Changed in This Session" section after every coding session.

Link major code changes to the corresponding entry in decision.md.

9. Code-Verified Flow — Milestone 1

Verified on: 2026-08-13

Entry point: app/main.py

Runtime command:

python -m uvicorn app.main:app --reload

Execution order:

Uvicorn process
    ↓
Imports `app.main`
    ↓
Creates the FastAPI `app` object
    ↓
Registers HTTP routes
    ↓
Browser/Postman sends request
    ↓
FastAPI matches the route
    ↓
`root()` or `health_check()` executes
    ↓
Python dictionary is returned
    ↓
FastAPI serializes it as JSON
    ↓
HTTP response is returned to the client

Verified functions

root()

Route: GET /

Purpose: Confirms that the Secure Distributed Data Access System API is running.

Verified response:

{"message":"Secure Distributed Data Access System is running"}

health_check()

Route: GET /health

Purpose: Provides a simple health status for the API process.

Verified response:

{"status":"healthy"}

What AI changed in this session

Added the initial FastAPI application in app/main.py.

Added fastapi and uvicorn[standard] to requirements.txt.

Added the FastAPI architecture decision to decision.md.

Guided local verification of the API with Uvicorn and the browser/Swagger UI.

Verification result

Both / and /health were verified successfully, and the FastAPI interactive documentation displayed both endpoints.

Current limitation: No authentication, authorization, database, encryption, temporary credential, distributed-node, or failover logic exists yet.

---

## 10. Planned Data Access Flow — PostgreSQL Node

**Status:** Planned — not yet implemented.

The first database-backed request is planned to follow this flow:

User / Client
    |
    v
FastAPI API
    |
    v
Request validation
    |
    v
Data access layer
    |
    v
PostgreSQL Data Node
    |
    v
Retrieve only requested field
    |
    v
Return minimal response to client

### Planned Example

Request:

`GET /customer/101/email`

Expected behavior:

1. FastAPI receives the request.
2. The application validates the requested customer and field.
3. The data access layer queries PostgreSQL.
4. The query retrieves only the `email` field.
5. The application returns only the requested email.

### Important limitation

This flow is **planned only**. PostgreSQL has not yet been connected to the application, so no database call is currently verified.

---

## 11. Code-Verified PostgreSQL Node — Milestone 2

**Verified on:** 2026-08-13

### Docker service

Service: `postgres`

Container: `secure-data-postgres`

Image: `postgres:17`

Port: `5432`

### Verification

Command:

`docker compose up -d`

Result:

PostgreSQL container started successfully.

Command:

`docker ps`

Result:

`secure-data-postgres` is running and exposing port `5432`.

Command:

`docker exec secure-data-postgres pg_isready -U secure_user -d secure_data`

Result:

`/var/run/postgresql:5432 - accepting connections`

### Current verified flow

Docker Compose
    ↓
PostgreSQL container
    ↓
Database `secure_data`
    ↓
PostgreSQL accepts connections

### Current limitation

The FastAPI application is **not connected to PostgreSQL yet**.

No application-level database query has been implemented or verified.

---

## 12. Code-Verified PostgreSQL Connection — Milestone 3

**Verified on:** 2026-08-13

### Entry point

`app/database.py`

### Function

`get_connection()`

### Execution flow

Python application
    ↓
Imports `app.database`
    ↓
Calls `get_connection()`
    ↓
Reads database configuration
    ↓
Psycopg 3 creates PostgreSQL connection
    ↓
PostgreSQL accepts connection
    ↓
Connection is returned to the caller
    ↓
Caller closes the connection

### Verification command

`python -c "from app.database import get_connection; conn = get_connection(); print('Database connection successful'); conn.close()"`

### Verification result

`Database connection successful`

### Current limitation

The connection has been verified, but the application has not yet created any database tables or performed a data query.

The FastAPI request path is also not connected to the database yet.

---

## 13. Code-Verified Customer Data — Milestone 4

**Verified on:** 2026-08-13

### Database object

Table: `customers`

### Fields

- `id`
- `name`
- `email`
- `phone`
- `address`

### Verification

Command:

`Get-Content app/schema.sql | docker exec -i secure-data-postgres psql -U secure_user -d secure_data`

Result:

- Table created successfully.
- 3 records inserted successfully.

Command:

`docker exec secure-data-postgres psql -U secure_user -d secure_data -c "SELECT * FROM customers;"`

Result:

- Alice Johnson
- Bob Smith
- Charlie Brown

### Current verified data flow

Application / SQL script
    ↓
Docker PostgreSQL container
    ↓
`secure_data` database
    ↓
`customers` table
    ↓
3 development records

### Current limitation

The FastAPI API still does not query this table.

The next implementation will connect an API endpoint to this data and demonstrate retrieving only one requested field.

---

## 14. Code-Verified Customer Email Endpoint — Milestone 5

**Verified on:** 2026-08-13

### Endpoint

`GET /customer/{customer_id}/email`

### Execution flow

Browser / API client
    ↓
HTTP GET request
    ↓
`app.main`
    ↓
FastAPI router
    ↓
`get_customer_email(customer_id)`
    ↓
JSON response

### Verified request

`GET /customer/1/email`

### Verified response

```json
{
    "customer_id": 1,
    "email": "placeholder@example.com"
}

---

## 15. Code-Verified Database-Backed Customer Email Endpoint — Milestone 6

**Verified on:** 2026-08-13

### Endpoint

`GET /customer/{customer_id}/email`

### Execution flow

Browser / API client
    ↓
HTTP GET request
    ↓
`app.main`
    ↓
FastAPI router
    ↓
`get_customer_email(customer_id)`
    ↓
`get_connection()`
    ↓
Psycopg 3
    ↓
PostgreSQL `customers` table
    ↓
`SELECT email FROM customers WHERE id = %s`
    ↓
Email value returned
    ↓
JSON response

### Verified request

`GET /customer/1/email`

### Verified response

```json
{
    "customer_id": 1,
    "email": "alice@example.com"
}

---

## 16. Code-Verified JWT Token Generation — Milestone 7

**Verified on:** 2026-08-13

### Function

`app.auth.create_access_token(user_id)`

### Execution flow

Application
    ↓
`create_access_token(1)`
    ↓
Read `JWT_SECRET` from environment
    ↓
Create JWT payload
    ↓
Add subject (`sub`)
    ↓
Add expiration (`exp`)
    ↓
Sign token using HS256
    ↓
Return JWT string

### Verification command

`python -c "from app.auth import create_access_token; print(create_access_token(1))"`

### Verification result

A signed JWT was generated successfully.

No insecure-key warning was produced after replacing the hardcoded fallback secret with the environment-based secret.

### Security improvement

The application no longer uses a weak hardcoded JWT signing secret.

The signing secret must now be supplied through the `JWT_SECRET` environment variable.

### Current limitation

We have verified token generation, but we have **not yet implemented**:

- User login
- Password verification
- JWT validation
- Protected API endpoints
- Authorization

---

## 17. Code-Verified Users Table — Milestone 8

**Verified on:** 2026-08-13

### Database object

Table: `users`

### Fields

- `id` — primary key
- `username` — unique username
- `password_hash` — stored password hash

### Verification

Command:

`Get-Content app/users.sql | docker exec -i secure-data-postgres psql -U secure_user -d secure_data`

Result:

`CREATE TABLE`

Command:

`docker exec secure-data-postgres psql -U secure_user -d secure_data -c "\d users"`

Result:

- `id` is the primary key.
- `username` has a unique constraint.
- `password_hash` is required.
- No plaintext password field exists.

### Current verified flow

User schema
    ↓
PostgreSQL
    ↓
`users` table
    ↓
Username + password hash can be stored

### Current limitation

No user record has been created yet.

Password hashing and login verification have not yet been connected to this table.

---

## 18. Code-Verified Argon2 Password Hashing — Milestone 9

**Verified on:** 2026-08-13

### Functions

`app.password.hash_password(password)`

`app.password.verify_password(password, password_hash)`

### Execution flow

Plaintext password
    ↓
`hash_password()`
    ↓
Argon2 PasswordHasher
    ↓
Password hash

For verification:

Submitted password
    ↓
`verify_password()`
    ↓
Compare against stored Argon2 hash
    ↓
True / False

### Verification command

`python -c "from app.password import hash_password, verify_password; h = hash_password('TestPassword123!'); print('Hash generated:', h != 'TestPassword123!'); print('Correct password:', verify_password('TestPassword123!', h)); print('Wrong password:', verify_password('WrongPassword!', h))"`

### Verification result

- Hash generated: `True`
- Correct password: `True`
- Wrong password: `False`

### Security result

Passwords are hashed before storage and are not stored as plaintext.

### Current limitation

Password hashing is verified, but it has not yet been connected to the `users` table or login endpoint.

---

## 19. Code-Verified Development User — Milestone 10

**Verified on:** 2026-08-13

### Database object

Table: `users`

### Development account

Username: `testuser`

Password: stored only as an Argon2 hash.

### Verification

The user record was inserted into PostgreSQL and then queried directly.

Verified result:

- User record exists.
- Username is `testuser`.
- Password is stored as an Argon2 hash beginning with `$argon2id$`.
- No plaintext password is stored in the database.

### Current verified flow

Development password
    ↓
Argon2 hashing
    ↓
Password hash
    ↓
`users.password_hash`
    ↓
PostgreSQL

### Security note

The development password is known only for local testing. It must not be reused for a real deployment.

### Current limitation

The login endpoint has not yet been implemented.

The application still does not retrieve the user record and verify the submitted password during an API login request.

---

## 20. Code-Verified Login Endpoint Structure — Milestone 11

**Verified on:** 2026-08-13

### Endpoint

`POST /login`

### Request model

`LoginRequest`

Fields:

- `username`
- `password`

### Execution flow

Swagger / API client
    ↓
`POST /login`
    ↓
Pydantic validates `LoginRequest`
    ↓
`login(request)`
    ↓
Placeholder response

### Verification result

The endpoint returned HTTP 200 successfully.

The response confirmed that the submitted username reached the login function.

### Current limitation

The endpoint currently does **not**:

- Query PostgreSQL for the user
- Verify the password against the Argon2 hash
- Generate a JWT
- Reject invalid credentials

### Next implementation

Connect the login function to PostgreSQL and verify the submitted password using the existing Argon2 password-verification function.

---

## 21. Code-Verified Database-Backed JWT Login — Milestone 12

**Verified on:** 2026-08-13

### Endpoint

`POST /login`

### Execution flow

Client
    ↓
POST `/login`
    ↓
`LoginRequest` validation
    ↓
Query PostgreSQL `users`
    ↓
Find username
    ↓
Retrieve `password_hash`
    ↓
Argon2 password verification
    ↓
Create JWT with `create_access_token()`
    ↓
Return bearer access token

### Verified request

```json
{
    "username": "testuser",
    "password": "TestPassword123!"
}

Verification result

HTTP status: 200

Response contains:

{
    "access_token": "<signed JWT>",
    "token_type": "bearer"
}
Security result
Password was verified against the stored Argon2 hash.
The plaintext password was not returned.
A signed JWT was generated only after successful authentication.
Current limitation

The JWT is currently issued but is not yet required to access the customer data endpoint.

The next step is JWT validation and protecting /customer/{customer_id}/email.

---

## 22. Code-Verified Protected Customer Endpoint — Milestone 13

**Verified on:** 2026-08-13

### Endpoint

`GET /customer/{customer_id}/email`

### Test

A request was made without an `Authorization: Bearer <JWT>` header.

### Execution flow

Client
    ↓
GET `/customer/1/email`
    ↓
`get_current_user()`
    ↓
No bearer token
    ↓
FastAPI security dependency rejects request
    ↓
HTTP 401 response

### Verification result

Response:

```json
{
    "detail": "Not authenticated"
}

Security result

Unauthenticated clients cannot reach the customer-data query.

Current limitation

A valid JWT is now required, but the system does not yet check whether the authenticated user is authorized to access the requested customer data.

---

## 23. Code-Verified Authenticated Customer Data Request — Milestone 14

**Verified on:** 2026-08-13

### Endpoint

`GET /customer/{customer_id}/email`

### Verification

A valid JWT obtained from `POST /login` was supplied as:

`Authorization: Bearer <JWT>`

### Execution flow

Client
    ↓
Valid bearer JWT
    ↓
`get_current_user()`
    ↓
JWT signature and expiration validation
    ↓
Authenticated user ID obtained
    ↓
`get_customer_email(customer_id)`
    ↓
PostgreSQL query
    ↓
`SELECT email FROM customers WHERE id = %s`
    ↓
Only email returned

### Verified request

`GET /customer/1/email`

### Verification result

HTTP status: `200`

Response:

```json
{
    "customer_id": 1,
    "email": "alice@example.com"
}

Security result
Requests without a JWT are rejected.
Requests with a valid JWT can reach the protected endpoint.
The response still contains only the requested email field.
Current limitation

Authentication is implemented, but authorization is not.

---

## 24. Code-Verified User-to-Customer Authorization Data — Milestone 15

**Verified on:** 2026-08-13

### Authorization relationship

User:

`testuser`

Customer:

`Customer 1`

Database relationship:

`users.customer_id = 1`

### Verification

Command:

`docker exec secure-data-postgres psql -U secure_user -d secure_data -c "SELECT id, username, customer_id FROM users;"`

### Verification result

```text
id | username | customer_id
---+----------+------------
2  | testuser | 1

Current flow

Authenticated user
↓
JWT contains user ID
↓
User ID maps to users.customer_id
↓
Requested customer ID can be compared
↓
Authorization decision

Current limitation

The relationship exists in PostgreSQL, but the FastAPI endpoint does not yet enforce the comparison.

---

## 25. Code-Verified Fine-Grained Authorization — Milestone 16

**Verified on:** 2026-08-13

### Authorization rule

`testuser` is associated with `customer_id = 1`.

### Allowed request

`GET /customer/1/email`

Result:

```text
HTTP 200

The requested email was returned.

Denied request

GET /customer/2/email

The same valid JWT was used.

Result:

HTTP 403 Forbidden

Response:

{
    "detail": "You are not authorized to access this customer"
}
Execution flow

JWT
↓
Authenticated user ID
↓
Lookup users.customer_id
↓
Compare with requested customer_id
↓
Match → continue
No match → 403 Forbidden
↓
Only authorized customer data can be queried

Security result

A valid authentication token is not sufficient to access arbitrary customer data.

The server performs an additional authorization check before executing the customer-data query.

Current limitation

The authorization model currently uses simple user-to-customer ownership.

---

## 26. Code-Verified Data Node Directory — Milestone 17

**Verified on:** 2026-08-13

### Module

`app/node_directory.py`

### Components

`DataNode`

`get_node_for_data(data_type)`

### Verification

Command:

`python -c "from app.node_directory import get_node_for_data; node = get_node_for_data('customer'); print(node); print(node.name, node.host, node.port)"`

### Verification result

```text
DataNode(name='customer-node-1', host='localhost', port=5432)
customer-node-1 localhost 5432
Current verified flow

Requested data type
↓
get_node_for_data("customer")
↓
DATA_NODES lookup
↓
customer-node-1
↓
localhost:5432

Security result

The directory contains only routing metadata.

It does not contain the customer's actual data.

Current limitation

The customer API does not yet use the node directory to locate its database.

The current implementation still connects directly using the existing database configuration.

---

## 27. Code-Verified Data Minimization Layer — Milestone 18

**Verified on:** 2026-08-13

### Module

`app/data_minimizer.py`

### Functions

`validate_customer_field(field)`

`build_customer_select(field)`

### Allowed-field test

Input:

`email`

Result:

```sql
SELECT email FROM customers WHERE id = %s

The requested field was accepted and included as the only selected column.

Rejected-field test

Input:

password_hash

Result:

ValueError: Field 'password_hash' is not available for access.

The sensitive field was rejected because it is not present in the allowlist.

Current verified flow

Requested field
↓
validate_customer_field()
↓
Allowlisted?
├── No → reject request
└── Yes
↓
build_customer_select()
↓
Generate query for only the requested field

Security result

The data-minimization layer prevents arbitrary field selection and prevents password_hash from being requested through this component.

Current limitation

The customer API endpoint still contains its own SQL query and does not yet use build_customer_select().

---

## 28. Code-Verified Customer Data Node — Milestone 19

**Verified on:** 2026-08-13

### Service

`app/customer_node/main.py`

### Runtime

Command:

`python -m uvicorn app.customer_node.main:app --port 8001`

### Service address

`http://127.0.0.1:8001`

### Endpoint

`GET /health`

### Verification result

```json
{
    "node": "customer-node-1",
    "status": "healthy"
}
Current verified architecture

Main API
↓
Customer Data Node
↓
127.0.0.1:8001

Security / architecture result

The customer data node now runs as a separate application process from the main API.

This establishes the first explicit service boundary in the distributed architecture.

Current limitation

The customer data node does not yet own or query the PostgreSQL customer data.

The main API still performs the customer database query directly.

---

## 29. Code-Verified Customer Data Node Retrieval — Milestone 20

**Verified on:** 2026-08-13

### Endpoint

`GET /customer/{customer_id}/email`

### Service

Customer Data Node

Address:

`http://127.0.0.1:8001`

### Verification

Request:

`GET /customer/1/email`

Result:

```json
{
    "customer_id": 1,
    "email": "alice@example.com"
}
Execution flow

Client / Service
↓
Customer Data Node
↓
get_customer_email(customer_id)
↓
PostgreSQL
↓
SELECT email FROM customers WHERE id = %s
↓
Email returned

Current architecture

Main API
↓
Node Directory
↓
Customer Data Node :8001
↓
PostgreSQL

Current limitation

The main API does not yet call the customer data node.

The main API currently performs the customer-data retrieval itself.

---

## 30. Code-Verified Main API to Customer Node Flow — Milestone 21

**Verified on:** 2026-08-13

### Verified request

`GET /customer/1/email`

### Execution flow

Client
    ↓
Main API :8000
    ↓
JWT authentication
    ↓
Fine-grained authorization
    ↓
Node Directory
    ↓
HTTP request
    ↓
Customer Data Node :8001
    ↓
`GET /customer/1/email`
    ↓
PostgreSQL
    ↓
Customer email
    ↓
HTTP response to Main API
    ↓
Response to client

### Verification result

Main API returned:

```json
{
    "customer_id": 1,
    "email": "alice@example.com"
}

Customer Data Node log confirmed:

GET /customer/1/email HTTP/1.1" 200 OK
Architecture result

The main API successfully retrieved customer data through the separate customer data-node service.

The main API is no longer required to directly perform the customer-data retrieval query.

Current limitation

Only one data node exists.

Node 2 and Node 3, service-to-service authentication, encryption in transit, and failover have not yet been implemented.
