from sqlalchemy import Column, PickleType

from ensysmod.database.base_class import Base
from ensysmod.database.ref_base_class import RefCRBase


class YearlyFullLoadHourMin(RefCRBase, Base):
    min_yearly_full_load_hour = Column(PickleType, nullable=False)
