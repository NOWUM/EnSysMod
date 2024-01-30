from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.crud.base_depends_component import CRUDBaseDependsComponent
from ensysmod.model import EnergyConversion
from ensysmod.schemas import EnergyConversionCreate, EnergyConversionUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDEnergyConversion(CRUDBaseDependsComponent[EnergyConversion, EnergyConversionCreate, EnergyConversionUpdate]):
    """
    CRUD operations for EnergyConversion
    """

    def create(self, db: Session, *, obj_in: EnergyConversionCreate) -> EnergyConversion:
        new_conversion: EnergyConversion = super().create(db, obj_in=obj_in)

        # Add energy conversion factors
        for conversion_factor_create in obj_in.conversion_factors:
            conversion_factor_create.ref_dataset = obj_in.ref_dataset
            conversion_factor_create.ref_component = new_conversion.component.id
            crud.energy_conversion_factor.create(db, obj_in=conversion_factor_create)

        return new_conversion


energy_conversion = CRUDEnergyConversion(EnergyConversion)
