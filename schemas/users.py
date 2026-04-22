from pydantic import BaseModel,Field,EmailStr
# from enum import Enum

# class RoleEnum(str, Enum):
#     customer = "customer"
#     admin = "admin"
    
class UserRequest(BaseModel):
    email:EmailStr
    password: str = Field(min_length=6, max_length=72)
    
class UserResponse(BaseModel):
    email:EmailStr
    message:str
    
class LoginUserResponse(BaseModel):
    email:EmailStr
    message:str
    access_token: str
    token_type: str
    
    