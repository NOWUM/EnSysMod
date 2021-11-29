from sqlalchemy import Column, Integer, String, ForeignKey

from ensysmod.database.base_class import Base


class EnergySource(Base):
    """
    EnergySource table definition

    See https://vsa-fine.readthedocs.io/en/latest/sourceSinkClassDoc.html
    """
    id = Column(Integer, primary_key=True, index=True)
    ref_component = Column(Integer, ForeignKey("energy_component.id"), index=True, nullable=False, unique=True)
    ref_commodity = Column(Integer, ForeignKey("energy_commodity.id"), index=True, nullable=False)

