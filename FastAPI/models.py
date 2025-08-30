from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float



class Transactions(Base):

    __tablename__ = 'transactions'

    id =  Column(Integer, primary_key= True, index= True)
    amount = Column(Float)
    categoory = Column(String)  
    description = Column(String)
    is_income =  Column(Boolean)
    date = Column(String)