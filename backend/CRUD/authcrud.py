from sqlalchemy.orm import Session
from models import User
from fastapi import HTTPException , status

from enumutils import RolesEnum as roles

def get_user_by_id(db:Session,user_id:int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db:Session,email:str):
    user_email = db.query(User).filter(User.email.ilike(f'%{email}%')).first()
    return user_email

def get_all_users(db:Session):
    return db.query(User).all()

def createUser(db:Session,email:str , password:str ):
    user = User (
        email  = email ,
        password = password 
 
        )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db:Session,user_id:int,role:roles):

    user_id = get_user_by_id(db,user_id)
    if not user_id:
        raise HTTPException(status_code=404,detail='not found ')
    
    user_id.role =  role
    db.commit()
    db.refresh(user_id)
    return user_id
