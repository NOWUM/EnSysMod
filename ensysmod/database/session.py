from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from ensysmod.core import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI,
                       pool_pre_ping=True,
                       connect_args={"check_same_thread": False},
                       poolclass=StaticPool)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
