from sqlalchemy import Column, Float

from ensysmod.database.base_class import Base
from ensysmod.database.ref_base_class import RefCRBase


class CapacityMin(RefCRBase, Base):
    capacity_min = Column(Float, nullable=False)
