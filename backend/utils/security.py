from pwdlib import PasswordHash
from fastapi import HTTPException,status
from datetime import datetime,timedelta,timezone
from jose import jwt,JWTError
from config import SECRET_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES,REFRESH_TOKEN_EXPIRE_DAYS

password_hasher=PasswordHash.recommended()

def hash_password(password:str) -> str:
    return password_hasher.hash(password)

def verify_password(password:str,password_hash:str)->bool:
    return password_hasher.verify(password,password_hash)

def create_access_token(user_id:int,username:str)->str:
    expire = datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    payload={
        "sub":str(user_id),
        "username":username,
        "exp":expire
    }
    
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)

def verify_access_token(access_token:str)->int:
    try:
        payload=jwt.decode(
            access_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        
        user_id=payload.get("sub")
        
        if user_id is None:
            raise HTTPException(
                 status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token"
            )
            
        return int(user_id)
    
    except (JWTError,ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token"
        )