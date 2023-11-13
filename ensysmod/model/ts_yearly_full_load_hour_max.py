from sqlalchemy import Column, Float

from ensysmod.database.base_class import Base
from ensysmod.database.ref_base_class import RefCRBase


class YearlyFullLoadHourMax(RefCRBase, Base):
    max_yearly_full_load_hour = Column(Float, nullable=False)
