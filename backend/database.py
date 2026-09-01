from sqlalchemy import create_engine
from models import Base
from sqlalchemy.orm import sessionmaker
from config import( DB_HOST,DB_PORT,DB_NAME,DB_USER,DB_PASSWORD)



DATABASE_URL=(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine=create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
SessionLocal=sessionmaker(bind=engine)

def get_session():
    with SessionLocal() as session:
        yield session
