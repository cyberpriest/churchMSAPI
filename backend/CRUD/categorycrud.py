#categorycrud.py
from sqlalchemy.orm import Session
from models import Category, Member
from fastapi import HTTPException
from schema import \
        (
        CreateCategory,
        
        )


def get_category_by_id(db:Session,category_id:int):
    return db.query(Category).filter(Category.id == category_id).first()

def get_all_categories(db:Session):
    return db.query(Category).all()

def get_members_by_id(db:Session,category_id:int):
    category = get_category_by_id(db,category_id)

    if not category:
        raise HTTPException(status_code=404,detail='category not found')

    return category.members


def get_members_by_name(db:Session,name:str,skip:int = 0, limit:int = 10):
    category = db.query(Category).filter(Category.name.ilike(f'%{name}%')).first()

    

    if not category:
        raise HTTPException(status_code=404,detail='category not found')
    
    query = db.query(Member).filter(Member.category_id == category.id)
    total = query.count()
    category_members = query.offset(skip).limit(limit).all()
    


    return {'category_members':category_members,'total':total}





    



def createcategory(db:Session,categoryin:CreateCategory):
    category = Category(
        **categoryin.model_dump()
    )
    db.add(category)
    db.commit()
    db.refresh(category)

    return category 


def  updatecategory(db:Session,category_id:int,category_update:CreateCategory):
    category = get_category_by_id(db,category_id)

    if not category:
        raise HTTPException(status_code=404,detail='category not found')

    for k,v in category_update.model_dump(exclude_unset=True).items():
        setattr(category,k,v)

    db.commit()
    db.refresh(category)
    return category

def deletecategory(db:Session,category_id:int):
    category = get_category_by_id(db,category_id)

    if not category:
        raise HTTPException(status_code=404,detail='category not found')

    db.delete(category)
    db.commit()
