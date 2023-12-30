from sqlalchemy import Column, Float

from ensysmod.database.base_class import Base
from ensysmod.database.ref_base_class import RefCRBase


class YearlyFullLoadHoursMax(RefCRBase, Base):
    yearly_full_load_hours_max = Column(Float, nullable=False)
