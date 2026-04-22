from database.db_connection import Base
from sqlalchemy import Column,Integer,String,CheckConstraint,Enum
from database.db_connection import Base
import enum

class RoleEnum(str, enum.Enum):
    customer = "customer"
    admin = "admin"

class User(Base):
    __tablename__='users'
    id=Column(Integer,primary_key=True,index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.customer)
   