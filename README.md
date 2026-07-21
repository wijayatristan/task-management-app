# Task Management App

A simple task management application built for a Front-End & Back-End Developer Internship technical assessment. Users can log in, view tasks on a Kanban board, create and edit tasks, change task status, and assign tasks to team members. It also includes an optional read-only AI assistant that can answer questions about the task data.

## Features

- JWT login with a seeded demo account (no registration)
- Kanban board with three columns: Todo, In Progress, Done
- Create, edit, and delete tasks
- Change task status from a dropdown
- Assign a task to a user, fetched from the backend
- Search tasks by title
- Filter tasks by status, assignee, and deadline
- "My Tasks" view showing only tasks assigned to the logged-in user
- Task detail drawer with full task information
- Optional AI Task Assistant that answers questions about task data (read-only)

## Tech Stack

**Frontend**
- Next.js (App Router)
- TypeScript
- Tailwind CSS
- lucide-react (icons)

**Backend**
- FastAPI
- SQLAlchemy
- Alembic (database migrations)
- Pydantic / pydantic-settings

**Database**
- PostgreSQL (via Docker Compose)

**Authentication**
- JWT (python-jose)
- Password hashing with passlib (bcrypt)

**AI**
- Google Gemini API, used only for classifying a question into a fixed set of intents. All actual data is still fetched by the backend through normal database queries. Optional and disabled by default.

## Project Structure

```
task-management-app/
├── backend/
│   ├── app/
│   │   ├── routers/        # auth, users, tasks, chat
│   │   ├── services/       # business logic per router
│   │   ├── models.py       # SQLAlchemy models (User, Task)
│   │   ├── schemas.py      # Pydantic request/response schemas
│   │   ├── security.py     # password hashing, JWT
│   │   ├── config.py       # environment-based settings
│   │   ├── database.py     # SQLAlchemy engine/session
│   │   ├── seed.py         # database seed script
│   │   └── main.py         # FastAPI app entrypoint
│   ├── alembic/             # database migrations
│   ├── docker-compose.yml   # PostgreSQL container
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── app/             # routes: /login, /tasks
│       ├── components/      # auth, tasks, chat, layout, ui
│       ├── lib/              # API client, auth helpers
│       └── types/
└── docs/
    ├── postman/              # Postman collection
    ├── erd/                  # ERD (DBML source + PNG export)
    └── planning/
```

## Prerequisites

- Git, to clone this repository
- PostgreSQL — either via Docker, or installed locally. Both are covered below, pick whichever you have available.
- Docker (optional — only needed if you want to run PostgreSQL in a container instead of installing it locally)
- Python 3.10 or later (backend)
- Node.js 20.9 or later (frontend, required by Next.js)
- npm

The backend and frontend themselves always run locally with Python/Node — they are not containerized either way, only the database setup differs.

## Getting Started From Scratch

This section is a single, straight-through walkthrough for someone who has never touched this project before, from cloning the repository to having it open and working in the browser. It assumes nothing is set up yet. You will need two terminal windows/tabs open at the same time: one for the backend, one for the frontend.

**1. Clone the repository**

```bash
git clone https://github.com/tristantowijaya/task-management-app.git
cd task-management-app
```

**2. Start PostgreSQL**

Choose one:

```bash
# Option A — with Docker
cd backend
docker compose up -d
cd ..
```

```bash
# Option B — without Docker (see "Installation" below for the full per-OS commands)
# install PostgreSQL, then create the taskapp role/database
```

**3. Set up and start the backend (first terminal)**

```bash
cd task-management-app/backend
cp .env.example .env

python3 -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate

pip install -r requirements.txt
alembic upgrade head
python -m app.seed

uvicorn app.main:app --reload
```

Leave this terminal running. The backend is now serving at `http://localhost:8000`.

**4. Set up and start the frontend (second terminal)**

```bash
cd task-management-app/frontend
cp .env.example .env.local

npm install
npm run dev
```

Leave this terminal running too. The frontend is now serving at `http://localhost:3000`.

**5. Open the app**

Go to `http://localhost:3000` in your browser and log in with:

```
Email:    demo@example.com
Password: password123
```

You should land on the tasks board with 6 seeded users available as assignees and no tasks yet. The rest of this README explains each of these steps in more detail, and what to do if something doesn't work.

## Installation

### 1. Database (PostgreSQL)

**Option A — with Docker**

```bash
cd backend
docker compose up -d
```

This starts a PostgreSQL container with a persistent volume, matching the credentials already set in `.env.example` (user `taskapp`, database `taskapp`, port `5432`).

**Option B — without Docker**

Install PostgreSQL locally and make sure it is running:

- macOS (Homebrew): `brew install postgresql@16 && brew services start postgresql@16`. If Homebrew itself isn't installed, either install it first from [brew.sh](https://brew.sh), or download [Postgres.app](https://postgresapp.com) instead — it's a regular macOS app, no package manager or terminal setup required.
- Linux (Debian/Ubuntu): `sudo apt install postgresql` (starts automatically as a service)
- Windows: install PostgreSQL from [postgresql.org](https://www.postgresql.org/download/windows/) (runs automatically as a service after install)

Then create a role and database matching `backend/.env.example` so the backend can connect without any further changes. The default superuser differs by platform, so use whichever applies:

```bash
# macOS (Homebrew) — the default superuser is your OS username, there is no "postgres" role
psql -d postgres -c "CREATE ROLE taskapp LOGIN PASSWORD 'taskapp';"
createdb -O taskapp taskapp

# Linux (apt) / Windows — default superuser is "postgres"
psql -U postgres -c "CREATE ROLE taskapp LOGIN PASSWORD 'taskapp';"
createdb -U postgres -O taskapp taskapp
```

If you already have PostgreSQL running with different credentials, that's fine too — just update `DATABASE_URL` in `backend/.env` (see below) to match your own user, password, and database name instead of creating a new role.

Both options end up with the same result: a PostgreSQL server reachable at the connection string in `DATABASE_URL`. Everything from this point on (migrations, seeding, running the backend) is identical either way.

### 2. Backend (FastAPI)

```bash
cd backend
cp .env.example .env

python3 -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Frontend (Next.js)

```bash
cd frontend
cp .env.example .env.local

npm install
```

## Environment Variables

### backend/.env.example

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string. Default matches the Docker Compose service. |
| `SECRET_KEY` | Secret used to sign JWTs. Change this to any random string. |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT expiry time in minutes. |
| `CORS_ORIGINS` | Allowed frontend origin(s) for CORS. |
| `ENABLE_AI_CHATBOT` | `true`/`false`. Turns the AI Task Assistant on or off. Defaults to `false`. |
| `GEMINI_API_KEY` | Google Gemini API key. Only required if `ENABLE_AI_CHATBOT=true`. Leave empty otherwise. |

### frontend/.env.example

| Variable | Description |
|---|---|
| `NEXT_PUBLIC_API_BASE_URL` | Base URL of the backend API, including the `/api/v1` prefix. |

No secrets are committed anywhere in this repository — `.env` files are git-ignored, only the `.env.example` templates are tracked.

## Database Setup

With the PostgreSQL container running and the backend virtual environment active:

```bash
cd backend
source .venv/bin/activate

alembic upgrade head
python -m app.seed
```

- `alembic upgrade head` creates the `users` and `tasks` tables.
- `python -m app.seed` clears the database and inserts the seed users listed below. It resets the ID sequences too, so on a fresh database the first user gets ID 1 and the first task created afterward gets ID 1. It is safe to run more than once — it always produces the same clean result, and the `tasks` table is always empty right after seeding.

## Running the Application

**Backend**

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload
```

Runs at `http://localhost:8000`. Interactive API docs are available at `http://localhost:8000/docs`.

**Frontend**

```bash
cd frontend
npm run dev
```

Runs at `http://localhost:3000`.

## Demo Credentials

```
Email:    demo@example.com
Password: password123
```

This account is created by the seed script along with five other users (Tristanto Wijaya, Calvin Setiawan, Wellson Charlest, Chelsea Willis, Olivia Joanna) who are available in the assignee dropdown. Only the demo account is needed to log in — there is no registration flow.

## API Documentation

The complete API documentation, including example requests and responses for every endpoint, is available as a Postman collection:

```
docs/postman/task-management.postman_collection.json
```

Recommended order to try it:

1. Import the collection into Postman.
2. Run **Login**.
3. The JWT is stored automatically in a collection variable and reused by the following requests.
4. Run **Get Users**.
5. Run **Create Task**.
6. Run **Get Task by ID**.
7. Run **Update Task**.
8. Run **Update Task Status**.
9. Run **Delete Task**.
10. Try **Ask Task Assistant** (returns a normal answer if the AI assistant is enabled, or a clear "disabled" message if it is not).

The collection already includes example success and error responses for each request, so it can be reviewed without running the server.

## Database Design

The ERD is available under `docs/erd/` as a DBML source file (`schema.dbml`) and a rendered image (`task-management-app-erd.png`).

The schema has two tables: `users` and `tasks`. Each task optionally belongs to one user through `tasks.assignee_id`, and a user can be the assignee of many tasks.

## AI Task Assistant

The AI Task Assistant is an optional, read-only feature. It answers a fixed set of questions about the current task data:

- List incomplete tasks
- Count completed tasks
- List tasks due today
- Get the assignee of a specific task

Gemini is only used to classify the question into one of these categories (or "unsupported" if it doesn't match). It never queries the database and never generates SQL — the backend runs a normal, predefined database query for whichever category was matched, and returns the answer.

To enable it, set in `backend/.env`:

```
ENABLE_AI_CHATBOT=true
GEMINI_API_KEY=your-key-here
```

If `ENABLE_AI_CHATBOT` is `false` or no API key is set, the rest of the application works normally — the assistant endpoint just responds with a message saying it is disabled.

## Notes

- The seed script always resets the database to the same state: 6 users, 0 tasks. Re-running it does not create duplicates.
- The AI Task Assistant is fully optional. The core application (auth, tasks, users) does not depend on it in any way.
- There is no user registration — only the seeded demo account and the other seeded users exist.

## License

This repository was built for a technical assessment and is not intended for production use.
