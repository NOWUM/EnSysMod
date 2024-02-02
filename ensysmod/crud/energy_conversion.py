from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.crud.base_depends_component import CRUDBaseDependsComponent
from ensysmod.model import EnergyConversion, EnergyConversionFactor
from ensysmod.schemas import EnergyConversionCreate, EnergyConversionUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDEnergyConversion(CRUDBaseDependsComponent[EnergyConversion, EnergyConversionCreate, EnergyConversionUpdate]):
    """
    CRUD operations for EnergyConversion
    """

    def create(self, db: Session, *, obj_in: EnergyConversionCreate) -> EnergyConversion:
        new_conversion: EnergyConversion = super().create(db, obj_in=obj_in)

        # Create energy conversion factors
        for conversion_factor_create in obj_in.conversion_factors:
            commodity = crud.energy_commodity.get_by_dataset_and_name(
                db, name=conversion_factor_create.commodity_name, dataset_id=new_conversion.ref_dataset
            )
            if commodity is None:
                raise ValueError(f"Commodity {conversion_factor_create.commodity_name} not found in dataset {new_conversion.ref_dataset}!")

            conversion_factor = EnergyConversionFactor(
                ref_component=new_conversion.component.id,
                ref_commodity=commodity.id,
                conversion_factor=conversion_factor_create.conversion_factor,
            )
            crud.energy_conversion_factor.create(db, obj_in=conversion_factor)

        return new_conversion


energy_conversion = CRUDEnergyConversion(EnergyConversion)
