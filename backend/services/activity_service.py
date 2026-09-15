from sqlalchemy.orm import Session
from models import ActivityLog

def create_activity_log(user_id:int,session_id:int,activity_type:str,description:str | None, ip_address:str | None, session:Session):
    
    activity=ActivityLog(
        user_id=user_id,
        session_id=session_id,
        activity_type=activity_type,
        description=description,
        ip_address=ip_address
    )
    
    session.add(activity)
    session.commit()
    session.refresh(activity)
    
    return activity