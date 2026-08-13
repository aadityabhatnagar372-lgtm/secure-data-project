# Secure Data Project

A distributed secure-data prototype demonstrating authentication, authorization, data minimization, encryption, short-lived access keys, audit logging, application-level failover, and PostgreSQL streaming replication.

---

## Project Overview

The system provides controlled access to customer data through a main FastAPI application and multiple customer data nodes.

The architecture separates:

- Authentication
- Authorization
- Data minimization
- Encryption
- Temporary access keys
- Distributed data-node routing
- Audit logging
- Database replication
- Application-level failover

The project is implemented as a local Docker/Python prototype.

---

## Architecture

```text
                         Client
                           |
                           v
                  +------------------+
                  |   FastAPI API    |
                  |      :8000       |
                  +------------------+
                           |
                +----------+----------+
                |                     |
                v                     v
        Authentication          Access-Key Service
                |                     |
                +----------+----------+
                           |
                           v
                   Authorization
                           |
                           v
                  Data Minimization
                           |
                           v
                    Node Directory
                           |
                +----------+----------+
                |                     |
                v                     v
        Customer Node 1       Replica Nodes
             :8001              :8002/:8003
                |                     |
                +----------+----------+
                           |
                           v
                 PostgreSQL Primary
                      :5432
                           |
                  +--------+--------+
                  |                 |
                  v                 v
          PostgreSQL Replica 1  PostgreSQL Replica 2
                 :5433               :5434
Main Components
Main API

The main FastAPI application provides:

JWT authentication
Customer authorization
Access-key issuance
Access-key validation
Data-minimized customer retrieval
Primary/replica failover routing
Audit logging
Customer Data Nodes

The prototype contains three customer application nodes:

customer-node-1 → :8001 → primary
customer-node-2 → :8002 → replica
customer-node-3 → :8003 → replica

The main API attempts the primary node first and then attempts replicas when the primary is unavailable.

PostgreSQL

The database layer contains:

secure-data-postgres
    :5432
    Primary

secure-data-postgres-replica1
    :5433
    Replica 1

secure-data-postgres-replica2
    :5434
    Replica 2

Both replicas use PostgreSQL streaming replication from the primary.

Replication is asynchronous.

Security Controls
JWT Authentication

Users authenticate through the login endpoint and receive a JWT.

The customer-data endpoint requires a valid bearer token.

Unauthenticated requests are rejected with HTTP 401.

Authorization

The project verifies that the authenticated user is authorized to access the requested customer.

Unauthorized customer access is rejected with HTTP 403.

Short-Lived Access Keys

Access keys are:

Generated using secure random tokens
Scoped to a user
Scoped to a customer
Scoped to a field
Valid for approximately 10 minutes

The protected customer-data endpoint requires a valid access key in:

X-Access-Key

Expired or invalid access keys are rejected.

Field-Level Authorization

An access key scoped to phone cannot be used to retrieve email.

A key scoped to Customer 1 cannot be used to access Customer 2.

Data Minimization

Customer responses return only the requested field.

For example:

{
    "customer_id": 1,
    "email": "alice@example.com"
}

Sensitive or unrelated customer fields are not returned.

Encryption

The project uses the cryptography library and Fernet encryption.

Encryption keys are provided through environment configuration rather than hard-coded into the application.

Audit Logging

The application records security-relevant events including:

Login success
Login failure
Access-key issuance
Authorization denial
Customer-data access
Data-node errors
Failover exhaustion

Sensitive values such as:

passwords
password hashes
JWTs
access keys
encryption keys

are filtered from audit output.

Failover

Application-level failover follows:

Primary Node
    |
    | unavailable
    v
Replica Node 1
    |
    | unavailable
    v
Replica Node 2

The primary-node failure path was tested against the running application.

The request successfully returned customer data after Customer Node 1 was stopped, and Customer Node 2 was confirmed to serve the request.

PostgreSQL Replication

The PostgreSQL primary streams WAL changes to two replicas.

Verified topology:

                 Primary
             172.30.0.3
                  |
         +--------+--------+
         |                 |
         v                 v
      Replica 1         Replica 2
      172.30.0.2        172.30.0.4

Both replicas were verified with:

state = streaming
sync_state = async

A customer record created on the primary was successfully retrieved from both replicas.

Docker Compose

The PostgreSQL topology is managed through:

docker-compose.yml

Services:

postgres
postgres-replica1
postgres-replica2

All services use:

172.30.0.0/16

through the deterministic Docker network:

secure-data-project_secure_data_network

Persistent database volumes are used for the primary and both replicas.

Project Structure
secure-data-project/
│
├── app/
│   ├── access_key.py
│   ├── access_key_store.py
│   ├── audit.py
│   ├── auth.py
│   ├── database.py
│   ├── data_minimizer.py
│   ├── encryption.py
│   ├── login.py
│   ├── node_directory.py
│   ├── password.py
│   └── routes.py
│
├── app/
│   ├── customer_node/
│   ├── customer_node_2/
│   └── customer_node_3/
│
├── docker/
│   └── postgres/
│       └── pg_hba.conf
│
├── tests/
│   ├── __init__.py
│   ├── test_access_key.py
│   ├── test_audit.py
│   ├── test_auth.py
│   ├── test_data_minimizer.py
│   ├── test_encryption.py
│   └── test_failover.py
│
├── decision.md
├── flow.md
├── docker-compose.yml
├── requirements.txt
└── README.md
Testing

The automated test suite currently contains:

18 tests
18 passed

Verified test areas:

Access Keys
4 tests passed
Audit Logging
2 tests passed
Authentication
3 tests passed
Data Minimization
5 tests passed
Encryption
2 tests passed
Failover
2 tests passed

Full test command:

pytest -v

Verified result:

18 passed
Manual Security Verification

The following behaviors were manually verified:

Unauthenticated access rejected
Missing access key rejected
Expired access key rejected
Wrong-customer access key rejected
Wrong-field access key rejected
Data minimization verified
Fernet encryption verified
Primary application-node failure verified
Replica recovery verified
PostgreSQL Replica 1 verified
PostgreSQL Replica 2 verified
Both PostgreSQL replicas verified as streaming
Environment Variables

The project uses environment variables for secrets and security configuration.

Examples include:

JWT_SECRET
ENCRYPTION_KEY
ENCRYPTION_KEY

Secrets should never be committed to Git.

For local development, configure them in the active environment before starting the application.

Running the PostgreSQL Topology

Start the database topology with:

docker compose up -d

Check the services:

docker compose ps

The expected database services are:

secure-data-postgres
secure-data-postgres-replica1
secure-data-postgres-replica2
Running the Main API

Activate the virtual environment:

.venv\Scripts\Activate.ps1

Start the FastAPI application:

python -m uvicorn app.main:app --port 8000

Swagger documentation:

http://127.0.0.1:8000/docs
Limitations

This project is a local security and distributed-systems prototype.

Important limitations include:

PostgreSQL replication is asynchronous.
Automatic PostgreSQL primary promotion/election is not implemented.
Application-level failover is implemented separately from database promotion.
Access-key storage is currently application-level storage and is not yet a shared distributed store.
Audit logs are application logs rather than a centralized production logging system.
Full production secret management is not implemented.
The current automated suite focuses primarily on unit-level and mocked failover behavior.
Full production operational monitoring and centralized observability are outside the current scope.
Security Design Summary

The protected-data flow is:

JWT Authentication
        |
        v
Customer Authorization
        |
        v
Access-Key Validation
        |
        +--> User Scope
        |
        +--> Customer Scope
        |
        +--> Field Scope
        |
        v
Data Minimization
        |
        v
Primary Data Node
        |
        +--> Replica Failover
        |
        v
Customer Data
        |
        v
Audit Event
Current Verification Status
Authentication                  ✅
Authorization                  ✅
Data minimization              ✅
Encryption                     ✅
Short-lived access keys        ✅
Access-key expiry              ✅
Field-level access control     ✅
Application failover           ✅
PostgreSQL replication         ✅
Audit logging                  ✅
Automated tests                ✅
Final security verification    ✅
Final documentation            ⏳
Project Documentation

Detailed implementation decisions and verification history are maintained in:

decision.md
flow.md

These files document the architecture, security decisions, implementation milestones, testing, replication setup, failover behavior, and verification results.