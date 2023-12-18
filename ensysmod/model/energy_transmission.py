from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import Session, relationship

from ensysmod.database.base_class import Base
from ensysmod.model.transmission_distance import TransmissionDistance
from ensysmod.model.transmission_loss import TransmissionLoss


class EnergyTransmission(Base):
    """
    EnergyTransmission table definition

    See https://vsa-fine.readthedocs.io/en/master/sourceCodeDocumentation/components/transmissionClassDoc.html
    """

    ref_component = Column(Integer, ForeignKey("energy_component.id"), index=True, nullable=False, primary_key=True)
    ref_commodity = Column(Integer, ForeignKey("energy_commodity.id"), index=True, nullable=False)

    # Relationships
    component = relationship("EnergyComponent")
    commodity = relationship("EnergyCommodity", back_populates="energy_transmissions")

    # properties
    @property
    def distances(self) -> list[TransmissionDistance]:
        session = Session.object_session(self)
        return session.query(TransmissionDistance).filter(TransmissionDistance.ref_component == self.ref_component).all()

    @property
    def losses(self) -> list[TransmissionLoss]:
        session = Session.object_session(self)
        return session.query(TransmissionLoss).filter(TransmissionLoss.ref_component == self.ref_component).all()
