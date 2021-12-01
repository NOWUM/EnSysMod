from sqlalchemy import Column, Integer, String, ForeignKey

from ensysmod.database.base_class import Base


class Region(Base):
    """
    Region table

    Stores the region information in database.
    """
    id = Column(Integer, primary_key=True, index=True)
    ref_dataset = Column(Integer, ForeignKey("dataset.id"), index=True, nullable=False)
    name = Column(String, unique=True, index=True, nullable=False)
