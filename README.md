## Overview
This project is a maintainable and secure RESTful Task Management API that demonstrates layered architecture design and ownership-based authorization.
It prevents unauthorized access to user-owned resources by enforcing JWT authentication and strict resource ownership validation.
This project also emphasis automatic testing,API documentation, containarized deployment.

## Highlight
JWT authentication
Ownership-based authorization
Automatic testing with pytest
OpenAPI3.0 ducumentation with Swagger UI
Dockerize deployment

## Tech stack
Backend
 - Python
 - Flask (Web Framework)
Database
 - SQLAlchemy2.0 (ORM)
 - MariaDB (Relation Database)
Security
 - JWT Authentication (flask-jwt-extended)
 - Ownership Authorization
Engineering practices
 - OpenAPI 3.0 (Swagger UI)
 - Pytest (Automated Testing)
 - Docker & Docker Compose

## Architecture
The backend fallows layer architecture

client 
 |
routes layer
 |
service layer
 |
model layer
 |
database

This seperate improve maintainability, testibility and clarity of business logic.

## Feature
Core Feature
 - Full CRUD operations for task management
 - OpenAPI 3.0 interactive API documention (Swagger UI)
 - Automated coverage with pytest
 - Containerize deployment using Docker Compose
 - CI pipeline automated validation
Secure
 - User authentication with JWT
 - Owership-Based autorization to protect user resources 
Engineering pratices
 - OpenAPI 3.0 interactive API documention (Swagger UI)
 - Automated coverage with pytest
 - Containerize deployment using Docker Compose
 - CI pipeline automated validation

## testing
Automated testing is implemented with pytest.

The test critical flow included:

 - JWT Authentication.
 - Ownenship-based Authorization.
 - TaskCRUD operations.
 - API error handling.

test can be executed with pytest.

## Document
- [Test Plan](docs/test-plan-v1.md)
- [Test Cases](docs/text_cases.md)

## Test Coverage Categories

- **Authentication**: verifies that requests without a valid token are rejected.
- **Authorization**: verifies that users cannot access or modify resources they do not own.
- **Success Path**: verifies that valid requests succeed and return expected responses.
- **Validation / Business Rule**: verifies that invalid inputs, such as missing fields, invalid values, malformed JSON, or duplicate data, are rejected with proper error responses.
- **Error Handling**: verifies that not-found scenarios and error responses follow a consistent JSON structure with correct status codes and standardized fields such as `code`, `type`, and `message`.

## how to run
enviroment variebles
copy .env.example .env
Run with Docker
docker compose up -d
API documentation:
https://project-task-api-q2o5.onrender.com/docs

## Project structure
app/ 
    routes/
    service/
    model/
tests/
docker-compose.yml
READNE.md
