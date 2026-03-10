# Freelancing Platform Backend

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Django](https://img.shields.io/badge/Django-REST%20Framework-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Project-Completed-brightgreen)
![Maintained](https://img.shields.io/badge/Maintained-Yes-success)

Backend implementation of a freelancing marketplace built using Django and Django REST Framework.

This project was developed as part of the **Infosys Springboard Internship Program**
under the guidance of **Mentor: Sridhar T**.

The system provides APIs for managing users, projects, proposals, contracts, messaging,
notifications, and reviews between clients and freelancers.


## Table of Contents

- [API Documentation](#api-documentation)
- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [System Architecture](#system-architecture)
- [Platform Workflow](#platform-workflow)
- [Key Features](#key-features)
- [Authentication](#authentication)
- [Projects](#projects)
- [Proposals](#proposals)
- [Contracts](#contracts)
- [Messaging](#messaging)
- [Notifications](#notifications)
- [Reviews](#reviews)
- [Admin APIs](#admin-apis)
- [Testing](#testing)
- [Demo Data](#demo-data)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Learning Outcomes](#learning-outcomes)
- [Future Improvements](#future-improvements)
- [Project Context](#project-context)
- [Author](#author)


--------------------------------------------------
API Documentation
--------------------------------------------------

The backend provides interactive API documentation using Swagger (OpenAPI).

You can explore and test all API endpoints directly in the browser.

Swagger UI

http://127.0.0.1:8000/api/docs/

OpenAPI Schema

http://127.0.0.1:8000/api/schema/

Redoc Documentation

http://127.0.0.1:8000/api/redoc/


The documentation allows developers to:

• View all available endpoints  
• Inspect request and response schemas  
• Test endpoints directly from the browser  
• Understand authentication requirements  


Authentication Example

To use protected endpoints:

1. Call the login API

POST /api/login/

Example request

{
  "username": "client_user",
  "password": "password123"
}

2. Copy the access token from the response

3. Click **Authorize** in Swagger UI

4. Enter

Bearer <access_token>


The API documentation automatically reflects all backend endpoints including:

Users  
Projects  
Proposals  
Contracts  
Messaging  
Notifications  
Reviews  
Dashboard APIs


--------------------------------------------------
Project Overview
--------------------------------------------------

The platform simulates a freelancing marketplace where:

Clients can post projects.
Freelancers can submit proposals.
Accepted proposals become contracts.
Users communicate through messages within contracts.
After completion both parties can leave reviews.

Platform workflow:

User Authentication
      ↓
Project Creation
      ↓
Proposal Submission
      ↓
Contract Creation
      ↓
Messaging
      ↓
Contract Completion
      ↓
Review System


--------------------------------------------------
Tech Stack
--------------------------------------------------

Python
Django
Django REST Framework
JWT Authentication (SimpleJWT)
SQLite (development)

Additional Libraries

django-filter
django-cors-headers
bleach (input sanitization)


--------------------------------------------------
System Architecture
--------------------------------------------------
```
                                             +----------------------+
                                             |      Frontend        |
                                             |  (React / Web App)   |
                                             +----------+-----------+
                                                        |
                                                        | HTTP Requests (JWT Auth)
                                                        v
                                             +----------------------+
                                             |    Django Backend    |
                                             |   Django REST API    |
                                             +----------+-----------+
                                                        |
        -------------------------------------------------------------------------------------------
        |           |           |           |           |          |              |               |
        v           v           v           v           v          v              v               v

   +---------+ +---------+ +---------+ +---------+ +---------+ +---------+ +---------------+ +-----------+
   |  Users  | |Projects | |Proposals| |Contracts| |Messaging| | Reviews | | Notifications | | Dashboard |
   |   App   | |   App   | |   App   | |   App   | |   App   | |   App   | |               | |           |
   +---------+ +---------+ +---------+ +---------+ +---------+ +---------+ +---------------+ +-----------+

                                                       |
                                                       v

                                           +----------------------+
                                           |       Database       |
                                           |       SQLite         |
                                           +----------------------+

```
### Architecture Highlights

- **Modular Django Apps:** Each core feature (projects, proposals, contracts, etc.) is implemented as a separate Django app for scalability.
- **JWT Authentication:** Secure token-based authentication using SimpleJWT.
- **Role-Based Access Control:** Clients, freelancers, and admins have different permissions.
- **Service Layer Logic:** Dashboard services aggregate platform data efficiently.
- **Secure APIs:** Input sanitization, throttling, and permission checks ensure security.

--------------------------------------------------
Platform Workflow
--------------------------------------------------

Client registers/login
        |
        v
Client posts project
        |
        v
Freelancer submits proposal
        |
        v
Client accepts proposal
        |
        v
Contract created
        |
        v
Client & Freelancer exchange messages
        |
        v
Work completed
        |
        v
Both users submit reviews


--------------------------------------------------
Key Features
--------------------------------------------------

• Role based authentication (Client / Freelancer / Admin)

• Project management for clients

• Proposal submission for freelancers

• Contract lifecycle management

• Messaging system within contracts

• Notification system

• Review and rating system

• Admin monitoring APIs

• Rate limiting for public endpoints

• Input sanitization to prevent XSS attacks

• Logging for important system actions


--------------------------------------------------
Authentication
--------------------------------------------------

Authentication uses JWT tokens.

Typical flow:

Register → Login → Receive access token → Use token in requests


Authentication APIs

POST /api/register/
POST /api/login/
POST /api/refresh/

GET  /api/profile/
GET  /api/users/


--------------------------------------------------
Projects
--------------------------------------------------

Clients can create and manage projects.

Project fields include:

title
description
budget
duration
skills_required
status

Status values:

open
in_progress
completed

Endpoints

GET    /api/projects/
POST   /api/projects/
GET    /api/projects/{id}/
PATCH  /api/projects/{id}/
DELETE /api/projects/{id}/


--------------------------------------------------
Proposals
--------------------------------------------------

Freelancers submit proposals to projects.

Proposal includes:

project
freelancer
bid_amount
cover_letter

Duplicate proposals from the same freelancer to the same project are prevented.

Endpoints

GET    /api/proposals/
POST   /api/proposals/
GET    /api/proposals/{id}/
PATCH  /api/proposals/{id}/
DELETE /api/proposals/{id}/


--------------------------------------------------
Contracts
--------------------------------------------------

A contract is created when a proposal is accepted.

Contract statuses

draft
active
completed

Lifecycle

Proposal → Contract → Active Work → Completed

Endpoints

GET    /api/contracts/
POST   /api/contracts/
GET    /api/contracts/{id}/
PATCH  /api/contracts/{id}/status/


--------------------------------------------------
Messaging
--------------------------------------------------

Users communicate inside contracts.

Each message contains

contract
sender
receiver
content
is_read
timestamp

Endpoints

POST   /api/messages/
GET    /api/messages/?contract={contract_id}
PATCH  /api/messages/{id}/read/


--------------------------------------------------
Notifications
--------------------------------------------------

Notifications are generated for important actions

• new message
• contract status change
• review submitted

Endpoints

GET   /api/notifications/
PATCH /api/notifications/{id}/read/


--------------------------------------------------
Reviews
--------------------------------------------------

After a contract is completed users can review each other.

Review contains

rating (1-5)
comment
reviewer
reviewee

Duplicate reviews are prevented.

Endpoints

POST  /api/reviews/
GET   /api/reviews/?contract={contract_id}


--------------------------------------------------
Admin APIs
--------------------------------------------------

Admin endpoints provide system monitoring.

GET /api/admin/contracts/
GET /api/admin/reviews/


--------------------------------------------------
Testing
--------------------------------------------------

The project includes automated tests covering models,
permissions, validation, and workflow.

Test Coverage

9 automated tests including

• Unit tests for models
• Integration workflow tests
• Permission validation
• API validation tests

Run tests

python manage.py test tests


Integration flow tested

Auth → Project → Proposal → Contract → Review


--------------------------------------------------
Demo Data
--------------------------------------------------

The project includes a demo data seeder.

Run

python manage.py seed_demo_data --reset

This generates

10 clients
10 freelancers
15 projects
multiple proposals
active contracts
completed contracts
messages
reviews


--------------------------------------------------
Project Structure
--------------------------------------------------

freelance-backend/

users/
projects/
proposals/
contracts/
messaging/
notifications/
reviews/
dashboard/

tests/
test_models.py
test_flow.py
test_api_validation.py

manage.py
requirements.txt
README.md
API_DOCUMENTATION.md


--------------------------------------------------
Quick Start
--------------------------------------------------

Clone repository

git clone <repository_url>

cd freelance-backend


Create virtual environment

python -m venv venv


Activate environment

venv\Scripts\activate


Install dependencies

pip install -r requirements.txt


Run migrations

python manage.py migrate


Start development server

python manage.py runserver


--------------------------------------------------
Learning Outcomes
--------------------------------------------------

Through this project the following concepts were explored:

• REST API development with Django REST Framework
• JWT based authentication
• Role based access control
• Database modeling and relationships
• Contract lifecycle management
• API validation and error handling
• Automated testing using Django tests
• Rate limiting and security practices
• Logging important backend actions


--------------------------------------------------
Project Context
--------------------------------------------------

This project was developed as part of the **Infosys Springboard Internship Program**
under the mentorship of **Sridhar T**.

The focus of the internship project was to design and implement a
production-style backend system demonstrating REST API design,
authentication, validation, testing, and secure backend practices.


--------------------------------------------------
Author
--------------------------------------------------

Harsh Kumar Nagre  
Infosys Springboard Intern
