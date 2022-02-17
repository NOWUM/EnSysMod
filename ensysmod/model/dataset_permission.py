from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, Boolean

from ensysmod.database.base_class import Base


class DatasetPermission(Base):
    """
    Dataset Permission class
    """
    id = Column(Integer, primary_key=True, index=True)
    ref_dataset = Column(Integer, ForeignKey("dataset.id"), index=True, nullable=False)
    ref_user = Column(Integer, ForeignKey("user.id"), index=True, nullable=False)
    allow_usage = Column(Boolean, nullable=False)
    allow_modification = Column(Boolean, nullable=False)
    allow_permission_grant = Column(Boolean, nullable=False)
    allow_permission_revoke = Column(Boolean, nullable=False)

    # table constraints
    __table_args__ = (
        UniqueConstraint("ref_dataset", "ref_user", name="_dataset_user_uc"),
    )
