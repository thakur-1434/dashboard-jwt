
# `Dashboard`

This Django project implements a user dashboard with JWT-based authentication using Django REST Framework and djangorestframework-simplejwt. It supports user registration, login, and secure access to user details through APIs. The project uses SQLite with environment variable configuration for database credentials and features a simple, styled dashboard UI where logged-in users can view their details and log out.
# 🧩 Django Dashboard Project with JWT Authentication

This project is a Django-based web application that implements user authentication using JWT, a dashboard UI, and basic user management APIs using Django REST Framework.

---

## 🔧 Features

-  User Registration API    ✅ 
-  User Login API (JWT Authentication) ✅ 
-  Get Authenticated User Details  ✅ 
-  Dashboard Page with User Info      ✅ 
-  Logout Functionality      ✅ 
-  Basic CSS Styling for Dashboard UI   ✅ 
-  SQLite with `.env` environment variable support   ✅ 


# Project Setup and Installation


Step 1: Create & activate a virtual environment

- python -m venv env
- source env/bin/activate

Step 2: Install dependencies

- pip install django djangorestframework psycopg2-binary python-dotenv djangorestframework-simplejwt

Step 3: Create Django project and app

- django-admin startproject dashboard_project
- cd dashboard_project
- python manage.py startapp dashboard

Step 4. Run migrations:

- python manage.py migrate

Step 5. Create a superuser (optional):

-  python manage.py createsuperuser

Step 6. Run the development server:

-  python manage.py runserver
# Usage instructions.

🔑 API Usage

📌 Register
- POST /api/register/

📌 Login

- POST /api/login/

📌 Get User Info

- GET /api/user/
Headers: Authorization: Bearer <access_token>

# 💻 Dashboard UI

Accessible at: http://localhost:8000/api/dashboard/

Requires login (via Django session)

Displays username, email, and logout button

🔓 Logout

- POST /logout/
## 🙌 Acknowledgements

- Django

- Django REST Framework

- SimpleJWT
