
from duckdb import limit
from sqlalchemy.orm import Session 
from fastapi import APIRouter, Depends, HTTPException
import schema, auth, database

from models import Category

from CRUD.categorycrud import (
    createcategory,
    get_all_categories,
    get_members_by_id,
    get_members_by_name,
    updatecategory,
    deletecategory
    )

category_router = APIRouter(prefix='/categories', tags=['Categories']) 




@category_router.post('/',response_model=schema.CategoryOut)
def add_category(
    data: schema.CreateCategory,
    db: Session = Depends(database.get_db),
    current_user = Depends(auth.required_roles(auth.RolesEnum.admin, auth.RolesEnum.pastor))):
    existing = db.query(Category).filter(Category.name == data.name).first() 
    if existing:
        raise HTTPException(status_code=400,detail='category with this name already exists')
    return createcategory(db,data)


@category_router.get('/',response_model=list[schema.CategoryOut])
def list_categories(
    db: Session = Depends(database.get_db),
    current_user = Depends(auth.required_roles(auth.RolesEnum.admin, auth.RolesEnum.pastor, auth.RolesEnum.moderator))):
    return get_all_categories(db)


def get_category(
    category_id: int,
    db: Session = Depends(database.get_db),
    current_user = Depends(auth.required_roles(auth.RolesEnum.admin, auth.RolesEnum.pastor, auth.RolesEnum.moderator))
):
    category = get_members_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail='category not found')
    return category


@category_router.put('/{category_id}',response_model=schema.CategoryOut)
def update_category(db:Session = Depends(database.get_db),
                    category_id:int = None,category_update:schema.CreateCategory = None,
                    current_user = Depends(auth.required_roles(auth.RolesEnum.admin, auth.RolesEnum.pastor))):
    return updatecategory(db,category_id,category_update)


def delete_category(
    category_id: int,
    db: Session = Depends(database.get_db),
    current_user = Depends(auth.required_roles(auth.RolesEnum.admin, auth.RolesEnum.pastor))
):
    deletecategory(db,category_id)
    return {'detail':'category deleted successfully'}

# @category_router.get('/{category_id}/members',response_model=list[schema.MembersOut])
# def get_members_by_category_id(
#     category_id: int,
#     db: Session = Depends(database.get_db),
#     current_user = Depends(auth.required_roles(auth.RolesEnum.admin, auth.RolesEnum.pastor, auth.RolesEnum.moderator))
# ):
#     return get_members_by_id(db,category_id)

def paginate_members(page: int = 1, limit: int = 10):
    skip = (page - 1) * limit
    return {'skip': skip, 'limit': limit}


@category_router.get('/{name}/members',response_model=schema.CategoryResponse)
def list_members_by_category_name(
    name:str,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(database.get_db),
    current_user = Depends(auth.required_roles(auth.RolesEnum.admin, auth.RolesEnum.pastor, auth.RolesEnum.moderator))
):
    pagination = paginate_members(page, limit)
    members = get_members_by_name(db,name,pagination['skip'],pagination['limit'])
    return {
        'limit':limit,
        'skip':pagination['skip'],
        'category_members': members['category_members'],
        'total': members['total']
        }