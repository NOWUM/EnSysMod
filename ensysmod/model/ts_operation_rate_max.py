from sqlalchemy import Column, PickleType

from ensysmod.database.base_class import Base
from ensysmod.database.ref_base_class import RefCRBase


class OperationRateMax(RefCRBase, Base):
    max_operation_rates = Column(PickleType, nullable=False)
