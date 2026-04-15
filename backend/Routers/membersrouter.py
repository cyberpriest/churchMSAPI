from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schema, auth, database
from CRUD.memberscrud import (
    create_member,
    get_all_members,
    get_member_by_id,
    update_member,
    delete_member
)
from models import User
from enumutils import RolesEnum


member_router = APIRouter(prefix='/members', tags=['Members'])



def  paginate(page :int = 1 , limit:int = 10) :
    skip = (page-1) * limit 
    return {'skip':skip,'limit':limit}


@member_router.get('/', response_model=schema.MembersResponse)
def list_members(
    user: User = Depends(auth.required_roles(RolesEnum.admin, RolesEnum.pastor,RolesEnum.moderator)),
    search :str =  None,
    page:int = 1 ,
    limit :int = 10 ,
    db: Session = Depends(database.get_db)):
    params  = paginate(page,limit)


    result =  get_all_members(db ,params['skip'],params['limit'],search)

    return {
        'total':result['total'],
        'limit':limit,
        'skip':params['skip'],
        'members':result['members']}

    


@member_router.get('/{member_id}', response_model=schema.MembersOut)
def get_member(
    member_id: int,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(auth.required_roles(RolesEnum.admin, RolesEnum.pastor))
):
    member = get_member_by_id(db, member_id)
    if not member:
        raise HTTPException(status_code=404, detail='member not found')
    return member


@member_router.post('/', response_model=schema.MembersOut)
def add_member(
    category_id: int,
    data: schema.CreateMembers,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(auth.required_roles(RolesEnum.admin, RolesEnum.pastor))
):
    return create_member(db, category_id, data)


@member_router.patch('/{member_id}', response_model=schema.MembersOut)
def edit_member(
    member_id: int,
    data: schema.UpdateMembers,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(auth.required_roles(RolesEnum.admin, RolesEnum.pastor))
):
    return update_member(db, member_id, data)


@member_router.delete('/{member_id}')
def remove_member(
    member_id: int,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(auth.required_roles(RolesEnum.admin, RolesEnum.pastor))
):
    return delete_member(db, member_id)