from fastapi import FastAPI,Depends
from database import get_session
from controllers.user_controller import user_router

app=FastAPI()

app.include_router(user_router)

@app.get("/")
def home(session=Depends(get_session)):
    return {"message":"GateNet API is running"}