
from sqlalchemy.orm import  Session 
import schema
from models import Service,Member,Attendance
from fastapi import HTTPException


def mark_attendance(db:Session,data:schema.MarkAttendance):
    service =  db.query(Service).filter(Service.id == data.service_id ).first()
    if not service :
        raise HTTPException(
            status_code=404,detail='service not found')
    
    members = db.query(Member).filter(Member.id == data.member_id ).first()
    if not members :
        raise HTTPException(
            status_code=404,detail='members not found')
    
    # prevent duplicate 
    existing = db.query(Attendance).filter(
        Attendance.service_id == data.service_id ,
        Attendance.member_id == data.member_id
        ).first()
    if existing:
        raise HTTPException(
            status_code=400,detail='already existing'
        )
    mark = Attendance(
        member_id= data.member_id,
        service_id= data.service_id,
        )
    db.add(mark)
    db.commit()
    db.refresh(mark)
    return mark
    
    

def get_attendance_report(db:Session,service_id:int):
    service =  db.query(Service).filter(Service.id == service_id ).first()
    if not service :
        raise HTTPException(
            status_code=404,detail='service not found')
    
    attendees =  db.query(Member).join(Attendance).filter(
        Attendance.service_id  ==  service_id
    ).all()

    present_ids  = [idx.id for idx in attendees]
    absent = db.query(Member).filter(
        ~Member.id.in_(present_ids)
        ).all()
    return {
        'service':service,
        'total_absent':len(absent),
        'total_attendees':len(attendees),
        'absent':absent,
        'attendees':attendees
        }


# i want to know member attendance report, so i can know how many times a member has attended service and which service they attended
def get_member_attendance_report(db:Session,member_id):
    member  =  db.query(Member).filter(Member.id == member_id).first()
    if not member :
        raise HTTPException(
            status_code=404,detail='member not found')
    
    attendance_record = db.query(Member).join(Attendance).filter(
        Attendance.member_id == member_id
    ).all()
    return {' member':member,'attendance_record':attendance_record}