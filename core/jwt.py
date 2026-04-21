from jose import JWTError,jwt
from datetime import datetime,timedelta
from database.db_connection import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.user import User

SECRET_KEY="your_secreate_key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30


def create_token(data: dict):
    to_encode = data.copy()
    # ALWAYS STRING
    to_encode["sub"] = str(to_encode["sub"])
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str, db: Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id: int = payload.get("user_id")
        user_id = int(user_id)
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(User).filter(User.id == user_id).first()

        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Token is invalid or expired")
       
       
 
    