Flask Notes App with User CRUD API + React Frontend
A full-stack Notes application with Flask backend, MongoDB database, and React frontend, featuring user authentication, CRUD operations, and modern containerized deployment.

Features
Complete User Management: Create, read, update, delete users with authentication

Notes System: Full CRUD operations for user notes

Session-based Authentication: Secure login/logout functionality

Password Security: Bcrypt hashing for secure password storage

Input Validation: Server-side validation with proper error handling

Responsive Design: Modern monochrome UI that works on all devices

RESTful API: Clean REST endpoints for all operations

Docker Support: Fully containerized application with hot reload

MongoDB Integration: NoSQL database with proper connection handling

Tech Stack
Backend: Flask (Python), PyMongo, Bcrypt
Database: MongoDB
Frontend: React (Vite), Axios
Authentication: Flask Sessions
Containerization: Docker + Docker Compose
API Format: REST

Prerequisites
Before you begin, ensure you have the following installed:

Docker Desktop (latest version)

Docker Compose (usually included with Docker Desktop)

Git (for cloning the repository)

Web Browser (Chrome, Firefox, Safari, Edge)

System Requirements:

RAM: Minimum 4GB (8GB recommended)

Storage: At least 2GB free space

OS: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)

Quick Start
1. Clone the Repository

text
git clone <your-repository-url>
cd flask-notes-app
2. Environment Setup

Create backend/.env:

text
MONGODB_URI=mongodb://mongodb:27017/notes_app
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-change-this-in-production
PORT=5000
LOG_LEVEL=INFO
HIDE_AUTH_401=True
Create frontend/.env:

text
VITE_API_URL=http://localhost:5000
3. Start the Application

text
docker-compose up --build
4. Access the Application

Frontend (React App): http://localhost:3000

Backend API: http://localhost:5000

MongoDB: localhost:27017

Project Structure
text
flask-notes-app/
├── backend/                    # Flask API server
│   ├── app/
│   │   ├── __init__.py        # Flask app factory
│   │   ├── config.py          # Configuration settings
│   │   ├── models/            # Data models
│   │   │   ├── __init__.py
│   │   │   ├── user.py        # User model with authentication
│   │   │   └── note.py        # Note model
│   │   ├── routes/            # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── users.py       # User CRUD endpoints
│   │   │   ├── notes.py       # Notes CRUD endpoints
│   │   │   └── auth.py        # Authentication endpoints
│   │   └── utils/             # Utility functions
│   │       ├── __init__.py
│   │       └── database.py    # MongoDB connection
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile            # Backend container config
│   ├── .env                  # Backend environment variables
│   └── run.py                # Application entry point
├── frontend/                  # React application
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── UserForm.jsx
│   │   │   ├── UsersList.jsx
│   │   │   ├── NotesList.jsx
│   │   │   ├── AddNoteForm.jsx
│   │   │   ├── LoginModal.jsx
│   │   │   ├── PasswordModal.jsx
│   │   │   └── EditProfileModal.jsx
│   │   ├── api/              # API integration
│   │   │   └── api.js
│   │   ├── App.jsx           # Main application component
│   │   ├── App.css           # Application styles
│   │   └── main.jsx          # React entry point
│   ├── public/
│   │   └── index.html
│   ├── package.json          # Node.js dependencies
│   ├── vite.config.js        # Vite configuration
│   ├── Dockerfile           # Frontend container config
│   └── .env                 # Frontend environment variables
├── docker-compose.yml        # Multi-container orchestration
├── .gitignore               # Git ignore rules
└── README.md                # This file
API Endpoints
User Management

GET /users - Get all users

GET /users/<id> - Get user by ID

POST /users - Create new user (requires: name, email, password)

PUT /users/<id> - Update user (accepts: name, email)

DELETE /users/<id> - Delete user

Notes Management

GET /users/<id>/notes - Get all notes for user

POST /users/<id>/notes - Create note for user (requires: title, content)

PUT /users/<id>/notes/<note_id> - Update note (accepts: title, content)

DELETE /users/<id>/notes/<note_id> - Delete note

Authentication

POST /login - Login with email/password

POST /login-with-password - Login with user ID/password

POST /logout - Logout current user

GET /current-user - Get current logged-in user

POST /verify-password - Verify user password

Health Check

GET /health - API health status