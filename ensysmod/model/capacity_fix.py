from sqlalchemy import Column, Float

from ensysmod.database.base_class import Base
from ensysmod.database.ref_base_class import RefCRBase


class CapacityFix(RefCRBase, Base):
    capacity_fix = Column(Float, nullable=False)
