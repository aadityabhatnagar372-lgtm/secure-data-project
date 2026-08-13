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