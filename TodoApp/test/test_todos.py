from fastapi import status
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from ..main import app
from ..database import Base
from ..routers.todos import get_current_user, get_db

from fastapi.testclient import TestClient

import pytest
from ..models import Todos, Users

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

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

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

def test_read_all_authenticated(test_todo):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        'id': 1,
        'title': 'Test Todo',
        'description': 'Test Description',
        'priority': 1,
        'complete': False,
        'owner_id': 1,
    }]
    
    
def test_read_one_authenticated(test_todo):
    response = client.get("/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'id': 1,
        'title': 'Test Todo',
        'description': 'Test Description',
        'priority': 1,
        'complete': False,
        'owner_id': 1,
    }
    
def test_read_one_authenticated_not_found():
    response = client.get("/todo/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found.'}
    
def test_create_todo(test_todo):
    request_data = {
        "title": "Mock Title",
        "description": "Mock Description",
        "priority": 2,
        "complete": False,
    }
    response = client.post("/todo/", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    
    if model is None:
        assert False, "Todo was not created"
    
    assert model.title == request_data.get("title")
    assert model.description == request_data.get("description")
    assert model.priority == request_data.get("priority")
    assert model.complete == request_data.get("complete")
    assert model.owner_id == 1
    
    