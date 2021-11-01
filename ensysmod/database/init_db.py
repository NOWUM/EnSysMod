import logging

# Import all models
# noinspection PyUnresolvedReferences
from ensysmod import model  # noqa: F401
from ensysmod.database.base_class import Base
from ensysmod.database.session import engine, SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_connection():
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
    except Exception as e:
        logger.error(e)
        raise e


def create_all():
    Base.metadata.create_all(engine)
