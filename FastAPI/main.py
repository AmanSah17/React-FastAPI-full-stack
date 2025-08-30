from fastapi import FastAPI, HTTPException, Depends
from typing import Annotated,List
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, engine
import models
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os









app = FastAPI()

origins = [
    'http://localhost:3000',

]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)


# Mount static files (React build output)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve React index.html on root
@app.get("/")
def serve_react():
    return FileResponse(os.path.join("static", "index.html"))


class TransactionBase(BaseModel):
    amount : float
    category : str
    description : str
    is_income : bool
    date: str

class TransactionModel(TransactionBase):

    id: int

    class Config:
        orm_mode = True


def get_db():
    db = SessionLocal()

    try: 
        yield db

    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

models.Base.metadata.create_all(bind = engine)


@app.post("/transactions/" ,  response_model= TransactionModel)

async def create_transactions(transaction: TransactionBase, db: db_dependency):
        db_transactions = models.Transactions(**transaction.dict())
        db.add(db_transactions)
        db.commit()
        db.refresh(db_transactions)
        return db_transactions





@app.get("/transactions/", response_model= List[TransactionModel])

async def read_transactions(db: db_dependency, skip : int = 0, limit: int = 200):
     
     transcations = db.query(models.Transactions).offset(skip).limit(limit=limit).all()

     return transcations
 


