##Overview
This project is a maintainable and secure RESTful Task Management API that demonstrates layered architecture design and ownership-based authorization.
It prevents unauthorized access to user-owned resources by enforcing JWT authentication and strict resource ownership validation.
This project also emphasis automatic testing,API documentation, containarized deployment.

##Highlight
JWT authentication
Ownership-based authorization
Automatic testing with pytest
OpenAPI3.0 ducumentation with Swagger UI
Dockerize deployment

##Tech stack
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

##Architecture
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

##Feature
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

##testing
Automated testing is implemented with pytest.
The test critical flow included:
JWT Authentication.
Ownenship-based Authorization.
Run test with pytest

##how to run
Run with Docker
docker compose up -d
API documentation:
https://project-task-api-q2o5.onrender.com/docs
