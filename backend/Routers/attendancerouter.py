#attendance router 
from fastapi import APIRouter,Depends

from models import User
from database import get_db
from sqlalchemy.orm import Session
from CRUD.attendancecrud import mark_attendance,get_attendance_report,get_member_attendance_report
from schema import MarkAttendance,AttendanceResponse
import auth,enumutils

attendance_router = APIRouter(
    prefix='/attendance',
    tags=['ATTENDANCE'])

@attendance_router.post('/mark',response_model=MarkAttendance)
def markattendance(data:MarkAttendance,
                   current_user:User = Depends(auth.required_roles(enumutils.RolesEnum.admin,
                                                                   enumutils.RolesEnum.pastor,
                                                                   enumutils.RolesEnum.moderator)),
                   db:Session = Depends(get_db)):
    mark = mark_attendance(
        db,
        data
        )
    return mark

@attendance_router.get('/report/{service_id}',response_model=AttendanceResponse)
def getServicereport(service_id:int,
              current_user:User = Depends(auth.required_roles(enumutils.RolesEnum.admin,
                                                              enumutils.RolesEnum.pastor,
                                                              enumutils.RolesEnum.moderator)),
              db:Session = Depends(get_db)):
    report = get_attendance_report(db,service_id)
    return report


@attendance_router.get('/member/{member_id}',response_model=AttendanceResponse)
def get_member_attendance(member_id:int,
                          db:Session =  Depends(get_db),
                          current_user:User = Depends(auth.required_roles(enumutils.RolesEnum.admin,
                                                                                              enumutils.RolesEnum.pastor,
                                                                                              enumutils.RolesEnum.moderator))):
    attendance = get_member_attendance_report(db,member_id)
    
    return attendance