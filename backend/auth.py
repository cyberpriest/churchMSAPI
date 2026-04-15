from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError,jwt
from sqlalchemy.orm import Session
from models import User,RolesEnum
from datetime import timedelta,datetime
from fastapi import HTTPException , status ,Depends
from database import get_db
from os import getenv
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

oauth = OAuth2PasswordBearer(tokenUrl='auth/login')
bcrypt = CryptContext(schemes=['bcrypt'],deprecated='auto')

SECRET_KEY = getenv('SECRET_KEY', 'fallback_secret_key_change_in_production')
EXPIRE_TIME =  20


def gen_pwd_hash(pwd:str)->str:
  
    return bcrypt.hash(pwd)

def check_pwd_hash(plain_pwd:str,secret_pwd:str)->bool:
    return bcrypt.verify(plain_pwd,secret_pwd)



def authenticate(db:Session, email:str,password:str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(
            status_code=404,detail='user not found')
    
    if not check_pwd_hash(password ,user.password):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,detail = 'wrong pass')
    return user 



def encode_token(data:dict):
    encode_data = data.copy()
    payload = {'exp':datetime.utcnow() + timedelta(minutes=EXPIRE_TIME)}
    encode_data.update(payload)
    return jwt.encode(encode_data,SECRET_KEY,algorithm='HS256')


def decode_token(token):
    return jwt.decode(token,SECRET_KEY,algorithms=['HS256'])




def get_current_user(db:Session = Depends(get_db),token:str = Depends(oauth))->User:
    
    err = HTTPException(
        status_code = status.HTTP_403_FORBIDDEN,
        detail=  'invalid creds',
        headers={'WWW-Authenticate': 'Bearer'})
         
    
    try :
        t =  decode_token(token)
        email = t.get('sub')
        if email is None:
            raise err


    except JWTError:
        raise err
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise err
    return user

def required_roles(*roles:RolesEnum):
    def check_roles(user: User = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='you do not have access'
            )
        return user    
    return check_roles  





# def required_roles(*roles):
#     def check_roles(user:User = Depends(get_current_user)):
#         if user.role not in roles :
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,detail='u do not have access'
#             ) 
#         return user
#     return check_roles