from datetime import date, timedelta

from app.database import Base, SessionLocal, engine
from app.models import Task, TaskStatus, User
from app.security import hash_password

DEMO_USERS = [
    {"name": "Admin User", "email": "admin@taskapp.com", "password": "password123"},
    {"name": "Alice Johnson", "email": "alice@taskapp.com", "password": "password123"},
    {"name": "Bob Smith", "email": "bob@taskapp.com", "password": "password123"},
    {"name": "Carol Davis", "email": "carol@taskapp.com", "password": "password123"},
    {"name": "David Lee", "email": "david@taskapp.com", "password": "password123"},
]


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        db.query(Task).delete()
        db.query(User).delete()
        db.commit()

        users = [
            User(name=u["name"], email=u["email"], hashed_password=hash_password(u["password"]))
            for u in DEMO_USERS
        ]
        db.add_all(users)
        db.commit()
        for user in users:
            db.refresh(user)

        admin, alice, bob, carol, david = users
        today = date.today()

        tasks = [
            Task(
                title="Set up project repository",
                description="Initialize the repo and configure base tooling.",
                deadline=today - timedelta(days=2),
                status=TaskStatus.done,
                assignee_id=admin.id,
            ),
            Task(
                title="Design database schema",
                description="Model users and tasks tables with relationships.",
                deadline=today + timedelta(days=1),
                status=TaskStatus.in_progress,
                assignee_id=alice.id,
            ),
            Task(
                title="Build authentication API",
                description="Implement JWT login and protected routes.",
                deadline=today + timedelta(days=3),
                status=TaskStatus.in_progress,
                assignee_id=bob.id,
            ),
            Task(
                title="Implement task CRUD endpoints",
                description="Create, read, update, delete tasks with validation.",
                deadline=today + timedelta(days=5),
                status=TaskStatus.todo,
                assignee_id=carol.id,
            ),
            Task(
                title="Write Postman collection",
                description="Document all API endpoints with example requests.",
                deadline=today + timedelta(days=7),
                status=TaskStatus.todo,
                assignee_id=david.id,
            ),
            Task(
                title="Build tasks page UI",
                description="Create the task list, filters, and search in the frontend.",
                deadline=today + timedelta(days=10),
                status=TaskStatus.todo,
                assignee_id=None,
            ),
        ]
        db.add_all(tasks)
        db.commit()

        print(f"Seeded {len(users)} users and {len(tasks)} tasks.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
