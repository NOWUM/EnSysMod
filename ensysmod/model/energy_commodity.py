from sqlalchemy import Column, Integer, String, ForeignKey

from ensysmod.database.base_class import Base


class EnergyCommodity(Base):
    id = Column(Integer, primary_key=True, index=True)
    ref_dataset = Column(Integer, ForeignKey("dataset.id"), index=True, nullable=False)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    unit = Column(String, nullable=False)
