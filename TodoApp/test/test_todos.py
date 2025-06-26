from ..routers.todos import get_current_user, get_db
from fastapi.testclient import TestClient
from fastapi import status
from ..models import Todos
from .utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

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

def test_update_todo(test_todo):
    request_data = {
        'title': 'Updated Title of already saved todo!',
        'description': 'Updated Description of already saved todo!',
        'priority': 5,
        'complete': False,
    }
    
    response = client.put('/todo/1', json=request_data)
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    
    assert model is not None
    assert model.title == 'Updated Title of already saved todo!'
    assert model.description == 'Updated Description of already saved todo!'
    assert model.priority == 5
    assert model.complete == False
    

def test_update_todo_not_found(test_todo):
    request_data = {
        'title': 'Updated Title of already saved todo!',
        'description': 'Updated Description of already saved todo!',
        'priority': 5,
        'complete': False,
    }
    
    response = client.put('/todo/99', json=request_data)
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found.'}
    

def test_delete_todo(test_todo):
    response = client.delete('/todo/1')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    
    assert model is None
    
def test_delete_todo_not_found(test_todo):
    response = client.delete('/todo/99')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found.'}
    
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    
    assert model is not None
    