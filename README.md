
📝 Flask Notes App (Full Stack)
A full-stack Notes application with Flask backend, MongoDB database, and React frontend. It features secure user authentication, full CRUD operations for notes, and a modern containerized setup using Docker.

🚀 Features:

✅ User Management: Create, read, update, delete users

🔐 Authentication: Secure session-based login/logout

📝 Notes System: CRUD operations for user-specific notes

🔒 Password Security: Bcrypt hashing

🛡️ Input Validation: Proper server-side validation and error handling

💻 Responsive UI: Monochrome theme, mobile-first design

🧪 REST API: Clean RESTful endpoints

🐳 Dockerized: Hot reload support with Docker & Docker Compose

🗃️ MongoDB Integration: NoSQL backend with proper connection handling

🛠 Tech Stack

Layer	        Technology
Frontend	    React (Vite), Axios
Backend	        Flask, Flask-Sessions, PyMongo, Bcrypt
Database	    MongoDB
Auth	        Session-based authentication
DevOps	        Docker, Docker Compose
API	            REST

⚙️ Prerequisites

Docker Desktop (latest)
Git
Web Browser (Chrome, Firefox, etc.)
Recommended: 8GB RAM, 2GB free space, Windows 10+/macOS 10.14+/Ubuntu 18.04+

🧑‍💻 Quick Start

1. Clone the Repository

git clone <your-repository-url>
cd flask-notes-app

2. Setup Environment Variables

backend/.env

MONGODB_URI=mongodb://mongodb:27017/notes_app
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-change-this-in-production
PORT=5000
LOG_LEVEL=INFO
HIDE_AUTH_401=True
frontend/.env

VITE_API_URL=http://localhost:5000

3. Start the App

docker-compose up --build

🌐 Access URLs

Service	            URL
Frontend (React)	http://localhost:3000
Backend (Flask)	    http://localhost:5000
MongoDB	            localhost:27017

🗂 Project Structure

![alt text](<Screenshot 2025-06-18 203017.png>)
![alt text](<Screenshot 2025-06-18 203042.png>)


📡 API Endpoints

👤 User Management
Method	    Endpoint	    Description
GET	        /users	        Get all users
GET	        /users/<id>	    Get user by ID
POST	    /users	        Create user
PUT	        /users/<id>	    Update user
DELETE	    /users/<id>	    Delete user

🗒 Notes Management
Method	    Endpoint	                        Description
GET	        /users/<id>/notes	                Get notes of a user
POST	    /users/<id>/notes	                Create a new note
PUT	        /users/<id>/notes/<note_id>	        Update note
DELETE	    /users/<id>/notes/<note_id>	        Delete note

🔐 Authentication
Method	    Endpoint	                Description
POST	    /login	                    Login with email/password
POST	    /login-with-password	    Login with ID/password
POST	    /logout	                    Logout current user
GET	        /current-user	            Get logged-in user details
POST	    /verify-password	        Verify user password

🩺 Health Check
Method	Endpoint	Description
GET	    /health	    Check API health

📦 Docker Commands
Build and Run (with hot reload) -
    docker-compose up --build
Stop -
    docker-compose down