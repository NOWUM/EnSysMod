from ensysmod.database.base_class import Base
from ensysmod.database.ref_base_class import RefCommodity, RefComponentUnique, RefDataset


class EnergyTransmission(RefCommodity, RefComponentUnique, RefDataset, Base):
    pass
