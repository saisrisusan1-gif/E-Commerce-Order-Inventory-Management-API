from fastapi import FastAPI,Depends,HTTPException
from schemas.users import UserRequest,UserResponse,LoginUserResponse
from database.db_connection import get_db,engine,Base
from models.user import User
from sqlalchemy.orm import Session
from core.hash import hash_password,verify_password
from core.auth import get_current_user
from core.jwt import create_token,verify_token
from fastapi.security import OAuth2PasswordRequestForm

Base.metadata.create_all(bind=engine)
app=FastAPI()


@app.post("/register",response_model=UserResponse)
def registration(user_register:UserRequest, db:Session=Depends(get_db)):
    existed=db.query(User).filter(User.email==user_register.email).first()
    if existed:
        raise HTTPException(status_code=409 ,detail="user already exists")
    hashed_password=hash_password(user_register.password)
    user=User(email=user_register.email,password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserResponse(email=user.email,message="Registration successful")


@app.post("/login",response_model=LoginUserResponse)
def login(user_login: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.email == user_login.username).first()
    
    if not user:
        raise HTTPException(status_code=404 ,detail="user not found")
    
    if not verify_password(user_login.password, user.password):
        raise HTTPException(status_code=401 ,detail="invalid password")
    
    token=create_token({"sub": user.id})
    return LoginUserResponse(
        email=user.email,
        message="logged in successfully",
        access_token=token,
        token_type="bearer"
    )
    
    
@app.get("/users/{user_id}")
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # optional protection
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "email": user.email
    }