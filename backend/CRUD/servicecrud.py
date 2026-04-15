# service crud


from sqlalchemy.orm import Session
from models import Service
from fastapi import HTTPException
import schema


def get_service_by_id(db:Session,service_id:int):
    return db.query(Service).filter(Service.id == service_id).first() 

def get_all_service(db:Session):
    return db.query(Service).order_by(Service.service_date.desc()).all()




def CreateService(db:Session,service_in:schema.CreateService):

    service =  Service(
        **service_in.model_dump()
    )
    db.add(service)
    db.commit()
    db.refresh(service)
    return service


def UpdateService(db:Session,service_id:int,service_in:schema.UpdateService):
    service = get_service_by_id(db,service_id)
    if not service:
        return HTTPException(status_code=404,detail='service not found')
    for key , value in service_in.model_dump(exclude_unset=True).items():
        setattr(service,key,value)
    db.commit()
    db.refresh(service)
    return service


def DeleteService(db:Session,service_id:int):
    service = get_service_by_id(db,service_id)
    if not service:
        return HTTPException(status_code=404,detail='service not found')
    db.delete(service)
    db.commit()
    return {'detail':'service deleted successfully'}    


