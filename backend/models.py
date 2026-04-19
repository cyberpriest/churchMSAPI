from database import Base
from sqlalchemy import Column, String, Integer, Enum, DateTime, Date, ForeignKey  # fixed: added ForeignKey import
from enumutils import RolesEnum
from sqlalchemy.orm import relationship
from datetime import datetime


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, index=True)
    role = Column(Enum(RolesEnum), default=RolesEnum.admin)
    password = Column(String, nullable=False)
    def __str__(self):
        return self.email or 'Unnamed User'


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    members = relationship('Member', back_populates='category')  # fixed: 'Members' -> 'Member', back_populates matches Member side
    def __str__(self):
        return self.name or 'Unnamed Category'

class Member(Base):
    __tablename__ = 'members'
    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, index=True)
    phone_no = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)  # fixed: was datetime.utcnow() — calling it freezes the value at startup

    category_id = Column(Integer, ForeignKey('categories.id'))  # fixed: was ForeignKey=('categories.id') — wrong syntax

    attendance = relationship('Attendance', back_populates='member')
    category = relationship('Category', back_populates='members')  # fixed: was 'categories' — naming now consistent
    def __str__(self):
        return self.fullname or  'Unnamed Member'


class Service(Base):
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True)
    service_name = Column(String)
    service_date = Column(Date)
    attendance = relationship('Attendance', back_populates='service')

    def __str__(self):
        return self.service_name
    


class Attendance(Base):
    __tablename__ = 'attendance'
    id = Column(Integer, primary_key=True)
    check_in_time = Column(DateTime, default=datetime.utcnow)

    member_id = Column(Integer, ForeignKey('members.id'))     # fixed: was members_id + wrong ForeignKey syntax
    service_id = Column(Integer, ForeignKey('services.id'))   # fixed: was ForeignKey=('service.id') — wrong table name + syntax

    service = relationship('Service', back_populates='attendance')   # fixed: was pointing back to 'Attendance'
    member = relationship('Member', back_populates='attendance')     # fixed: was pointing back to 'Attendance'

    def __str__(self):
        try:
            member_name = str(self.member) if self.member else 'no member'
            service_name = str(self.service) if self.service else 'no service'
            return f'{member_name}-{service_name}'
        except Exception:
            return f'Attendance {self.id}'



