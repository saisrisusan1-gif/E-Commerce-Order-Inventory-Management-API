from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.users import UserRequest, UserResponse, LoginUserResponse
from database.db_connection import get_db
from models.user import User, RoleEnum
from core.hash import hash_password, verify_password
from core.jwt import create_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user: UserRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()

    if existing:
        raise HTTPException(status_code=409, detail="User already exists")

    new_user = User(
        email=user.email,
        password=hash_password(user.password),
        role=RoleEnum.customer
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserResponse(email=new_user.email, message="Registration successful")


@router.post("/login", response_model=LoginUserResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = create_token({
        "sub": str(user.id),
        "role": user.role.value
    })

    return LoginUserResponse(
        email=user.email,
        message="Login successful",
        access_token=token,
        token_type="bearer"
    )