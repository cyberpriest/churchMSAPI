from sqladmin import ModelView, Admin
from models import User,Member,Category,Service,Attendance

from starlette.requests import Request
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy.orm import Session 
from database import SessionLocal
import auth
from jose import JWTError



class AuthAdmin(AuthenticationBackend):

    async def login(self,request:Request)->bool:
        form =  await request.form()
        email = form.get('username') 
        password = form.get('password')

        db:Session = SessionLocal()

        try :
            user = db.query(User).filter(User.email ==  email).first()
            if not user :
                return False 
            
            if not auth.check_pwd_hash(password,user.password):
                return False 
            
            if user.role.value != 'admin':
                return  False
            
            encode_token = auth.encode_token({'sub':user.email})
            
            request.session.update({'admin_token': encode_token})
            return True
        finally:
            db.close() 

    async def  logout(self,request:Request)->bool:
        request.session.clear()
        return True
    
    async def authenticate(self,request:Request):
        get_token = request.session.get('admin_token')
        if not get_token:
            return False
        
        try :
            decode = auth.decode_token(get_token)
            email = decode.get('sub')
            if email is None:
                return False
            
            db:Session = SessionLocal()
            try:

                user = db.query(User).filter(User.email == email).first()
                return user is not None  and user.role.value == 'admin'
            finally:
                db.close()
        
        except JWTError:
            return False




class UserAdmin(ModelView, model=User):
    name = 'User'
    name_plural = 'Users'
    icon = 'fa-solid fa-users-gear' 
    column_list = [User.id, User.email, User.role]
    column_sortable_list = [User.id, User.email, User.role]
    column_searchable_list = [User.email]
class MemberAdmin(ModelView, model=Member):
    name = 'Member'
    name_plural = 'Members'
    icon = 'fa-solid fa-church'

    column_list = [
        Member.id,
        Member.fullname,
        Member.email,
        Member.phone_no,
        Member.category,         # shows related category name
        Member.created_at,
    ]
    column_formatters = {
        Member.created_at: lambda m, a: m.created_at.strftime('%d %b %Y,%I:%M %p') if m.created_at else '-'
    }
    column_sortable_list = [
        Member.id,
        Member.fullname,
        Member.email,
        Member.phone_no,
        Member.created_at,
    ]
    column_searchable_list = [Member.fullname,Member.email]
    column_details_list = [
        Member.id,
        Member.fullname,
        Member.email,
        Member.phone_no,
        Member.category,
        Member.created_at,
        Member.attendance,  
    ]
    form_columns = [
            Member.fullname,
            Member.email,
            Member.phone_no,
            Member.category, ]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    page_size = 20
    page_size_options = [10, 20, 50]   
class CategoryAdmin(ModelView, model=Category):
    name = 'Category'
    name_plural = 'Categories'
    icon = 'fa-solid fa-tags'

    column_list = [
        Category.id,
        Category.name,
        Category.members,        # shows count of members in this category
    ]

    column_searchable_list = [Category.name]
    column_sortable_list = [Category.id, Category.name]

    column_details_list = [
        Category.id,
        Category.name,
        Category.members,
    ]

    form_columns = [Category.name]

    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

    page_size = 20
    page_size_options = [10, 20, 50]
class ServiceAdmin(ModelView, model=Service):
    name = 'Service'
    name_plural = 'Services'
    icon = 'fa-solid fa-calendar-days'

    column_list = [
        Service.id,
        Service.service_name,
        Service.service_date,
        Service.attendance,  # shows count of attendance records for this service
    ]

    column_searchable_list = [Service.service_name]
    column_sortable_list = [Service.id, Service.service_name, Service.service_date]
    

    column_details_list = [
        Service.id,
        Service.service_name,
        Service.service_date,
        Service.attendance,
    ]

    column_formatters = {
        Service.service_date:lambda m ,a :m.service_date.strftime('%d %b %Y')
        if m.service_date else '-'
    }
    form_columns = [Service.service_name, Service.service_date]

    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

    page_size = 20
    page_size_options = [10, 20, 50]
class AttendanceAdmin(ModelView, model=Attendance):
    name = 'Attendance'
    name_plural = 'Attendance Records'
    icon = 'fa-solid fa-check'

    column_list = [
        Attendance.id,
        Attendance.check_in_time,
        Attendance.member,  # shows member's fullname
        Attendance.service,  # shows service name
    ]
    column_formatters = {
        Attendance.check_in_time :lambda m ,a :m.check_in_time.strftime('%d %b %Y,%I:%M %p')
        if m.check_in_time else '-'
    }

    column_searchable_list = [
        Attendance.member,
        Attendance.service,
    ]

    column_sortable_list = [
        Attendance.id,
        Attendance.check_in_time,
        Attendance.member,
        Attendance.service,
    ]

    column_details_list = [
        Attendance.id,
        Attendance.check_in_time,
        Attendance.member,
        Attendance.service,
    ]

    form_columns = [Attendance.member, Attendance.service]

    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

    page_size = 20
    page_size_options = [10, 20, 50]
def setup_admin(app,engine):
    auth_backend = AuthAdmin(secret_key='fallback_session_key_change_in_production')
    admin = Admin(app, engine, title="Charis Bapt. CMS", authentication_backend=auth_backend)
    admin.add_view(UserAdmin)
    admin.add_view(MemberAdmin)
    admin.add_view(AttendanceAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(ServiceAdmin)
    return admin