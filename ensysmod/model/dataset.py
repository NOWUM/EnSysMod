from sqlalchemy import Column, Integer, String

from ensysmod.database.base_class import Base


class Dataset(Base):
    """
    Dataset class

    Represents a energy dataset in the database.
    A dataset contains Regions, Commodities, Sources, Conversions, Storages, Transmissions.
    It is the basis for a energy model.
    """
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    hours_per_time_step = Column(Integer, nullable=False, default=1)
    number_of_time_steps = Column(Integer, nullable=False, default=8760)
    cost_unit = Column(String, nullable=False, default='1e9 Euro')
    length_unit = Column(String, nullable=False, default='km')
