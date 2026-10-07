from fastapi import Depends, HTTPException, APIRouter , Request
from typing import Annotated
from ..database import SessionLocal
from pydantic import BaseModel
from ..models import Users
from starlette import status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm , OAuth2PasswordBearer
from jose import jwt , JWTError
from datetime import timedelta,datetime,timezone
from fastapi.templating import Jinja2Templates


router = APIRouter(prefix='/auth',tags=['auth'])
SECRET_KEY = 'd2ce1c8e76474477be248f52a44f94ec7e9b53aff8657519bdf7ac135b81e481'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

class CreateUserRequest(BaseModel):
    email : str
    username : str
    first_name : str
    last_name : str
    password : str
    role : str 
    phone_number : str

class Token(BaseModel):
    access_token : str
    token_type : str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]

templates = Jinja2Templates(directory="Todo/templates")

#PAGES
@router.get('/login-page')
def render_login_page(request : Request):
    return templates.TemplateResponse(request=request,name='login.html')

@router.get('/register-page')
def render_register_page(request : Request):
    return templates.TemplateResponse(request=request,name='register.html')



#ENDPOINTS
def authenticate_user(username : str , password : str , db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password,user.hashed_password):
        return False
    return user

def create_access_token(username : str,user_id : int,role : str,expires_time:timedelta):
    encode = {'sub':username,'id':user_id,'role':role}
    expires = datetime.now(timezone.utc) + expires_time
    encode.update({'exp':expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

create_acess_token = create_access_token

async def get_current_user(token : Annotated[str, Depends(oauth_bearer)]):
    try:
        payload = jwt.decode(token , SECRET_KEY , algorithms=[ALGORITHM])
        username : str = payload.get('sub')
        user_id : int = payload.get('id')
        user_role : str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate user.")

        return {'username':username , 'id' : user_id , 'user_role' : user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate user.")



    

@router.post('/',status_code = status.HTTP_201_CREATED)
async def create_user(db : db_dependency,create_user : CreateUserRequest):
    existing_user = db.query(Users).filter(
        (Users.username == create_user.username) | (Users.email == create_user.email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email already registered.")

    create_user_model = Users(
        email = create_user.email,
        username = create_user.username,
        first_name = create_user.first_name,
        last_name = create_user.last_name,
        role = create_user.role,
        hashed_password = bcrypt_context.hash(create_user.password),
        is_active = True,
        phone_number = create_user.phone_number
    )

    db.add(create_user_model)
    db.commit()


@router.post('/token',response_model=Token)
async def login_access_for_token(form_data : Annotated[OAuth2PasswordRequestForm , Depends()] ,
                                db : db_dependency):
    user = authenticate_user(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')

    token = create_acess_token(user.username,user.id,user.role,timedelta(minutes=20))
    return {'access_token':token , 'token_type':'bearer'}
