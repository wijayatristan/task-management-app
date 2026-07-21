# Task Management App

A full-stack task management application developed for a Front-End and Back-End Developer Internship technical assessment.

The application allows users to authenticate, manage tasks through a Kanban board, assign tasks to team members, and search or filter task data.

## Screenshots

**Kanban Board**

![Kanban Board](docs/screenshots/kanban-board.png)

**Login**

![Login](docs/screenshots/login.png)

**Task Detail Drawer**

![Task Detail Drawer](docs/screenshots/task-detail.png)

**AI Task Assistant**

![AI Task Assistant](docs/screenshots/ai-assistant.png)

## Features

- JWT authentication with a seeded demo account
- Kanban board with Todo, In Progress, and Done columns
- Create, view, update, and delete tasks
- Change task status and assignee
- Search tasks by title
- Filter tasks by status, assignee, and deadline
- My Tasks view for the authenticated user
- Task detail drawer
- Interactive FastAPI documentation
- PostgreSQL migrations using Alembic
- Reproducible database seed script
- Optional read-only AI task assistant

## Tech Stack

**Frontend**

- Next.js
- React
- TypeScript
- Tailwind CSS

**Backend**

- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- JWT authentication

**Database**

- PostgreSQL
- Docker Compose

## Project Structure

```text
task-management-app/
├── backend/
├── frontend/
└── docs/
```

## Prerequisites

Make sure the following software is installed:

- Git
- Python 3.12
- Node.js 20.9 or later
- Docker Desktop

PostgreSQL does not need to be installed separately because it runs through Docker Compose.

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/wijayatristan/task-management-app.git
cd task-management-app
```

### 2. Start PostgreSQL

Enter the backend directory, create the backend environment file, and start PostgreSQL.

**macOS**

```bash
cd backend
cp .env.example .env
docker compose up -d
```

**Windows PowerShell**

```powershell
Set-Location backend
Copy-Item .env.example .env
docker compose up -d
```

You can verify that the PostgreSQL container is running with:

```bash
docker compose ps
```

### Using an Existing PostgreSQL Installation

Docker is not required when PostgreSQL is already installed locally.

1. Create a PostgreSQL database.
2. Update `DATABASE_URL` in `backend/.env`.

Example:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/task_management
```

```bash
python -m alembic upgrade head
python -m app.seed
```

### 3. Run the Backend

Run the following commands from the backend directory.

**macOS**

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m alembic upgrade head
python -m app.seed
python -m uvicorn app.main:app --reload
```

**Windows PowerShell**

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m alembic upgrade head
python -m app.seed
python -m uvicorn app.main:app --reload
```

If PowerShell blocks virtual environment activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the virtual environment again:

```powershell
.\.venv\Scripts\Activate.ps1
```

The backend will run at:

```text
http://localhost:8000
```

Interactive API documentation is available at:

```text
http://localhost:8000/docs
```

Keep the backend terminal running.

### 4. Run the Frontend

Open a second terminal and navigate to the cloned repository.

**macOS**

```bash
cd path/to/task-management-app/frontend
cp .env.example .env.local
npm install
npm run dev
```

**Windows PowerShell**

```powershell
Set-Location path\to\task-management-app\frontend
Copy-Item .env.example .env.local
npm install
npm run dev
```

Replace `path/to/task-management-app` with the actual location of the cloned repository.

The frontend will run at:

```text
http://localhost:3000
```

## Demo Account

Use the following seeded account to log in:

```text
Email: demo@example.com
Password: password123
```

The seed script also creates additional users that can be selected as task assignees.

## Environment Variables

The project includes environment variable templates for both the backend and frontend.

### Backend

The backend environment file is:

```text
backend/.env
```

It is created from:

```text
backend/.env.example
```

**macOS**

```bash
cp .env.example .env
```

**Windows PowerShell**

```powershell
Copy-Item .env.example .env
```

The backend uses the following variables:

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: secret used to sign JWT tokens
- `ACCESS_TOKEN_EXPIRE_MINUTES`: access-token lifetime
- `CORS_ORIGINS`: frontend origins allowed to access the backend
- `ENABLE_AI_CHATBOT`: enables or disables the AI assistant
- `GEMINI_API_KEY`: Gemini API key used when the AI assistant is enabled

The default values in `.env.example` are configured for local development with Docker Compose.

Do not commit the actual `.env` file.

### Frontend

The frontend environment file is:

```text
frontend/.env.local
```

It is created from:

```text
frontend/.env.example
```

**macOS**

```bash
cp .env.example .env.local
```

**Windows PowerShell**

```powershell
Copy-Item .env.example .env.local
```

The frontend uses the following API URL:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
```

Do not place private API keys or backend secrets inside frontend environment variables.

## AI Task Assistant

The AI Task Assistant is optional, read-only, and disabled by default.

Gemini is used only to classify questions into predefined intents. Database access is handled through predefined backend queries. The AI cannot generate or execute SQL.

The assistant supports questions such as:

- List incomplete tasks
- Count completed tasks
- List tasks due today
- Get the assignee of a specific task

### Enable the AI Assistant

1. Open the following file:

   ```text
   backend/.env
   ```

2. Set the following variables:

   ```env
   ENABLE_AI_CHATBOT=true
   GEMINI_API_KEY=your-gemini-api-key
   ```

   Replace `your-gemini-api-key` with a valid Gemini API key.

3. Save the file.
4. Stop the running backend with:

   ```text
   Control + C
   ```

5. Restart the backend from the backend directory with the virtual environment active:

   ```bash
   python -m uvicorn app.main:app --reload
   ```

Refresh the frontend after the backend has restarted.

Never commit a real Gemini API key to the repository.

## Database Commands

Run these commands from the backend directory with the Python virtual environment active.

**Apply Database Migrations**

```bash
python -m alembic upgrade head
```

**Reset Seed Data**

```bash
python -m app.seed
```

The seed command resets the application data and deletes existing tasks.

**Check the PostgreSQL Container**

```bash
docker compose ps
```

**Stop PostgreSQL While Preserving Data**

```bash
docker compose down
```

**Remove PostgreSQL and Stored Database Data**

```bash
docker compose down -v
```

Running `docker compose down -v` permanently deletes the PostgreSQL Docker volume.

To rebuild the database afterward:

```bash
docker compose up -d
python -m alembic upgrade head
python -m app.seed
```

## API Documentation

FastAPI automatically provides interactive API documentation.

Swagger UI:

```text
http://localhost:8000/docs
```

OpenAPI JSON:

```text
http://localhost:8000/openapi.json
```

A Postman collection is also available at:

```text
docs/postman/
```

## Additional Documentation

- Postman collection: `docs/postman/`
- Database design: `docs/erd/`
- Planning documentation: `docs/planning/`

## Notes

- The project does not include user registration.
- Only the seeded demo account is intended for login.
- The AI assistant is optional and disabled by default.
- The seed script deletes existing task data whenever it is run.
- Environment files are ignored by Git and must be created from the provided templates.
- The application is intended for local development and technical-assessment purposes.
