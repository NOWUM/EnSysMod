from typing import List

from sqlalchemy import Column, Integer, String, and_, ForeignKey
from sqlalchemy.orm import relationship, Session

from ensysmod.database.base_class import Base
from ensysmod.model.energy_commodity import EnergyCommodity
from ensysmod.model.energy_component import EnergyComponent
from ensysmod.model.energy_conversion import EnergyConversion
from ensysmod.model.energy_sink import EnergySink
from ensysmod.model.energy_source import EnergySource
from ensysmod.model.energy_storage import EnergyStorage
from ensysmod.model.energy_transmission import EnergyTransmission
from ensysmod.model.region import Region
from ensysmod.model.user import User


class Dataset(Base):
    """
    Dataset class

    Represents a energy dataset in the database.
    A dataset contains Regions, Commodities, Sources, Conversions, Storages, Transmissions.
    It is the basis for a energy model.
    """
    id = Column(Integer, primary_key=True)
    ref_created_by = Column(Integer, ForeignKey("user.id"), index=True, nullable=False)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    hours_per_time_step = Column(Integer, nullable=False, default=1)
    number_of_time_steps = Column(Integer, nullable=False, default=8760)
    cost_unit = Column(String, nullable=False, default='1e9 Euro')
    length_unit = Column(String, nullable=False, default='km')

    regions: List[Region] = relationship("Region", back_populates="dataset")
    commodities: List[EnergyCommodity] = relationship("EnergyCommodity", back_populates="dataset")
    created_by: User = relationship("User")

    @property
    def sources(self) -> List[EnergySource]:
        sess = Session.object_session(self)
        return sess.query(EnergySource).join(EnergyComponent) \
            .filter(and_(EnergyComponent.ref_dataset == self.id,
                         EnergyComponent.id == EnergySource.ref_component)) \
            .all()

    @property
    def sinks(self) -> List[EnergySink]:
        sess = Session.object_session(self)
        return sess.query(EnergySink).join(EnergyComponent) \
            .filter(and_(EnergyComponent.ref_dataset == self.id,
                         EnergyComponent.id == EnergySink.ref_component)) \
            .all()

    @property
    def conversions(self) -> List[EnergyConversion]:
        sess = Session.object_session(self)
        return sess.query(EnergyConversion).join(EnergyComponent) \
            .filter(and_(EnergyComponent.ref_dataset == self.id,
                         EnergyComponent.id == EnergyConversion.ref_component)) \
            .all()

    @property
    def storages(self) -> List[EnergyStorage]:
        sess = Session.object_session(self)
        return sess.query(EnergyStorage).join(EnergyComponent) \
            .filter(and_(EnergyComponent.ref_dataset == self.id,
                         EnergyComponent.id == EnergyStorage.ref_component)) \
            .all()

    @property
    def transmissions(self) -> List[EnergyTransmission]:
        sess = Session.object_session(self)
        return sess.query(EnergyTransmission).join(EnergyComponent) \
            .filter(and_(EnergyComponent.ref_dataset == self.id,
                         EnergyComponent.id == EnergyTransmission.ref_component)) \
            .all()
