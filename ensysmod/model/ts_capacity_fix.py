from sqlalchemy import Column, PickleType

from ensysmod.database.base_class import Base
from ensysmod.database.ref_base_class import RefCRBase


class CapacityFix(RefCRBase, Base):
    fix_capacities = Column(PickleType, nullable=False)
