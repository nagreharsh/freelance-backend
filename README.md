# Freelance Platform Backend (Django + DRF)

This is the backend API for a Freelancing Platform built using Django and Django REST Framework.

## 🚀 Features

### 🔐 Authentication
- JWT Authentication (Access + Refresh Tokens)
- Custom User Model (Client / Freelancer / Admin)
- Role-based access control

### 📁 Projects
- Clients can create and manage projects
- Filtering, search, ordering supported

### 📄 Proposals
- Freelancers submit proposals to open projects
- Clients can accept or reject proposals
- One accepted proposal creates one contract

### 📑 Contracts
- Strict lifecycle:
  - draft → active → completed / disputed
- Controlled status transitions
- Automatic timestamp handling
- One-to-one Proposal ↔ Contract enforcement

### 💬 Messaging
- Contract-based messaging
- Read status tracking

### 🔔 Notifications
- Triggered on:
  - New messages
  - Reviews
- Unread count support

### ⭐ Reviews
- Bidirectional (Client ↔ Freelancer)
- Allowed only after contract completion
- Duplicate review prevention
- Proper validation (no 500 errors)

---

## 🛠 Tech Stack
- Python
- Django
- Django REST Framework
- SQLite (Development)
- JWT Authentication

---

## 📬 API Testing
All endpoints tested using Postman.

---

## 👨‍💻 Author
Harsh Nagre
