from sqlalchemy import Column, Float

from ensysmod.database.base_class import Base
from ensysmod.database.ref_base_class import RefCRBase


class CapacityMax(RefCRBase, Base):
    capacity_max = Column(Float, nullable=False)
