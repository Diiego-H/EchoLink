""" User related CRUD methods """
from sqlalchemy.orm import Session
from models.user import User, UserInput, UserLogin, UserUpdate, RoleEnum
from core.security import get_password_hash, verify_password, create_access_token
from fastapi import HTTPException, status
from crud.listener import create_listener
from crud.artist import create_artist

# User creation
def create_user(db: Session, user_input: UserInput) -> User:
    # Check if username already exists
    existing_user_by_username = db.query(User).filter(User.username == user_input.username).first()
    if existing_user_by_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists.")

    # Check if email already exists
    existing_user_by_email = db.query(User).filter(User.email == user_input.email).first()
    if existing_user_by_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists.")

    # If validation passes, create the user
    user = User(
        username=user_input.username,
        email=user_input.email,
        hashed_password=get_password_hash(user_input.password),
        description=user_input.description,
        genre=user_input.genre,
        visibility=user_input.visibility,
        role=user_input.role,
        image_url=str(user_input.image_url) if user_input.image_url else None
    )
    db.add(user)
    db.commit()

    # Create role object
    if user_input.role == RoleEnum.listener:
        create_listener(db, user)
    elif user_input.role == RoleEnum.artist:
        create_artist(db, user)

    db.refresh(user)
    return user

# Get user by username
def get_user_by_username(db: Session, username: str) -> User:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user

# Get user by email
def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()

# Get user by id
def get_user_by_id(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()

# Update user by username
def update_user(db: Session, user: User, user_update: UserUpdate) -> User:
    
    # Check if username already exists
    existing_user_by_username = db.query(User).filter(User.username == user_update.username).first()
    if existing_user_by_username and user.id != existing_user_by_username.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists.")

    # Check if email already exists
    existing_user_by_email = db.query(User).filter(User.email == user_update.email).first()
    if existing_user_by_email and user.id != existing_user_by_email.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists.")

    # If validation passes, update the user
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)

    if user_update.password:
        user.hashed_password = get_password_hash(user_update.password)

    db.commit()
    db.refresh(user)
    return user

# Authenticate user, returning a valid access token, if possible
def authenticate(db: Session, user_login: UserLogin) -> str:
    user = get_user_by_email(db, user_login.email)
    if not user:
        raise ValueError('The email is not associated to any account.')
    if not verify_password(user_login.password, user.hashed_password):
        raise ValueError('Incorrect password.')
    
    # Create token
    token = create_access_token(user.id)

    # Update user's token
    user.token = token
    db.commit()
    
    return user

# Deauthenticate user, invalidating its current access token
def deauthenticate(db: Session, user: User):
    user.token = None
    db.commit()

# Function to delete a user's account
def delete_user_account(db: Session, user: User):
    # Check if the user exists
    user = get_user_by_id(db, user.id)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account not found.")

    # Delete the user account
    deauthenticate(db, user)
    db.delete(user)
    db.commit()
    return {"detail": "Account deleted successfully"}

# Get a user's role
def get_role(user: User) -> RoleEnum:
    if user.role is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The user has no role.")
    
    return user.role