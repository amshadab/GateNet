from fastapi import FastAPI,Depends
from database import get_session
from schemas.user_schema import UserRegister

app=FastAPI()

@app.get("/")
def home(session=Depends(get_session)):
    return {"message":"GateNet API is running"}