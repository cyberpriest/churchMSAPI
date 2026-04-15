from sqlalchemy.orm import Session
from models import Member
from fastapi import HTTPException
from schema import CreateMembers, UpdateMembers


def get_member_by_id(db: Session, member_id: int):
    return db.query(Member).filter(Member.id == member_id).first()







def get_all_members(db: Session,skip:int = 0 ,limit:int =  10,search:str = None):
    query = db.query(Member)

    if search :
        query =  query.filter(
            Member.fullname.ilike(f'%{search}%') |
            Member.email.ilike(f'%{search}%') )
        
        
    total = query.count()

    members = query.order_by(Member.created_at.desc())\
            .offset(skip).limit(limit).all()
    return {'members':members,'total':total}

def create_member(db: Session, category_id: int, members_in: CreateMembers):
    member = Member(
        **members_in.model_dump(),
        category_id=category_id     
    )
    db.add(member)
    db.commit()
    db.refresh(member)
    return member


def update_member(db: Session, member_id: int, members_update: UpdateMembers):
    member = get_member_by_id(db, member_id)

    if not member:
        raise HTTPException(status_code=404, detail='member not found')

    for k, v in members_update.model_dump(exclude_unset=True).items():
        setattr(member, k, v)

    db.commit()
    db.refresh(member)
    return member


def delete_member(db: Session, member_id: int):
    member = get_member_by_id(db, member_id)

    if not member:
        raise HTTPException(status_code=404, detail='member not found')

    db.delete(member)
    db.commit()
    return {'message': 'member deleted'}   # fixed: was calling db.refresh after delete — crashes