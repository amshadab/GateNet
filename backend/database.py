import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from models import Base
from sqlalchemy.orm import sessionmaker

load_dotenv()


DB_HOST=os.getenv("DB_HOST")
DB_PORT=os.getenv("DB_PORT")
DB_NAME=os.getenv("DB_NAME")
DB_USER=os.getenv("DB_USER")
DB_PASSWORD=os.getenv("DB_PASSWORD")

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
