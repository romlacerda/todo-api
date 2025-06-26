from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from ..main import app
from ..database import Base
from ..models import Todos, Users
from ..routers.auth import bcrypt_context

SQLALCHEMY_DATABASE_URL = "sqlite:///testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return Users(
        id=1,
        username="testuser",
        email="test@test.com",
        role="admin",
    )

client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title="Test Todo",
        description="Test Description",
        priority=1,
        complete=False,
        owner_id=1,
    )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos"))
        connection.commit()


@pytest.fixture
def test_user():
    user = Users(
        id=1,
        username="testuser",
        email="test@test.com",
        hashed_password=bcrypt_context.hash("testpassword"),
        role="admin",
        first_name="Test",
        last_name="User",
        phone_number="1234567890",
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users"))
        connection.commit()