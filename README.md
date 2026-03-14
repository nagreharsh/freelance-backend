### Architecture Highlights

- 🧩 **Modular Django Apps:** Each core feature (projects, proposals, contracts, etc.) is implemented as a separate Django app for scalability.
- 🔐 **JWT Authentication:** Secure token-based authentication using SimpleJWT.
- 👥 **Role-Based Access Control:** Clients, freelancers, and admins have different permissions.
- ⚙️ **Service Layer Logic:** Dashboard services aggregate platform data efficiently.
- 🛡 **Secure APIs:** Input sanitization, throttling, and permission checks ensure security.

--------------------------------------------------
🔄 Platform Workflow
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
⭐ Key Features
--------------------------------------------------

• 🔐 Role based authentication (Client / Freelancer / Admin)

• 📂 Project management for clients

• 📨 Proposal submission for freelancers

• 📜 Contract lifecycle management

• 💬 Messaging system within contracts

• 🔔 Notification system

• ⭐ Review and rating system

• 🛠 Admin monitoring APIs

• 🚦 Rate limiting for public endpoints

• 🧼 Input sanitization to prevent XSS attacks

• 📜 Logging for important system actions


--------------------------------------------------
🔐 Authentication
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
📂 Projects
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
📨 Proposals
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
📜 Contracts
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
💬 Messaging
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
🔔 Notifications
--------------------------------------------------

Notifications are generated for important actions

• 💬 new message
• 🔄 contract status change
• ⭐ review submitted

Endpoints

GET   /api/notifications/
PATCH /api/notifications/{id}/read/


--------------------------------------------------
⭐ Reviews
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
🛠 Admin APIs
--------------------------------------------------

Admin endpoints provide system monitoring.

GET /api/admin/contracts/
GET /api/admin/reviews/


--------------------------------------------------
🧪 Testing
--------------------------------------------------

The project includes automated tests covering models,
permissions, validation, and workflow.

Test Coverage

9 automated tests including

• 🧪 Unit tests for models
• 🔗 Integration workflow tests
• 🔐 Permission validation
• ✔ API validation tests

Run tests

python manage.py test tests


Integration flow tested

Auth → Project → Proposal → Contract → Review


--------------------------------------------------
📊 Demo Data
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
📁 Project Structure
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
⚡ Quick Start
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
🎓 Learning Outcomes
--------------------------------------------------

Through this project the following concepts were explored:

• 🌐 REST API development with Django REST Framework  
• 🔐 JWT based authentication  
• 👥 Role based access control  
• 🗄 Database modeling and relationships  
• 📜 Contract lifecycle management  
• ✔ API validation and error handling  
• 🧪 Automated testing using Django tests  
• 🚦 Rate limiting and security practices  
• 📜 Logging important backend actions  


--------------------------------------------------
📖 Project Context
--------------------------------------------------

This project was developed as part of the **Infosys Springboard Internship Program**
under the mentorship of **Sridhar T**.

The focus of the internship project was to design and implement a
production-style backend system demonstrating REST API design,
authentication, validation, testing, and secure backend practices.


--------------------------------------------------
👨‍💻 Author
--------------------------------------------------

Harsh Kumar Nagre  
Infosys Springboard Intern
