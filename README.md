## Overview
This project is a maintainable and secure RESTful Task Management API that demonstrates layered architecture design and ownership-based authorization.
It prevents unauthorized access to user-owned resources by enforcing JWT authentication and strict resource ownership validation.
This project also emphasizes automatic testing,API documentation, containarized deployment.

## Highlights
JWT authentication
Ownership-based authorization
Automatic testing with pytest
OpenAPI 3.0 ducumentation with Swagger UI
Dockerized deployment

## Tech stack
Backend
 - Python
 - Flask (Web Framework)
Database
 - SQLAlchemy 2.0 (ORM)
 - MariaDB (Relational Database)
Security
 - JWT Authentication (flask-jwt-extended)
 - Ownership-based authorization
Engineering practices
 - OpenAPI 3.0 (Swagger UI)
 - Pytest (Automated Testing)
 - Docker & Docker Compose

## Architecture
The backend follows layer architecture

client
  |
routes layer
  |
service layer
  |
model layer
  |
database

This seperation improves maintainability, testibility and clarity of business logic.

## Feature
Core Features
 - Full CRUD operations for task management
 - OpenAPI 3.0 interactive API documenttaion (Swagger UI)
 - Automated coverage with pytest
 - Containerized deployment using Docker Compose
 - CI pipeline automated validation
Security
 - User authentication with JWT
 - Owership-Based authorization to protect user resources 
Engineering Pratices
 - OpenAPI 3.0 interactive API documentation (Swagger UI)
 - Automated coverage with pytest
 - Containerized deployment using Docker Compose
 - CI pipeline automated validation

## Testing
Automated testing is implemented with pytest.

The critical test flows include:

 - JWT Authentication.
 - Ownenship-based authorization.
 - Task CRUD operations.
 - API error handling.

tests can be executed with pytest.

## Documents
- [Test Plan](docs/test-plan-v1.md)
- [Test Cases](docs/test_cases.md)
- [Sample bug reports](docs/bug-report-samples.md)

## Test Coverage Categories

- **Authentication**: verifies that requests without a valid token are rejected.
- **Authorization**: verifies that users cannot access or modify resources they do not own.
- **Success Path**: verifies that valid requests succeed and return expected responses.
- **Validation / Business Rule**: verifies that invalid inputs, such as missing fields, invalid values, malformed JSON, or duplicate data, are rejected with proper error responses.
- **Error Handling**: verifies that not-found scenarios and error responses follow a consistent JSON structure with correct status codes and standardized fields such as `code`, `type`, and `message`.

## How to run
### Environment Variables
Copy `.env.example` to `.env`.

### Run with Docker
docker compose up -d
API documentation:
https://project-task-api-q2o5.onrender.com/docs

## Project Structure
app/
  routes/
  service/
  model/
tests/
docker-compose.yml
README.md
