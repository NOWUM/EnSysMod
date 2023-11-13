from sqlalchemy import Column, Float

from ensysmod.database.base_class import Base
from ensysmod.database.ref_base_class import RefCRBase


class CapacityFix(RefCRBase, Base):
    fix_capacity = Column(Float, nullable=False)
