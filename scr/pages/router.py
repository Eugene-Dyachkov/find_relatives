from typing import Annotated

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates


from models import User, Relatives, Link
from auth.router import get_current_user

from users.router import registration, my_relatives

pages_router = APIRouter(prefix="/pages", tags=['Pages'])

templates = Jinja2Templates(directory="templates")

@pages_router.get("/auth", name='Authorization')
def get_base(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})

@pages_router.get("/registration", name='Register')
def get_base(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@pages_router.get("/main", name='Main')
def get_base(request: Request):
    return templates.TemplateResponse("main_window.html", {"request": request})

@pages_router.get("/email_register", name='EmailRegister')
def get_base(request: Request):
    return templates.TemplateResponse("auth_email.html", {"request": request})



@pages_router.get("/hello", name='Hello')
def hello():
    return {"Hello": "Word"}


# user: Annotated[User, Depends(get_current_user)],
