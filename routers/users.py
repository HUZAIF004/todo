from starlette import status
from fastapi import APIRouter , Depends , HTTPException , Path
from ..database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from ..models import Todos , Users
from pydantic import BaseModel,Field
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(
    prefix='/users',tags=['users']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session , Depends(get_db)]
user_dependency = Annotated[dict , Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')


class UserVerification(BaseModel):
    password : str
    new_password : str = Field(min_length=6)

@router.get('/',status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db:db_dependency):
    if user is None :
        raise HTTPException(status_code=401,detail='Authentication failed')
    return db.query(Users).filter(Users.id == user.get('id')).first()

@router.put('/change_password',status_code=status.HTTP_204_NO_CONTENT)
async def create_password(user : user_dependency , db :db_dependency , user_verfication : UserVerification):
    if user is None:
        raise HTTPException(status_code=401,detail="Authentication failed")
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if not bcrypt_context.verify(user_verfication.password,user_model.hashed_password):
        raise HTTPException(status_code=401,detail="Error on password change")
    user_model.hashed_password = bcrypt_context.hash(user_verfication.new_password)
    db.add(user_model)
    db.commit()

@router.put('/update_phone_number/{phone_number}',status_code=status.HTTP_204_NO_CONTENT)
async def update_phone_number(user : user_dependency , db : db_dependency , phone_number):
    if user is None:
        raise HTTPException(status_code=401,detail="Authentication failed")
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()