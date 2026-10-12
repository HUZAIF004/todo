# 📝 FastAPI Todo Application

A modern, production-ready Fullstack & RESTful Todo Application built with **FastAPI**, **SQLAlchemy**, **PostgreSQL**, **Alembic**, and **Jinja2 Templates**. Features secure JWT authentication, role-based access control (RBAC), database migrations, and a comprehensive automated test suite.

---

## 🚀 Features

- **Robust REST API & Fullstack Web UI**: Fully functional REST endpoints alongside interactive web pages rendered via Jinja2 templates.
- **Secure Authentication & Authorization**:
  - JWT (JSON Web Tokens) with HS256 encryption.
  - Password hashing using `passlib` & `bcrypt`.
  - OAuth2 Password Bearer flow for API clients and cookie-based sessions for browser UI.
- **Role-Based Access Control (RBAC)**:
  - Separate permissions for standard `user` and `admin` roles.
  - Admin endpoints to view and manage all system todos.
- **Todo Management (CRUD)**:
  - Create, read, update, and delete personal todo items.
  - Priority levels (1–5) and completion tracking.
- **User Profile Management**:
  - Update passwords and contact phone numbers.
- **Database Support & Migrations**:
  - SQLAlchemy ORM supporting PostgreSQL (production) and SQLite (testing/CI).
  - Schema versioning and migration management with Alembic.
- **Testing & Quality Assurance**:
  - Automated test suite using `pytest` and `httpx`.

---

## 🛠️ Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.13+)
- **Server**: [Uvicorn](https://www.uvicorn.org/)
- **Database & ORM**: [SQLAlchemy](https://www.sqlalchemy.org/), [PostgreSQL](https://www.postgresql.org/) (`psycopg2-binary`), [SQLite](https://www.sqlite.org/)
- **Database Migrations**: [Alembic](https://alembic.sqlalchemy.org/)
- **Security**: [python-jose](https://github.com/mpdavis/python-jose), [passlib](https://passlib.readthedocs.io/), [bcrypt](https://github.com/pyca/bcrypt)
- **Templating**: [Jinja2](https://palletsprojects.com/p/jinja/)
- **Testing**: [pytest](https://pytest.org/), [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio), [httpx](https://www.python-httpx.org/)
- **Package Manager**: [uv](https://docs.astral.sh/uv/)

---

## 📂 Project Structure

```text
Todo/
├── alembic/                    # Alembic migration scripts and environment
├── alembic.ini                 # Alembic configuration
├── database.py                 # SQLAlchemy engine and session configuration
├── main.py                     # Application entry point and router mounting
├── models.py                   # SQLAlchemy data models (Users, Todos)
├── pyproject.toml              # Project dependencies and metadata
├── routers/
│   ├── admin.py                # Admin endpoints (moderation and system oversight)
│   ├── auth.py                 # Authentication, registration, and token generation
│   ├── todos.py                # Todo CRUD endpoints & template views
│   └── users.py                # User profile endpoints (password change, phone update)
├── static/                     # CSS, JavaScript, and static assets
├── templates/                  # Jinja2 HTML templates (auth, todo views)
├── test/                       # Automated test suite
│   ├── test_admin.py
│   ├── test_auth.py
│   ├── test_example.py
│   ├── test_main.py
│   ├── test_todos.py
│   ├── test_users.py
│   └── utils.py                # Test fixtures and test database setup
└── uv.lock                     # Locked dependency graph
```

---

## ⚙️ Getting Started

### Prerequisites

- **Python 3.13+**
- **uv** (recommended) or standard **pip**
- **PostgreSQL** (optional for local development; can use SQLite)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/fastapi-todo.git
cd fastapi-todo/Todo
```

### 2. Environment Variables

Create an `.env` file or export the `DATABASE_URL` environment variable:

```bash
# PostgreSQL (Default)
DATABASE_URL="postgresql+psycopg2://postgres:yourpassword@localhost:5432/TodoApplicationDatabase"

# Alternatively, SQLite for local lightweight testing:
DATABASE_URL="sqlite:///./todosapp.db"
```

### 3. Install Dependencies

#### Using `uv` (Recommended)
```bash
uv sync
```

#### Using standard `pip` & virtual environment
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

pip install -r <(uv pip compile pyproject.toml)
# or install directly from pyproject.toml:
pip install .
```

---

## 🗄️ Database Migrations

Run database migrations using Alembic:

```bash
# Apply migrations to the latest revision
alembic upgrade head

# Generate a new migration revision after model changes
alembic revision --autogenerate -m "describe changes"
```

---

## 🏃 Running the Application

Start the development server with Uvicorn:

```bash
# From inside the Todo directory:
uv run uvicorn main:app --reload

# Or if the virtual environment is already activated:
uvicorn main:app --reload
```

The application will be accessible at:
- **Web UI**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Interactive Swagger Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Alternative ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📖 API & Web Routes Overview

### 🌐 Web Pages (Jinja2 Templates)
| Method | Route | Description |
|---|---|---|
| `GET` | `/` | Redirects to `/todo/todo-page` |
| `GET` | `/auth/login-page` | Login page |
| `GET` | `/auth/register-page` | User registration page |
| `GET` | `/todo/todo-page` | User todo list dashboard |
| `GET` | `/todo/add-todo-page` | Create new todo form |
| `GET` | `/todo/edit-todo-page/{id}` | Edit existing todo form |

### 🔐 Authentication (`/auth`)
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/auth/` | Register a new user |
| `POST` | `/auth/token` | OAuth2 access token login (returns JWT) |

### ✅ Todo Items (`/todo`)
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/todo/` | List all todos for current user |
| `GET` | `/todo/{todo_id}` | Retrieve specific todo by ID |
| `POST` | `/todo/` | Create a new todo |
| `PUT` | `/todo/{todo_id}` | Update an existing todo |
| `DELETE` | `/todo/{todo_id}` | Delete a todo |

### 👤 User Management (`/users`)
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/users/` | Get current user profile details |
| `PUT` | `/users/change_password` | Change user password |
| `PUT` | `/users/update_phone_number/{phone}` | Update phone number |

### 🛡️ Admin (`/admin`)
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/admin/` | View all todos across all users |
| `DELETE` | `/admin/todo/delete_todo/{id}` | Delete any todo by ID |

### 🩺 System (`/`)
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/healthy` | Health check endpoint (`{"status": "healthy"}`) |

---

## 🧪 Running Tests

The test suite runs against an isolated SQLite test database with pre-configured fixtures:

```bash
# Run all tests using uv
uv run pytest test/

# Run with verbose output
uv run pytest -v test/
```

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
