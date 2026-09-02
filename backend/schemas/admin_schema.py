from pydantic import BaseModel

class AdminUserResponse(BaseModel):
    id:int
    f_name:str
    l_name:str
    username:str
    role:str
    status:str
    
class UserStatusResponse(BaseModel):
    id:int
    username:str
    status:str