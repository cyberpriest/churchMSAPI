from fastapi import APIRouter ,Depends,HTTPException,status
import schema,auth,database
from CRUD  import authcrud  
from models import User
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from enumutils import RolesEnum

auth_router = APIRouter(prefix='/auth',tags=['USER AUTHENTICATIONS']) 


@auth_router.post('/signup',response_model=schema.UserOut)
def createuser(user_in:schema.CreateUser,db:Session = Depends(database.get_db)):
    check = db.query(User).filter(User.email == user_in.email).first()
    if check:
          raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='user already exist')
    user = authcrud.createUser(
        db,
        user_in.email,
        auth.gen_pwd_hash(user_in.password)
        )
    
    return user




@auth_router.post('/login',response_model=schema.Token)

def loginuser(formdata:OAuth2PasswordRequestForm = Depends(),db:Session =  Depends(database.get_db)):
        email = formdata.username
        user = auth.authenticate(db,email =  email,password=formdata.password)
        _create_token = auth.encode_token(data={'sub':user.email,'role':user.role.value,'user_id':user.id})
        return {'access_token':_create_token,'token_type':'bearer'}


@auth_router.patch('/users/{user_id}/roles',response_model=schema.UserOut)
def assign_role(user_id:int,role:RolesEnum,
                current_user:User = Depends(auth.required_roles(RolesEnum.admin)),
                db:Session = Depends(auth.get_db)):
      assign = authcrud.update_user(
            db,
            user_id,
            role)
      return assign


@auth_router.get('/users',response_model=list[schema.UserOut])
def getallusers(db:Session = Depends(database.get_db),current_user:User = Depends(auth.required_roles(RolesEnum.admin))):
    users = authcrud.get_all_users(db)
    return users

@auth_router.get('/users/email',response_model=schema.UserOut)
def getuser_by_email(email:str,db:Session=Depends(database.get_db),current_user:User = Depends(auth.required_roles(RolesEnum.admin))):
      email = authcrud.get_user_by_email(db,email)
      return email