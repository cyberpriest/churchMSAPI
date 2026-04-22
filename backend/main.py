from fastapi import  FastAPI
from database import engine,Base
from starlette.middleware.sessions import SessionMiddleware
from admin import setup_admin
from fastapi.middleware.cors import CORSMiddleware
from os import getenv
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from Routers.membersrouter import member_router
from Routers.authsrouter import auth_router
from Routers.categoryrouter import category_router
from Routers.attendancerouter import attendance_router
from Routers.servicerouter import service_router

app = FastAPI(title=' CHRUCH MANAGEMENT SYS. ')
app.add_middleware(
    CORSMiddleware,
    allow_origins=[

   'https://church-management-system--joshuatimi41.replit.app',
    'https://b4bf9a33-eb59-4655-b543-fd5238a46652-00-2veq4rcu396gy.riker.replit.dev'] , # Adjust this in production to restrict origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware,
                   same_site='lax',
                   https_only=True,
                   secret_key='fallback_session_key_change_in_production')

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(category_router)
app.include_router(member_router)
app.include_router(service_router)
app.include_router(attendance_router)




setup_admin(app,engine)

