from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def home():
    return {"message":"GateNet API is running"}