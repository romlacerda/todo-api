from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, status
from ..models import Todos, Users
from ..database import SessionLocal
from .auth import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

user_dependency = Annotated[Users, Depends(get_current_user)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3, max_length=50)
    description: str = Field(min_length=0, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool
 

@router.get("/")
async def read_all(user: user_dependency, db: db_dependency):
    return db.query(Todos).filter(Todos.owner_id == user.id).all()

@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.id).first()
    
    if todo_model is not None:
        return todo_model
    
    raise HTTPException(status_code=404, detail="Todo not found.")
    
    
@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, todo: TodoRequest, db: db_dependency):
    todo_model = Todos(**todo.model_dump(), owner_id=user.id)
    
    db.add(todo_model)
    db.commit()
    
@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, db: db_dependency, todo: TodoRequest, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.id).first()
   
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")
    
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    
    db.add(todo_model)
    db.commit()
    
@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.id).first()
    
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")
    
    db.delete(todo_model)
    
    db.commit()
    