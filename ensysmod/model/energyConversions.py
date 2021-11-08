from sqlalchemy import Column, Integer, String

from ensysmod.database.base_class import Base


class EnergyConversion(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    descripition = Column(String, nullable=True)
