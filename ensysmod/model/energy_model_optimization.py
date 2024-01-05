from sqlalchemy import Column, Float, ForeignKey, Integer, PickleType
from sqlalchemy.orm import relationship

from ensysmod.database.base_class import Base


class EnergyModelOptimization(Base):
    ref_model = Column(Integer, ForeignKey("energy_model.id"), nullable=False, primary_key=True, index=True)

    start_year = Column(Integer, nullable=False)
    end_year = Column(Integer, nullable=True)
    number_of_steps = Column(Integer, nullable=True)
    years_per_step = Column(Integer, nullable=True)
    CO2_reference = Column(Float, nullable=True)
    CO2_reduction_targets = Column(PickleType, nullable=True)

    # relationships
    model = relationship("EnergyModel", back_populates="optimization_parameters")
