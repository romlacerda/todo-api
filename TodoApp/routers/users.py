from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from ..models import Todos, Users
from ..database import SessionLocal
from .auth import bcrypt_context, get_current_user

router = APIRouter(
    prefix='/user',
    tags=['user']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

user_dependency = Annotated[Users, Depends(get_current_user)]

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str
    new_password_confirm: str
    
class PhoneNumberRequest(BaseModel):
    phone_number: str
    
    
@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    user_model = db.query(Users).filter(Users.id == user.id).first()

    if user_model is not None:
        return user_model
    
    raise HTTPException(status_code=404, detail="User not found")
    
@router.put("/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, password_data: ChangePasswordRequest):
    current_user = db.query(Users).filter(Users.id == user.id).first()
    
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not bcrypt_context.verify(password_data.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    if password_data.new_password != password_data.new_password_confirm:
        raise HTTPException(status_code=400, detail="Password mismatch")
    
    current_user.hashed_password = bcrypt_context.hash(password_data.new_password)
    db.add(current_user)
    db.commit()
    
@router.put("/change-phone-number", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user: user_dependency, db: db_dependency, request: PhoneNumberRequest):
    user_model = db.query(Users).filter(Users.id == user.id).first()
    
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_model.phone_number = request.phone_number
    db.add(user_model)
    db.commit()