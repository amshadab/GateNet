from pydantic import BaseModel

class UserRegister(BaseModel):
    f_name:str
    l_name:str
    username:str
    password:str
    