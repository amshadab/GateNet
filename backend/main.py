from fastapi import FastAPI,Depends
from database import get_session
from controllers.user_controller import user_router
from controllers.admin_controller import admin_router
from controllers.setup_controller import setup_rouer

app=FastAPI()

app.include_router(user_router)
app.include_router(admin_router)
app.include_router(setup_rouer)

@app.get("/")
def home(session=Depends(get_session)):
    return {"message":"GateNet API is running"}