## Overview

SweatMates is a workout tracking application that allows users to:

- **Create an account**
- **Log in** and receive an authorized JWT token
- **Add workouts** with details such as body group focus, notes, and associated exercises
- **Manage exercises** within workouts, tracking sets, reps, weights, and goals

## Architecture

The backend is built using:

- **Flask** (Python web framework)
- **PostgreSQL** (Relational database)
- **SQLAlchemy** (ORM for database interactions)
- **Flask-Migrate** (Handles database migrations)
- **JWT Authentication** (Secure user authentication using JSON Web Tokens)
- **Docker & Docker Compose** (Containerized environment for easy deployment)

## Setup Instructions

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/SweatMates.git
cd SweatMates/backend
```

### 2. Set Up Environment Variables

Create a `.env` file inside `backend/` following the structure of `.env.example`:

```sh
HOSTNAME=localhost
DATABASE=sweatmates
DB_USERNAME=postgres
DB_PASSWORD=yourpassword
PORT_ID=5432
JWT_SECRET=your_super_secret_key
JWT_EXPIRATION_SECONDS=3600
```

### 3. Build and Run with Docker

```sh
docker-compose up --build -d
```

This starts both the backend and database containers.

### 4. Run Database Migrations

```sh
docker-compose exec backend flask db upgrade
```

Your backend should now be running at `http://localhost:5000`.

Test endpoints using Postman, Insomnia, etc.

## Updating the Application

Whenever changes are made, follow these steps:

| Change Type                    | Command to Run                                                                                              |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| Only `docker-compose.yml`      | `docker-compose up -d`                                                                                      |
| `Dockerfile` or dependencies   | `docker-compose up --build -d`                                                                              |
| `requirements.txt` updated     | `docker-compose build backend && docker-compose up -d`                                                      |
| Database models (`models.py`)  | `docker-compose exec backend flask db migrate -m "message"`  `docker-compose exec backend flask db upgrade` |
| Full reset (remove everything) | `docker-compose down --volumes --rmi all`  `docker-compose up --build -d`                                   |

## API Endpoints

### 1. Authentication

- **POST /signup** - Create a new user
- **POST /login** - Authenticate and receive a JWT token

### 2. Workouts

- **POST /addworkout** (Requires JWT) - Add a new workout with details

**NOTE:** UI (ReactJS) is still in development and will come in future iterations.