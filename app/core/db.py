from sqlmodel import create_engine, SQLModel, Session
from app.core.config import settings

# SQLite ke liye special argument lagta hai
is_sqlite = settings.DATABASE_URL.startswith("sqlite")
connect_args = {"check_same_thread": False} if is_sqlite else {}

engine = create_engine(settings.DATABASE_URL, echo=True, connect_args=connect_args)

def init_db():
    """DB Tables create karne ke liye"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Har request ke liye ek session generator"""
    with Session(engine) as session:
        yield session