from sqlalchemy import Column, PickleType

from ensysmod.database.base_class import Base
from ensysmod.database.ref_base_class import RefCRBase


class CapacityMax(RefCRBase, Base):
    max_capacities = Column(PickleType, nullable=False)
