from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from ensysmod.database.base_class import Base


class Region(Base):
    """
    Region table

    Stores the region information in database.
    """
    id = Column(Integer, primary_key=True, index=True)
    ref_dataset = Column(Integer, ForeignKey("dataset.id"), index=True, nullable=False)
    name = Column(String, index=True, nullable=False)

    # relationships
    dataset = relationship("Dataset")

    # table constraints
    __table_args__ = (
        UniqueConstraint("ref_dataset", "name", name="_region_dataset_name_uc"),
    )
