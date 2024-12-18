from fastapi import APIRouter, Depends, HTTPException
from pytest import Session
from core.config import get_db
from core.security import CurrentUser
from models.user import UserLogin, Token
from crud.user import authenticate, deauthenticate

router = APIRouter()

@router.post("/")
def login_access_token(user_login: UserLogin, db: Session = Depends(get_db)) -> Token:
    """
    User login, get an access token for future requests
    """
    try:
        user = authenticate(db, user_login)
        return Token(access_token=user.token, username=user.username)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/check_token")
def login_check_token(user: CurrentUser):
    """
    Check access token is valid
    """
    pass

@router.post("/logout")
def login_logout(user: CurrentUser, db: Session = Depends(get_db)):
    """
    User logout, delete access token
    """
    deauthenticate(db, user)