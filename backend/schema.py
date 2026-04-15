from unittest.mock import Base
from pydantic import BaseModel,EmailStr, StringConstraints
from typing import Annotated, Optional
from datetime import datetime


######### User SCHEMA ##########
class UserBase(BaseModel):
    email: str
    password: Annotated[
        str,
        StringConstraints(min_length=6, max_length=72)
    ]


class CreateUser(UserBase):
    pass


class UpdateUser(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None


class UserOut(BaseModel):
    id: int
    email: str
    

    class Config:               # fixed: was 'class from_attributes' — wrong syntax
        from_attributes = True  # Pydantic v2 (use orm_mode=True if on Pydantic v1)

class UserLogin(BaseModel):
    email:EmailStr
    password:str
#####################################


######### Category SCHEMA ##########
class CategoryBase(BaseModel):
    name: str


class CreateCategory(CategoryBase):
    pass


class CategoryOut(BaseModel):
    id: int
    name: str
  

    class Config:
        from_attributes = True


#####################################


######### Members SCHEMA ##########
class MembersBase(BaseModel):
    fullname: str
    email: str
    phone_no: int


class CreateMembers(MembersBase):  # fixed: was inheriting from UserBase (email+password) — Members don't have passwords
    pass


class UpdateMembers(BaseModel):
    fullname: Optional[str] = None
    email: Optional[str] = None
    phone_no: Optional[int] = None


class MembersOut(BaseModel):
    id: int
    fullname: str
    email: str
    phone_no: int
    category: Optional[CategoryOut] = None 

class MembersResponse(BaseModel):
    total:int
    limit:int
    skip:int
    members : list[MembersOut]
    
class CategoryResponse(BaseModel):
    
    limit:int
    skip:int
    category_members : list[MembersOut]
    total:int
    
    class Config:
        from_attributes = True


#####################################


class Token(BaseModel):
    access_token:str
    token_type:str





class ServiceBase(BaseModel):
    service_name:str
    service_date:datetime


class CreateService(ServiceBase):
    pass

class UpdateService(BaseModel):
    service_name: Optional[str] = None
    service_date: Optional[datetime] = None


class ServiceOut(BaseModel):
    id:int
    service_name:str
    service_date:datetime

    class Config:
        from_attributes = True  


class MarkAttendance(BaseModel):
    service_id :int 
    member_id :int

class AttendanceResponse(BaseModel):
    service :ServiceOut
    total_absent:int
    total_attendees:int
    absent:list[MembersOut]
    attendees:list[MembersOut]
