from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from core.security import get_current_user
from core.config import get_db
from core.security import CurrentUser
from crud.user import create_user as create_user_crud, \
    get_user_by_username as get_user_by_username_crud, \
    update_user as update_user_crud, \
    delete_user_account as delete_user_account_crud, \
    get_role
import models.user as user_model

router = APIRouter()

@router.post("/user", response_model=user_model.UserOutput)
async def add_user(
    user_input: user_model.UserInput,
    db: Session = Depends(get_db)
):
    user = create_user_crud(db, user_input)
    return user_model.UserOutput.model_validate(user)

@router.get("/{username}", response_model=user_model.UserOutput)
async def get_user_by_username(
    username: str,
    db: Session = Depends(get_db)
):
    user = get_user_by_username_crud(db, username)
    return user_model.UserOutput.model_validate(user)

@router.put("/user", response_model=user_model.UserOutput)
async def update_user(
    user_update: user_model.UserUpdate,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    user = update_user_crud(db, current_user, user_update)
    return user_model.UserOutput.model_validate(user)

@router.delete("/user", status_code=status.HTTP_200_OK)
async def delete_user(
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    
    respose = delete_user_account_crud(db, current_user)
    return respose

@router.get("/role", response_model=user_model.RoleEnum)
async def retrieve_role(user: CurrentUser):
    return get_role(user)