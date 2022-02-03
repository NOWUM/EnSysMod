from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from ensysmod.database.base_class import Base
from ensysmod.model import Dataset


class EnergyModel(Base):
    id = Column(Integer, primary_key=True, index=True)
    ref_dataset = Column(Integer, ForeignKey("dataset.id"), index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)

    # relationships
    dataset: Dataset = relationship("Dataset")
    parameters = relationship("EnergyModelParameter", back_populates="model")

    # table constraints
    __table_args__ = (
        UniqueConstraint("ref_dataset", "name", name="_commodity_name_dataset_uc"),
    )
