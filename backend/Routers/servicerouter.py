#service router

from fastapi import APIRouter,Depends,HTTPException
import schema,auth
from database import get_db 
from sqlalchemy.orm import Session
from CRUD.servicecrud import get_all_service, get_service_by_id,get_all_services,CreateService,UpdateService,DeleteService
from enumutils import RolesEnum as roles

service_router = APIRouter(prefix='/services',tags=['SERVICES'])

@service_router.post('/',response_model=schema.ServiceOut)
def create_service(service_in:schema.CreateService,
                   current_user = Depends(auth.required_roles(roles.admin,roles.pastor)),
                   db:Session = Depends(get_db)):
    service = CreateService(db,service_in)
    return service


@service_router.put('/{service_id}',response_model=schema.ServiceOut)
def update_service(service_id:int,service_in:schema.UpdateService,
                   current_user = Depends(auth.required_roles(roles.admin,roles.pastor)),
                   db:Session = Depends(get_db)):
    service = UpdateService(db,service_id,service_in)
    return service

@service_router.delete('/{service_id}',response_model=schema.ServiceOut)
def delete_service(service_id:int,db:Session = Depends(get_db)):
    delservice = DeleteService(db,service_id)
    return delservice

@service_router.get('/{service_id}',response_model=schema.ServiceOut)
def get_service(service_id:int,db:Session = Depends(get_db)):
    service = get_service_by_id(db,service_id)
    return service


@service_router.get('/',response_model=list[schema.ServiceOut])
def get_services(db:Session = Depends(get_db)):
    services = get_all_services(db)
    return services

