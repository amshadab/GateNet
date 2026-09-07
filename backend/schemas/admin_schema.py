from pydantic import BaseModel,Field,field_validator

class AdminSetupResponse(BaseModel):
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

class SetupStatusResponse(BaseModel):
    setup_required:bool
    
class AdminSetupRequest(BaseModel):
    f_name:str=Field(min_length=2,max_length=100)
    l_name:str=Field(min_length=2,max_length=100)
    username:str=Field(min_length=3,max_length=100)
    password:str=Field(min_length=8, max_length=128)
    
    @field_validator("f_name","l_name","username")
    @classmethod
    def validate_text(cls, value:str)->str:
        value=value.strip()
            
        if not value:
            raise ValueError("Field cannot be Empty")
        
        return value
    