from sqlalchemy import Column, PickleType

from ensysmod.database.base_class import Base
from ensysmod.database.ref_base_class import RefCRBase


class OperationRateFix(RefCRBase, Base):
    fix_operation_rates = Column(PickleType, nullable=False)
