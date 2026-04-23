from database.db_connection import Base
from sqlalchemy import Column,Integer,String,TEXT,NUMERIC
from database.db_connection import Base

class Product(Base):
    __tablename__='products'
    id=Column(Integer,primary_key=True,index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(TEXT)
    price = Column(NUMERIC(10,2),nullable=False)
    stock=Column(Integer,nullable=False)
    category=Column(String,nullable=False)
   