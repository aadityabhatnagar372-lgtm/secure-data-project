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

---

## 31. Code-Verified Customer Data Node 2 — Milestone 22

**Verified on:** 2026-08-13

### Service

`app/customer_node_2/main.py`

### Runtime

Command:

`python -m uvicorn app.customer_node_2.main:app --port 8002`

### Service address

`http://127.0.0.1:8002`

### Endpoint

`GET /health`

### Verification result

```json
{
    "node": "customer-node-2",
    "status": "healthy"
}
Current distributed-node architecture

Customer Node 1
↓
127.0.0.1:8001

Customer Node 2
↓
127.0.0.1:8002

Architecture result

Two independent customer data-node services can run simultaneously on separate ports.

Current limitation

Node 2 currently provides only a health endpoint.

It is not yet connected to customer data or used by the node directory for request routing.

---

## 32. Code-Verified Customer Data Node 3 — Milestone 23

**Verified on:** 2026-08-13

### Service

`app/customer_node_3/main.py`

### Runtime

Command:

`python -m uvicorn app.customer_node_3.main:app --port 8003`

### Service address

`http://127.0.0.1:8003`

### Endpoint

`GET /health`

### Verification result

```json
{
    "node": "customer-node-3",
    "status": "healthy"
}
Current distributed-node architecture

Customer Node 1
↓
127.0.0.1:8001

Customer Node 2
↓
127.0.0.1:8002

Customer Node 3
↓
127.0.0.1:8003

Architecture result

Three independent customer data-node services can now run simultaneously on separate ports.

Current limitation

Only Node 1 currently serves customer data.

Nodes 2 and 3 currently provide health endpoints only.

The node directory does not yet route requests between all three nodes.

---

## 33. Code-Verified Fernet Encryption — Milestone 24

**Verified on:** 2026-08-13

### Module

`app/encryption.py`

### Functions

`encrypt_data(data)`

`decrypt_data(token)`

### Verification

Test plaintext:

`Sensitive test data`

Encryption produced a Fernet token successfully.

Decryption returned the original plaintext.

### Verification result

```text
Decryption successful: True
Current verified flow

Plaintext data
↓
encrypt_data()
↓
Fernet encrypted token
↓
decrypt_data()
↓
Original plaintext

Security result

The encryption key is supplied through the ENCRYPTION_KEY environment variable rather than being hardcoded in source code.

The round-trip test confirms that encrypted data can be recovered with the correct key.

Current limitation

The encryption service is not yet integrated into the customer-data request flow.

---

## 34. Code-Verified 10-Minute Access Key Generation — Milestone 25

**Verified on:** 2026-08-13

### Module

`app/access_key.py`

### Function

`generate_access_key(user_id, customer_id, field)`

### Verification

Test input:

- User ID: `2`
- Customer ID: `1`
- Field: `email`

### Verification result

- Token generated: `True`
- User ID: `2`
- Customer ID: `1`
- Field: `email`
- Expiration was generated approximately 10 minutes after creation.

### Current verified flow

Authorized user
    ↓
`generate_access_key()`
    ↓
Cryptographically random token
    ↓
Bind token to user/customer/field
    ↓
Set expiration to 10 minutes
    ↓
Return access-key record

### Security result

The access key is:

- Random
- User-scoped
- Customer-scoped
- Field-scoped
- Time-limited

### Current limitation

The access key is only generated at this stage.

It is not yet stored, validated, used to access data, or rejected after expiration.

### Next step

Implement access-key storage and validation so expired or incorrectly scoped keys cannot be used.

---

## 35. Code-Verified Access Key Storage and Expiry — Milestone 26

**Verified on:** 2026-08-13

### Module

`app/access_key_store.py`

### Functions

`store_access_key(access_key)`

`get_access_key(token)`

### Valid-key verification

A generated access key was stored and then retrieved successfully.

Verified:

- User ID: `2`
- Customer ID: `1`
- Field: `email`

### Expired-key verification

A key with an expiration timestamp one second in the past was stored.

Validation result:

```text
Before validation: None
After validation: None

The expired key was rejected and removed from the in-memory store.

Current verified flow

Generate access key
↓
Store access key
↓
Client presents token
↓
get_access_key(token)
↓
Check expiration
├── Valid → return scoped access record
└── Expired → remove and reject

Security result

The access-key store now enforces server-side expiration.

A key cannot be retrieved from the store after its expiration time.

Current limitation

The access key is not yet connected to the customer-data request flow.

The application does not yet require this 10-minute key before returning protected data.

The store is also in-memory, so it is not shared between multiple API processes or nodes.

---

## 36. Code-Verified Scoped Access-Key Issuance — Milestone 27

**Verified on:** 2026-08-13

### Endpoint

`POST /access-key`

### Verified request

```json
{
    "customer_id": 1,
    "field": "email"
}

A valid JWT was supplied with the request.

Verification result

HTTP status: 200

Response contained:

access_key
customer_id = 1
field = email
expires_at

The expiration timestamp was approximately 10 minutes after issuance.

Verified flow

JWT
↓
Authentication
↓
Customer authorization
↓
Generate scoped access key
↓
Store access key
↓
Return token and expiration

Security result

The temporary access key is issued only after the authenticated user passes the customer authorization check.

The key is scoped to the requested customer and field and has a 10-minute expiration.

Current limitation

The customer-data endpoint does not yet require the issued access key.

---

## 37. Code-Verified Access-Key Enforcement — Milestone 28

**Verified on:** 2026-08-13

### Endpoint

`GET /customer/{customer_id}/email`

### Test

A valid JWT was supplied, but no `X-Access-Key` header was provided.

### Verification result

HTTP status:

`401 Unauthorized`

Response:

```json
{
    "detail": "Access key is required"
}
Security result

A valid JWT alone is no longer sufficient to retrieve customer data.

The protected data endpoint now requires both:

JWT authentication
A valid scoped access key
Current flow

JWT
↓
Authenticate user
↓
Require X-Access-Key
↓
Validate access key
↓
Validate scope
↓
Retrieve customer data

Current limitation

We have verified that the access key is required, but we still need to verify:

valid access key → allowed
wrong customer → rejected
wrong user → rejected
wrong field → rejected
expired access key → rejected

---

## 38. Code-Verified Temporary Access-Key Data Retrieval — Milestone 29

**Verified on:** 2026-08-13

### Endpoint

`GET /customer/{customer_id}/email`

### Required credentials

- Valid JWT
- Valid `X-Access-Key`

### Verification

A valid JWT was used to authenticate the user.

A newly issued 10-minute access key scoped to:

- Customer: `1`
- Field: `email`

was supplied in the `X-Access-Key` header.

### Verification result

HTTP status:

`200 OK`

Response:

```json
{
    "customer_id": 1,
    "email": "alice@example.com"
}
Verified flow

JWT
↓
Authentication
↓
Customer authorization
↓
Issue scoped access key
↓
Store access key
↓
Client supplies X-Access-Key
↓
Validate token
↓
Validate user scope
↓
Validate customer scope
↓
Validate field scope
↓
Customer Data Node
↓
Return customer email

Security result

The customer-data endpoint now requires both authentication and a valid short-lived scoped access key.

The access key limits access to the authorized user, customer, and field and expires after 10 minutes.

Current limitation

The valid-key path is verified.

Remaining access-key security tests include:

Wrong customer
Wrong user
Wrong field
Expired key

These tests should be completed before marking the access-key integration fully tested.

---

## 39. Code-Verified Access-Key Customer Scope — Milestone 30

**Verified on:** 2026-08-13

### Test

An access key issued for:

- Customer: `1`
- Field: `email`

was used to request:

`GET /customer/2/email`

The JWT was valid.

### Verification result

HTTP status:

`403 Forbidden`

Response:

```json
{
    "detail": "Access key is not valid for this customer"
}
Security result

An access key cannot be reused to access a different customer from the customer for which it was issued.

Current verified access-key controls
Authentication through JWT
Customer authorization
Access-key existence
Access-key expiration
User scope
Customer scope

---

## 40. Code-Verified Access-Key Field Scope — Milestone 31

**Verified on:** 2026-08-13

### Test

A valid access key was issued with:

- Customer: `1`
- Field: `phone`

The same key was then used to request:

`GET /customer/1/email`

The JWT was valid and the customer matched, but the access-key field scope did not match the requested field.

### Verification result

HTTP status:

`403 Forbidden`

Response:

```json
{
    "detail": "Access key is not valid for this field"
}
Security result

An access key scoped to one field cannot be reused to access a different field.

Verified access-key controls
Token existence
Token expiration
User scope
Customer scope
Field scope

---

## 41. Code-Verified Access-Key Expiration — Milestone 32

**Verified on:** 2026-08-13

### Test

An access-key record with an expiration timestamp one second in the past was inserted into the access-key store.

### Verification result

```text
Expired key result: None

The expired key was rejected by get_access_key().

Security result

Expired access keys cannot be retrieved from the access-key store and therefore cannot be used for protected data access.

Verified access-key controls
Token existence
10-minute expiration
User scope
Customer scope
Field scope
Current limitation

Expiration has been verified at the access-key store level.

---

## 42. Code-Verified Primary and Replica Node Directory — Milestone 33

**Verified on:** 2026-08-13

### Module

`app/node_directory.py`

### Verification

Command:

`python -c "from app.node_directory import get_primary_node, get_replica_nodes; print('Primary:', get_primary_node('customer')); print('Replicas:', get_replica_nodes('customer'))"`

### Verification result

Primary:

```text
DataNode(
    name='customer-node-1',
    host='localhost',
    port=8001,
    role='primary'
)

Replicas:

DataNode(
    name='customer-node-2',
    host='localhost',
    port=8002,
    role='replica'
)

DataNode(
    name='customer-node-3',
    host='localhost',
    port=8003,
    role='replica'
)
Current architecture

Customer data
↓
Primary Node 1
↓
Replica Node 2
↓
Replica Node 3

Security / availability result

The directory now explicitly identifies the primary node and replica nodes, providing the metadata required for an explicit failover path.

Current limitation

The replicas are metadata entries only.

Actual customer-data replication has not yet been implemented, and the request flow does not yet automatically fail over to a replica when the primary is unavailable.

---

## 43. Code-Verified Primary-to-Replica Failover — Milestone 34

**Verified on:** 2026-08-13

### Failure condition

Customer Node 1 was stopped and was therefore unavailable on port `8001`.

### Request

The main API received:

`GET /customer/1/email`

with a valid JWT and valid scoped access key.

### Main API result

HTTP status:

`200 OK`

Response:

```json
{
    "customer_id": 1,
    "email": "alice@example.com"
}
Replica verification

Customer Node 2 log confirmed:

GET /customer/1/email HTTP/1.1" 200 OK
Verified flow

Main API
↓
Primary Node 1 unavailable
↓
Try Replica Node 2
↓
Customer data retrieved
↓
HTTP 200 returned to client

Availability result

The main API can continue serving an authorized request when the primary application node is unavailable.

Current limitation

The current implementation demonstrates application-level service failover.

Node 2 and Node 3 currently use the same PostgreSQL data source, so independent database replication has not yet been implemented.

---

## 44. Code-Verified PostgreSQL Streaming Replication — Milestone 35

**Verified on:** 2026-08-13

### Primary database

`secure-data-postgres:5432`

### Replica database

`secure-data-postgres-replica1:5433`

### Replication state

Replica 1 reported:

```text
status = streaming
sender_host = secure-data-postgres
sender_port = 5432

Replica 1 also reported:

pg_is_in_recovery() = true
Replication test

A new customer record was inserted into the primary:

id = 4
name = Replication Test
email = replication@example.com

The same record was then queried from Replica 1 and returned successfully.

Verification result
Primary
    ↓
WAL streaming replication
    ↓
Replica 1
    ↓
Replication Test record available
Security / availability result

The first independent PostgreSQL replica is now receiving changes from the primary.

This provides actual database-level redundancy in addition to the previously implemented application-level failover.

Current limitation

Only Replica 1 has been configured so far.

Replica 2 has not yet been configured for PostgreSQL streaming replication.

---

## 45. Code-Verified PostgreSQL Replica 2 — Milestone 36

**Verified on:** 2026-08-13

### Replica 2

Container:

`secure-data-postgres-replica2`

Host port:

`5434`

### Replication state

Replica 2 reported:

```text
pg_is_in_recovery() = true

Its WAL receiver reported:

status = streaming
sender_host = secure-data-postgres
sender_port = 5432
Replication test

The record created on the primary:

id = 4
name = Replication Test
email = replication@example.com

was successfully retrieved from Replica 2.

Verification result
Primary
    ↓
WAL streaming
    ├── Replica 1
    └── Replica 2

Both replicas now contain the replicated test record.

Availability result

The PostgreSQL layer now has:

1 primary
2 streaming replicas
Current limitation

The database replicas are running independently, but the Docker Compose configuration has not yet been updated to manage the complete replication topology declaratively.

The application services also still need explicit database-node-to-database mapping.

---

## 46. Code-Verified Dual PostgreSQL Replication Streams — Milestone 37

**Verified on:** 2026-08-13

### Primary replication status

The primary PostgreSQL server reported two active WAL replication connections.

### Verification command

`docker exec secure-data-postgres psql -U secure_user -d secure_data -c "SELECT application_name, client_addr, state, sync_state FROM pg_stat_replication;"`

### Verification result

```text
application_name | client_addr | state      | sync_state
-----------------+-------------+------------+-----------
walreceiver      | 172.18.0.3  | streaming  | async
walreceiver      | 172.18.0.4  | streaming  | async
Interpretation
Replica 1 is actively streaming from the primary.
Replica 2 is actively streaming from the primary.
Both replicas are asynchronous standbys.
Current architecture

PostgreSQL Primary
↓ WAL streaming
├── PostgreSQL Replica 1
└── PostgreSQL Replica 2

Availability result

The PostgreSQL layer now has two active streaming replicas.

Combined with the application-level failover routing, the system has both:

database-level replication
application-level replica failover
Current limitation

The replication topology is currently created manually with Docker commands.

---

## 47. Code-Verified Dual PostgreSQL Replica Topology — Milestone 38

**Verified on:** 2026-08-13

### Primary database

`secure-data-postgres`

Network address:

`172.30.0.3`

### Replica 1

`secure-data-postgres-replica1`

Network address:

`172.30.0.2`

### Replica 2

`secure-data-postgres-replica2`

Network address:

`172.30.0.4`

### Replication status

The primary reported two active replication connections:

```text
client_addr | state      | sync_state
------------+------------+-----------
172.30.0.2 | streaming  | async
172.30.0.4 | streaming  | async
Data replication verification

The test record:

id = 4
name = Replication Test
email = replication@example.com

was successfully retrieved from Replica 1 and Replica 2.

Verified architecture
                PostgreSQL Primary
                172.30.0.3
                      │
             ┌────────┴────────┐
             │                 │
          streaming         streaming
             │                 │
             ▼                 ▼
        Replica 1          Replica 2
        172.30.0.2         172.30.0.4
             │                 │
             └──── replicated data ────┘
Availability result

The system now has:

one PostgreSQL primary
two PostgreSQL streaming replicas
verified data replication to both replicas
application-level failover routing
Current limitation

The Docker Compose file currently defines the primary and Replica 1, but Replica 2 still needs to be added declaratively to Compose.

The existing manually created Replica 2 should remain running until its Compose definition is added and verified.

---

## 48. Code-Verified Compose-Managed PostgreSQL Topology — Milestone 39

**Verified on:** 2026-08-13

### Docker Compose services

```text
secure-data-postgres
    PostgreSQL Primary
    Host port: 5432

secure-data-postgres-replica1
    PostgreSQL Replica 1
    Host port: 5433

secure-data-postgres-replica2
    PostgreSQL Replica 2
    Host port: 5434
Verification

Command:

docker compose ps

Result:

secure-data-postgres            Up
secure-data-postgres-replica1   Up
secure-data-postgres-replica2   Up
Replication verification

The primary reported two active WAL streaming connections:

172.30.0.2 → streaming → async
172.30.0.4 → streaming → async
Architecture result

The PostgreSQL primary and both replicas are now managed by the project's Docker Compose configuration.

All three services use the deterministic Docker network:

secure-data-project_secure_data_network

with subnet:

172.30.0.0/16

Availability result

The project now has a reproducible local PostgreSQL topology consisting of one primary and two streaming replicas.

Current limitation

The database replication is asynchronous.

The project does not yet implement automatic PostgreSQL promotion/election if the primary database itself fails. Application-level failover has been implemented separately.

---

## 49. Code-Verified Secure Audit Logging — Milestone 40

**Verified on:** 2026-08-13

### Module

`app/audit.py`

### Function

`audit_event(event, **details)`

### Verification

A `login_success` audit event was generated with normal event details and deliberately supplied sensitive values.

### Verification result

```text
audit_event=login_success details={'user_id': 2, 'username': 'testuser'}
Audit test completed

The following sensitive values were intentionally supplied but were not included in the log:

Password
Access key
Other configured secret fields
Security result

The audit logger records security-relevant events while filtering configured sensitive fields from log output.

Current limitation

The audit logger has been verified independently, but security events have not yet been added to the actual login, access-key, authorization, data-access, and failover paths.

---

## 50. Code-Verified Login Audit Logging — Milestone 41

**Verified on:** 2026-08-13

### Integrated events

The login flow now records:

- `login_success`
- `login_failure`

### Successful-login verification

```text
audit_event=login_success details={'user_id': 2, 'username': 'testuser'}
Successful login audit test completed
Failed-login verification
audit_event=login_failure details={'username': 'testuser'}
Failed login audit test completed
Security result

Login events are now auditable without logging:

passwords
password hashes
JWTs
access keys
encryption keys
other configured secrets
Current limitation

Audit logging is currently integrated into the login flow only.

It has not yet been integrated into:

access-key issuance
access-key rejection
authorization denial
customer-data access
node failover
data-node errors

---

## 51. Code-Verified Protected Data Audit Logging — Milestone 42

**Verified on:** 2026-08-13

### Verified audit events

The protected-data flow now records:

- `access_key_issued`
- `authorization_denied`
- `customer_data_access`

### Verification result

```text
audit_event=access_key_issued details={'user_id': 2, 'customer_id': 1, 'field': 'email'}
audit_event=authorization_denied details={'user_id': 2, 'customer_id': 2, 'reason': 'customer_mismatch'}
audit_event=customer_data_access details={'user_id': 2, 'customer_id': 1, 'field': 'email'}
Protected-flow audit test completed
Secret filtering

An access-key value was deliberately supplied to the audit function:

DO_NOT_LOG

The value was not included in the generated log output.

Security result

Audit logging is now integrated into important protected-data workflows without exposing the access-key token.

Current limitation

Node failover events and data-node errors are not yet explicitly logged.

---

## 52. Code-Verified Node Failover Audit Logging — Milestone 43

**Verified on:** 2026-08-13

### Verified audit events

The node-routing layer now records:

- `data_node_error`
- `data_node_failover_exhausted`

### Verification result

```text
audit_event=data_node_error details={'node': 'customer-node-1', 'customer_id': 1, 'error': 'connection_error'}
audit_event=data_node_failover_exhausted details={'customer_id': 1, 'attempted_nodes': ['customer-node-1', 'customer-node-2', 'customer-node-3']}
Failover audit test completed
Security result

Node failures and exhausted failover attempts are now observable through the audit logger.

No JWT, access key, password, or encryption key is included in these events.

Current audit coverage

The application now has audit logging for:

Login success
Login failure
Access-key issuance
Authorization denial
Customer-data access
Data-node errors
Failover exhaustion

---

## 53. Code-Verified Automated Test Suite — Milestone 44

**Verified on:** 2026-08-13

### Test command

```text
pytest -v
Verification result
18 passed in 0.38s
Test coverage
Access-key tests
Scoped access-key generation
10-minute expiration
Access-key storage and retrieval
Expired access-key rejection
Audit tests
Safe audit details are logged
Sensitive values are filtered
Authentication tests
JWT contains the user ID
JWT expiration is present
Valid bearer credentials return the user ID
Invalid JWTs are rejected
Data-minimization tests
Allowed customer fields
Valid email field
Unauthorized field rejection
Correct email SELECT query
Unauthorized field rejection in query builder
Encryption tests
Fernet encrypt/decrypt round trip
Encrypted value does not contain plaintext
Failover tests
Primary failure causes replica usage
All-node failure produces 503
Overall result
18 / 18 automated tests passed

The current automated suite covers the core security and availability mechanisms implemented by the prototype.

Current limitation

The tests are primarily unit-level tests and mocked failover tests.

---

## 54. Final Security Verification Checklist — Milestone 45

**Verification scope**

The final manual verification will cover the major security and availability controls implemented in the project.

### Authentication

- Valid JWT authentication
- Invalid JWT rejection
- Successful login audit event
- Failed login audit event

### Authorization

- Unauthorized customer access rejected
- Wrong-user access key rejected
- Wrong-customer access key rejected
- Wrong-field access key rejected

### Data minimization

- Only the requested customer field is returned
- Unauthorized fields are rejected

### Short-lived access keys

- Access key generation
- Approximately 10-minute expiration
- Expired key rejection
- Missing access key rejection

### Encryption

- Fernet encryption/decryption
- Plaintext is not exposed in encrypted output
- Encryption key is supplied through environment configuration

### Audit logging

- Login events
- Authorization-denial events
- Access-key issuance
- Customer-data access
- Data-node errors
- Failover exhaustion
- Sensitive secrets excluded from logs

### Availability

- Primary node failure
- Application-level replica failover
- PostgreSQL Replica 1
- PostgreSQL Replica 2
- Streaming replication to both replicas

### Automated verification

Current automated result:

`18 passed`

### Final limitation

The final manual security verification must still be performed against the running application and Docker PostgreSQL topology before the project can be considered fully verified.

### Final documentation

After the manual checks pass, update the README with the final architecture, security controls, verification results, and project limitations.

---

## 55. Code-Verified Expired Access-Key Rejection — Milestone 46

**Verified on:** 2026-08-13

### Test

An access key with an expiration timestamp in the past was created and supplied to:

`GET /customer/1/email`

A valid JWT was also supplied.

### Verification result

HTTP status:

`401 Unauthorized`

Response:

```json
{
    "detail": "Invalid or expired access key"
}
Security result

The protected customer-data endpoint rejects expired access keys before data retrieval occurs.

Access-key verification summary

The following behaviors have now been verified:

Access-key generation
Access-key storage
Approximately 10-minute expiration
Missing access-key rejection
Expired access-key rejection
User scope validation
Customer scope validation
Field scope validation